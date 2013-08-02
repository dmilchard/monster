import unittest
import interface_formatter
import csv
from os import remove
from os.path import abspath, join, exists, split

class test_formatter(unittest.TestCase):

    def setUp(self):
        cur_dir = split(abspath(__file__))[0]
        self.input_path = join(cur_dir, 'test.csv')
        self.output_path = join(cur_dir, 'output.csv')
        self.formatter = interface_formatter.InterfaceFormatter(self.input_path,
                self.output_path, None)

    def delete_output_file(self):
        if exists(self.output_path):
            remove(self.output_path)

    def test_output_file_is_created(self):
        self.delete_output_file()
        self.formatter.run()
        self.assertTrue(exists(self.output_path))

    def test_output_file_has_expected_row_count(self):
        self.delete_output_file()
        self.formatter.run()
        rows_per_employee = len(self.formatter.position_map)

        with open(self.input_path) as input_csv:
            reader = csv.reader(input_csv)
            num_emps = len([row for row in reader])

        with open(self.output_path) as output_csv:
            reader = csv.reader(output_csv)
            output_rows = len([row for row in reader])

        self.assertEqual(output_rows, rows_per_employee * num_emps)

    def test_get_lines_treats_values_correctly(self):
        test_function_one = lambda row, x: row[x[0]]
        test_function_two = lambda row, x: row[x[0]] + row[x[1]]
        new_position_map = (
                ('TEST_STRING',
                    ('test1', 3, 'LITERAL')),
                ('TEST_POSITION',
                    ('test2', 3, 3)),
                ('TEST_FUNCTION_ONE',
                    ('test3', 4, test_function_one, 2)),
                ('TEST_FUNCTION_TWO',
                    ('test4', 5, test_function_two, 3, 1)),
                ('TEST_EVERYTHING',
                    ('test5', 3, 1),
                    ('test6', 4, test_function_one, 0),
                    ('test7', 6, 'ANOTHER_LITERAL'),
                    ('test8', 7, test_function_two, 2, 5))
                )
        row = ['this', 'is', 'a', 'test', 'input', 'row']
        expected_output = [
                ['TEST_STRING','','LITERAL'],
                ['TEST_POSITION','','test'],
                ['TEST_FUNCTION_ONE','','','a'],
                ['TEST_FUNCTION_TWO','','','','testis'],
                ['TEST_EVERYTHING','','is','this','','ANOTHER_LITERAL','arow']
                ]
        
        original_position_map = self.formatter.position_map
        self.formatter.position_map = new_position_map
        self.assertEqual(self.formatter._get_lines(row), expected_output)

        self.formatter._position_map = original_position_map


class test_additional_functions(unittest.TestCase):
    ''' Tests for functions called by the formatter to allow formatted or
        calculated fields.
    '''

    def test_get_date_returns_expected_format(self):
        row = ['20/07/1983']
        self.assertEqual(interface_formatter.format_date(row, [0]), '20071983')
        row = ['01/02/2013']
        self.assertEqual(interface_formatter.format_date(row, [0]), '01022013')


if __name__ == '__main__':
    unittest.main()
