#!/usr/bin/env python3
"""
API Signature Query Tool V3 - Enhanced Multi-Signature Support
==============================================================

Improved to return ALL matching signatures for an API, not just the first one.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional


def search_api_signature(api_name: str, api_type: Optional[str] = None,
                        database_path: str = "/home/user/tt-metal/ttnn_op_generator/api_signatures_database.json") -> Dict:
    """
    Search for an API's signature in the database.
    Returns ALL matching signatures, not just the first one.
    
    Args:
        api_name: Name of the API to search for
        api_type: Optional type filter (function, class, etc.)
        database_path: Path to the signatures database
        
    Returns:
        Dictionary with:
        - found: bool
        - api: Single API info (if only one match)
        - matches: List of all matches (if multiple)
        - multiple: bool (true if multiple matches)
        - count: Number of matches
    """
    try:
        with open(database_path, 'r') as f:
            db = json.load(f)
        
        matches = []
        
        # Search through all APIs
        for key, api_info in db["apis"].items():
            api_matches = False
            
            # 1. Direct name match
            if api_info.get("name") == api_name:
                api_matches = True
            
            # 2. Check if key ends with our API name (handles namespaced entries)
            # e.g., "function::tt::log_debug" matches search for "log_debug"
            if key.endswith(f"::{api_name}"):
                api_matches = True
            
            # 3. Check namespace-qualified names
            # Handle cases like searching for "log_debug" when db has "tt::log_debug"
            if "::" in api_info.get("name", ""):
                name_parts = api_info["name"].split("::")
                if name_parts[-1] == api_name:
                    api_matches = True
            
            # 4. Also check if the full name contains our search as a suffix
            # e.g., searching for "DataMovementProcessor::RISCV_0" should find
            # "tt::tt_metal::DataMovementProcessor::RISCV_0"
            if api_info.get("name", "").endswith(api_name):
                api_matches = True
            
            # 5. Check the signature field too
            if api_name in api_info.get("signature", ""):
                # More specific check - ensure it's the actual function name
                sig_parts = api_info["signature"].split("(")[0].strip().split()
                if sig_parts and sig_parts[-1] == api_name:
                    api_matches = True
            
            # 6. For enum values, check full_name field
            if api_info.get("full_name", "").endswith(api_name):
                api_matches = True
            
            # Apply type filter if specified
            if api_matches and api_type:
                if api_info.get("type") != api_type:
                    api_matches = False
            
            if api_matches:
                matches.append(api_info)
        
        # Remove duplicates based on key
        unique_matches = []
        seen_keys = set()
        for match in matches:
            if match["key"] not in seen_keys:
                seen_keys.add(match["key"])
                unique_matches.append(match)
        
        # Return results in the expected format
        if len(unique_matches) == 0:
            return {
                "found": False,
                "message": f"API '{api_name}' not found"
            }
        elif len(unique_matches) == 1:
            return {
                "found": True,
                "api": unique_matches[0]
            }
        else:
            return {
                "found": True,
                "multiple": True,
                "matches": unique_matches,
                "count": len(unique_matches)
            }
            
    except FileNotFoundError:
        return {
            "found": False,
            "error": f"Database not found: {database_path}"
        }
    except Exception as e:
        return {
            "found": False,
            "error": str(e)
        }


def search_all_signatures(api_name: str, api_type: Optional[str] = None,
                         database_path: str = "/home/user/tt-metal/ttnn_op_generator/api_signatures_database.json") -> Dict:
    """
    Alternative function that always returns all matches in a consistent format.
    
    Returns:
        Dictionary with:
        - found: bool
        - matches: List of all matching API entries
        - count: Number of matches
    """
    result = search_api_signature(api_name, api_type, database_path)
    
    # Normalize the result format
    if not result.get("found"):
        return {
            "found": False,
            "matches": [],
            "count": 0,
            "error": result.get("error"),
            "message": result.get("message")
        }
    
    if result.get("multiple"):
        return {
            "found": True,
            "matches": result["matches"],
            "count": result["count"]
        }
    else:
        # Single match - wrap in a list
        return {
            "found": True,
            "matches": [result["api"]],
            "count": 1
        }


def main():
    parser = argparse.ArgumentParser(
        description="Query API signatures from the database with multi-signature support"
    )
    
    parser.add_argument(
        "api_name",
        help="Name of the API to search for"
    )
    
    parser.add_argument(
        "--type", "-t",
        help="API type (function, class, enum_value, etc.)"
    )
    
    parser.add_argument(
        "--db",
        default="/home/user/tt-metal/ttnn_op_generator/api_signatures_database.json",
        help="Path to the API signature database"
    )
    
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output results as JSON"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Show all database fields for each match"
    )
    
    args = parser.parse_args()
    
    # Search for the API
    result = search_api_signature(args.api_name, args.type, args.db)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["found"]:
            if result.get("multiple"):
                print(f"Found {result['count']} matches for '{args.api_name}':\n")
                for i, api in enumerate(result["matches"], 1):
                    print(f"{i}. {api['type']}: {api['signature']}")
                    print(f"   Header: {api['header']}")
                    if api.get('parameters'):
                        print(f"   Parameters: {api['parameters']}")
                    if args.all:
                        for k, v in api.items():
                            if k not in ['type', 'signature', 'header', 'parameters']:
                                print(f"   {k}: {v}")
                    print()
            else:
                api = result["api"]
                print(f"Found: {api['signature']}")
                print(f"Type: {api['type']}")
                print(f"Header: {api['header']}")
                if api.get('parameters'):
                    print(f"Parameters: {api['parameters']}")
                if args.all:
                    for k, v in api.items():
                        if k not in ['type', 'signature', 'header', 'parameters']:
                            print(f"{k}: {v}")
        else:
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(result["message"])


if __name__ == "__main__":
    import sys
    sys.exit(main())