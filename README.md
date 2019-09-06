注:虽然python使用了有5年,但由于工作中并不需要使用到爬虫,所以并没有去花心思去学习它.最近突然想学一下爬虫,所以从最基础的知识点结合实际用例来整理一下,所以本文适合初学者来写一个简单的爬虫.

本文主要解决:
1.  爬虫需要使用到哪些库.
2.  如何爬取图片.
3.  如果绕过服务器的校验.
> 本文就尝试爬取(https://www.mn52.com/) 上的图片

### 1.  爬虫需要使用到哪些库
```
# 发送get,post 请求获取页面代码
import requests
# 用于解析HTML
from lxml import etree
# 用于做正则表达式提取,需要的信息
import re 
```

### 2. 如何爬取图片
> 我使用的是chrome浏览器,在源代码中聚焦相应的页面也会有高亮对定位非常方便.

#### 2.1 定位关键信息
页面上有很多页,每一页也有很多缩略图,每一个缩略图点击进去又分缩略图和实际全图,而我们最终的目标是获取到实际的全图,以下来分解每一步:
##### - 定位分页
所有分页的信息保存在, \<div clss = "itemapges"\> 中,读取到末页的编号,我们就可以去依次便利全页面了
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019090615170057.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hscG93ZXI=,size_16,color_FFFFFF,t_70)
所以有以下代码:
```python
#获取最大分页的number
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
```
##### -定位主页下的缩略图链接页面
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190906160017511.png)
缩略图均放在了picbox之中
```python
def get_picbox(html):
    picbox_list = page_list = html.xpath('//div[@class="picbox"]//a')
    ret = []
    for i in picbox_list:
#       print(i.attrib['href'])
       ret.append(i.attrib['href'])
    return ret    
```
##### -定位图片地址
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190906170421991.png)
```python
#这里我偷了懒直接获取所有image标签
def get_img(html):
    picbox_list = page_list = html.xpath('//img')
    ret = []
    for i in picbox_list:
       print(i.attrib['src'])
       ret.append(i.attrib['src'])
    return ret    
```


### 3. 绕过服务器校验
当我使用下面代码去下载图片时候会得到告警信息
```python
def download_pic(url):
    pic_ = requests.get(url)
    re_file = re.search("(.*?.jpg)",url.split("/")[-1])
    file_name = "tmp"
    if re_file:
      file_name = re_file.group(0);
    print(pic_.content)
    with open(file_name,'wb') as file:
      file.write(pic_.content)
```
```python
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head><title>403 Forbidden</title></head>
<body bgcolor="white">
<h1>403 Forbidden</h1>
<p>You don't have permission to access the URL on this server.<hr/>Powered by Tengine</body>
</html>
```
服务器的校验机制识别出我发出请求的方式有问题,所以拒绝了我的请求.
我的解决办法是设置header,模拟的浏览器绕过的,方式如下 观察image.mn52.com下的headers部分:
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190906181727108.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hscG93ZXI=,size_16,color_FFFFFF,t_70)
将此部分加入到请求的header部分,这里使用了urllib2 具体的代码如下:
```python
def download_pic(url,ref_url):
    random_header = random.choice(my_headers)
    req = urllib2.Request(url)
    req.add_header("user-agent",random_header)
    req.add_header("host","image.mn52.com")
    req.add_header("referer",ref_url)
    req.add_header("get",url)
    
    content=urllib2.urlopen(req).read()
    print(content)
    re_file = re.search("(.*?.jpg)",url.split("/")[-1])
    file_name = "tmp"
    if re_file:
      file_name = re_file.group(0);
    #print(pic_.content)
    with open(file_name,'wb') as file:
      file.write(content)
```
这下就可以下载到图片了.


到这里基本的爬虫功能就实现了注意:
1. 如果出现段时间内过多的请求服务器可能会有IP校验.
2. 尝试的时候不要太多使用这个网站,毕竟美女图片这么全的网站也很重要.

update:20190906
这里填补一个xpath的坑:
如果想在当前节点下获得其子节点要 **相对路径定位**如下:
```python
    for i in picbox_list:
       print(i.attrib['href'])
       print etree.tostring(i, encoding="utf-8", pretty_print=True).decode("utf-8")
       img_list = i.xpath('.//img') #这里使用相对目录
 ```

