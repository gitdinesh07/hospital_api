from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from pymongo import MongoClient
from bson.json_util import dumps
import json


class WebScrap:
    i = 1
    f_data = '['
    data = ''
    record = 0
    loc = ""

    def scrap_method(self, city):
        try:
            WebScrap.loc = city
            for c in range(1, 6):
                try:
                    source_url="https://www.sehat.com/"+WebScrap.loc+"/hospitals?page="+c.__str__()
                    uclient = uReq(source_url)
                    page_html = uclient.read()
                    uclient.close()
                except Exception:
                    # return 0 if url or city not found
                    return 0
                page_soup = soup(page_html, "html.parser")
                container = page_soup.find_all("div", {"class": "col-md-6 col-sm-6 col-xs-9 padding-left-10"} )
                r=0
                while r<=len(container)-1:
                    if r==len(container)-1 and c==5:
                        WebScrap.data += '{\"hospital_name\":' + '\"' + container[r].span.text + '\",\"address\":\"'+container[r].p.text.strip() + '\"}'
                    else:
                        WebScrap.data += '{\"hospital_name\":' + '\"' + container[r].span.text+'\",\"address\":\"'+container[r].p.text.strip()+'\"},'

                    WebScrap.record +=1

                    r = r + 1

                if r!=10:
                    break

                else :
                    WebScrap.i = c
            WebScrap.f_data += '{\"_id\" : \"' + WebScrap.loc + '\",\"Page\" :' + WebScrap.i.__str__() + ',\"total_record\" :' + WebScrap.record.__str__() + ', \"details\" :[ '
            WebScrap.f_data += WebScrap.data+']}]'
            return WebScrap.f_data
        except:
            # Return 2 if find some error
            return 2

    def imp_data_mongo(self):
        client = MongoClient("localhost", 27017)
        collection = client.hospital_detail[WebScrap.loc]
        collection.insert(json.loads(WebScrap.f_data))

    def exp_data_mongo(self, city_name):
        try:
            client = MongoClient("localhost", 27017)
            collection = client.hospital_detail[city_name]
            data = collection.find()
            exp_data = object
            for r in data:
                exp_data = r
            return dumps(exp_data)
        except TypeError:
            return 0
