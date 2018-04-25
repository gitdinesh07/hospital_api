from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from pymongo import MongoClient
from bson.json_util import dumps
import json
import urllib.request as chk_req


class WebScrap:
    i = 1
    f_data = '['
    data = ''
    record = 0
    loc = ""
    client = MongoClient("localhost", 27017)

    def __init__(self, city):
        WebScrap.loc = city
        WebScrap.loc = WebScrap.loc.lower()
    def scrap_method(self):
        try:

            for c in range(1, 6):
                try:
                    source_url = "https://www.sehat.com/"+WebScrap.loc+"/hospitals?page="+str(c)
                    req = chk_req.urlopen(source_url)
                    if req.getcode() == 200 :
                       uclient = uReq(source_url)
                       page_html = uclient.read()
                       uclient.close()
                    else:
                       return 0
                except :
                    # return 0 if url or city not found
                    return 0
                page_soup = soup(page_html, "html.parser")
                container = page_soup.find_all("div", {"class": "col-md-6 col-sm-6 col-xs-9 padding-left-10"} )
                r = 0
                while r <= len(container)-1:
                    if r == len(container)-1 and c == 5:
                        WebScrap.data += '{\"hospital_name\":' + '\"' + container[r].span.text + '\",\"address\":\"'+container[r].p.text.strip() + '\"}'
                    else:
                        WebScrap.data += '{\"hospital_name\":' + '\"' + container[r].span.text+'\",\"address\":\"'+container[r].p.text.strip()+'\"},'

                    WebScrap.record += 1

                    r = r + 1

                if r != 10:
                    break

                else :
                    WebScrap.i = c
            WebScrap.f_data += '{\"_id\" : \"' + WebScrap.loc + '\",\"Page\" :' + WebScrap.i.__str__() + ',\"total_record\" :' + WebScrap.record.__str__() + ', \"details\" :[ '
            WebScrap.f_data += WebScrap.data+']}]'

            collection = WebScrap.client.hospital_detail[WebScrap.loc]
            collection.insert(json.loads(WebScrap.f_data))
            return 1
        except Exception as e:
            # Return 2 if find some error
            return 0

    def imp_data_mongo(self):
        try:
            collection = WebScrap.client.hospital_detail[WebScrap.loc]
            collection.insert(json.loads(WebScrap.f_data))
            return 1
        except Exception as e:
            return str(e)

    def exp_data_mongo(self):
        try:
            collection = WebScrap.client.hospital_detail[WebScrap.loc]
            data = collection.find()
            exp_data = object
            for r in data:
                exp_data = r
            return dumps(exp_data)
        except Exception:
            return 0

