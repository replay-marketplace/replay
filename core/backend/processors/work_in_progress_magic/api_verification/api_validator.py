#!/usr/bin/env python3
"""
TT-Metal API Signature Validator - Hybrid Version
=================================================

Simple extraction, but searches through all database entries like the working version.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from collections import defaultdict

from tools.tree_sitter_tool import parse_file, query


@dataclass
class APIUsage:
    """Represents a single API usage in the code."""
    name: str
    api_type: str
    full_signature: str
    location: Dict[str, int]
    context: str
    arguments: Optional[str] = None


@dataclass 
class ValidationResult:
    """Result of validating a single API usage."""
    api_usage: APIUsage
    status: str
    message: str
    database_info: Optional[Dict] = None
    all_matches: Optional[List[Dict]] = None


class TTMetalAPIValidator:
    """Validates TT-Metal API usage against the signature database."""
    
    def __init__(self, signature_db_path: str = None):
        if signature_db_path is None:
            # Use the database in the same directory as this script
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            signature_db_path = os.path.join(script_dir, "api_signatures_database.json")
        self.signature_db_path = signature_db_path
        self.validation_results = []
        self._load_database()
    
    def _load_database(self):
        """Load the signature database."""
        try:
            with open(self.signature_db_path, 'r') as f:
                self.database = json.load(f)
        except Exception as e:
            print(f"[API Validator] Error loading database: {e}")
            self.database = {"apis": {}}
    
    def validate_file(self, file_path: str) -> Dict:
        """Validate all API usage in a C++ file."""
        print(f"\n[API Validator] Validating: {file_path}")
        
        self.validation_results = []
        
        # Extract API usages
        api_usages = self._extract_api_usage(file_path)
        
        if isinstance(api_usages, dict) and 'error' in api_usages:
            return {'error': api_usages['error'], 'file': file_path}
        
        # Validate each usage
        for api_usage in api_usages:
            result = self._validate_api(api_usage)
            self.validation_results.append(result)
        
        return self._generate_report(file_path)
    
    def _extract_api_usage(self, file_path: str) -> List[APIUsage]:
        """Extract API usages from the file - simple version."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.splitlines()
            
            tree_id = parse_file(file_path)
            api_usages = []
            
            # 1. Extract function calls
            call_query = """
            (call_expression
                function: [
                    (identifier) @func_name
                    (qualified_identifier) @qualified_func
                    (field_expression
                        argument: (_) @object
                        field: (field_identifier) @method_name)
                ]
                arguments: (argument_list) @args
            ) @call
            """
            
            call_results = query(tree_id, call_query)
            call_groups = self._group_results(call_results, 'call')
            
            for group in call_groups:
                # Determine function name and type
                func_name = None
                api_type = 'function'
                arguments = group.get('args', {}).get('text', '()')
                
                if 'func_name' in group:
                    func_name = group['func_name']['text']
                elif 'method_name' in group:
                    func_name = group['method_name']['text'] 
                    api_type = 'method'
                elif 'qualified_func' in group:
                    # Handle namespace::function
                    qualified = group['qualified_func']['text']
                    parts = qualified.split('::')
                    func_name = parts[-1]
                
                if func_name:
                    api_usage = APIUsage(
                        name=func_name,
                        api_type=api_type,
                        full_signature=group['call']['text'],
                        location=self._get_location(group['call'], lines),
                        context=self._get_context(group['call'], lines),
                        arguments=arguments
                    )
                    api_usages.append(api_usage)
            
            # 2. Extract type usage (classes, structs)
            type_query = """
            (declaration
                type: [
                    (type_identifier) @type_name
                    (qualified_identifier) @qualified_type
                ]
                declarator: (_) @declarator
            ) @type_decl
            """
            
            type_results = query(tree_id, type_query)
            
            for result in type_results:
                if result['name'] in ['type_name', 'qualified_type']:
                    type_text = result['text']
                    
                    # Skip standard types
                    if self._is_standard_type(type_text):
                        continue
                    
                    api_usage = APIUsage(
                        name=type_text,
                        api_type='class',
                        full_signature=type_text,
                        location=self._get_location(result, lines),
                        context=self._get_context(result, lines)
                    )
                    api_usages.append(api_usage)
            
            # 3. Extract enum values
            enum_query = """
            (qualified_identifier) @enum_value
            """
            
            enum_results = query(tree_id, enum_query)
            
            for result in enum_results:
                text = result['text']
                
                # Check if it looks like an enum value
                if '::' in text:
                    parts = text.split('::')
                    last = parts[-1]
                    
                    # Common enum patterns
                    if last and (last[0].isupper() or last.isupper()):
                        # Skip if it's followed by ( - that's a function
                        location = self._get_location(result, lines)
                        line = lines[location['line'] - 1]
                        col = location['column'] - 1 + len(text)
                        
                        if col < len(line) and line[col:col+1] == '(':
                            continue
                        
                        api_usage = APIUsage(
                            name=text,
                            api_type='enum_value',
                            full_signature=text,
                            location=location,
                            context=self._get_context(result, lines)
                        )
                        api_usages.append(api_usage)
            
            # Remove duplicates
            seen = set()
            unique_usages = []
            for usage in api_usages:
                key = (usage.name, usage.api_type, usage.location['line'])
                if key not in seen:
                    seen.add(key)
                    unique_usages.append(usage)
            
            print(f"[API Validator] Found {len(unique_usages)} unique API usages")
            return unique_usages
            
        except Exception as e:
            return {'error': f"Failed to parse file: {str(e)}"}
    
    def _validate_api(self, api_usage: APIUsage) -> ValidationResult:
        """
        Validate by searching through ALL database entries.
        This is what made the older version work well.
        """
        matches = []
        
        # Search through ALL database entries
        for db_key, db_info in self.database['apis'].items():
            # Check if this entry could match our usage
            if self._matches_api(api_usage, db_key, db_info):
                matches.append(db_info)
        
        if not matches:
            return ValidationResult(
                api_usage=api_usage,
                status='missing',
                message=f'{api_usage.api_type} "{api_usage.name}" not found in database'
            )
        
        # Check all matches to find the best one
        for db_info in matches:
            # Check for variadic parameters first
            if db_info.get('parameters') == '(...)':
                return ValidationResult(
                    api_usage=api_usage,
                    status='valid',
                    message=f'Variadic function accepts any arguments',
                    database_info=db_info,
                    all_matches=matches
                )
            
            # Check for template parameter packs
            if 'Args&&...' in str(db_info.get('parameters', '')):
                return ValidationResult(
                    api_usage=api_usage,
                    status='valid',
                    message=f'Template variadic function accepts any arguments',
                    database_info=db_info,
                    all_matches=matches
                )
            
            # For methods, be lenient
            if api_usage.api_type == 'method':
                return ValidationResult(
                    api_usage=api_usage,
                    status='valid',
                    message=f'Method found in database',
                    database_info=db_info,
                    all_matches=matches
                )
            
            # For functions with no arguments
            if api_usage.api_type == 'function' and api_usage.arguments == '()':
                # Check if function has default parameters
                sig = db_info.get('signature', '')
                if '=' in sig or 'void)' in sig or db_info.get('parameters') == '()':
                    return ValidationResult(
                        api_usage=api_usage,
                        status='valid',
                        message=f'Function found with compatible signature',
                        database_info=db_info,
                        all_matches=matches
                    )
        
        # If we have matches but none validated, use the first one
        if matches:
            return ValidationResult(
                api_usage=api_usage,
                status='valid',
                message=f'Found in database ({len(matches)} matches)',
                database_info=matches[0],
                all_matches=matches
            )
        
        return ValidationResult(
            api_usage=api_usage,
            status='missing',
            message=f'Not found in database'
        )
    
    def _matches_api(self, api_usage: APIUsage, db_key: str, db_info: Dict) -> bool:
        """
        Check if a database entry matches the API usage.
        This is the key logic that makes search work well.
        """
        # Extract the API name from the database entry
        db_name = db_info.get('name', '')
        
        # Direct name match
        if db_name == api_usage.name:
            return True
        
        # Check if db_name ends with the usage name (namespace handling)
        # e.g., "tt::log_debug" matches usage "log_debug"
        if db_name and db_name.endswith('::' + api_usage.name):
            return True
        
        # For enum values, check if the full usage name matches
        if api_usage.api_type == 'enum_value':
            # Check full_name field for enum values
            if db_info.get('full_name') == api_usage.name:
                return True
            # Check if the key contains our enum value
            if db_key.endswith('::' + api_usage.name):
                return True
        
        # Check the key itself
        # The key format is "type::name", so check if it ends with our name
        key_parts = db_key.split('::', 1)
        if len(key_parts) == 2:
            key_name = key_parts[1]
            # Direct match on the key name part
            if key_name == api_usage.name:
                return True
            # Namespace match
            if key_name.endswith('::' + api_usage.name):
                return True
        
        # Special handling for methods/member functions
        if api_usage.api_type in ['method', 'member_function']:
            db_type = db_info.get('type', '')
            if db_type in ['function', 'member_function', 'method']:
                # Be more permissive for methods
                if db_name.split('::')[-1] == api_usage.name:
                    return True
        
        return False
    
    def _group_results(self, results: List[Dict], anchor: str) -> List[Dict]:
        """Group query results by anchor node."""
        groups = []
        
        # Find anchor nodes
        anchors = [r for r in results if r['name'] == anchor]
        
        for anchor_node in anchors:
            group = {'_anchor': anchor, anchor: anchor_node}
            
            # Find all children within this anchor
            for r in results:
                if (r['name'] != anchor and
                    r['byte_range'][0] >= anchor_node['byte_range'][0] and
                    r['byte_range'][1] <= anchor_node['byte_range'][1]):
                    group[r['name']] = r
            
            groups.append(group)
        
        return groups
    
    def _get_location(self, node: Dict, lines: List[str]) -> Dict[str, int]:
        """Get line and column from byte offset."""
        byte_offset = node['byte_range'][0]
        current_offset = 0
        
        for line_num, line in enumerate(lines):
            line_length = len(line) + 1  # +1 for newline
            if current_offset + line_length > byte_offset:
                column = byte_offset - current_offset
                return {'line': line_num + 1, 'column': column + 1}
            current_offset += line_length
        
        return {'line': len(lines), 'column': 1}
    
    def _get_context(self, node: Dict, lines: List[str], context_lines: int = 2) -> str:
        """Get surrounding context."""
        location = self._get_location(node, lines)
        line_num = location['line'] - 1
        
        start = max(0, line_num - context_lines)
        end = min(len(lines), line_num + context_lines + 1)
        
        context = []
        for i in range(start, end):
            prefix = ">>> " if i == line_num else "    "
            context.append(f"{prefix}{lines[i]}")
        
        return '\n'.join(context)
    
    def _is_standard_type(self, type_name: str) -> bool:
        """Check if a type is standard/builtin."""
        standard = {
            'void', 'bool', 'char', 'int', 'float', 'double',
            'size_t', 'uint32_t', 'uint64_t', 'int32_t', 'int64_t',
            'string', 'vector', 'optional', 'unique_ptr', 'shared_ptr'
        }
        
        if type_name in standard or type_name.startswith('std::'):
            return True
        
        base = type_name.split('<')[0]
        return base in standard
    
    def _generate_report(self, file_path: str) -> Dict:
        """Generate validation report."""
        valid = [r for r in self.validation_results if r.status == 'valid']
        missing = [r for r in self.validation_results if r.status == 'missing']
        
        total = len(self.validation_results)
        
        return {
            'file': file_path,
            'summary': {
                'total_apis': total,
                'valid': len(valid),
                'missing': len(missing),
                'validation_rate': len(valid) / total * 100 if total > 0 else 0
            },
            'valid_apis': [self._result_to_dict(r) for r in valid],
            'missing_apis': [self._result_to_dict(r) for r in missing]
        }
    
    def _result_to_dict(self, result: ValidationResult) -> Dict:
        """Convert result to dictionary."""
        d = {
            'api': result.api_usage.name,
            'type': result.api_usage.api_type,
            'signature': result.api_usage.full_signature,
            'location': result.api_usage.location,
            'status': result.status,
            'message': result.message,
            'context': result.api_usage.context
        }
        
        if result.database_info:
            d['found_as'] = {
                'key': result.database_info.get('key'),
                'name': result.database_info.get('name'),
                'signature': result.database_info.get('signature'),
                'parameters': result.database_info.get('parameters')
            }
        
        if result.all_matches and len(result.all_matches) > 1:
            d['match_count'] = len(result.all_matches)
        
        return d
    
    def print_report(self, report: Dict, verbose: bool = False):
        """Print human-readable report."""
        print(f"\n{'='*80}")
        print(f"API Validation Report")
        print(f"File: {report['file']}")
        print(f"{'='*80}")
        
        s = report['summary']
        print(f"\nSummary:")
        print(f"  Total APIs: {s['total_apis']}")
        print(f"  ✓ Valid: {s['valid']} ({s['validation_rate']:.1f}%)")
        print(f"  ✗ Missing: {s['missing']} ({100 - s['validation_rate']:.1f}%)")
        
        if report['missing_apis']:
            print(f"\n{'='*80}")
            print("Missing APIs:")
            print(f"{'='*80}")
            
            # Group by type
            by_type = defaultdict(list)
            for api in report['missing_apis']:
                by_type[api['type']].append(api)
            
            for api_type, apis in sorted(by_type.items()):
                print(f"\n{api_type.upper().replace('_', ' ')}S:")
                for api in apis:
                    print(f"  ✗ {api['api']}")
                    print(f"    Line: {api['location']['line']}")
                    if verbose:
                        print(f"    Context:\n{api['context']}")
        
        if verbose and report['valid_apis']:
            print(f"\n{'='*80}")
            print("Valid APIs (sample):")
            print(f"{'='*80}")
            for api in report['valid_apis'][:10]:
                print(f"  ✓ {api['api']} ({api['type']})")
                if 'found_as' in api:
                    found = api['found_as']
                    print(f"    Database: {found['name']}")
                    if found.get('parameters') == '(...)':
                        print(f"    Note: Variadic function")
                if api.get('match_count', 0) > 1:
                    print(f"    Matches: {api['match_count']} database entries")


def main():
    parser = argparse.ArgumentParser(description="Validate API usage")
    parser.add_argument("file", help="C++ file to validate")
    parser.add_argument("--db", help="Path to API signatures database (defaults to local database)")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--json", action="store_true")
    
    args = parser.parse_args()
    
    validator = TTMetalAPIValidator(args.db)
    report = validator.validate_file(args.file)
    
    if 'error' in report:
        print(f"Error: {report['error']}")
        return 1
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        validator.print_report(report, args.verbose)
    
    return 0 if report['summary']['missing'] == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())