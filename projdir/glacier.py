import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from .models import Glacier

class Glacier_Logic:
	def __init__(self):
		self.glacierdb = Glacier.objects.all()

	def mainfunc(self):
		if not self.glacierdb.exists():
			return False
		else:
			glacierdata = pd.DataFrame.from_records([s.to_dict() for s in self.glacierdb])
			self.grp1 = glacierdata.groupby(["Year"]).mean()["Mean"]
			means = self.grp1.values

			x_learn = [ (i, i**2, i**4) for i in self.grp1.index ]
			y_learn = [ i for i in means ]

			x_train, x_test, y_train, y_test = train_test_split(x_learn, y_learn, test_size=0.2, random_state=46)
			self.clf = LinearRegression().fit(x_train, y_train)
			self.tests = [x_test, y_test]
			accuracy = self.clf.score(x_test, y_test)
			self.accu = float(accuracy)
			#print ("Accuracy: ", self.clf.score(x_test, y_test))

			# Select some future "years"
			pred_years = range(1935, 2030)

			# Prepare dataset
			x_pred = [ (i, i**2, i**4) for i in pred_years ]

			# Predict values
			self.y_pred = self.clf.predict(x_pred)

			self.x_plt = [ i for i in pred_years ]

			return True

	def accuracy(self):
		return(self.accu*100)

	def gettests(self):
		return self.tests

	def disp(self):
		return_list = []
		return_list.append(self.grp1.index.tolist())		#0 - graph1_X
		return_list.append(self.grp1.values.tolist())		#1 - graph1_Y

		return_list.append(self.x_plt)						#2 - graph2_X2
		return_list.append(self.y_pred.tolist())			#3 - graph2_Y2

		return return_list

	def pred(self, x_userinputY):
		Y = int(x_userinputY)
		x_userinput = [[Y,  Y**2, Y**4]]
		result = self.clf.predict(x_userinput)
		return result