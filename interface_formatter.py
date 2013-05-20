import csv
import sys

class Interface_Formatter():

	def __init__(self, input_file, output_dir, log_file):
		self.input_file = input_file
		self.output_dir = output_dir
		self.position_map = {
			'00EMPLOYEE': {
				'new_employee': (6, -1)},
			'10PERDET': {
				'surname': (7, -1),
				'first_forename': (8, -1),
				'other_forenames': (9, -1),
				'title': (10, -1),
				'gender': (11, -1),
				'known_as_forename': (12, -1),
				'dob': (13, -1),
				'nino': (14, -1),
				'email': (18, -1),
				'address_1': (19, -1),
				'address_2': (20, -1),
				'address_3': (21, -1),
				'address_4': (22, -1),
				'country': (25, -1),
				'post_code': (26, -1),
				'home_tel': (27, -1),
				'mobile_tel': (29, -1),
				'passport_no': (42, -1),
				'passport_country': (43, -1),
				'passport_expiry': (44, -1)},
			'15ADDDET': {
				'nationality': (6, -1),
				'ethnic_origin': (7, -1),
				'country_of_birth': (8, -1),
				'notice_period': (18, -1),
				'religion': (22, -1),
				'sexual_orientation': (23, -1)},
			'20RELATION': {
				'rel_surname': (8, -1),
				'rel_first_forename': (9, -1),
				'rel_title': (11, -1),
				'rel_address_1': (16, -1),
				'rel_address_2': (17, -1),
				'rel_address_3': (18, -1),
				'rel_address_4': (19, -1),
				'rel_post_code': (23, -1),
				'rel_home_tel': (24, -1),
				'rel_work_tel': (25, -1),
				'rel_mobile_tel': (26, -1)},
			'30BANK': {
				'pay_method': (7, -1)},
			'35EMPBASIC': {
				'current_start_date': (6, -1).
				'current_start_reason': (7, -1),
				'suspended_indicator': (9, -1),
				'employee_type': (10, -1),
				'original_start_date': (11, -1),
				'original_start_reason': (12, -1),
				'probation_date': (13, -1)}
			}

	def run(self):
		with open(self.input_file, 'r') as csvfile:
			reader = csv.reader(csvfile)
			transaction_id = 1
			for row in reader:
				transaction = self.get_lines(row, transaction_id)
				print(transaction)
				transaction_id += 1

	def get_lines(self, row, transaction_id):
		"""Walks through the position map dictionaries to get the indexes of the
			associated fields in the TMS output row, the literal value to be inserted,
			or the function to be run on the field value in the TMS file"""
		lines = []
		for record_type in self.position_map.keys():
			line = [record_type, transaction_id]

			for field in self.position_map[record_type].keys():
				params = self.position_map[record_type][field]
				
				# Duck tests for the type of the paramater.
				# If it's a function, call it with the value from the third argument:
				if callable(params[1]):
					params[1](row[params[2]])
				else:
					# Duck test for string object:
					try:
						params[1].islower()
						print('string\n')

					# Object must be an index:
					except:
						print('number\n')

		return


if __name__ == '__main__':
	if len(sys.argv) != 4:
		sys.stderr.write('Usage: format_file <input_file> <output_dir> <log_file>\n')
		sys.exit(1)

	input_file, output_dir, log_file = sys.argv[1:]
	formatter = Interface_Formatter(input_file, output_dir, log_file)
	formatter.run()
