from django.db import models

# Create your models here.
class CO2(models.Model):
	Year = models.IntegerField()
	Month = models.IntegerField()
	co2_ppm = models.FloatField()

	def __str__(self):
		return '{} {} {}'.format(self.Year,self.Month,self.co2_ppm)

	def to_dict(self):
		return {
			'Year': self.Year,
			'Month': self.Month,
			'co2_ppm': self.co2_ppm,
		}

class Temperature(models.Model):
	Year = models.IntegerField()
	Month = models.IntegerField()
	Temp = models.FloatField()

	def __str__(self):
		return '{} {} {}'.format(self.Year,self.Month,self.Temp)

	def to_dict(self):
		return {
			'Year': self.Year,
			'Month': self.Month,
			'Temp': self.Temp,
		}

class Glacier(models.Model):
	Year = models.IntegerField()
	Mean = models.FloatField()

	def __str__(self):
		return '{} {}'.format(self.Year,self.Mean)

	def to_dict(self):
		return {
			'Year': self.Year,
			'Mean': self.Mean,
		}