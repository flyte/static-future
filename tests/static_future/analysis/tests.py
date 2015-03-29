import __future__
import textwrap
import unittest

from static_future.analysis import future_imports, features, compiler_flags


class FutureImportsTests(unittest.TestCase):

    def test_extract_single_future_import(self):
        """Extract a single import from __future__"""
        code = textwrap.dedent("""\
            from __future__ import print_function
            """)
        names = list(future_imports(code))
        self.assertEqual(names, ["print_function"])

    def test_extract_multiple_future_imports_lines(self):
        """Extract multiple __future__ imports on separate lines"""
        code = textwrap.dedent("""\
            from __future__ import print_function
            from __future__ import absolute_import
            """)
        names = list(future_imports(code))
        self.assertEqual(names, ["print_function", "absolute_import"])

    def test_extract_multiple_future_imports_parentheses(self):
        """Extract multiple __future__ imports within parentheses"""
        code = textwrap.dedent("""\
            from __future__ import (print_function, absolute_import)
            """)
        names = list(future_imports(code))
        self.assertEqual(names, ["print_function", "absolute_import"])

    def test_extract_multiple_future_imports_parentheses_lines(self):
        """Extract multiple __future__ imports within parentheses two lines"""
        code = textwrap.dedent("""\
            from __future__ import (print_function,
                absolute_import)
            """)
        names = list(future_imports(code))
        self.assertEqual(names, ["print_function", "absolute_import"])

    def test_extract_multiple_future_imports_lines_escape(self):
        """Extract multiple __future__ imports with newline escaped"""
        code = textwrap.dedent("""\
            from __future__ import print_function, \
                absolute_import
            """)
        names = list(future_imports(code))
        self.assertEqual(names, ["print_function", "absolute_import"])

    def test_extract_correct_future_imports_when_imported_as_another(self):
        """Extract only the correct imports when one is imported as another"""
        code = textwrap.dedent("""\
            from __future__ import print_function as absolute_import
            """)
        names = list(future_imports(code))
        self.assertEqual(names, ["print_function"])

    def test_extract_correct_future_imports_with_other_code(self):
        """Extract only the correct imports when code exists in src"""
        code = textwrap.dedent("""\
            from __future__ import print_function

            while True:
                print("Hello, world!")
            """)
        names = list(future_imports(code))
        self.assertEqual(names, ["print_function"])


class FeaturesTests(unittest.TestCase):

    def test_extract_single_future_import(self):
        """Extract a single import from __future__"""
        code = textwrap.dedent("""\
            from __future__ import print_function
            """)
        ftures = list(features(code))
        self.assertEqual(ftures, [__future__.print_function])

    def test_extract_multiple_future_imports_lines(self):
        """Extract multiple __future__ imports on separate lines"""
        code = textwrap.dedent("""\
            from __future__ import print_function
            from __future__ import absolute_import
            """)
        ftures = list(features(code))
        self.assertEqual(ftures, [
            __future__.print_function, __future__.absolute_import])

    def test_extract_multiple_future_imports_parentheses(self):
        """Extract multiple __future__ imports within parentheses"""
        code = textwrap.dedent("""\
            from __future__ import (print_function, absolute_import)
            """)
        ftures = list(features(code))
        self.assertEqual(ftures, [
            __future__.print_function, __future__.absolute_import])

    def test_extract_multiple_future_imports_parentheses_lines(self):
        """Extract multiple __future__ imports within parentheses two lines"""
        code = textwrap.dedent("""\
            from __future__ import (print_function,
                absolute_import)
            """)
        ftures = list(features(code))
        self.assertEqual(ftures, [
            __future__.print_function, __future__.absolute_import])

    def test_extract_multiple_future_imports_lines_escape(self):
        """Extract multiple __future__ imports with newline escaped"""
        code = textwrap.dedent("""\
            from __future__ import print_function, \
                absolute_import
            """)
        ftures = list(features(code))
        self.assertEqual(ftures, [
            __future__.print_function, __future__.absolute_import])

    def test_extract_correct_future_imports_when_imported_as_another(self):
        """Extract only the correct imports when one is imported as another"""
        code = textwrap.dedent("""\
            from __future__ import print_function as absolute_import
            """)
        ftures = list(features(code))
        self.assertEqual(ftures, [__future__.print_function])

    def test_extract_correct_future_imports_with_other_code(self):
        """Extract only the correct imports when code exists in src"""
        code = textwrap.dedent("""\
            from __future__ import print_function

            while True:
                print("Hello, world!")
            """)
        ftures = list(features(code))
        self.assertEqual(ftures, [__future__.print_function])


class CompilerFlagsTests(unittest.TestCase):

    def test_extract_single_future_import(self):
        """Extract a single import from __future__"""
        code = textwrap.dedent("""\
            from __future__ import print_function
            """)
        flags = compiler_flags(code)
        self.assertEqual(flags, __future__.print_function.compiler_flag)

    def test_extract_multiple_future_imports_lines(self):
        """Extract multiple __future__ imports on separate lines"""
        code = textwrap.dedent("""\
            from __future__ import print_function
            from __future__ import absolute_import
            """)
        flags = compiler_flags(code)
        expected_flags = __future__.print_function.compiler_flag | \
            __future__.absolute_import.compiler_flag
        self.assertEqual(flags, expected_flags)

    def test_extract_multiple_future_imports_parentheses(self):
        """Extract multiple __future__ imports within parentheses"""
        code = textwrap.dedent("""\
            from __future__ import (print_function, absolute_import)
            """)
        flags = compiler_flags(code)
        expected_flags = __future__.print_function.compiler_flag | \
            __future__.absolute_import.compiler_flag
        self.assertEqual(flags, expected_flags)

    def test_extract_multiple_future_imports_parentheses_lines(self):
        """Extract multiple __future__ imports within parentheses two lines"""
        code = textwrap.dedent("""\
            from __future__ import (print_function,
                absolute_import)
            """)
        flags = compiler_flags(code)
        expected_flags = __future__.print_function.compiler_flag | \
            __future__.absolute_import.compiler_flag
        self.assertEqual(flags, expected_flags)

    def test_extract_multiple_future_imports_lines_escape(self):
        """Extract multiple __future__ imports with newline escaped"""
        code = textwrap.dedent("""\
            from __future__ import print_function, \
                absolute_import
            """)
        flags = compiler_flags(code)
        expected_flags = __future__.print_function.compiler_flag | \
            __future__.absolute_import.compiler_flag
        self.assertEqual(flags, expected_flags)

    def test_extract_correct_future_imports_when_imported_as_another(self):
        """Extract only the correct imports when one is imported as another"""
        code = textwrap.dedent("""\
            from __future__ import print_function as absolute_import
            """)
        flags = compiler_flags(code)
        self.assertEqual(flags, __future__.print_function.compiler_flag)

    def test_extract_correct_future_imports_with_other_code(self):
        """Extract only the correct imports when code exists in src"""
        code = textwrap.dedent("""\
            from __future__ import print_function

            while True:
                print("Hello, world!")
            """)
        flags = compiler_flags(code)
        self.assertEqual(flags, __future__.print_function.compiler_flag)

    def test_StringIO_import_error(self):
        """If StringIO cannot be imported from StringIO then import from io"""
        # @TODO: Mock this somehow for more coverage points
        pass
