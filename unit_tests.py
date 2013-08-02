import unittest
import interface_formatter
from os import remove
from os.path import abspath, join, exists, split

class test_formatter(unittest.TestCase):

    def setUp(self):
        cur_dir = split(abspath(__file__))[0]
        self.input_path = join(cur_dir, 'test.csv')
        self.output_path = join(cur_dir, 'output.csv')
        self.formatter = interface_formatter.InterfaceFormatter(self.input_path,
                self.output_path, None)

    def test_output_file_is_created(self):
        if exists(self.output_path):
            remove(self.output_path)
        self.formatter.run()
        self.assertTrue(exists(self.output_path))


class test_additional_functions(unittest.TestCase):
    ''' Tests for functions called by the formatted to allow formatted or
        calculated fields.
    '''

    def test_get_date_returns_expected_format(self):
        row = ['20/07/1983']
        self.assertEqual(interface_formatter.format_date(row, [0]), '20071983')
        row = ['01/02/2013']
        self.assertEqual(interface_formatter.format_date(row, [0]), '01022013')


if __name__ == '__main__':
    unittest.main()
