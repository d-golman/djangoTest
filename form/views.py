#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render
import requests
import sys
from subprocess import run, PIPE
from django.utils.encoding import python_2_unicode_compatible
from .forms import SnippetForm
from django.http import HttpResponse
import pymongo
import collections
import sys
import msg

def home(request):
        form = SnippetForm()
        return render(request, 'form/index.html', {'form':form})

def external(request):
        if request.method == 'POST':
                form = SnippetForm(request.POST)
                if form.is_valid():
                        inp  = form.cleaned_data['Search']
        
        result = Output(inp.lower().capitalize())

        return render(request,'form/index.html',{'form':form,
                'Occ':result['occupation'],
                'Amount':result['resumes amount'],
                'AvgSal':str(result['avg salary']) + " рублей",
                'HighestSal':str(result['high salary']) + " рублей",
                'LowestSal':str(result['low salary']) + " рублей",
                'AvgAge':result['avg age'],
                'OldAge':result['old age'],
                'YoungAge':result['young age'],
                'AvgExp':result['avg exp'],
                'lastJobs':str(result['last jobs']).replace('[','').replace(']','')
                })

def MongoConnect():
    url = 'mongodb+srv://cluster0-od56m.mongodb.net/test'
    dbs = pymongo.MongoClient(url,username='user1',password='database')
    mongo = dbs
    hh_ru = mongo.hh_ru
    collection = hh_ru.resumes
    return collection

def FindResumes(occupation):
    collection = MongoConnect()
    resumes = []
    for resume in collection.find({"occupation" : occupation}):
        resumes.append(resume)
    return resumes

def AvgSal(resumes):
    total = 0
    for i in resumes:
        total+=i['salary']
    avg = int(total/len(resumes))
    return avg

def Amount(resumes):
    amount = len(resumes)
    return(amount)

def HighestSal(resumes):
    max = 0
    for i in resumes:
        if i['salary'] > max: max = i['salary']
    return int(max)

def LowestSal(resumes):
    min = 100000
    for i in resumes:
        if i['salary'] < min: min = i['salary']
    return int(min) 

def AvgAge(resumes):    
    total = 0
    for i in resumes:
        if i['age'] != None:
            total+=i['age']
    avg = int(total/len(resumes))
    return avg

def OldAge(resumes):
    max = 0
    for i in resumes:
        if None != i['age'] > max: max = i['age']
    return int(max)

def YoungAge(resumes):
    min = 100
    for i in resumes:
        if None != i['age'] < min: min = i['age']
    return int(min)

def AvgExp(resumes):
    total = 0
    for i in resumes:
        total+=i['exp']
    avg = int(total/len(resumes))
    return avg

def lastJobs(resumes):
    jobs = []
    for i in resumes:
        if i['lastJob'] != None: jobs.append(i['lastJob'])
    counter = collections.Counter(jobs)
    mostPop = (counter.most_common(5))
    return mostPop

def Output(occupation):
    resumes = FindResumes(occupation)
    result = []
    if resumes != []:
        result = {
        'occupation':occupation,
        'resumes amount':Amount(resumes),
        'avg salary':AvgSal(resumes),
        'high salary':HighestSal(resumes),
        'low salary':LowestSal(resumes),
        'avg age':AvgAge(resumes),
        'old age':OldAge(resumes),
        'young age':YoungAge(resumes),
        'avg exp':AvgExp(resumes),
        'last jobs':lastJobs(resumes)
        }
    else:
        result = {'occupation': '',
                        'resumes amount': 0,
                        'avg salary': 0,
                        'high salary': 0,
                        'low salary': 0,
                        'avg age': 0,
                        'old age': 0,
                        'young age': 0,
                        'avg exp': 0,
                        'last jobs': []}                        
    return result
