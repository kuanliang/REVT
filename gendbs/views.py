from gensite.gendbs.forms import ExpForm
from django import forms
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse
from gensite.gendbs.models import *

def exp_form(typedb):
	class ExpForm(forms.ModelForm):
		refdb=forms.ModelChoiceField(label="RefDB", queryset=RefDB.objects.filter(typedb=typedb))
		primer=forms.ModelChoiceField(label="Primer", queryset=Primer.objects.filter(typedb=typedb))
		vregion=forms.ModelChoiceField(label="Vregion", queryset=Vregion.objects.filter(typedb=typedb))
		class Meta:
			model = Experiment

	return ExpForm()

def exp_post(request, offset=1):
	try:
		offset=int(offset)
	except ValueErr:
		offset = 1
	if request.method == 'POST':
		form = ExpForm(request.POST)	#form = exp_form(request.POST, typedb=typedb)
		if form.is_valid():
			form.save()
			response='{"status": "success"}'
		else:
			item = form.errors.popitem()
			response="{\"status\": \"error\", \"item\": \"%s\"}" % item[0]
		
		return HttpResponse(response)
			
	else:
		form = exp_form(typedb=offset)
		user=request.user
		return render_to_response('experiment.html', {'form': form, 'user': user, 'index': 4, 'typedb': offset})

def exp_list(request):
	data1=Experiment.objects.filter(users=request.user, typedb=1)
	data2=Experiment.objects.filter(users=request.user, typedb=2)
	

	range1=""
	for item in data1:
		range1 += "\t{name: \"%s\",\n" % item.name
		range1 += "\tdata: [[ %d, 0.98],[ %d, 0.98]]},\n" % (item.start, item.end)

	result1=""
	for item in data1:
		if item.is_execute:
			result1 += "\t{name: \"%s\",\n" % item.name
			result1 += "\tdata: ["
			for ret in item.result_set.all():
				if ret.tax_id.id==1:
					result1 += "%0.10f" % ret.accuracy
				else:
					result1 += ",%0.10f" % ret.accuracy
			result1 += "]},\n"
	
	naive1=""
	for item in data1:
		if item.classifier.id == 3: #Naive ID
			naive1 += "\t{name: \"%s\", \n" % item.name
			naive1 += "\tdata: ["
			for ret in item.result_set.all():
				naive1 += "[%0.10f, %0.10f]," % (ret.accuracy, ret.bootstrap)
			naive1 += "]},\n"

	range2=""
	for item in data2:
		range2 += "\t{name: \"%s\",\n" % item.name
		range2 += "\tdata: [[ %d, 0.98],[ %d, 0.98]]},\n" % (item.start, item.end)

	result2=""
	for item in data2:
		if item.is_execute:
			result2 += "\t{name: \"%s\",\n" % item.name
			result2 += "\tdata: ["
			for ret in item.result_set.all():			
				if ret.tax_id.id==1:
					result2 += "%0.10f" % ret.accuracy
				else:
					result2 += ",%0.10f" % ret.accuracy

			result2 += "]},\n"

	naive2=""
	for item in data2:
		if item.classifier.id == 3: #Naive ID
			naive2 += "\t{name: \"%s\", \n" % item.name
			naive2 += "\tdata: ["
			for ret in item.result_set.all():
				naive2 += "[%0.10f, %0.10f]," % (ret.accuracy, ret.bootstrap)
			naive2 += "]},\n"



	table = ""
	for item in data1:
		table += "<tr>\n"
		table += "<td>%s</td>\n" % item.name
		table += "<td>%s</td>\n" % item.refdb
		table += "<td>%s</td>\n" % item.extraction
		table += "<td>%d</td>\n" % item.start
		table += "<td>%d</td>\n" % item.end
		table += "<td>%s</td>\n" % item.classifier
		table += "<td>%s</td>\n" % item.create_date
		if item.is_execute:
			for ret in item.result_set.all():
				table += "<td title=\"%0.10f\">%0.2f</td>\n" % (ret.accuracy, ret.accuracy * 100)
		else:
			table += '<td colspan="6" style="text-align: center;">No Execute!</td>\n'
			
		table += "</tr>\n"
	becteria=table

	table = ""
	for item in data2:
		table += "<tr>"
	
		table += "<td>%s</td>\n" % item.name
		table += "<td>%s</td>" % item.refdb
		table += "<td>%s</td>" % item.extraction
		table += "<td>%d</td>" % item.start
		table += "<td>%d</td>" % item.end
		table += "<td>%s</td>\n" % item.classifier
		table += "<td>%s</td>" % item.create_date
		if item.is_execute:
			for ret in item.result_set.all():
				table += "<td title=\"%0.10f\">%0.2f</td>\n" % (ret.accuracy, ret.accuracy * 100)
		else:
			table += '<td colspan="6" style="text-align: center;">No Execute!</td>'

		table += "</tr>\n"
	fungi=table

	return render_to_response('exp_list.html', {'becteria': becteria ,'fungi': fungi, 'result1': result1, 'result2': result2, 'range1': range1, 'range2': range2, 'naive1': naive1, 'naive2': naive2})

def history(request):
	data1=Experiment.objects.filter(typedb=1)
	data2=Experiment.objects.filter(typedb=2)

	table1 = ""
	for item in data1:
		table1 += "<tr>"
		table1 += "<td>%s</td>" % item.users
		table1 += "<td>%s</td>" % item.name
		table1 += "<td>%s</td>" % item.refdb
		table1 += "<td>%s</td>" % item.extraction
		table1 += "<td>%d</td>" % item.start
		table1 += "<td>%d</td>" % item.end
		table1 += "<td>%s</td>" % item.create_date
		if item.is_execute:
			if item.result_set.all():
				for ret in item.result_set.all():
					table1 += "<td title=\"%0.10f\">%0.2f</td>" % (ret.accuracy, ret.accuracy*100)
			else:
				table1 += '<td colspan="6" style="text-align: center;">Unknown</td>'

		else:
			table1 += '<td colspan="6" style="text-align: center;">No Execute</td>'
			
		table1 += "</tr>\n"

	table2 = ""
	for item in data2:
		table2 += "<tr>"
		table2 += "<td>%s</td>" % item.users
		table2 += "<td>%s</td>" % item.name
		table2 += "<td>%s</td>" % item.refdb
		table2 += "<td>%s</td>" % item.extraction
		table2 += "<td>%d</td>" % item.start
		table2 += "<td>%d</td>" % item.end
		table2 += "<td>%s</td>" % item.create_date
		if item.is_execute:
			if item.result_set.all():
				for ret in item.result_set.all():
					table2 += "<td title=\"%0.10f\">%0.2f</td>" % (ret.accuracy, ret.accuracy*100)
			else:
				table2 += '<td colspan="6" style="text-align: center;">Unknown</td>'
		else:
			table2 += '<td colspan="6" style="text-align: center;">No Execute</td>'

		table2 += "</tr>\n"

	return render_to_response('history.html', {'table1': table1 ,'table2': table2})


def data_json(request, db=1):
	try:
		db=int(db)
	except ValueErr:
		db=1
	hyper=HyperVariable.objects.filter(typedb=db)
	output = '{"Accuracy": {\n\t"label": "Accuracy",\n\t"data":[\n'
	first=True
	for row in hyper:
		if first:
			output +='[%d, %0.10f]\n' % (row.value, row.accuracy)
			first=False
		else:
			output +=',[%d, %0.10f]\n' % (row.value, row.accuracy)
	output+=']},\n'

	output += '"Entropy": {\n\t"label": "Entropy",\n\t"data":[\n'
	first=True
	for row in hyper:
		if first:
			output +='[%d, %0.10f]\n' % (row.value, row.entropy)
			first=False
		else:
			output +=',[%d, %0.10f]\n' % (row.value, row.entropy)
	output+=']},\n'
	primer=Primer.objects.filter(typedb=db)
	output += '"Primer": {\n\t"label": "Primer",\n\t"data":[\n'
	first=True
	for row in primer:
		if first:
			output +='[%d, %0.10f]\n' % (row.position_start, row.position_top)
			first=False
		else:
			output +=',[%d, %0.10f]\n' % (row.position_start, row.position_top)

		output +=',[%d, %0.10f]\n' % (row.position_end, row.position_top)
		output +=',null\n'
	output+=']},\n'

	output += '"Primer_Name": {\n\t"data":[\n'
	first=True
	for row in primer:
		if first:
			output +='["%s", %d, %d, %0.10f]\n' % (row.name, row.position_start, row.position_end, row.position_top)
			first=False
		else:
			output +=',["%s", %d, %d, %0.10f]\n' % (row.name, row.position_start, row.position_end, row.position_top)
	output+=']},\n'

	vregion=Vregion.objects.filter(typedb=db)
	output += '"Vregion": {\n\t"label": "Vregion",\n\t"data":[\n'
	first=True
	for row in vregion:
		if first:
			output +='[%d, %0.10f]\n' % (row.position_start, row.position_top)
			first=False
		else:
			output +=',[%d, %0.10f]\n' % (row.position_start, row.position_top)

		output +=',[%d, %0.10f]\n' % (row.position_end, row.position_top)
		output +=',null\n'
	output+=']},'
	output += '"Vregion_Name": {\n\t"data":[\n'
	first=True
	for row in vregion:
		if first:
			output +='["%s", %d, %0.10f]\n' % (row.name, row.position_start, row.position_top)
			first=False
		else:
			output +=',["%s", %d, %0.10f]\n' % (row.name, row.position_start, row.position_top)
	output+=']}}\n'

	return HttpResponse(output)

def data_json2(request, db=1):
	try:
		db=int(db)
	except ValueErr:
		db=1
	output = '{\n'
	
	#HyperVariable Output Start
	hyper=HyperVariable.objects.filter(typedb=db)
	output += '\t"Accuracy": {\n'
	output += '\t\t"name": "Accuracy",\n'
	output += '\t\t"data":[\n'
	first=True
	for row in hyper:
		if first:
			output +='\t\t\t[%d, %0.10f]\n' % (row.value, row.accuracy)
			first=False
		else:
			output +='\t\t\t,[%d, %0.10f]\n' % (row.value, row.accuracy)
	output+='\t\t]\n\t},\n'

	output += '\t"Entropy": {\n'
	output += '\t\t"name": "Entropy",\n'
	output += '\t\t"data":[\n'
	first=True
	for row in hyper:
		if first:
			output += '\t\t\t[%d, %0.10f]\n' % (row.value, row.entropy)
			first=False
		else:
			output += '\t\t\t,[%d, %0.10f]\n' % (row.value, row.entropy)
	output+='\t\t]\n\t},\n'
	
	#HyperVariable Output End

	#Primer Output Start
	primer=Primer.objects.filter(typedb=db)

	output += '\t"Primer_Name": {\n'
	output += '\t\t"data":[\n'
	first=True
	for row in primer:
		if first:
			output +='\t\t\t["%s", %d, %d, %0.2f]\n' % (row.name, row.position_start, row.position_end, row.position_top)
			first=False
		else:
			output +='\t\t\t,["%s", %d, %d, %0.2f]\n' % (row.name, row.position_start, row.position_end, row.position_top)
	output+='\t\t]\n\t},\n'
	#Primer Output End


	vregion=Vregion.objects.filter(typedb=db)

	output += '\t"Vregion_Name": {\n'
	output += '\t\t"data":[\n'
	first=True
	for row in vregion:
		if first:
			output +='\t\t\t["%s", %d, %d, %0.2f]\n' % (row.name, row.position_start, row.position_end, row.position_top)
			first=False
		else:
			output +='\t\t\t,["%s", %d, %d, %0.2f]\n' % (row.name, row.position_start, row.position_end, row.position_top)
	output+='\t\t]\n\t}\n'

	output += '}'

	return HttpResponse(output)


def hyper_json(requset, db=1):
	try:
		db=int(db)
	except ValueErr:
		db = 1
	p = HyperVariable.objects.filter(typedb=db)
	response = "{\"Accuracy\": {\n"
	response += "\t\"label\": \"Accuracy\",\n\t\"data\":[\n"
	t = True
	for d in p:
		if t:
			response += "[%d, %0.10f]\n" % (d.value, d.accuracy)
			t = False
		else:
			response += " ,[%d, %0.10f]\n" % (d.value, d.accuracy)
	response += "]},\n"
	response += "\"Entropy\": {\n"
	response += "\t\"label\": \"Entropy\",\n\t\"data\":[\n"
	t = True
	for d in p:
		if t:
			response += "[%d, %0.10f]\n" % (d.value, d.entropy)
			t = False
		else:
			response += " ,[%d, %0.10f]\n" % (d.value, d.entropy)
	response += "]}}"

	return HttpResponse(response)

def Vregion_json(request, db=1):
	try:
		db=int(db)
	except ValueErr:
		db = 1

	p = Vregion.objects.filter(typedb=db)
	response = "{\"data\": [\n"
	t= True
	for d in p:
		if t:
			response += "{\"name\": \"%s\", \"value\" :[%d, %d], \"top\": %f}\n" % (d.name, d.position_start, d.position_end, d.position_top)
			t = False
		else:
			response += ",{\"name\": \"%s\", \"value\" :[%d, %d], \"top\": %f}\n" % (d.name, d.position_start, d.position_end, d.position_top)
	response += "]}"
	return HttpResponse(response)
	
def Primer_json(request, db=1):
	try:
		db=int(db)
	except ValueErr:
		db = 1

	p = Primer.objects.filter(typedb=db)
	response = "{\"data\": [\n"
	t= True
	for d in p:
		if t:
			response += "{\"name\": \"%s\", \"value\" :[%d, %d], \"top\": %f}\n" % (d.name, d.position_start, d.position_end, d.position_top)
			t = False
		else:
			response += ",{\"name\": \"%s\", \"value\" :[%d, %d], \"top\": %f}\n" % (d.name, d.position_start, d.position_end, d.position_top)
	response += "]}"
	return HttpResponse(response)

def plot(request, db=1):
	try:
		db=int(db)
	except ValueErr:
		db = 1
	
	return render_to_response('plot.html', {'data1': data1, 'data2': data2})
