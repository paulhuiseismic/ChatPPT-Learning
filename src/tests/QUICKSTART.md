# ChatPPT Unit Tests - Quick Start Guide

## 🚀 Quick Start

### Run All Tests (Recommended)
```bash
cd src/tests
python run_tests.py
```

### Run Tests on Windows
```bash
cd src/tests
run_tests.bat
```

### Run with unittest
```bash
cd src/tests
python -m unittest discover -v
```

## 📊 Test Coverage

- **60+ Unit Tests** covering all core modules
- **100% Pass Rate**
- **No Breaking Changes**

## 📁 Test Files

```
src/tests/
├── test_data_structures.py      (14 tests)
├── test_layout_manager.py       (16 tests)
├── test_slide_builder.py        (5 tests)
├── test_input_parser.py         (9 tests)
├── test_config.py               (4 tests)
├── test_utils.py                (2 tests)
├── test_template_manager.py     (4 tests)
├── test_chat_history.py         (4 tests)
└── test_gradio_app.py           (8 tests)
```

## ✅ What's Tested

- ✅ Data structures (SlideContent, Slide, PowerPoint)
- ✅ Layout management and encoding
- ✅ Slide building with various content types
- ✅ Markdown input parsing
- ✅ Configuration loading
- ✅ Utility functions
- ✅ Template management
- ✅ Chat history sessions
- ✅ Gradio app functions

## 📖 Documentation

- **Detailed Guide**: `src/tests/README.md`
- **Implementation Summary**: `UNIT_TEST_SUMMARY.md`

## 🎯 Example Commands

```bash
# Run specific test file
python test_data_structures.py

# Run specific test class
python -m unittest test_layout_manager.TestLayoutManager

# Run specific test method
python -m unittest test_config.TestConfig.test_config_loading

# Run with verbose output
python run_tests.py -v 2

# Run with quiet output
python run_tests.py -v 0
```

## ✨ Features

- 🔍 Comprehensive coverage of core functionality
- 🛡️ Error handling and edge case testing
- 📝 Well-documented test cases
- 🔄 Independent, isolated tests
- ⚡ Fast execution with mocked dependencies
- 🎨 Clean, maintainable code

---
**Status**: ✅ Complete | **Tests**: 60+ | **Pass Rate**: 100%

