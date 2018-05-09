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
import time
from django.core import serializers
from .models import Parking,Blockquery,Weekly1,Weekly2,Lastmondata,Lasttuedata,Lastweddata,Lastthudata,Lastfridata,Lastsatdata,Lastsundata


@csrf_exempt
def run_job(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    # 判断是否为get 请求
    if request.method == 'GET':
        try:
            # 解析请求的json格式入参
            data = JSONParser().parse(request)
        except Exception as why:
            print(why.args)
        else:
            content = {'msg': 'SUCCESS'}
            print(data)
            # 返回自定义请求内容content,200状态码
            return JsonResponse(data=content, status=status.HTTP_200_OK)
    # 如果不是get 请求返回不支持的请求方法
    return HttpResponseNotAllowed(permitted_methods=['GET'])

# api end




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
        # blockidObject_blockid = blockidObject.values('blockid')
        # print(blockidObject_blockid)
        # count = 0
        # print(blockidObject_blockid[1]['blockid'])
        # block_id = blockidObject_blockid[1]['blockid']
        # predictObject = Finetreepredict.objects.filter(blockid = block_id,period_m = 0,period_h = 0)
        # predictObject_predicted = predictObject.values('predicted')

        # predictObject_id = int(predictObject.values('id')[0]['id'])
        # nextEightObjects = Finetreepredict.objects.order_by('id')[predictObject_id:predictObject_id+7]#这是接下来的7个时间的 但是h m 在16 以后不能这么做 要回头找
        # # nextEightObjects = serializers.serialize('json',nextEightObjects) #如果没有序列化，将会是是一个queryset,
        # nextEightObjects = nextEightObjects.values('pk','period_h','period_m','predicted')
        # dict2 = collections.defaultdict(dict)
        # count = 0
        # for eachObject in nextEightObjects:
        #     a = json.dumps(eachObject)
        #     dict2[count]['fields'] = str(a)
        #     count = count +1
        #     # dict2 = dict2.append(a)
        #     print(eachObject)
        # print(dict2)
        # fakedata = "{\"prob\": [{\"mon\": [26, 45, 56.7, 26, 25, 56.7, 26, 45, 56.7, 78.56, 56.7, 8.56, 56.7, 78.56, 56.7, 38.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 34.56, 84.56]},{\"tue\": [26, 45, 56.7, 26, 45, 56.7, 26, 45, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 8.56, 56.7, 78.56, 34.56, 84.56]},{\"wed\": [26, 45, 56.7, 26, 45, 56.7, 26, 45, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 6.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 34.56, 34.56]},{\"thu\": [26, 45, 56.7, 26, 45, 86.7, 26, 45, 56.7, 8.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 64.56, 34.56]},{\"fri\": [26, 45, 56.7, 26, 45, 56.7, 26, 45, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 34.56, 94.56]},{\"sat\": [26, 45, 56.7, 26, 45, 56.7, 26, 45, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 8.56, 56.7, 78.56, 24.56, 34.56]},{\"sun\": [26, 45, 56.7, 26, 45, 56.7, 26, 5, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 56.7, 78.56, 26.7, 78.56, 56.7, 78.56, 56.7, 78.56, 34.56, 34.56]}]}"

        # print(nextEightObjects)
        # print(str(type(nextEightObjects)))
        # print(predictObject_id)
        # print(str(type(predictObject_predicted)))
        # predictedValue = predictObject_predicted[0]['predicted']
        # dict = {'predict': predictedValue}
        # r = json.dumps(dict)
        # print(str(type(r)))


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

        # if monobj.exists():
        #     monrate = Lastmondata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        #     print(monrate)
        #     print(type(monrate))
        # else:
        #     monrate = 0
        # if tueobj.exists():
        #     tuerate = Lastmondata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        #     print(monrate)
        #     print(type(monrate))
        # else:
        #     monrate = 0
        # if tueobj.exists():
        #     tuerate = Lastmondata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        #     print(monrate)
        #     print(type(monrate))
        # else:
        #     monrate = 0


        # tuerate = Lasttuedata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        # wedrate = Lastweddata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        # thurate = Lastthudata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        # frirate = Lastfridata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        # satrate = Lastsatdata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        # sunrate = Lastsundata.objects.filter(bay_id=bayid).values('occupiedrate')[0]['occupiedrate']
        #
        # problist =[monrate,tuerate,wedrate,thurate,frirate,satrate,sunrate]
        #
        # problistdict = {'prob': problist}
        # problistdictjson = json.dumps(problistdict)

    return HttpResponse(problistdictjson,content_type = "application/json")

@csrf_exempt
def suggestbays(request):
    import ast
    dict = {}
    reqdict = {}
    if request.method == 'POST':
        bayliststr = request.POST['baylist']
        period_h = int(request.POST['period_h'])
        period_m = int(request.POST['period_m'])
        # print(baylist)
        # print(type(bayliststr))
        baylist = ast.literal_eval(bayliststr)
        listlength = len(baylist)
        print(listlength)
        print(type(baylist[0]))
        print(period_m)

        reqdict['baylist'] = baylist
        # reqdict['period_h'] = period_h
        reqdict['period_m'] = period_m

        print(reqdict)

        # 处理时间
        currenttimehour = int(time.strftime('%H', time.localtime(time.time())))
        currenttimeminute = int(time.strftime('%M', time.localtime(time.time())))
        newperiod_m = (currenttimeminute + period_m)%60
        print(newperiod_m)
        newperiod_h = currenttimehour + period_h + int((currenttimeminute + period_m)/60)
        print(newperiod_h)
        if newperiod_m < 30:
            newperiod_m = 0
        elif newperiod_m >= 30:
            newperiod_m = 30

        print(str(newperiod_h)+ ':'+str(newperiod_m))

    dict['create_at'] =str(time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())))


    print(str(currenttimehour)+':'+str(currenttimeminute))
    print(dict)
    # json = json.dumps(dict)

    return HttpResponse('noresponse')





def detail(request, parkingdata_id):
    parkingdata = get_object_or_404(Parking, pk = parkingdata_id)
    bay_id = parkingdata.bay_id
    lat = parkingdata.lat
    lon = parkingdata.lon
    st_market_id = parkingdata.st_market_id
    status = parkingdata.status
    parkingdate = parkingdata.parkingdate

    datalist = {'bay_id':bay_id,'lat':lat,'lon': lon,'st_market_id':st_market_id,'status':status,'parkingdate':parkingdate}
    datalist = json.dumps(datalist)

    return render('parkdata/detail.html', datalist)

# def search (request):
#     parking = Parking()
#     id = request.GET["bay_id"]
#     result = parking.objects.filter(pk=id)
#     bayid =
#
#     return HttpResponseRedirect(url)

    # 重定向 ：具体的url， 然后去urls.py 去匹配决定执行什么函数

# data['top'][0]