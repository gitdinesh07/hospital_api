from bs4 import BeautifulSoup as soup
from urllib.request import  urlopen as uReq
from pymongo import MongoClient
import json



class web_scrap:

   i= 1
   f_data='[';
   data=''
   record=0;
   loc=""
   def __init__(self,loc):
       web_scrap.loc=loc
   def scrap_method(self):
      try :

          for c in range(1,6):
              try:
                  source_url="https://www.sehat.com/"+web_scrap.loc+"/hospitals?page="+c.__str__()
                  uClient = uReq(source_url);
                  page_html = uClient.read();
                  uClient.close();
              except:
                  #return 1 if url or city not found
                  return 1
              page_soup = soup(page_html,"html.parser");
              container = page_soup.find_all("div", {"class": "col-md-6 col-sm-6 col-xs-9 padding-left-10"} );

              r=0;

              while r<=len(container)-1:
                  if r==len(container)-1 and c==5:
                      web_scrap.data += '{\"hospital_name\":' + '\"' + container[r].span.text + '\",\"address\":\"' + container[r].p.text.strip() + '\"}';
                  else:
                     web_scrap.data +='{\"hospital_name\":'+'\"'+container[r].span.text+'\",\"address\":\"'+container[r].p.text.strip()+'\"},';

                  web_scrap.record +=1;

                  r = r + 1;

              if r!=10:
                  break

              else :
                    web_scrap.i = c;

          web_scrap.f_data += '{\"_id\" : \"' + web_scrap.loc + '\",\"Page\" :' + web_scrap.i.__str__() + ',\"total_record\" :' + web_scrap.record.__str__() + ', \"details\" :[ ';
          web_scrap.f_data +=web_scrap.data+']}]';
          return(web_scrap.f_data)
      except:
        #Return 2 if find some error
          return 2




   def imp_data_mongo(self):
        client = MongoClient("localhost", 27017)
        collection = client.hospital_detail[web_scrap.loc]
        collection.insert(json.loads(web_scrap.f_data))

   def exp_data_mongo(self):

        client = MongoClient("localhost", 27017)
        collection = client.hospital_detail[web_scrap.loc];
        data=collection.find()
        for r in data:
            print(r)


emp1 = web_scrap('mumbai');
emp1.scrap_method();
#emp1.imp_data_mongo()
#emp1.exp_data_mongo()
