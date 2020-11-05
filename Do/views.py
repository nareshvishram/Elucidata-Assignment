from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import pandas as pd
from django.conf import settings


def Home(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]
        file_field = File_Filed()
        file_field.file = excel_file
        file_field.save()
        return render(request, "Operation_Menu.html")

    return render(request, "index.html")


def Operation_Menu(request):
    return render(request, "Operation_Menu.html")

####################APIT ONE##########
def Task1(request, oper_name):
    data = File_Filed.objects.last()
    df = pd.read_excel(data.file)
    df = df.fillna(0)
    count = 0
    if oper_name in "PC":
        ## child Data set 1 which ends with 'PC'
        df = df[df['Accepted Compound ID'].str.endswith('PC') == True]
        df.to_excel(r'' + settings.MEDIA_ROOT + '\File task11.xlsx', index=False)
        count = 1
    elif oper_name in "LPC":
        ## child Data set 1 which ends with 'LPC'
        df = df[df['Accepted Compound ID'].str.endswith('LPC') == True]
        df.to_excel(r'' + settings.MEDIA_ROOT + '\File task12.xlsx', index=False)
        count = 2
    else:
        ## child Data set 1 which ends with 'plasmalogen'
        df = df[df['Accepted Compound ID'].str.endswith('plasmalogen') == True]
        df.to_excel(r'' + settings.MEDIA_ROOT + '\File task13.xlsx', index=False)
        count = 3
    dict = {"flag": str(count)}
    return render(request, "Task1.html", dict)

################### API 2 ###############

def Task2(request):
    data1 = File_Filed.objects.last()
    df = pd.read_excel(data1.file)
    df['Retention Time Roundoff (in mins)'] = round(df['Retention time (min)'])
    x = df
    di = x.to_dict(orient='records')
    data = list()
    for i in di:
        data.append(i)
    dict = {"data": data, "file": data1}

    df.to_excel(r'' + settings.MEDIA_ROOT + '\File task2.xlsx', index=False)

    return render(request, "Task2.html", dict)

######################## API 3 ####################
def Task3(request):
    data = File_Filed.objects.last()
    df = pd.read_excel(data.file)
    df = df.fillna(0)
    df['Retention Time Roundoff (in mins)'] = round(df['Retention time (min)'])
    dff = df.groupby('Retention Time Roundoff (in mins)').mean().reset_index()
    dff.drop(['m/z', 'Retention time (min)'], axis=1)
    di = df.to_dict(orient='records')
    data = list()
    for i in di:
        data.append(i)
    dict = {"data": data}
    df.to_excel(r'' + settings.MEDIA_ROOT + '\File task3.xlsx', index=False)
    return render(request, "Task3.html", dict)
