# encoding: utf-8
import urllib2
import re
from pyquery import PyQuery as pq
'''
Created on 2016年8月9日
国家统计局全国区划数据爬取
@author: hcy
'''
class AreaSpider(object):
    # 初始话方法
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = { 'User-Agent' : self.user_agent }
        
        self.baseURL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015'
        self.urlSuffix = '.html'
        self.contents = [ ]
        self.timeout = 120
        self.file = '/home/hcy/Work/G7/data/city_use/search_use_count/area2015.txt'
        self.f = open(self.file, "w+")
        
    def getPage(self, index):
        try:
            # url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html'
            url = self.baseURL + '/' + index + self.urlSuffix
            # 构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request,timeout=self.timeout)
            # 将页面内容转化为gbk编码
            # pageContent = response.read().decode('gbk')
            pageContent = response.read().decode('gbk','ignore')
            return pageContent
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接国家统计局错误原因", e.reason
                print u"连接失败的url"+url
            return None
     
    # 得到所有省份
    def getProvince(self, index,fromProv):
        pageContent = self.getPage(index) 
        pattern = re.compile('<table class=.*>.*</table>', re.S)
        items = re.findall(pattern, pageContent)
        doc = pq(items[0])
        trs = doc('tr').filter(lambda i: i >= 3)
        for tr in trs.items():
            for td in tr('td').items():
                index = td('a').attr('href').split('.')[0]
                if(int(index)<fromProv): 
                    continue
                name = td('a').html().split('<')[0]
                code = index + '0000000000'
                areatype = '000'
                self.writeData(name, code, areatype)
                self.getContents(index)        
    # 传入某一页代码，返回本页不带图片的段子列表
    def getContents(self, index):
        # 递归终止条件
        if (index == '') : return 
        pageContent = self.getPage(index)
        if not pageContent:
            print "页面加载失败...."
            return None
        # 解析html，得到想要的内容
        pattern = re.compile('<table class=.*>.*<tr class=.*>.*</tr>.*</table>', re.S)
        items = re.findall(pattern, pageContent)
        # 需要的内容<table>...</table>
        doc = pq(items[0])
        trs = doc('tr').filter(lambda i: i >= 1)
        for tr in trs.items():
            td = tr('td')
            if(td('a').html() != None):
                code = td('a').eq(0).html()
                code1 = code[0:2]
                code2 = code[2:4]
                code3 = code[4:6]
                code4 = code[6:9]
                code5 = code[9:12]
                if (code3 == '00' and code4 == '000'):
                    index = code1 + '/' + code1 + code2
                elif (code3 != '00' and code4 == '000') :
                    index = code1 + '/' + code2 + '/' + code1 + code2 + code3
                elif (code3 == '00' and code4 != '000') :
                    index = code1 + '/' + code2 + '/' + code1 + code2 + code3+code4
                elif (code4 != '000' and code5 == '000') :
                    index = code1 + '/' + code2 + '/' + code3 + '/' + code1 + code2 + code3 + code4
                name = td('a').eq(1).html()
                areatype = '000'    
#                  self.contents.append({'name':name,'code':code,'areatype':areatype})
                #print {'name':name, 'code':code, 'areatype':areatype}
                self.writeData(name, code, areatype)
#                  con = self.contents[0]
#                  f = open(self.file,"w+")
#                  row = td('a').eq(1).html()
#                 row = con['name'].encode('utf-8')+'\t'+con['code']+'\t'+con['type']+'\n'
#                  f.write(row);
            else :
                index = ''
                if td.eq(2).html() != None:
                    name = td.eq(2).html()
                    code = td.eq(0).html()
                    areatype = td.eq(1).html()
#                      self.contents.append({'name':name,'code':code,'areatype':areatype})
                    #print {'name':name, 'code':code, 'areatype':areatype}
                    self.writeData(name, code, areatype)
                else:
                    name = td.eq(1).html()
                    code = td.eq(0).html()
                    areatype = '000'
#                      self.contents.append({'name':name,'code':code,'areatype':areatype})
                    #print {'name':name, 'code':code, 'areatype':areatype}
                    self.writeData(name, code, areatype)
            # 递归调用
            self.getContents(index)
    # 开始方法
    def writeData(self, name, code, areatype):
        try:
            row = name.encode('utf-8')+ '\t' + code + '\t' + areatype + '\n'
            self.f.write(row)
        except Exception as e:
            print e
            print '---------->异常code:' + code    
    #从某个链接开始遍历        
    def startOne(self, index):
        print u"--------->正在读取国家统计居区划信息"
        self.getContents(index)
        self.f.close()
        # print u"--------->读取到的条数有:"+len(self.contents)
#         print u"--------->正在写入文件到"+self.file
#         f = open(self.file,"w+")
#         for con in self.contents:
#             row = con['name'].encode('utf-8')+'\t'+con['code']+'\t'+con['areatype']+'\n'
#             f.write(row);
#         f.close()
        print u"--------->写入文件完毕，恭喜爬取数据成功！"   
    #默认遍历所有省份，fromProv从哪个省份开始  
    def startAll(self, index,fromProv=0):
        print u"--------->正在读取国家统计居区划信息"
        self.getProvince(index,fromProv)
        self.f.close()
        print u"--------->写入文件完毕，恭喜爬取数据成功！"   
                 
spider = AreaSpider()
spider.startAll('index',45)
#spider.startOne('65/43/25/654325204')
            
            
            
        
