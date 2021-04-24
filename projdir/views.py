from django.shortcuts import render, redirect
import projdir.co2 as proj_co2
import projdir.temp as proj_temp
import projdir.glacier as proj_glacier
import json
import populate
from .models import CO2, Temperature, Glacier

# Create your views here.
def homepage(request):
	return render(request,'homepage.html')

def mainpage(request):
	return render(request,'mainpage.html')

def dashboard(request):
	co2_obj = proj_co2.CO2_Logic()
	if not co2_obj.mainfunc():
		return render(request,'empty.html',{'append':''})
	temp_obj = proj_temp.Temp_Logic()
	if not temp_obj.mainfunc():
		return render(request,'empty.html',{'append':''})
	glacier_obj = proj_glacier.Glacier_Logic()
	if not glacier_obj.mainfunc():
		return render(request,'empty.html',{'append':''})
	co2_accuracy = co2_obj.accuracy()
	temp_accuracy = temp_obj.accuracy()
	glacier_accuracy = glacier_obj.accuracy()
	co2_value_month = co2_obj.dashboard()[0]
	co2_value_year = co2_obj.dashboard()[1]
	temp_value = temp_obj.dashboard()
	return render(request,'dashboard.html',{'co2_accuracy':co2_accuracy, 'temp_accuracy':temp_accuracy, 'glacier_accuracy':glacier_accuracy, 'co2_value_year':co2_value_year, 'co2_value_month': co2_value_month, 'temp_value':temp_value})
#################################### CO2 ##################################
def co2_add_dataset(request):
	return render(request,'co2_add_dataset.html')

def co2_view(request):
	#logic
	co2_obj = proj_co2.CO2_Logic()
	if not co2_obj.mainfunc():
		append = 'mainpage/#co2'
		return render(request,'empty.html',{'append':append})
	else:
		data = co2_obj.disp()
		graph1_X = data[0]
		graph1_Y = data[1]
		graph2_X1 = data[2]
		graph2_Y1 = data[3]
		graph2_X2 = data[4]
		graph2_Y2 = data[5]
		return render(request,'co2_view.html', {'graph1_X':graph1_X, 'graph1_Y': graph1_Y, 'graph2_X1': graph2_X1, 'graph2_Y1': graph2_Y1, 'graph2_X2': graph2_X2, 'graph2_Y2': graph2_Y2})

def co2_truncate(request):
	CO2.objects.all().delete()
	return redirect('mainpage/#co2')

def co2_predict(request):
	#logic
	if request.method=='GET':
		return render(request, 'co2_predict.html', {'result': ''})
	# if this is a POST request we need to process the form data
	else:
		# create a form instance and populate it with data from the request:
		year=request.POST.get("year")
		month=request.POST.get("month")
		co2_obj = proj_co2.CO2_Logic()
		if not co2_obj.mainfunc():
			append = 'mainpage/#co2'
			return render(request,'empty.html',{'append':append})
		else:
			res = co2_obj.pred(year, month)
			result = str(res[0])
			return render(request, 'co2_predict.html', {'result': 'Predicted CO<sub>2</sub> Concentration is <b>'+result+' ppm </b>'})

	# if a GET (or any other method) we'll create a blank form
	return render(request, 'co2_predict.html', {'result': ''})

def co2_table(request):
	co2_obj = proj_co2.CO2_Logic()
	if not co2_obj.mainfunc():
		append = 'mainpage/#co2'
		return render(request,'empty.html',{'append':append})
	else:
		tests = co2_obj.gettests()
		months = []
		years = []
		orig_ppm = []
		pred_ppm = []
		for i, j in zip(tests[0], tests[1]):
			months.append(i[0])
			years.append(i[1])
			orig_ppm.append(j)
		for i, j in zip(years, months):
			res = co2_obj.pred(i, j)
			pred_ppm.append(float(res[0]))
		return render(request,'co2_table.html', {'years':years, 'months':months, 'orig_ppm':orig_ppm, 'pred_ppm':pred_ppm})

def co2_loading(request):
	result = populate.start_co2()
	append = 'co2'
	if result == '':
		return render(request, 'success.html',{'append':append})
	else:
		return render(request, 'failure.html', {'result': result})

#################################### TEMP ##################################

def temp_add_dataset(request):
	return render(request,'temp_add_dataset.html')

def temp_view(request):
	temp_obj = proj_temp.Temp_Logic()
	if not temp_obj.mainfunc():
		append = 'mainpage/#temp'
		return render(request,'empty.html',{'append':append})
	else:
		data = temp_obj.disp()
		graph1_X = data[0]
		graph1_Y = data[1]
		graph2_X1 = data[2]
		graph2_Y1 = data[3]
		graph2_X2 = data[4]
		graph2_Y2 = data[5]
		return render(request,'temp_view.html', {'graph1_X':graph1_X, 'graph1_Y': graph1_Y, 'graph2_X1': graph2_X1, 'graph2_Y1': graph2_Y1, 'graph2_X2': graph2_X2, 'graph2_Y2': graph2_Y2})

def temp_truncate(request):
	Temperature.objects.all().delete()
	return redirect('mainpage/#temp')

def temp_predict(request):
	#logic
	if request.method=='GET':
		return render(request, 'temp_predict.html', {'result': ''})
	# if this is a POST request we need to process the form data
	else:
		# create a form instance and populate it with data from the request:
		year=request.POST.get("year")
		month=request.POST.get("month")
		temp_obj = proj_temp.Temp_Logic()
		if not temp_obj.mainfunc():
			append = 'mainpage/#temp'
			return render(request,'empty.html',{'append':append})
		else:
			res = temp_obj.pred(year, month)
			result = str(res[0])
			return render(request, 'temp_predict.html', {'result': 'Predicted Global Temperature is <b>'+result+' °C </b>'})
	# if a GET (or any other method) we'll create a blank form
	return render(request, 'temp_predict.html', {'result': ''})

def temp_table(request):
	temp_obj = proj_temp.Temp_Logic()
	if not temp_obj.mainfunc():
		append = 'mainpage/#temp'
		return render(request,'empty.html',{'append':append})
	else:
		tests = temp_obj.gettests()
		months = []
		years = []
		orig_temp = []
		pred_temp = []
		for i, j in zip(tests[0], tests[1]):
			months.append(i[0])
			years.append(i[1])
			orig_temp.append(j)
		for i, j in zip(years, months):
			res = temp_obj.pred(i, j)
			pred_temp.append(float(res[0]))
		return render(request,'temp_table.html', {'years':years, 'months':months, 'orig_temp':orig_temp, 'pred_temp':pred_temp})

def temp_loading(request):
	result = populate.start_temp()
	append = 'temp'
	if result == '':
		return render(request, 'success.html',{'append':append})
	else:
		return render(request, 'failure.html', {'result': result})

#################################### GLACIERS ##################################

def glacier_add_dataset(request):
	return render(request,'glacier_add_dataset.html')

def glacier_view(request):
	#logic
	glacier_obj = proj_glacier.Glacier_Logic()
	if not glacier_obj.mainfunc():
		append = 'mainpage/#ice'
		return render(request,'empty.html',{'append':append})
	else:
		data = glacier_obj.disp()
		graph1_X = data[0]
		graph1_Y = data[1]
		graph2_X = data[2]
		graph2_Y = data[3]

		return render(request,'glacier_view.html', {'graph1_X':graph1_X, 'graph1_Y': graph1_Y, 'graph2_X': graph2_X, 'graph2_Y': graph2_Y})
	
def glacier_truncate(request):
	Glacier.objects.all().delete()
	return redirect('mainpage/#ice')


def glacier_predict(request):
	#logic
	if request.method=='GET':
		return render(request, 'glacier_predict.html', {'result': ''})	
	# if this is a POST request we need to process the form data
	else:
		# create a form instance and populate it with data from the request:
		year=request.POST.get("year")
		glacier_obj = proj_glacier.Glacier_Logic()
		if not glacier_obj.mainfunc():
			append = 'mainpage/#ice'
			return render(request,'empty.html',{'append':append})
		else:
			res = glacier_obj.pred(year)
			result = str(res[0])
			return render(request, 'glacier_predict.html', {'result': 'Predicted Mean Cumulative Mass balance is <b>'+result+' </b>'})

	# if a GET (or any other method) we'll create a blank form
	return render(request, 'glacier_predict.html', {'result': ''})

def glacier_table(request):
	glacier_obj = proj_glacier.Glacier_Logic()
	if not glacier_obj.mainfunc():
		append = 'mainpage/#ice'
		return render(request,'empty.html',{'append':append})
	else:
		tests = glacier_obj.gettests()
		years = []
		orig_bal = []
		pred_bal = []
		for i, j in zip(tests[0], tests[1]):
			years.append(i[0])
			orig_bal.append(j)
		for i in years:
			res = glacier_obj.pred(i)
			pred_bal.append(float(res[0]))
		return render(request,'glacier_table.html', {'years':years, 'orig_bal':orig_bal, 'pred_bal':pred_bal})

def glacier_loading(request):
	result = populate.start_glacier()
	append = 'mainpage/#ice'
	if result == '':
		return render(request, 'success.html',{'append':append})
	else:
		return render(request, 'failure.html', {'result': result})
