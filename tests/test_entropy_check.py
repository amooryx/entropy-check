import argparse
import math
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import entropy_check
import rclib


class MeasureFileTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.directory = Path(self.temp_dir.name)

    def test_empty_file_has_zero_size_and_entropy(self):
        path = self.directory / "empty.bin"
        path.touch()

        self.assertEqual(entropy_check.measure_file(path), (0, 0.0))

        context = rclib.Context(
            args=argparse.Namespace(), tool="entropy-check", target=str(path)
        )
        with redirect_stdout(StringIO()):
            self.assertEqual(entropy_check.run(context), 0)
        self.assertEqual(context.data, {"entropy": 0.0, "size": 0})

    def test_unicode_path_and_utf8_contents(self):
        path = self.directory / "données-密码-🔐.bin"
        content = "naïve café 密码 🔐".encode("utf-8")
        path.write_bytes(content)

        size, entropy = entropy_check.measure_file(path)

        self.assertEqual(size, len(content))
        self.assertGreater(entropy, 0.0)
        self.assertLessEqual(entropy, 8.0)

    def test_large_file_is_measured_across_multiple_chunks(self):
        path = self.directory / "large.bin"
        content = bytes(range(256)) * 8192
        path.write_bytes(content)

        size, entropy = entropy_check.measure_file(path)

        self.assertEqual(size, len(content))
        self.assertTrue(math.isclose(entropy, 8.0))

    def test_repeated_byte_has_zero_entropy(self):
        path = self.directory / "repeated.bin"
        path.write_bytes(b"A" * 1000)

        self.assertEqual(entropy_check.measure_file(path), (1000, 0.0))

    def test_high_byte_entropy_is_reported_as_a_heuristic(self):
        path = self.directory / "uniform.bin"
        path.write_bytes(bytes(range(256)))
        context = rclib.Context(
            args=argparse.Namespace(), tool="entropy-check", target=str(path)
        )

        with redirect_stdout(StringIO()):
            self.assertEqual(entropy_check.run(context), 0)

        self.assertEqual(context.findings[0].severity, "medium")
        self.assertIn("consistent with", context.findings[0].title)
        self.assertIn("heuristic only", context.findings[0].detail)


if __name__ == "__main__":
    unittest.main()
