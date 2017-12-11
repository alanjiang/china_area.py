import urllib.request as req
import urllib.error as error
import sys
import re
import os
import os.path
import time
import random
'''

Ahthor :Alan P Jiang
To get the Province, City , Town as well as Village names for China
Date: 12 Dec,2017
Email: jiangpenghnlg@126.com
If you get problems when use it, please contact me by email above.
'''
def downloadfile(homepage,path,filename):

    time.sleep(random.randint(1,6))
    request = req.Request(homepage)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)') 
    response = req.urlopen(request)  
    html = response.read().decode("GBK")
    file=open(path+'\\'+filename,'w')
    file.write(html)
    file.close()
    return path+'\\'+filename


def getChinaPages(refname,filename):

    dics={}
    with open(filename,'r') as file:

         strs=re.findall(r'<td><a href=\'(\d{2}.html)\'>(\D+)<br/></a></td>',file.read())
         file.close()
         with open(os.path.dirname(filename)+'/'+refname,'w') as outfile:
              for str in strs:

                  outfile.write(str[0]+','+str[1]+'\t\n')
                  dics[str[0]]=str[1]
         outfile.close()
    return dics

def getProPages(refname,filename):
    dics={}
    with open(filename,'r') as file:
         strs=re.findall(r'<td><a href=\'(\d{2}/\d{4}.html)\'>(\d+)</a></td><td><a href=\'\d{2}/\d{4}.html\'>(\D+)</a></td>',file.read())
         file.close()
         with open(os.path.dirname(filename)+'/'+refname,'a') as outfile:
              for str in strs:
                  outfile.write(str[0]+','+str[1]+','+str[2]+'\t\n')
                  dics[str[0]]=str[1]+','+str[2]

         outfile.close()

    return dics

def getCityPages(refname,filename):
    dics={}
    with open(filename,'r') as file:
         strs=re.findall(r'<tr class=\'countrytr\'><td><a href=\'(\d{2}/\d+.html)\'>(\d+)</a></td><td><a href=\'\d{2}/\d+.html\'>(\D+)</a></td></tr>',file.read())
         file.close()
         with open(os.path.dirname(filename)+'/'+refname,'a') as outfile:
              for str in strs:
                  outfile.write(str[0]+','+str[1]+','+str[2]+'\t\n')
                  dics[str[0]]=str[1]+','+str[2]

         outfile.close()

    return dics

def getCountryPages(refname,filename):
    dics={}
    with open(filename,'r') as file:
         strs=re.findall(r'<td><a href=\'(\d{2}/\d{9}.html\'>(\d+)</a></td><td><a href=\'\d{2}/\d{9}.html\'>(\D+)</a></td>',file.read())
         file.close()
         with open(os.path.dirname(filename)+'/'+refname,'a') as outfile:
              for str in strs:
                  outfile.write(str[0]+','+str[1]+','+str[2]+'\t\n')
                  dics[str[0]]=str[1]+','+str[2]

         outfile.close()

    return dics




def getRelHtml(htmlLinkPath):

    regex=[r'\d{2}/(\d{9}).html',r'\d{2}/(\d{6}).html',r'\d{2}/(\d{4}).html',r'(\d{2}).html']

    s=''
    for reg in regex:
        print ('---htmlLinkPath='+htmlLinkPath)
        match=re.search(reg,htmlLinkPath)
        if match:
           s=match.group(1)
           break
    print('s='+s)
    if (len(s)==2):
        return s+'.html'
    elif (len(s)==4):

        return s[0:2]+'/'+s+'.html'
    elif (len(s)==6):

        return s[0:2]+'/'+d[2:4]+'/'+s[4:6]+'/'+s+'.html'



def spider():
    webroot='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
    localroot='F:/software/spider'
    file=downloadfile(webroot+'index.html',localroot,'index.html')
    lists=getChinaPages('china.txt',file)
    provinces={}
    citys={}
    countrys={}
    for (k,v) in lists.items():
        print (k+','+v)
        file=downloadfile(webroot+k,localroot,k)
        provinces=getProPages('province.txt',file)
        for(m,n) in provinces.items():
           print(m+','+n)
           html=m.split('/')[1]
           m=getRelHtml(m)
           print(webroot+m)
           file=downloadfile(webroot+m,localroot,html)
           citys=getCityPages('city.txt',file)
           for(x,y) in citys.items():
               print(x+','+y)
               html=x.split('/')[1]

               x=getRelHtml(x)
               print(webroot+x)
               file=downloadfile(webroot+x,localroot,html)
               countrys=getCountryPages('country.txt',file)
               for(a,b) in countrys.items():
                   print(a+','+b)

                   html=a.split('/')[1]
                   a=getRelHtml(a)
                   file=downloadfile(webroot+a,localroot,html)
def callSpider():
    try:
        spider()
    except error.HTTPError:
           print('HTTP error')
           time.sleep(20)
           callSpider()

if __name__=='__main__':
    callSpider()
                       
                       
    
