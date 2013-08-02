from __future__ import print_function
import csv
import sys

class InterfaceFormatter():
    """ Reads a CSV extract containing new starter information from TMS and
        outputs a CSV file in the format required by the ResourceLink HR
        Interface.
		
		Fields in the output file may be a literal value (such as
        "Y" for a new starter), a value from the input file, or a value
        derived by running a function using a value from the input file (such
        as a date formatter). Process is exposed through the run function.
    """

    def __init__(self, input_file, output_file, log_file):
        """ Sets the input and outputfiles and builds the map that dictates
		    what do output for each field.
		"""
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file

        # [ (rec_type, (name, position, action, field1, ...), ... ), ... ) ]
        #
        # Each tuple within the map represents a line to be written to the csv
        # file. Within each the first element is the record type, and the
        # second is another tuple holding:
        #    - field name;
        #    - position in the line to put the value;
        #    - literal value to enter / position to find the value in the TMS
        #      data / function to run on the value from the TMS data;
        #    - (if a function is provided) the list of positions to find the
        #      value in the TMS file that should be passed to the function.
        self.position_map = (('00EMPLOYEE',
                              ('new_employee', 6, 'Y')),
                             ('10PERDET',
                              ('surname', 7, 1),
                              ('first_forename', 8, 0),
                              ('other_forenames', 9, None),
                              ('title', 10, None),
                              ('gender', 11, None),
                              ('known_as_forename', 12, None),
                              ('dob', 13, None),
                              ('nino', 14, None),
                              ('email', 18, None),
                              ('address_1', 19, None),
                              ('address_2', 20, None),
                              ('address_3', 21, None),
                              ('address_4', 22, None),
                              ('country', 25, None),
                              ('post_code', 26, None),
                              ('home_tel', 27, None),
                              ('mobile_tel', 29, None),
                              ('passport_no', 42, None),
                              ('passport_country', 43, None),
                              ('passport_expiry', 44, None)),
                             ('15ADDDET',
                              ('nationality', 6, None),
                              ('ethnic_origin', 7, None),
                              ('country_of_birth', 8, None),
                              ('notice_period', 18, None),
                              ('religion', 22, None),
                              ('sexual_orientation', 23, None)),
                             ('20RELATION',
                              ('rel_surname', 8, None),
                              ('rel_first_forename', 9, None),
                              ('rel_title', 11, None),
                              ('rel_address_1', 16, None),
                              ('rel_address_2', 17, None),
                              ('rel_address_3', 18, None),
                              ('rel_address_4', 19, None),
                              ('rel_post_code', 23, None),
                              ('rel_home_tel', 24, None),
                              ('rel_work_tel', 25, None),
                              ('rel_mobile_tel', 26, None)),
                             ('30BANK',
                              ('pay_method', 7, None)),
                             ('35EMPBASIC',
                              ('current_start_date', 6, format_date, 2),
                              ('current_start_reason', 7, None),
                              ('suspended_indicator', 9, None),
                              ('employee_type', 10, None),
                              ('original_start_date', 11, None),
                              ('original_start_reason', 12, None),
                              ('probation_date', 13, None)))

    def run(self):

        with open(self.input_file, 'r') as input_file, open(self.output_file, 
                'wb') as output_file:

            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            # Call _get_lines to process each row in the output file and
            # write the resulting records to the output file.
            [[writer.writerow(line) for line in self._get_lines(row)] \
                    for row in reader]


    def _get_lines(self, row, transaction_id = ''):
        """ Translates a row in the input csv file into multiple rows as
            outlined by the position map """

        lines = []

        # Each list item is a tuple representing a line to be output.
        for record in self.position_map:

            # The first element of each tuple is the record type.
            line = [record[0], transaction_id]

            # The second element is another tuple that holds information on
            # what should be output:
            # field[0] holds the field name (documentation purposes).
            # field[1] holds the position in the output file.
            # field[2] holds the function / value / field ref.
            # field[3] holds the field ref to pass to the function (if any).
            position = 2
            for field in record[1:]:

                # Add empty strings to the list until the position is reached.
                # -1 used as output positions start at 1 not 0 for consistency
                # with NGA's documentation.
                while position < field[1] - 1:
                    line.append('')
                    position += 1

                # Duck test for the type of the paramater.
                # If it's a function, call it with the row and the list of
                # field positions that hold the data to transform.
                if callable(field[2]):
                    line.append(field[2](row, field[3:]))
                else:
                    # If it's a string, add the value.
                    try:
                        field[2].isupper()
                        line.append(field[2])

                    # If it's not a string or a function it must be a number so
                    # use this as the position of the value in the input file.
                    except AttributeError:

                        # Note: explicitly compares to None so that 0 is a
                        # valid index.
                        if field[2] != None:
                            line.append(row[field[2]])

                position += 1

            # Add the complete line to the return list.
            lines.append(line)

        return lines


def format_date(row, position):
    """ Removes slashes from a date string in the format DD/MM/YYYY """
    date = row[position[0]]
    return date[:2] + date[3:5] + date[6:]

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: format_file <input_file> <output_file> '
                         '<log_file>\n')
        sys.exit(1)

    input_file, output_file, log_file = sys.argv[1:]
    formatter = InterfaceFormatter(input_file, output_file, log_file)
    formatter.run()
