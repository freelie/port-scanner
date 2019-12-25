from scapy.all import *
from threading import Thread
from time import sleep,time
see=None
end=[]
min = 0
max = 0
value = 0
d={}
b=time()
urls=[]
mesto=5
mesto_2 = 1
code = [0,0,0]
port_range = (1,1000)
timeout_S,timeout_A,timeout_F = 30,30,30
ipaddr=["192.168.100."+str(i) for i in range(20)]
l=0
class DownloadThread(Thread):
    def __init__(self, url, name):
        Thread.__init__(self)
        self.name = name
        self.url = url

    def run(self):
        global see
        global d
        global value
        global port_range
        global timeout_S
        global timeout_A
        global timeout_F
        if code[0] == True:
            pkt = IP(dst=self.url)/TCP(dport=port_range,flags="S")
            a = sr(pkt,timeout=timeout_S)
            r, u = a
            see=r
            for i in r:
                if i[1][1].flags == "SA":
                    d[i[0].dst].append(str(i[1][1].sport))
                    if code[1] == True:
                        a=sr1(IP(dst=i[0].dst)/TCP(dport = i[1][1].sport,flags = "A"),timeout = timeout_A)
                        if a == None:
                            d[i[0].dst][-1]=str(d[i[0].dst][-1])+"*"
                else:
                    if code[2]==True:
                        a=sr1(IP(dst=i[0].dst)/TCP(dport = i[1][1].sport,flags = "F"),timeout = timeout_F)
                        if a==None:
                            d[i[0].dst].append(str(i[1][1].sport))


        global end
        end.append(self.name)
        global mesto_2
        mesto_2+=1
        value+=port_range[1]-port_range[0]+1
class DownloadThread2(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
    def run(self):
        global d
        pkt=IP(dst=self.url)/ICMP()
        a=sr1(pkt,timeout=3)
        if a!=None:
            if (a[0].src in urls)!=1:
                urls.append(a[0].src)
            for url in urls:
                d[url]=[]

        global l
        global mesto
        global value
        mesto+=1
        l+=1
        value+=1

def main(urls):
    global mesto
    for url in ipaddr:
        thread = DownloadThread2(url)
        while True:
            if mesto>0:
                break
        mesto-=1
        thread.start()
    global l
    while True:
        if l>len(urls):
            break
    global mesto_2
    global max
    max = len(ipaddr) + len(d)*(len(range(port_range[0],port_range[1]))+1)
    for item, url in enumerate(urls):
        name = "Поток %s" % (item+1)
        thread = DownloadThread(url, name)
        while True:
            sleep(2)
            if mesto_2>0:
                break
        mesto_2-=1
        thread.start()

def start():
    global ipaddr
    global max
    global value
    value = 0
    max = len(ipaddr) + len(ipaddr)*len((range(port_range[0],port_range[1]+1)))
    main(urls)
    while True:
        if len(end)>=len(urls):
            break
        sleep(1)
    print(time()-b)

