import requests
import numpy as np
from lxml import etree 
import re
import urllib2
import random
import os
#curl -d '{"instances": [1.0,  2.0]}'   -X POST http://localhost:8502/v1/models/half_plus_three:predict
SERVER_URL = 'https://www.mn52.com/meinvmingxing/list_5_2.html'
#my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
#"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
#"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
#"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
#"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]
my_headers=["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"]

def get_last_page_number(html):
    page_list = html.xpath('//div[@class="itempages"]//a')
    page_max = -1
    for i in page_list:
       number_str = etree.tostring(i, encoding="utf-8", pretty_print=True).decode("utf-8")
       matchNumber = re.search("list_(.+)_(.+)\.html",number_str)
       if matchNumber:
           if page_max < int(matchNumber.group(2)):
	     page_max = int(matchNumber.group(2))
    return page_max

#i.attrib['alt'].replace(" ","")
def get_picbox(html):
    picbox_list = html.xpath('//div[@class="picbox"]//a')
    ret = []
    for i in picbox_list:
#       print(i.attrib['href'])
#       print etree.tostring(i, encoding="utf-8", pretty_print=True).decode("utf-8")
       img_list = i.xpath('.//img')
#       print etree.tostring(img_list[0], encoding="utf-8", pretty_print=True).decode("utf-8")
       album_name =  img_list[0].attrib['alt'].replace(" ","")
#       print(album_name)
       ret.append((i.attrib['href'],album_name))
    return ret    

def get_img(html):
    picbox_list = html.xpath('//div[@class="list-pic"]//div[@class="img-wrap"]//img')
#    print etree.tostring(html, encoding="utf-8", pretty_print=True).decode("utf-8")
    ret = set()
    for i in picbox_list:
       #print(i.attrib['src'])
       ret.add((i.attrib['src']))
    return ret    

def download_pic(url,ref_url,name):
    print(url)
    print(ref_url)
#    random_header = random.choice(my_headers)
#    req = urllib2.Request(url)
#    req.add_header("user-agent",random_header)
#    req.add_header("host","image.mn52.com")
#    req.add_header("referer",ref_url)
#    req.add_header("get",url)
    try:
        random_header = random.choice(my_headers)
        req = urllib2.Request(url)
        req.add_header("user-agent",random_header)
        req.add_header("host","image.mn52.com")
        req.add_header("referer",ref_url)
        req.add_header("get",url)

        content=urllib2.urlopen(req).read()
#        re_file = re.search("(.*?.[jpg|png]])",url.split("/")[-1])
#        file_name = "tmp"
#        if re_file:
#          file_name = re_file.group(0);
        file_name = url.split("/")[-1].split("?")[0]
        with open(os.path.join(name,file_name),'wb') as file:
          file.write(content)
    except:
        print("Error:%s"% url)
#    with open()
   
def my_request2():
    parser = etree.HTMLParser(encoding="utf-8")
#    html = etree.parse("meinv.html",parser=parser)
    response = requests.get(SERVER_URL)
    text = response.content
    html = etree.HTML(text)
    page_number = get_last_page_number(html)
    print("total page number:[%d]" % page_number)
    url_root = "https://www.mn52.com"
    #https://www.mn52.com/meinvmingxing/list_5_2.html
    # for now only download 3 page
    #page_number = 1
    for i in range(1,page_number+1):
       cur_url =  url_root +"/meinvmingxing/list_5_" + str(i) + ".html"
       response = requests.get(cur_url)
       text = response.content
       html = etree.HTML(text)
       picbox_list = get_picbox(html)
#       print(picbox_list)
       for picbox,name in picbox_list:
          print(name)
          if not os.path.exists(name):
            os.mkdir(name)
          picbox_url = url_root + picbox
#          print(picbox_url)
          picbox_response = requests.get(picbox_url)
          picbox_html = etree.HTML(picbox_response.content,parser=parser)
          ret = get_img(picbox_html)
          print ret
          for each_img in ret:
            download_pic("https:" + each_img,picbox_url,name)

#    s = etree.tostring(html).decode()
#    print(s)

#def my_request3():
#    parser = etree.HTMLParser(encoding="utf-8")
#    html = etree.parse("meinv2.html",parser=parser)
#    ret= get_img(html)
#    print(ret)
##    t = etree.tostring(html, encoding="utf-8", pretty_print=True)
##    print(t.decode("utf-8"))
#
#def my_requests():
#    response = requests.get(SERVER_URL)
#    text = response.content
#    html = etree.HTML(text)
#    print("-----------")
#    s = etree.tostring(html).decode()
#    print(s)


if __name__ == "__main__":
    my_request2()
    #download_pic("http://blog.csdn.net/qysh123/article/details/44564943")
    #download_pic("https://image.mn52.com/img/allimg/190828/8-1ZRQQ110.jpg")
#    download_pic("https://image.mn52.com/img/allimg/190828/8-1ZRQQ111-50.jpg","xx")
