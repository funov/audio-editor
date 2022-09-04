import unittest
from unittest.mock import patch, mock_open

from model.audio_info import AudioInfo
from model.files_utils import replace_with_rename
from model.time_utils import (
    to_str_time,
    from_str_time_to_int_seconds,
    get_file_name,
    _add_start_zeros,
    _convert
)


class AudioInfoTests(unittest.TestCase):
    def setUp(self):
        pass


class FilesUtilsTests(unittest.TestCase):
    def setUp(self):
        pass


class TimeUtilsTests(unittest.TestCase):
    def setUp(self):
        self.expected_to_str_time_zeros = '00:00:00'
        self.expected_to_str_time = '55:31:03'

        self.expected_from_str_time_to_int_seconds_zeros = 0
        self.expected_from_str_time_to_int_seconds = 199_863

        self.expected_add_start_zeros = '05.45'

        self.expected_convert = (0, 6)

    def test_to_str_time_zeros(self):
        str_time = to_str_time(0, 0, 0)

        self.assertEqual(self.expected_to_str_time_zeros, str_time)

    def test_to_str_time(self):
        str_time = to_str_time(63, 90, 54)

        self.assertEqual(self.expected_to_str_time, str_time)

    def test_from_str_time_to_int_seconds_zeros(self):
        int_seconds = from_str_time_to_int_seconds('00:00:00')

        self.assertEqual(self.expected_from_str_time_to_int_seconds_zeros, int_seconds)

    def test_from_str_time_to_int_seconds(self):
        int_seconds = from_str_time_to_int_seconds('55:31:03')

        self.assertEqual(self.expected_from_str_time_to_int_seconds, int_seconds)

    def test_unique_file_names(self):
        file_names = []

        for i in range(1_000):
            file_names.append(get_file_name())

        self.assertEqual(len(file_names), len(set(file_names)))

    def test_add_start_zeros(self):
        result = _add_start_zeros(5.45)

        self.assertEqual(self.expected_add_start_zeros, result)

    def test_convert(self):
        result = _convert(180, 3)

        self.assertEqual(self.expected_convert, result)
