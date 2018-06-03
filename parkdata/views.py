from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView,ListView
import collections #to get nested dictionary
# api from web
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
import json
import time,datetime
from datetime import timedelta
from django.core import serializers
from .models import Parking,Blockquery,Weekly1,Weekly2,Lastmondata,Lasttuedata,Lastweddata,Lastthudata,Lastfridata,Lastsatdata,Lastsundata





@csrf_exempt
def predict(request):
    if request.method == 'GET':
        print(str(type(request)))
        streetMarker = request.GET.get('streetMarker')
        print(streetMarker)
        # print(type(streetMarker))
        blockidObject = Blockquery.objects.filter(streemarker = streetMarker)
        if blockidObject.exists():
            print("right street marker!")
            blockidObject_values = blockidObject.values_list
            # print(blockidObject_values)
            blockidObject_blockid = blockidObject.values('blockid')[0]['blockid']

            # print(blockidObject_blockid)
            # print(type(blockidObject_blockid))

            predictObject = Weekly2.objects.filter(blockid=blockidObject_blockid)
            predictedValues = predictObject.values('predicted','id','weekday')
            # print(predictedValues)
            count = 0
            list=[]
            for eachobject in predictedValues:
                # print(eachobject)
                count = count+1
                list.append(eachobject['predicted'])
            # print(count)

            # print(list)

            mon={'mon':list[24:48]}
            tue={'tue':list[48:72]}
            wed={'wed':list[72:96]}
            thu={'thu':list[96:120]}
            fri={'fri':list[120:144]}
            sat={'sat':list[144:168]}
            sun={'sun':list[0:24]}
            dict={'prob':[mon,tue,wed,thu,fri,sat,sun]}
            dict = json.dumps(dict)

            # print(dict)
        else:
            return HttpResponse("wrong street marker")
 


    return HttpResponse(dict,content_type = "application/json")

@csrf_exempt
def lastWeekdata(request):
    if request.method == 'GET':
        # print(str(type(request)))
        bayid = request.GET.get('bayid')
        monobj = Lastmondata.objects.filter(bay_id=bayid).values('occupiedrate')
        tueobj = Lasttuedata.objects.filter(bay_id=bayid).values('occupiedrate')
        wedobj = Lastweddata.objects.filter(bay_id=bayid).values('occupiedrate')
        thuobj = Lastthudata.objects.filter(bay_id=bayid).values('occupiedrate')
        friobj = Lastfridata.objects.filter(bay_id=bayid).values('occupiedrate')
        satobj = Lastsatdata.objects.filter(bay_id=bayid).values('occupiedrate')
        sunobj = Lastsundata.objects.filter(bay_id=bayid).values('occupiedrate')

        ojblist =[monobj,tueobj,wedobj,thuobj,friobj,satobj,sunobj]
        ratelist = []
        for eachobj in ojblist:
            if eachobj.exists():
                eachrate = eachobj[0]['occupiedrate']
                ratelist = ratelist + [eachrate]
            else:
                eachrate = 0
                ratelist = ratelist + [eachrate]
        # print(ratelist)
        problistdict = {'prob': ratelist}
        problistdictjson = json.dumps(problistdict)

    return HttpResponse(problistdictjson,content_type = "application/json")

@csrf_exempt
def suggestbays(request):
    import ast
    dict = {}
    reqdict = {}
    if request.method == 'POST':
        # req = json.loads(request.body)
        # streetmarkerliststr = req['baylist']
        # period_h = req['period_h']
        # period_m = req['period_h']

        streetmarkerliststr = request.POST.get('baylist')
        period_h = int(request.POST.get('period_h'))
        period_m = int(request.POST.get('period_m'))

        print(streetmarkerliststr)
        print(type(streetmarkerliststr))
        print(period_h)
        print(type(period_h))
        print(period_m)
        print(type(period_m))

        streetmarkerlist = json.loads(streetmarkerliststr)
        print(streetmarkerlist)
        print(type(streetmarkerlist))
        print(streetmarkerlist[0])


        # 处理时间 process time
        currentweekday = int(time.strftime('%w', time.localtime(time.time())))
        currenttimehour = int(time.strftime('%H', time.localtime(time.time())))
        currenttimeminute = int(time.strftime('%M', time.localtime(time.time())))
        newperiod_m = (currenttimeminute + period_m)%60
        print(newperiod_m)
        newperiod_h = currenttimehour + period_h + int((currenttimeminute + period_m)/60)
        print(newperiod_h)
        if newperiod_m >= 30: #if minutes are more than 30, we compare the predicted values in next period, else we compare the current period
            newperiod_h+=1
        if newperiod_h >23 : #if hours are more than 23, we compare the predicted values in next period next day, else we compare the current period
            currentweekday +=1
            newperiod_h = newperiod_h%24
        if currentweekday >6:
            currentweekday = currentweekday%7

        # 找相对应的block find corresponding block
        listlength = len(streetmarkerlist)
        print(listlength)

        streetmarkerlistindex = -1
        list2 = []
        for eachbayid in streetmarkerlist:
            blockidObject = Blockquery.objects.filter(streemarker=eachbayid)
            print(blockidObject)
            if blockidObject.exists():
                streetmarkerlistindex += 1
                print("streetmarkerlistindex :" + str(streetmarkerlistindex))
                # print("right street marker!")
                blockidObject_values = blockidObject.values_list
                # print(blockidObject_values)
                blockidObject_blockid = blockidObject.values('blockid')[0]['blockid']
                #
                # print(blockidObject_blockid)
                # print(type(blockidObject_blockid))

                predictObject = Weekly2.objects.filter(blockid=blockidObject_blockid,weekday=currentweekday,period=newperiod_h)
                # print(predictObject)
                predictedValues = predictObject.values('predicted')[0]['predicted']
                print(predictedValues)
                print(type(predictedValues))
            else:
                predictedValues = 1
                print('streetmarker does not exist, no predicted data')
            list2.append(predictedValues)
            print(list2)

        # sort the values, pick up top 3 with smallest values
        tmp = {}
        for i in range(0, len(list2)):
            tmp[i] = [list2[i], streetmarkerlist[i]]
        tmp_sorted = sorted(tmp.items(), key=lambda x: x[1][0])
        lowest3 = tmp_sorted[0:3]

        lowest1 = tmp_sorted[0]
        print("lowest1")
        print(lowest1)

        lowest1blockidObject = Blockquery.objects.filter(streemarker=eachbayid)
        lowest1blockidObject_blockid = lowest1blockidObject.values('blockid')[0]['blockid']
        # print(lowest1blockidObject_blockid)
        streetmarkersObject = Blockquery.objects.filter(blockid=lowest1blockidObject_blockid)
        streetmarkers = streetmarkersObject.values('streemarker')
        print(type(streetmarkers))
        print("streetmarkers")
        print(streetmarkers)

        blockstreetmarkerlist = []
        for each in streetmarkers:
            eachstreetmarker = each['streemarker']
            blockstreetmarkerlist.append(eachstreetmarker)
            print(eachstreetmarker)
        print("blockstreetmarkerlist")
        print(blockstreetmarkerlist)

        blockstreetmarkerdict ={}
        blockstreetmarkerdict['sortedstreetmarkers'] = blockstreetmarkerlist
        blockstreetmarkerjson = json.dumps(blockstreetmarkerdict)




        sortedStreetMarkerlist =[]
        for each in lowest3:
            streetmarker = each[1][1]
            sortedStreetMarkerlist.append(streetmarker)
        print(sortedStreetMarkerlist)

        sortedStreetMarkerdict = {}
        sortedStreetMarkerdict['sortedstreetmarkers'] = sortedStreetMarkerlist
        print(sortedStreetMarkerdict)
        sortedStreetMarkerdictjson = json.dumps(sortedStreetMarkerdict)
        print(sortedStreetMarkerdictjson)
        print(type(sortedStreetMarkerdictjson))

        return HttpResponse(blockstreetmarkerjson,content_type= "application/json")

  

