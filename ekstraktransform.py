# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 21:37:07 2019

@author: reyhan
"""

import re
import csv

data = {}         # berisi pasangan key:value
listofdict = []   #list yg berisi kumpulan dictionary, didalam dictionary terdapat 10 pasang key:value
inpt = []
label = []

pattern = ["(?=GET|POST).*", "(Host: ).*", "(User-Agent: ).*", "(Accept: ).*", "(Referer: ).*", "(Accept-Encoding: ).*", "(Accept-Language: ).*", "(Cookie: ).*", "(Content-Length: ).*", "(Content-Type: ).*"]

#sectionB = []
#cleandata = []
#numericdata = []

a = list(range(128))
rangeAsciiazAZ = a[65:91]+a[97:123] #[65:90] utk a-z , [97:122] utk A-Z, jika pakai slice (.. , ..) berbeda lagi caranya
rangeAscii09 = a[48:58]

def countofDgt(arg):
    countDgt = 0
    for char in arg:
        if ord(char) in rangeAscii09:  # ord(), sebagai ordinal 
            countDgt += 1            # sebelumnya pakai chr(), tetapi ujung2 nya adalah len tetap membaca 1 karakter
    return countDgt

def countofLtr(arg):
    countLtr = 0
    for char in arg:
        if ord(char) in rangeAsciiazAZ:
            countLtr += 1
    return countLtr

def countofSpchar(arg):
    countSpchar = 0
    for char in arg:
        if (ord(char) not  in rangeAsciiazAZ) and (ord(char) not  in rangeAscii09):
            countSpchar += 1
    return countSpchar

def readLog(filename, value, limit):
    global listofdict, data            # !! menjadikan variabel local ke global, agar defisini sebelumnya(diluar def) dapat berfungsi di dalam def read log
    with open (filename,'r') as ifile:
        filelistnow = ifile.readlines() #1
        for item in filelistnow:        #2        #kalau udh kena semua, for ini di indent lebih dalam dari #writematchincsv
            for k in pattern:
                    x = re.match(k,item)
                    if x:
                        if re.match ("(?=GET |POST ).*", x.group(0)): # !! x.group(0) membantu agar menjadi string, tanpa itu, tetap <re.object ...xxxx >
                            if len(data) !=0:
                                listofdict.append(data)
                                data = {}               #  !!, item dalam data{} kembali di kosongkan, setiap saat kembalinya posisi dgn pattern GET|POST, data sebagai dictionary sdh berisi dengan 13 pasang key:value
                                if limit == len(listofdict):
                                    break
                                    
                            data["RequestLine"]= x.group(0)
                            x1 = x.group(0).split(" ")
                            data["Method"]= x1[0]
                            x2 = x1[1].split("?")
                            data["Path"]= x2[0]          # !!, data["Path"] sebagai key,  x2[0]  sebagai value dalam dict
                            if len(x2) > 1:             # !!, after split berdasar ? , .....path  sbg data ke 1, .....arguments sbg data ke 2
                                data["Arguments"]=x2[1]
                        else:
                            temp = x.group(0).split(": ")
                            data[temp[0]] = temp[1]
                #                data.append(x.group(0))
            if limit == len(listofdict):
                break
        
        if data==None:             #3
            listofdict.append(data)
                
        for item in listofdict:    #4
            inpt.append([
                len(item["RequestLine"]),
                len(item["Method"]),
                len(item["Path"]),
                len(item.setdefault("Arguments","")),  # !!,  .setdefault( ... , ... ), berarti 
                len(item["Host"]),
                len(item["User-Agent"]),
                len(item["Accept"]),
                len(item["Referer"]),
                len(item["Accept-Encoding"]),
                len(item["Accept-Language"]),
                len(item["Cookie"]),
                len(item["Content-Length"]),
                len(item["Content-Type"]),
                countofDgt(item["Path"]),
                countofLtr(item["Path"]),
                countofSpchar(item["Path"]),
                countofDgt(item.setdefault("Arguments","")),
                countofLtr(item.setdefault("Arguments","")),
                countofSpchar(item.setdefault("Arguments","")),
                ])
            label.append([value])
            
        listofdict = []  #5

def writelog(filename):
    with open(filename,'w', newline='') as ofile:
            writematchincsv= csv.writer(ofile, delimiter=',')
            writematchincsv.writerow(["lengthRequestLine","lengthMethodGETorPOST","lengthPath","lengthArguments","lengthHost","lengthUserAgent","lengthAccept","lengthReferer","lengthAcceptEncoding","lengthAcceptLanguage","lengthCookie","lengthContentLength","lengthContentType","lengthofDgtinPath","lengthofLtrinPath","lengthofSpcharinPath","lengthofDgtinArguments","lengthofLtrinArguments","lengthofSpcharinArguments", "Label"])
            for i in range(len(inpt)):
                writematchincsv.writerow(inpt[i]+label[i])
            #                if x == inpt[76]:   #jika ingin data di tulis ke csv smpai habis, comment baris ini, dan baris break
            #                    break            
readLog('modsec_auditmalicious.log',1, 100)
readLog('modsec_auditnormal100.log',0, 100)
writelog('Book6.csv')
