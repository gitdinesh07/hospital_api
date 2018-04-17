from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from . import get_data


def default(request):
    return render(request, "default.html")


class HospitalList(APIView):

    def get(self, request, city_name):
        obj = get_data.WebScrap()
        mydata = obj.exp_data_mongo(city_name)
        if mydata == 0:
            get_d = obj.scrap_method(city_name)
            if get_d == 0:
                return Response(None);
            else:
                obj.imp_data_mongo()
                mydata = obj.exp_data_mongo(city_name)
                d = json.loads(mydata)
                return Response(d)
        else:
            d = json.loads(mydata)
            return Response(d)

