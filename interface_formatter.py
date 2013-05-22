import csv
import sys

class Interface_Formatter():

    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file

        #  [ (rec_type, (name, position, action, field), ...), ... ]
        self.position_map = [('00EMPLOYEE',
                              ('new_employee', 6, 'Y')),
                             ('10PERDET',
                              ('surname', 7, 1),
                              ('first_forename', 8, 0),
                              ('dob', 13, self.format_date, 2))]

##      self.position_map = {
##          '00EMPLOYEE': {
##              'new_employee': (6, -1)},
##          '10PERDET': {
##              'surname': (7, -1),
##              'first_forename': (8, -1),
##              'other_forenames': (9, -1),
##              'title': (10, -1),
##              'gender': (11, -1),
##              'known_as_forename': (12, -1),
##              'dob': (13, -1),
##              'nino': (14, -1),
##              'email': (18, -1),
##              'address_1': (19, -1),
##              'address_2': (20, -1),
##              'address_3': (21, -1),
##              'address_4': (22, -1),
##              'country': (25, -1),
##              'post_code': (26, -1),
##              'home_tel': (27, -1),
##              'mobile_tel': (29, -1),
##              'passport_no': (42, -1),
##              'passport_country': (43, -1),
##              'passport_expiry': (44, -1)},
##          '15ADDDET': {
##              'nationality': (6, -1),
##              'ethnic_origin': (7, -1),
##              'country_of_birth': (8, -1),
##              'notice_period': (18, -1),
##              'religion': (22, -1),
##              'sexual_orientation': (23, -1)},
##          '20RELATION': {
##              'rel_surname': (8, -1),
##              'rel_first_forename': (9, -1),
##              'rel_title': (11, -1),
##              'rel_address_1': (16, -1),
##              'rel_address_2': (17, -1),
##              'rel_address_3': (18, -1),
##              'rel_address_4': (19, -1),
##              'rel_post_code': (23, -1),
##              'rel_home_tel': (24, -1),
##              'rel_work_tel': (25, -1),
##              'rel_mobile_tel': (26, -1)},
##          '30BANK': {
##              'pay_method': (7, -1)},
##          '35EMPBASIC': {
##              'current_start_date': (6, -1).
##              'current_start_reason': (7, -1),
##              'suspended_indicator': (9, -1),
##              'employee_type': (10, -1),
##              'original_start_date': (11, -1),
##              'original_start_reason': (12, -1),
##              'probation_date': (13, -1)}
##          }

    def run(self):

        # Monster source file:
        with open(self.input_file, 'r') as input_file:
            reader = csv.reader(input_file)
            transaction_id = 1

            # Output file formatted for RL:
            with open(self.output_file, 'wb') as output_file:
                writer = csv.writer(output_file)

                # Transform each row in the Monster file into the format
                # required by RL and write to the output file.
                for row in reader:

                    for line in self.get_lines(row, transaction_id):
                        writer.writerow(line)

                    transaction_id += 1

    def get_lines(self, row, transaction_id = ''):

        lines = []

        # Each list item in the array represents a line to be output.
        for record in self.position_map:

            # The first element of each tuple in the list is the record type.
            line = [record[0], transaction_id]

            # Subsequent elements in each tuple hold the details about how to
            # output the field.
            # field[0] holds the field name (refernce only).
            # field[1] holds the position in the output file.
            # field[2] holds the action.
            # field[3:] holds the remaining parameters (if any)
            position = 2
            for field in record[1:]:

                # Add empty strings to the list until the position is
                # reached.
                while position < field[1] - 1:
                    line.append('')
                    position += 1

                # Duck tests for the type of the paramater.
                # If it's a function, call it with the value from the
                # third argument:
                if callable(field[2]):
                    line.append(field[2](row[field[3]]))
                else:
                    # If it's a string, add the value.
                    try:
                        field[2].islower()
                        line.append(field[2])

                    # If not a string or a function it must be a number so
                    # use this as the position of the value in the monster
                    # file.
                    except AttributeError:
                        line.append(row[field[2]])

                position += 1

            # Add the complete line to the return list.
            lines.append(line)

        return lines

    def format_date(self, date):
        """ Removes slashes from a date string"""
        return date[:2] + date[3:5] + date[6:]


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.stderr.write('Usage: format_file <input_file> <output_dir> <log_file>\n')
        sys.exit(1)

    input_file, output_file, log_file = sys.argv[1:]
    formatter = Interface_Formatter(input_file, output_file, log_file)
    formatter.run()
