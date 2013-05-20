import csv
import sys

class Interface_Formatter():

	def __init__(self, input_file, output_dir, log_file):
		self.input_file = input_file
		self.output_dir = output_dir
		self.position_map = {
			'00EMPLOYEE': {
				'new_employee': (6, 'Y')},
			'10PERDET': {
				'surname': (7, 2),
				'first_forename': (8, 1),
				'title': (11, 6),
				'dob': (13, 7)}
			}

	def run(self):
		with open(self.input_file, 'r') as csvfile:
			reader = csv.reader(csvfile)
			transaction_id = 1
			for row in reader:
				self.get_lines(row, transaction_id)

	def get_lines(self, row, transaction_id):
		"""Walks through the position map dictionaries to get the indexes of the
			associated fields in the TMS output row, the literal value to be inserted,
			or the function to be run on the field value in the TMS file"""
		lines = []
		for rec_type in self.position_map.keys():
			line = [rec_type, transaction_id]

			for field in self.position_map[rec_type].keys():
				params = self.position_map[rec_type][field]
				
				# Duck tests for the type of the paramater.
				# If it's a function, call it with the third argument:
				if callable(params[1]):
					params[1](params[2])

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
