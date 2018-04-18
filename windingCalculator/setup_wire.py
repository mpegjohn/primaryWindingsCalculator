import os
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
			'windingCalculator.settings')

import django
django.setup()
from designer.models import Wire

def populate():

	with open("wire_sizes.csv") as csvfile:
	        reader = csv.reader(csvfile)
		first_row = 1
		for row in reader:

			if first_row == 1:
				first_row = 0
				continue

			w = Wire(diameter=float(row[0]),
				grade_1_dia_max=float(row[1]),
				grade_2_dia_max=float(row[2]))
			w.save(force_insert=True)	

if __name__ == '__main__':
	populate()
