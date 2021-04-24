import os
import django
import csv
import sys
import datetime as dt

os.environ.setdefault('DJANGO_SETTINGS_MODULE','TEProject.settings')

django.setup()

from projdir.models import CO2, Temperature, Glacier

def start_co2():
	try:
		with open('co2_dataset.csv') as csvfile:
			reader=csv.DictReader(csvfile)
			for row in reader:
				if len(row) > 3:
					raise Exception("extraCol")
				if row['co2_ppm']:
					p=CO2(Year=row['Year'],Month=row['Month'], co2_ppm=row['co2_ppm'])
					p.save()
			return ''
	except:
		error = str(sys.exc_info()[0])
		if error == "<class 'KeyError'>":
			return 'Error: One/More Column Missing/Name Mismatch'
		if error == "<class 'ValueError'>":
			return 'Error: Column contains Invalid Value'
		if error == "<class 'Exception'>":
			return 'Error: Extra Columns present in dataset'


def start_temp():
	try:
		with open('temp_dataset.csv') as csvfile:
			reader=csv.DictReader(csvfile)

			for row in reader:
				year = (int(dt.datetime.strptime(row['Date'], "%Y-%m-%d").strftime('%Y')))
				month = (int(dt.datetime.strptime(row['Date'], "%Y-%m-%d").strftime('%m')))
				p=Temperature(Year=year, Month=month, Temp=row['LandMaxTemperature'])
				p.save()
			return ''
	except:
		error = str(sys.exc_info()[0])
		if error == "<class 'KeyError'>":
			return 'Error: One/More Column Missing/Name Mismatch'
		if error == "<class 'ValueError'>":
			return 'Error: Column contains Invalid Value'


def start_glacier():
	try:
		with open('glacier_dataset.csv') as csvfile:
			reader=csv.DictReader(csvfile)
			for row in reader:
				if len(row) > 2:
					raise Exception("extraCol")
				p=Glacier(Year=row['Year'],Mean=row['Mean_cumulative_mass_balance'])
				p.save()
			return ''
	except:
		error = str(sys.exc_info()[0])
		if error == "<class 'KeyError'>":
			return 'Error: One/More Column Missing/Name Mismatch'
		if error == "<class 'ValueError'>":
			return 'Error: Column contains Invalid Value'
		if error == "<class 'Exception'>":
			return 'Error: Extra Columns present in dataset'