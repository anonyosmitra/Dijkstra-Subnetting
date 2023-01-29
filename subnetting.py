from tabulate import tabulate
import math
from operator import*

req=[["Y",435], ["X",1726], ["B",1430], ["M",254], ["I",7175], ["C",5], ["A",51]]
mask=18
netIp="105.74.79.214"
RevOrder=False


countHosts=0
res={}
tabHist=[]
def printTable():
    print(tabulate(tabHist,headers=["Subnet","Required","Granted","Mask","Network","Broadcast","Host Tally"]))
def get2Pow(n):
    i=0
    while n>math.pow(2,i):
        i+=1
    return i
def getClosestBinNum(n):
    return int(math.pow(2,get2Pow(n)))
def popMaxReq():
    global req
    if len(req)==0:
        return None
    mx=req[0]
    for i in req:
        if i[1]>mx[1]:
            mx=i
        elif i[1]==mx[1]:
            if RevOrder:
                if i[0]>mx[0]:
                    mx=i
            elif i[0]<mx[0]:
                mx=i
    req.remove(mx)
    return mx
def toBin(x):
	return(format(int(x), '08b'))
def addbins(a,b):
    return bin(add(int(a,2),int(b,2)))

def toInt(x):
	return(int(x, 2))

def getMaskingAddress(mask):
    a=""
    a+="1"*int(mask)
    a+="0"*((8*4)-int(mask))
    return (a)

def isMasking(add,mask):
    for i in range(0,len(add)):
        if mask[i]=="1" and add[i]!="0":
            return(False)
    return(True)
def getMask(add):
    return add.split("/")[1]
def netAddressBin(ipBin,mask):
    a=ipBin[0:mask]
    a+="0"*(32-mask)
    return a
def getAddress(add):
    add = (add.split("/")[0]).split(".")
    for i in range(0,len(add)):
        add[i] = toBin(add[i])
    return "".join(add)

def getAvailableHosts(mask):
    hosts=(8*4)-int(mask)
    return toInt("1"*hosts)-1

def make32Bit(b):
    if (len(b) < 32):
        b = ("0" * (32 - len(b))) + b
    return b
def ipToBin(a):
    b=[]
    for i in a.split("."):
       b+=[toBin(i)]
    return("".join(b))
def binToIp(b):
    b=make32Bit(b)
    return ".".join([str(toInt(b[0:8])),str(toInt(b[8:16])),str(toInt(b[16:24])),str(toInt(b[24:32]))])
def setUp():
    global res,req,netIp
    print("Input: "+netIp)
    netIp=binToIp(netAddressBin(ipToBin(netIp),mask))
    print("Net Address: " + netIp)
    for i in req:
        res[i[0]]={"Required": i[1],"Granted": getClosestBinNum(i[1]+2),"Mask":binToIp(getMaskingAddress(32-get2Pow(8)))+"/"+str(32-get2Pow(getClosestBinNum(i[1]+2)))}
        i[1]=getClosestBinNum(i[1]+2)
def start():
    setUp()
    global countHosts,netIp,res,tabHist
    while len(req)>0:
        a=popMaxReq()
        res[a[0]]["Network"]=netIp
        netIp=binToIp((addbins(ipToBin(netIp),make32Bit(toBin(res[a[0]]["Granted"]-1)))).split("b")[1])
        res[a[0]]["Broadcast"] = netIp
        netIp = binToIp((addbins(ipToBin(netIp), make32Bit(toBin(1)))).split("b")[1])
        countHosts+=res[a[0]]["Granted"]
        tabHist+=[[a[0],res[a[0]]["Required"],res[a[0]]["Granted"],res[a[0]]["Mask"],res[a[0]]["Network"],res[a[0]]["Broadcast"],countHosts]]
    printTable()
start()
