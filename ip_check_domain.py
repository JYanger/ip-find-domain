#!/usr/bin/env Python
# coding=utf-8
#https://github.com/JYanger/

import sys,os,socket,ssl,Queue,threading,time,re,xlrd,xlwt
from xlutils.copy import copy
socket.setdefaulttimeout(1)

global ip
global Domain
ip = []
Domain = []

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
    buf1=""
    try:
        client1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client1.connect(("www.114best.com",80))
        client1.sendall('''GET /ip/114.aspx?w={} HTTP/1.1\r\nHost: www.114best.com:80\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0\r\n\r\n'''.format(domain))
        buf = client1.recv(1024)
        while len(buf):
            try:
                buf1 = buf1 + buf
                buf = client1.recv(1024)
            except socket.error as e:
                break
        buf1 = buf1.decode('utf-8')
        vule = re.findall(r'alt="(.*?)" src="view.gif"', buf1, re.I)
        if ("".join(vule)) != "":
            ip.append(domain)
            Domain.append(("".join(vule)))
            print "| ip:"+domain + '  || Domain: ' + ("".join(vule)) + '  |'
        else:
            ip.append(domain)
            Domain.append("NULL")
            print "| ip:"+domain + '  || Domain: ' + "NULL"
        client1.close()
        #print ip
        #print Domain
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
        #domain1 = re.findall(r'(?<![\.\d])(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?![\.\d])',ip,re.I) #正则匹配ip地址
        ip = ("".join(domain1))
        #print ip
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
        print(u"----*----开始通过ip反查域名[www.114best.com]...[Current Time: "+ time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"]")
        print(u"----*----正在通过ip反查域名[www.114best.com]...请等待")
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
    #print len(ip)
    print u"正在写入excel...请等待"
    for i in range(len(ip)):
        for j in range(len(Domain)):
            write(i+1,0,ip[i])
            write(j+1,1,Domain[j])

if __name__=="__main__":
    IP_Survival_detection()
    result()
    print u"写入excel结束."

