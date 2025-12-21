"""
Test runner for ChatPPT project
Run all unit tests with coverage reporting
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests(verbosity=2):
    """
    Run all unit tests in the tests directory

    Args:
        verbosity: Level of output detail (0=quiet, 1=normal, 2=verbose)

    Returns:
        TestResult object
    """
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result


def run_specific_module(module_name, verbosity=2):
    """
    Run tests for a specific module

    Args:
        module_name: Name of the test module (e.g., 'test_data_structures')
        verbosity: Level of output detail

    Returns:
        TestResult object
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(module_name)

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run ChatPPT unit tests')
    parser.add_argument(
        '-m', '--module',
        help='Run tests for specific module (e.g., test_data_structures)',
        default=None
    )
    parser.add_argument(
        '-v', '--verbosity',
        help='Verbosity level (0-2)',
        type=int,
        default=2
    )

    args = parser.parse_args()

    print("=" * 70)
    print("ChatPPT Unit Tests")
    print("=" * 70)

    if args.module:
        print(f"\nRunning tests for module: {args.module}\n")
        result = run_specific_module(args.module, args.verbosity)
    else:
        print("\nRunning all tests...\n")
        result = run_all_tests(args.verbosity)

    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

