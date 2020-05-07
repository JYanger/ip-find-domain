#!/usr/bin/env Python
# -*- coding: utf-8 -*- 
#https://github.com/JYanger/

import sys,os,socket,ssl,Queue,threading,time,re,xlrd,xlwt,urllib2,urllib
from xlutils.copy import copy

global ip
global Domain
ip = []
Domain = []
type = sys.getfilesystemencoding()


class MyThread(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            try:
                ip = self.queue.get(block=False)
                check(ip,)
            except Exception as e:
                break   

def check(domain):
    global ip
    global Domain
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
    try:
        domain1 ="https://dns.aizhan.com/{}/".format(domain)
        domain1 = str(domain1)
        request = urllib2.Request(domain1,headers = headers)
        response = urllib2.urlopen(request,timeout=3)
        time.sleep(0.3)
        buf1 = response.read().decode("UTF-8").encode(type)
        #print buf1
        regex = r'''" rel="nofollow" target="_blank">(.*?)</a>'''
        vule = re.findall(regex,buf1,re.I | re.M)
        #print ("".join(vule))
        if ("".join(vule)) != "":
            ip.append(domain)
            Domain.append(("".join(vule)))
            print "| ip:"+domain + '  || Domain: ' + ("".join(vule)) + '  |'
        else:
            ip.append(domain)
            Domain.append("NULL")
            print "| ip:"+domain + '  || Domain: ' + "NULL"
    except socket.error as e:
        pass      
                            
def check_all(iplist,Thread_nums):
    threads = []
    queue = Queue.Queue()
    file = open(iplist,'r')
    for ip in file.readlines():
        ip=ip.replace('\n','')
        ip=ip.replace('\r','')
        ip = str(ip.replace('\n',''))
        if 'http' not in ip:
            ip = 'http://' + str(ip)
        if ip.count('/') <3:
            ip = ip + '/'
        domain1 = re.findall(r'://(.*?)/', ip, re.I)
        domain2 = re.findall(r'(.*?)//', ip, re.I)
        if ":" in "".join(domain1):
            domain1 = re.findall(r'://(.*?):', ip, re.I)
        ip = ("".join(domain1))
        queue.put(ip)
    file.close()
    for i in range(int(Thread_nums)):
        MyThread(queue).setDaemon(True)
        threads.append(MyThread(queue))    
    for t in threads:
        try:
            t.start()
        except Exception as e:
            pass
    for t in threads:
        try:
            t.join()
        except Exception as e:
            pass

def IP_Survival_detection():
    if len(sys.argv)!=3:
        print("e.g: python2 "+os.path.basename(sys.argv[0])+" [iplist.txt] "+"[Thread_num]")
        sys.exit()
    else:
        start_time = time.time()
        print(u"----*----开始通过ip反查域名[dns.aizhan.com]...[Current Time: "+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"]")
        print(u"----*----正在通过ip反查域名[dns.aizhan.com]...请等待")
        check_all(sys.argv[1],int(sys.argv[2]))
        time.sleep(2) 
        print(u"----*----检查结束...[Current Time: "+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"]")
        
def write(p,q,value):                                              #创建excel的写入函数
    if os.path.exists("ip_domain.xls"):
        
        w1 =xlrd.open_workbook('ip_domain.xls')
        ws1= w1.sheet_by_index(0)
        #nrows = ws1.nrows

        w = copy(w1)
        ws = w.get_sheet(0)
        #print nrows
        #print value
        ws.write(p,q,value)
        w.save('ip_domain.xls')
                
    else:
        try:
            w = xlwt.Workbook(encoding='utf-8')
            ws = w.add_sheet("ip_damain")
            ws.write(0,0,"ip地址")
            ws.write(0,1,"域名信息")
            w.save('ip_domain.xls')
        except Exception as e:
            print "crate .xls file failed!"
            
        w1 =xlrd.open_workbook('ip_domain.xls')
        ws1= w1.sheet_by_index(0)
        #nrows = ws1.nrows
        w = copy(w1)
        ws = w.get_sheet(0)
        ws.write(p,q,value)
        w.save('ip_domain.xls')

def result():
    global ip
    global Domain
    print u"正在写入excel...请等待"
    for i in range(len(ip)):
        write(i+1,0,ip[i])
    for j in range(len(Domain)):   
        write(j+1,1,Domain[j])

if __name__=="__main__":
    IP_Survival_detection()
    result()
    print u"写入excel结束."
