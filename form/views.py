# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import requests
import sys
from subprocess import run, PIPE
from django.utils.encoding import python_2_unicode_compatible
from .forms import SearchForm
from django.http import HttpResponse

inp = ''

def home(request):
	form = SearchForm()
	return render(request, 'form/home.html', {'form':form})

def external(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			inp  = form.cleaned_data['Search']
	
	Occ = run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'occupation'],shell=False,stdout=PIPE)
	print(inp)
	print(inp.encode("UTF-8"))
	Amount = run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'resumes amount'],shell=False,stdout=PIPE)
	AvgSal = run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'avg salary'],shell=False,stdout=PIPE)
	HighestSal= run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'high salary'],shell=False,stdout=PIPE)
	LowestSal= run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'low salary'],shell=False,stdout=PIPE)
	AvgAge= run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'avg age'],shell=False,stdout=PIPE)
	OldAge= run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'old age'],shell=False,stdout=PIPE)
	YoungAge= run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'young age'],shell=False,stdout=PIPE)
	AvgExp= run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'avg exp'],shell=False,stdout=PIPE)
	lastJobs= run([sys.executable,'form/mongo.py',inp.encode("UTF-8"),'last jobs'],shell=False,stdout=PIPE)

	return render(request,'form/home.html',{
		'Occ':Occ.stdout.decode('cp1251'),
		'Amount':Amount.stdout.decode('cp1251'),
		'AvgSal':AvgSal.stdout.decode('cp1251'),
		'HighestSal':HighestSal.stdout.decode('cp1251'),
		'LowestSal':LowestSal.stdout.decode('cp1251'),
		'AvgAge':AvgAge.stdout.decode('cp1251'),
		'OldAge':OldAge.stdout.decode('cp1251'),
		'YoungAge':YoungAge.stdout.decode('cp1251'),
		'AvgExp':AvgExp.stdout.decode('cp1251'),
		'lastJobs':lastJobs.stdout.decode('cp1251').replace('[','').replace(']','')
		})