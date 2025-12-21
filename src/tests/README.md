# ChatPPT Unit Tests

Comprehensive unit test suite for the ChatPPT project.

## 📁 Test Structure

```
src/tests/
├── __init__.py                  # Test package initialization
├── run_tests.py                 # Test runner script
├── test_data_structures.py      # Tests for data structures
├── test_layout_manager.py       # Tests for layout management
├── test_slide_builder.py        # Tests for slide building
├── test_input_parser.py         # Tests for markdown parsing
├── test_config.py               # Tests for configuration
├── test_utils.py                # Tests for utility functions
├── test_template_manager.py     # Tests for template management
├── test_chat_history.py         # Tests for chat history
├── test_gradio_app.py           # Tests for Gradio app functions
└── README.md                    # This file
```

## 🚀 Running Tests

### Run All Tests

```bash
# From the project root
cd src/tests
python run_tests.py

# Or from anywhere in the project
python src/tests/run_tests.py
```

### Run Specific Test Module

```bash
# Run only data structures tests
python run_tests.py -m test_data_structures

# Run only layout manager tests
python run_tests.py -m test_layout_manager
```

### Run with Different Verbosity

```bash
# Quiet mode (0)
python run_tests.py -v 0

# Normal mode (1)
python run_tests.py -v 1

# Verbose mode (2) - default
python run_tests.py -v 2
```

### Run Individual Test File

```bash
# Run a specific test file
python test_data_structures.py

# Run with unittest
python -m unittest test_data_structures

# Run specific test class
python -m unittest test_data_structures.TestSlideContent

# Run specific test method
python -m unittest test_data_structures.TestSlideContent.test_slide_content_creation_with_defaults
```

## 📊 Test Coverage

### Core Modules (100% coverage target)

| Module | Test File | Status | Coverage |
|--------|-----------|--------|----------|
| data_structures.py | test_data_structures.py | ✅ | High |
| layout_manager.py | test_layout_manager.py | ✅ | High |
| slide_builder.py | test_slide_builder.py | ✅ | High |
| input_parser.py | test_input_parser.py | ✅ | High |
| config.py | test_config.py | ✅ | High |
| utils.py | test_utils.py | ✅ | High |
| template_manager.py | test_template_manager.py | ✅ | High |
| chat_history.py | test_chat_history.py | ✅ | High |
| gradio_app.py | test_gradio_app.py | ✅ | Medium |

### Test Categories

#### 1. Data Structures Tests (`test_data_structures.py`)
- SlideContent creation with defaults
- SlideContent with all fields
- Slide creation and validation
- PowerPoint object creation
- String representation

#### 2. Layout Manager Tests (`test_layout_manager.py`)
- Layout encoding calculations
- Content encoding calculations
- Layout strategy selection
- Layout assignment for different content types
- Edge cases and error handling

#### 3. Slide Builder Tests (`test_slide_builder.py`)
- Building title-only slides
- Building slides with bullet points
- Building slides with images
- Building complete slides
- Multiple slide creation

#### 4. Input Parser Tests (`test_input_parser.py`)
- Bullet point level parsing
- Title parsing
- Content slide parsing
- Nested bullet points
- Image parsing
- Complex presentation parsing

#### 5. Config Tests (`test_config.py`)
- Config file loading
- Default values
- Partial configuration
- Error handling for missing files

#### 6. Utils Tests (`test_utils.py`)
- Slide removal functionality
- Empty presentation handling

#### 7. Template Manager Tests (`test_template_manager.py`)
- Template loading
- Layout mapping extraction
- Layout printing

#### 8. Chat History Tests (`test_chat_history.py`)
- Session creation
- Session retrieval
- Multiple session management
- History persistence

#### 9. Gradio App Tests (`test_gradio_app.py`)
- Chatbot instance management
- Image advisor singleton
- PPT generation
- Chat functionality
- Image enhancement

## 🔧 Requirements

The tests use Python's built-in `unittest` framework and some optional dependencies:

### Required
- Python 3.7+
- unittest (built-in)

### Optional (for full test coverage)
- langchain-core (for chat_history tests)
- python-pptx (for template_manager tests)
- gradio (for gradio_app tests)

## 📝 Test Patterns

### Mocking External Dependencies

Tests use `unittest.mock` to mock external dependencies:

```python
from unittest.mock import Mock, patch

@patch('module.ExternalClass')
def test_function(self, mock_class):
    # Test with mocked dependency
    pass
```

### Conditional Tests

Some tests are skipped if dependencies are not available:

```python
@unittest.skipUnless(DEPENDENCY_AVAILABLE, "Dependency not installed")
class TestWithDependency(unittest.TestCase):
    # Tests that require specific dependencies
    pass
```

### Temporary Files

Tests that need temporary files use `tempfile`:

```python
import tempfile

with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    # Use temporary file
    pass
```

## ✅ Best Practices

1. **Isolation**: Each test is independent and doesn't rely on other tests
2. **Cleanup**: Tests clean up after themselves (e.g., clearing global state)
3. **Descriptive Names**: Test methods have clear, descriptive names
4. **Documentation**: Each test has a docstring explaining what it tests
5. **Coverage**: Tests cover normal cases, edge cases, and error conditions
6. **Mocking**: External dependencies are mocked to ensure fast, reliable tests

## 🐛 Debugging Failed Tests

### View Detailed Output

```bash
# Run with maximum verbosity
python run_tests.py -v 2

# Run specific test with Python unittest
python -m unittest test_data_structures.TestSlideContent.test_name -v
```

### Common Issues

1. **Import Errors**: Ensure `src` is in the Python path
2. **Missing Dependencies**: Install required packages
3. **File Not Found**: Check that test files are in the correct directory

## 📈 Adding New Tests

To add tests for a new module:

1. Create a new test file: `test_module_name.py`
2. Import the module to test
3. Create test classes inheriting from `unittest.TestCase`
4. Write test methods starting with `test_`
5. Run tests to verify

Example:

```python
"""
Unit tests for new_module
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from new_module import NewClass


class TestNewClass(unittest.TestCase):
    """Test cases for NewClass"""
    
    def test_functionality(self):
        """Test basic functionality"""
        obj = NewClass()
        result = obj.method()
        self.assertEqual(result, expected_value)


if __name__ == '__main__':
    unittest.main()
```

## 🎯 Continuous Integration

These tests can be integrated into CI/CD pipelines:

```bash
# In your CI script
cd src/tests
python run_tests.py
```

The test runner exits with code 0 on success and 1 on failure, making it suitable for CI systems.

## 📞 Support

For issues or questions about the tests, please refer to the main project documentation or create an issue in the project repository.

