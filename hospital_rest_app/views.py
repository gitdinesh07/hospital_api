from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.http import HttpResponse
from . import get_data
import gc


def default(request):
    return render(request, "default.html")


class HospitalList(APIView):

    def get(self, request,city_name):
            obj = get_data.WebScrap(city_name)
            mydata = obj.exp_data_mongo()
            if mydata == 0:
                return Response()
            else:
                return Response(json.loads(mydata))


def post_city(self,city_name):
    obj = get_data.WebScrap(city_name).scrap_method()
    if obj == 1:
        return HttpResponse("<h4> sucess .. </h4>")
    else:
       return HttpResponse("<h4>"+str(obj)+ "</h4>")