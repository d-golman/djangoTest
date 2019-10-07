import pymongo
import collections
import sys
import msg

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

def Output(occupation, index):
    resumes = FindResumes(occupation)
    result = []
    result.append({
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
    })
    return result[0][index]

out = Output(sys.argv[1].decode('cp1251'),sys.argv[2])
print(out)