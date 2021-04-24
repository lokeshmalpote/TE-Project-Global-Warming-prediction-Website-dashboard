import pandas as pd
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import json
from .models import Temperature

class Temp_Logic:
	def __init__(self):
		self.tempdb = Temperature.objects.all()

	def mainfunc(self):
		if not self.tempdb.exists():
			return False
		else:
			tempdata = pd.DataFrame.from_records([s.to_dict() for s in self.tempdb])
			self.grp1 = tempdata.groupby(["Year"]).mean()["Temp"]
			self.grp2 = tempdata.groupby(["Year", "Month"]).mean()["Temp"]
			self.x = [dt.datetime(year=i[0], month=i[1], day=1) for i in self.grp2.index]
			self.means = self.grp2.values

			#
			means_annual = self.grp1.values
			x_learn_annual = [ (i, i**2, i**4, i**6) for i in self.grp1.index ]
			y_learn_annual = [ i for i in means_annual ]
			x_train_annual, x_test_annual, y_train_annual, y_test_annual = train_test_split(x_learn_annual, y_learn_annual, test_size=0.15, random_state=56)
			clf_annual = LinearRegression().fit(x_train_annual, y_train_annual)
			
			#

			x_learn = [ (i.month, i.year, i.month**2, i.year**2, i.month**3, i.year**3, i.month**4, i.year**4) for i in self.x]
			y_learn = [ i for i in self.means ]

			x_train, x_test, y_train, y_test = train_test_split(x_learn, y_learn, test_size=0.2, random_state=16)
			self.clf = LinearRegression().fit(x_train, y_train)
			self.tests = [x_test, y_test]
			accuracy = self.clf.score(x_test, y_test)
			self.accu = float(accuracy)
			#print ("Accuracy: ", self.clf.score(x_test, y_test))

			# Select some future "years"
			pred_years = range(1850, 2050)
			pred_months = range(1, 13)

			# Prepare dataset
			x_pred = []
			for y in pred_years:
			    for m in pred_months:
			        x_pred.append([m, y,m**2, y**2,m**3, y**3,m**4, y**4])
			
			#
			self.x_pred_annual = [ (i, i**2,i**4, i**6) for i in pred_years ]

			# Predict values
			self.y_pred_annual = clf_annual.predict(self.x_pred_annual)

			#

			# Predict values
			y_pred = self.clf.predict(x_pred)
			self.y_plt = y_pred.tolist()
			# plot the predicted values
			self.x_plt = [dt.datetime(i[1], i[0], 15) for i in x_pred]

			self.dash_x = []
			for i, j in zip(x_pred, y_pred):
				if (i[0]==1 and j>4.5):
					self.dash_x.append(i[0])
					self.dash_x.append(i[1])
					break
			return True

	def dashboard(self):
		for i,j in zip(self.x_pred_annual, self.y_pred_annual):
			if (j-self.y_pred_annual[0])>1.6:
				return i[0]

	def accuracy(self):
		return(self.accu*100)

	def gettests(self):
		return self.tests
	
	def myconverter(o):
		if isinstance(o, datetime.datetime):
			return o.__str__()

	def disp(self):
		return_list = []
		return_list.append(self.grp1.index.tolist())		#0 - graph1_X
		return_list.append(self.grp1.values.tolist())		#1 - graph1_Y

		x1 = []
		for i in self.x:
			x1.append(i.isoformat())

		x1_plt=json.dumps(x1, default=self.myconverter)
		# Mean values.
		y1_plt = self.means.tolist()

		return_list.append(x1_plt)							#2 - graph2_X1
		return_list.append(y1_plt)							#3 - graph2_Y1

		x_ = []
		for i in self.x_plt:
			x_.append(i.isoformat())

		x_plot=json.dumps(x_, default=self.myconverter)
		return_list.append(x_plot)							#4 - graph2_X2
		return_list.append(self.y_plt)						#5 - graph2_Y2

		return return_list

	def pred(self, Y, M):
		x_userinputY = int(Y)
		x_userinputM = int(M)
		x_userinput = [[x_userinputM, x_userinputY, x_userinputM**2, x_userinputY**2, x_userinputM**3, x_userinputY**3, x_userinputM**4, x_userinputY**4]]
		result = self.clf.predict(x_userinput)
		return result