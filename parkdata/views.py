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




# predict possibility
@csrf_exempt
def predict(request):
    if request.method == 'GET':
        
        streetMarker = request.GET.get('streetMarker')
        
        blockidObject = Blockquery.objects.filter(streemarker = streetMarker) # get the object with the street marker in the url
        if blockidObject.exists():
            print("right street marker!")
            blockidObject_values = blockidObject.values_list
            blockidObject_blockid = blockidObject.values('blockid')[0]['blockid']
            predictObject = Weekly2.objects.filter(blockid=blockidObject_blockid)
            predictedValues = predictObject.values('predicted','id','weekday') # get the attributes predicted possibility, id, and weekday of the object
            
            # make a list of all the parking possibilities in the block
            count = 0
            list=[]
            for eachobject in predictedValues:
               
                count = count+1
                list.append(eachobject['predicted'])


            mon={'mon':list[24:48]}
            tue={'tue':list[48:72]}
            wed={'wed':list[72:96]}
            thu={'thu':list[96:120]}
            fri={'fri':list[120:144]}
            sat={'sat':list[144:168]}
            sun={'sun':list[0:24]}
            dict={'prob':[mon,tue,wed,thu,fri,sat,sun]}
            dict = json.dumps(dict) # turn list to the form of JSON
            
        else:
            return HttpResponse("wrong street marker")
 


    return HttpResponse(dict,content_type = "application/json")


# visualise the historical data
@csrf_exempt
def lastWeekdata(request):
    if request.method == 'GET':
   
        bayid = request.GET.get('bayid')
        # get the  occupied rates of objects from monday to sunday
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
        problistdictjson = json.dumps(problistdict) # turn list to the form of JSON

    return HttpResponse(problistdictjson,content_type = "application/json")


# recommend parking lots base on users' locations
@csrf_exempt
def suggestbays(request):
    import ast
    dict = {}
    reqdict = {}
    if request.method == 'POST':
  
        # get the key values in requests
        streetmarkerliststr = request.POST.get('baylist')
        period_h = int(request.POST.get('period_h'))
        period_m = int(request.POST.get('period_m'))

        streetmarkerlist = json.loads(streetmarkerliststr)
        
        # process time, calculate the estimated time when the user arrive the destination
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

        # find corresponding blocks of the street makers inthe baylist
        listlength = len(streetmarkerlist)
        streetmarkerlistindex = -1
        list2 = []
        # make a list of parking possibilities of the street markers in the baylist
        for eachbayid in streetmarkerlist:
            blockidObject = Blockquery.objects.filter(streemarker=eachbayid)
            if blockidObject.exists():
                streetmarkerlistindex += 1
                blockidObject_values = blockidObject.values_list
                blockidObject_blockid = blockidObject.values('blockid')[0]['blockid']
                predictObject = Weekly2.objects.filter(blockid=blockidObject_blockid,weekday=currentweekday,period=newperiod_h)
                predictedValues = predictObject.values('predicted')[0]['predicted']
                print(predictedValues)
                print(type(predictedValues))
            else:
                predictedValues = 1
                print('streetmarker does not exist, no predicted data')
            list2.append(predictedValues)
            

        # sort the values(opposite to the parking possibilities), pick up top 3 with smallest values
        # the smaller the value is , the higher the parking possibility is
        tmp = {}
        for i in range(0, len(list2)):
            tmp[i] = [list2[i], streetmarkerlist[i]]
        tmp_sorted = sorted(tmp.items(), key=lambda x: x[1][0])
        lowest3 = tmp_sorted[0:3]

        
        lowest1 = tmp_sorted[0] # the list of street marker with the lowest value 
        lowest1blockidObject = Blockquery.objects.filter(streemarker=eachbayid)
        lowest1blockidObject_blockid = lowest1blockidObject.values('blockid')[0]['blockid']
        streetmarkersObject = Blockquery.objects.filter(blockid=lowest1blockidObject_blockid)
        streetmarkers = streetmarkersObject.values('streemarker')
   
        blockstreetmarkerlist = []
        for each in streetmarkers:
            eachstreetmarker = each['streemarker']
            blockstreetmarkerlist.append(eachstreetmarker)
   
        blockstreetmarkerdict ={}
        blockstreetmarkerdict['sortedstreetmarkers'] = blockstreetmarkerlist
        blockstreetmarkerjson = json.dumps(blockstreetmarkerdict)



        # return to the street markers in the block with the highest parking possibilities
        sortedStreetMarkerlist =[]
        for each in lowest3:
            streetmarker = each[1][1]
            sortedStreetMarkerlist.append(streetmarker)

        sortedStreetMarkerdict = {}
        sortedStreetMarkerdict['sortedstreetmarkers'] = sortedStreetMarkerlist
        sortedStreetMarkerdictjson = json.dumps(sortedStreetMarkerdict)
       

        return HttpResponse(blockstreetmarkerjson,content_type= "application/json")

  

