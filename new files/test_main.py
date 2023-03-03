import unittest
from unittest.mock import patch, mock_open
import csv
import os
import datetime
from main import format_title, write_csv

class TestFormatTitle(unittest.TestCase):

    def test_format_title_less_than_cols(self):
        items = ['a', 'b', 'c']
        expected_output = items + ['', '', '', '', '']
        self.assertEqual(format_title(items, cols=8), expected_output)

    def test_format_title_more_than_cols(self):
        items = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
        expected_output = items[:11] + ['', '', '', '']
        self.assertEqual(format_title(items, cols=15), expected_output)


class TestWriteCSV(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_write_csv(self, mock_file):
        rows = [['a', 'b', 'c'], ['1', '2', '3']]
        filename = 'test.csv'

        write_csv(filename, rows)

        mock_file.assert_called_once_with(filename, 'a', newline='')
        target = csv.writer(mock_file(), delimiter='\t', lineterminator=os.linesep)
        target.writerows(rows)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_csv_empty_rows(self, mock_file):
        rows = []
        filename = 'test.csv'

        write_csv(filename, rows)

        mock_file.assert_called_once_with(filename, 'a', newline='')
        target = csv.writer(mock_file(), delimiter='\t', lineterminator=os.linesep)
        target.writerows(rows)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_csv_datetime_filename(self, mock_file):
        rows = [['a', 'b', 'c'], ['1', '2', '3']]
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'{current_time}.csv'

        write_csv(filename, rows)

        mock_file.assert_called_once_with(filename, 'a', newline='')
        target = csv.writer(mock_file(), delimiter='\t', lineterminator=os.linesep)
        target.writerows(rows)



