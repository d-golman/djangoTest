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
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import plotly.offline as opy

def home(request):
        form = SnippetForm()
        result = Output2()
        return render(request, 'form/index.html', {
            'form':form,
            'head': 'Общая информация',
            's1': "Новосибирский государственный технический университет (НГТУ) — многопрофильный университет в Новосибирске. В настоящий момент НГТУ является одним из крупнейших вузов региона — осуществляется подготовка по 95 направлениям. В составе университета 17 факультетов и институтов. Является участником программы — Опорные университеты России.",
            's3': "На данный момент на сайте hh.ru представлено " + result['amount'] + " резюме выпускников НГТУ.",
            's5': "Средняя зарплата составляет " + result['avg'] + " рублей.",
            's7': "Самые популярные профессии: " + result['MostPopOcc'],            
            's9': "Самые популярные места работы: " + result['MostPopJob'],    
            'app4':app4()         
            })

def search(request):
        if request.method == 'POST':
                form = SnippetForm(request.POST)
                if form.is_valid():
                        inp  = form.cleaned_data['Search']
        
        result = Output(inp.lower().capitalize())

        return render(request,'form/search.html',{
                'head': "Результаты поиска",
                'form':form,
                's1':"Профессия: " + result['occupation'],
                's2':"Всего резюме: " + str(result['resumes amount']),
                's3':"Средняя зарплата: " + str(result['avg salary']) + " рублей",
                's4':"Самая высокая зарплата: " + str(result['high salary']) + " рублей",
                's5':"Самая низкая зарплата: " + str(result['low salary']) + " рублей",
                's6':"Средний возраст: " + str(result['avg age']),
                's7':"Самый старший: " + str(result['old age']),
                's8':"Самый младший: " + str(result['young age']),
                's9':"Среднй опыт работы: " + str(result['avg exp']),
                's10':"Самые частые места работы: " + str(result['last jobs']).replace('[','').replace(']','').replace("'",'')
                })

def MongoConnect(coll):
    url = 'mongodb+srv://cluster0-od56m.mongodb.net/test'
    dbs = pymongo.MongoClient(url,username='user1',password='database')
    mongo = dbs
    hh_ru = mongo.hh_ru
    collection = hh_ru[coll]
    return collection

def FindResumes(occupation):
    collection = MongoConnect('resumes')
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

def Output2():
    collection = MongoConnect('resumes').find()
    resumes = []
    occs = []
    jobs = []
    total = 0
    for resume in collection:
        resumes.append(resume)
    for resume in resumes:
        if resume['occupation'] != None: occs.append(resume['occupation'])
        counter1 = collections.Counter(occs)
        mostPopOcc = (counter1.most_common(3))
        total+=resume['salary']
        avg = int(total/len(resumes))
        if resume['lastJob'] != None: jobs.append(resume['lastJob'])
        counter2 = collections.Counter(jobs)
        mostPopJob = (counter2.most_common(3))
    result = {
        'amount': str(len(resumes)),
        'MostPopOcc': str(mostPopOcc).replace('[','').replace(']','').replace("'",''),
        'avg': str(avg),
        'MostPopJob': str(mostPopJob).replace('[','').replace(']','').replace("'",'')
    }
    return result



def app1():
    app1 = DjangoDash('Gender')
    genders = ["Мужской", "Женский"]
    GenderValues = MongoConnect('genders').find()[0]
    app1.layout = html.Div([
        dcc.Graph(
            figure={
                'data': [go.Pie(labels=genders, values=[GenderValues['Мужской'], GenderValues['Женский']], 
                marker = {'colors': [ '#4CAC40', '#79C25A','#95D46C','#B1D979', '#BBCD32', '#D2D83F']})],
                    "layout": go.Layout(margin=dict(l=0,r=120,b=0,t=0),legend={"x": 1, "y": 0.5})
            }
        )
    ])
    return app1
def app2():
    app2 = DjangoDash('Age')
    ages = ["14-18", "18-30","30-40","40-50","50-60","60+"]
    AgesValues = MongoConnect('ages').find()[0]
    app2.layout = html.Div([
        dcc.Graph(
            figure={
                'data': [go.Pie(labels=ages, values=[AgesValues['14-18'],AgesValues['18-30'],AgesValues['30-40'],AgesValues['40-50'],AgesValues['50-60'],AgesValues['60+']], 
                marker = {'colors': [ '#4CAC40', '#79C25A','#95D46C','#B1D979', '#BBCD32', '#D2D83F']})],
                "layout": go.Layout(margin=dict(l=0,r=120,b=0,t=0),legend={"x": 1, "y": 0.5})
            }
        )
    ])
    return app2

def app3():
    app3 = DjangoDash('Areas')
    areasValues = MongoConnect('areas').find()[0]
    app3.layout = html.Div(children=[
        dcc.Graph(
            figure={
                'data': [{'x': list(areasValues.keys())[1:],
                'y': list(areasValues.values())[1:], 'type': 'bar',}],
                'layout': go.Layout(colorway=["#4CAC40"], hovermode="closest",margin=dict(l=50,r=60,b=120,t=30)),                            
                            
            }
        )
    ])
    return app3

def app4():
    skillsValues = MongoConnect('skills').find()[0]
    x = list(skillsValues.keys())[1:]
    y = list(skillsValues.values())[1:]
    div = opy.plot({"data":[go.Bar(x=x, y=y)], "layout": go.Layout(colorway=["#4CAC40"], hovermode="closest",margin=dict(l=40,r=0,b=200,t=30))}, xaxis = {'titlefont':{'family':'Fira Sans'}} output_type='div')
    return div