# exp_to_acos Demo

This demo showcases the replay system's ability to generate a complete implementation of a mathematical function (`acos` - inverse cosine) from a high-level prompt and template code.

## Overview

The `exp_to_acos` demo demonstrates:

1. **Template-based Code Generation**: Starting from a generic exponential function template
2. **LLM-guided Transformation**: Using AI to transform the template into a specific mathematical function
3. **Iterative Development**: Multiple versions showing the evolution of the implementation
4. **Documentation Integration**: Using reference materials to guide the transformation

## Demo Structure

### Input Components

- **Prompt File**: `examples/prompts/create_new_op_from_generic.txt`
  - Contains instructions to create an `acos` function from a generic template
  - References template files and documentation
  - Specifies transformation requirements

- **Template Files**: Generic mathematical operation implementation
  - Base structure for mathematical operations
  - Placeholder code to be customized
  - Build system configuration

- **Documentation**: API guides and mathematical references
  - Function specifications
  - Implementation guidelines
  - Testing requirements

### Output Structure

Each demo run creates a versioned output directory:

```
examples/demos/exp_to_acos/
├── latest/           # Symlink to most recent version
├── 1/               # First run
│   ├── code/        # Generated acos implementation
│   └── replay/      # Execution logs and metadata
├── 2/               # Second run (refinements)
│   ├── code/        # Improved implementation
│   └── replay/      # Updated execution logs
└── ...              # Additional iterations
```

### Generated Artifacts

#### Code Directory (`{version}/code/`)
- **acos.cpp**: Main implementation of the inverse cosine function
- **acos.h**: Header file with function declarations
- **test_acos.cpp**: Unit tests for the implementation
- **CMakeLists.txt**: Build configuration
- **README.md**: Generated documentation

#### Replay Directory (`{version}/replay/`)
- **epic.png**: Visualization of the execution graph
- **docs/**: Referenced documentation files
- **template/**: Original template files
- **run_logs/**: Build and test execution logs
- **client/**: LLM request/response logs

## Running the Demo

### Prerequisites

1. **Environment Setup**:
   ```bash
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

2. **Dependencies**:
   - Python 3.7+
   - Anthropic API access
   - C++ compiler (for generated code testing)

### Execution

Run the demo script:

```bash
cd examples/demos
./run_exp_to_acos_demo.sh
```

This script:
1. Validates the prompt file exists
2. Creates the output directory structure
3. Executes the replay system
4. Shows the generated output location

### Manual Execution

For more control, run replay directly:

```bash
python3 replay.py \
    "examples/prompts/create_new_op_from_generic.txt" \
    "exp_to_acos" \
    --output_dir "examples/demos"
```

## Workflow Demonstration

The demo illustrates a complete development workflow:

### 1. Template Analysis
- LLM analyzes the generic exponential function template
- Identifies components that need modification for `acos`
- Plans the transformation approach

### 2. Mathematical Implementation
- Replaces exponential calculations with inverse trigonometric logic
- Implements domain validation (-1 ≤ x ≤ 1)
- Adds appropriate error handling

### 3. Test Generation
- Creates comprehensive unit tests
- Covers edge cases (boundaries, invalid inputs)
- Validates mathematical accuracy

### 4. Build Integration
- Updates build configuration for new function
- Ensures proper compilation flags
- Integrates with existing build system

### 5. Documentation
- Generates function documentation
- Includes usage examples
- Documents implementation details

## Example Transformations

### Input Template (Exponential Function)
```cpp
// Generic exponential operation
float generic_exp(float x) {
    return expf(x);
}
```

### Generated Output (Inverse Cosine)
```cpp
// Inverse cosine function implementation
float acos_implementation(float x) {
    // Validate input domain
    if (x < -1.0f || x > 1.0f) {
        return NAN;  // Invalid input
    }
    
    // Calculate acos using appropriate algorithm
    return acosf(x);
}
```

## Learning Outcomes

This demo demonstrates several key capabilities:

### AI-Assisted Development
- **Code Understanding**: LLM comprehends existing template structure
- **Domain Knowledge**: Applies mathematical knowledge to generate correct implementations
- **Best Practices**: Follows coding standards and error handling patterns

### Automated Testing
- **Test Generation**: Creates comprehensive test suites automatically
- **Edge Case Handling**: Identifies and tests boundary conditions
- **Validation**: Ensures mathematical correctness

### Build Automation
- **Configuration Management**: Updates build files appropriately
- **Dependency Handling**: Manages library requirements
- **Integration**: Ensures new code fits existing system

### Documentation Generation
- **API Documentation**: Creates clear function documentation
- **Usage Examples**: Provides practical usage examples
- **Implementation Notes**: Documents design decisions

## Typical Results

A successful run produces:

1. **Functional Code**: Working `acos` implementation that compiles and runs
2. **Comprehensive Tests**: Test suite covering normal and edge cases
3. **Build Integration**: Updated CMakeLists.txt that builds successfully
4. **Documentation**: Clear documentation explaining the implementation

## Debugging and Analysis

### Execution Logs
- **run_logs/**: Contains build and test output
- **client/**: Shows LLM interactions and decision-making process
- **epic.png**: Visual representation of the execution workflow

### Common Issues
- **Build Failures**: Check run logs for compilation errors
- **Test Failures**: Review generated tests for mathematical accuracy
- **LLM Errors**: Examine client logs for API issues

### Iterative Improvement
Multiple runs often show:
- **First Run**: Basic working implementation
- **Second Run**: Improved error handling and optimization
- **Third Run**: Enhanced documentation and test coverage

## Educational Value

This demo serves as an excellent example for:

- **AI-Assisted Programming**: How LLMs can transform code intelligently
- **Template-Based Development**: Using templates for rapid prototyping
- **Automated Testing**: Generating comprehensive test suites
- **Documentation**: Creating maintainable, well-documented code

The demo showcases the replay system's ability to handle complex, multi-step development tasks that require domain knowledge, code understanding, and engineering best practices. 