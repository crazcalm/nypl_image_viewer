import unittest
from unittest import TestCase
from pathlib import Path
from tempfile import TemporaryDirectory

from nypl_image_viewer.filesystem import write_file


class TestWriteFile(TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.test_data = "hello world"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_write_file(self) -> None:
        expected_num_of_files = 1

        dest_dir = (self.temp_dir.name, "testing", "filesytem")
        dest_name = "test_file.txt"

        write_file(data=self.test_data, dest_dir=dest_dir, dest_name=dest_name)

        result_file = Path(*dest_dir, dest_name)
        self.assertTrue(result_file.is_file())
        self.assertEqual(result_file.read_text(), self.test_data)

        # Calling write_file twice does not result in multiple files
        write_file(data=self.test_data, dest_dir=dest_dir, dest_name=dest_name)

        result_dir = Path(*dest_dir)
        self.assertEqual(
            len(list(result_dir.iterdir())),
            expected_num_of_files,
        )


if __name__ == "__main__":
    unittest.main()
