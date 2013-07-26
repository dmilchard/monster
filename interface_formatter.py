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

        # [ (rec_type, (name, position, action, field), ... ), ... ) ]
        #
        # Each tuple within the map represents a line to be written to the csv
        # file. Within each the first element is the record type, and the
        # second is another tuple holding:
        #    - field name;
        #    - position in the line to put the value;
        #    - literal value to enter / position to find the value in the TMS
        #      data / function to run on the value from the TMS data;
        #    - (if a function is provided) the position to find the value in
        #      the TMS file that should be passed to the function.
        self.position_map = (('00EMPLOYEE',
                              ('new_employee', 6, 'Y')),
                             ('10PERDET',
                              ('surname', 7, 1),
                              ('first_forename', 8, 0),
                              ('surname', 7, -1),
                              ('first_forename', 8, -1),
                              ('other_forenames', 9, -1),
                              ('title', 10, -1),
                              ('gender', 11, -1),
                              ('known_as_forename', 12, -1),
                              ('dob', 13, -1),
                              ('nino', 14, -1),
                              ('email', 18, -1),
                              ('address_1', 19, -1),
                              ('address_2', 20, -1),
                              ('address_3', 21, -1),
                              ('address_4', 22, -1),
                              ('country', 25, -1),
                              ('post_code', 26, -1),
                              ('home_tel', 27, -1),
                              ('mobile_tel', 29, -1),
                              ('passport_no', 42, -1),
                              ('passport_country', 43, -1),
                              ('passport_expiry', 44, -1)),
                             ('15ADDDET',
                              ('nationality', 6, -1),
                              ('ethnic_origin', 7, -1),
                              ('country_of_birth', 8, -1),
                              ('notice_period', 18, -1),
                              ('religion', 22, -1),
                              ('sexual_orientation', 23, -1)),
                             ('20RELATION',
                              ('rel_surname', 8, -1),
                              ('rel_first_forename', 9, -1),
                              ('rel_title', 11, -1),
                              ('rel_address_1', 16, -1),
                              ('rel_address_2', 17, -1),
                              ('rel_address_3', 18, -1),
                              ('rel_address_4', 19, -1),
                              ('rel_post_code', 23, -1),
                              ('rel_home_tel', 24, -1),
                              ('rel_work_tel', 25, -1),
                              ('rel_mobile_tel', 26, -1)),
                             ('30BANK',
                              ('pay_method', 7, -1)),
                             ('35EMPBASIC',
                              ('current_start_date', 6, format_date, 2),
                              ('current_start_reason', 7, -1),
                              ('suspended_indicator', 9, -1),
                              ('employee_type', 10, -1),
                              ('original_start_date', 11, -1),
                              ('original_start_reason', 12, -1),
                              ('probation_date', 13, -1)))

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
                # If it's a function, call it with the value from the field ref
                # represented by the forth element:
                if callable(field[2]):
                    line.append(field[2](row[field[3]]))
                else:
                    # If it's a string, add the value.
                    try:
                        field[2].isupper()
                        line.append(field[2])

                    # If it's not a string or a function it must be a number so
                    # use this as the position of the value in the input file.
                    except AttributeError:
                        # Ignore -1 placeholder
                        if field[2] == -1:
                            continue
                        line.append(row[field[2]])

                position += 1

            # Add the complete line to the return list.
            lines.append(line)

        return lines


def format_date(date):
    """ Removes slashes from a date string """
    return date[:2] + date[3:5] + date[6:]

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: format_file <input_file> <output_file> '
                         '<log_file>\n')
        sys.exit(1)

    input_file, output_file, log_file = sys.argv[1:]
    formatter = InterfaceFormatter(input_file, output_file, log_file)
    formatter.run()
