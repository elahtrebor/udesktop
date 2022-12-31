import network
import socket
import time
import os
import re

def urldecode(str):
    dic = {"%0A":"\n","%20":" ","%21":"!","%22":'"',"%23":"#","%24":"$","%26":"&","%27":"'","%28":"(","%29":")","%2A":"*","%2B":"+","%2C":",","%2F":"/","%3A":":","%3B":";","%3D":"=","%3F":"?","%40":"@","%5B":"[","%5D":"]","%5C":"\\","%7B":"{","%7D":"}"}
    for k,v in dic.items(): str=str.replace(k,v)
    return str


addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        helpstr = """command are:
                 ls, cat, pwd, ifconfig
                 cd, uname, df, mkdir
                 rmdir, stat, light
                """
        request = str(request)

        if request.find('cmd=ls') != -1:
         try:
           if re.search('cmd=ls%20', request):
            fname = re.search('cmd=ls%20(.*?) HTTP', request).group(1)
           else:
            fname = ""
           output = os.listdir(fname)
           response = "\n".join(output)
         except:
            response = "Coudn't list directory\n"
        elif request.find('cmd=stat') != -1:
           try:
            fname = re.search('cmd=stat%20(.*?) HTTP', request).group(1)
            output = os.stat(fname)
            response = str(output[0]) + " " + str(output[6]) + " " + str(output[9]) + "\n"
           except:
             response = "Couldn't stat\n"
        elif request.find('cmd=help') != -1:
           response = helpstr
        elif request.find('cmd=df') != -1:
            try:
              total = float(os.statvfs('/')[2]) * float(os.statvfs('/')[0])
              used = float(os.statvfs('/')[3]) * float(os.statvfs('/')[0])
              free = total - used
              response = "Total: " + str(total) + " Free: " + str(free) + "\n"
            except:
              response = "Couldn't get disk free\n"
        elif request.find('cmd=uname') != -1:
          try:
           response = "\n".join(os.uname())
          except:
           response = "Couldn't get uname info\n"
        elif request.find('cmd=ifconfig') != -1:
           try:
             wlan = network.WLAN(network.STA_IF)
             status = wlan.ifconfig()
             response = ("\nIP........... " +
             status[0] +
             "\nNETMASK......." +
             status[1] + "\n" +
             "GATEWAY......." +
             status[2])
           except:
             response = "Couldn't get interface or check syntax.\n"
        elif request.find("cmd=pwd") != -1:
          try:
           response = os.getcwd()
          except:
            response = "Couln't get current directory\n"
        elif request.find("cmd=cd") != -1:
           try:
            dir = re.search('cmd=cd%20(.*?) HTTP', request).group(1)
            os.chdir(dir)
            response = dir
           except:
            response = "Couldn't cd\n"
        elif request.find("cmd=rm%20") != -1:
           try:
            fname = re.search('cmd=rm%20(.*?) HTTP', request).group(1)
            os.unlink(fname)
            response = "Removed file: " + fname
           except:
            response = "Could't remove file\n"
        elif request.find("cmd=mkdir%20") != -1:
           try:
            dir = re.search('cmd=mkdir%20(.*?) HTTP', request).group(1)
            os.mkdir(dir)
            response = "Created dir: " + dir
           except:
            response = "Couldn't make directory\n"
        elif request.find("cmd=rmdir%20") != -1:
           try:
            dir = re.search('cmd=rmdir%20(.*?) HTTP', request).group(1)
            os.rmdir(dir)
            response = "Removed dir: " + dir
           except:
            response = "Couldn't remove directory\n"
        elif request.find("cmd=echo%20") != -1:
           try:
            str1 = re.search('cmd=echo%20(.*?) HTTP', request).group(1)
            str1 = str1.replace("%20"," ")  
            response = str1
           except:
            response = "Couldn't echo\n"
        elif request.find("cmd=cat") != -1:
          try:
           fname = re.search('cmd=cat%20(.*?) HTTP', request).group(1)
           file1 = open(fname, "r")
           response = file1.read()
           file1.close()
          except:
            response = "Couldn't read file\n"
        elif request.find("cmd=nslookup") != -1:
          try:
           hname=re.search('cmd=nslookup%20(.*?) HTTP',request).group(1)
           response = socket.getaddrinfo(hname,80)[0][-1][0]
          except:
            response = "Couldn't lookup name\n"
        elif request.find("fileobject=getDirectory") != -1:
         try:
           response = ""
           fpath = re.search('filepath=(.*?) ', request).group(1)
           dir = os.listdir(fpath)
           #print(dir)
           if not re.match('[a-z]',fpath):
             sep = "/"
           else:
              sep = ""
           for i in dir:
             #print("Statting: " + fpath + sep + i + "\n")
             fdetails = os.stat(fpath + sep + i)
             if fdetails[0] == 32768:
              response += (i + ",file," + str(fdetails[6]) +"\n")
             else:
              response += (i + ",folder," + str(fdetails[6]) + "\n")
         except:
               response = "\n"
        elif request.find("fileobject=") != -1:
          try:
           fname = re.search('fileobject=(.*?)&filecontents=', request).group(1)
           fcontents = re.search('filecontents=(.*?) HTTP', request).group(1)
           fcontents = urldecode(fcontents) 
           file1 = open(fname, "w")
           file1.write(fcontents) 
           file1.close()
           response = "File written."
          except:
           response = "Couldn't get file object\n"
        elif request.find("getFile=") != -1:
          try:
           fname = re.search('getFile=(.*?) HTTP', request).group(1)
           file1 = open(fname, "r")
           response = file1.read()
           file1.close()
          except:
              response = "Couldn't get file\n"
        elif request.find("cmd=./") != -1:
           bin =re.search('cmd=./(.*?) HTTP',request).group(1)
           bin = bin.replace("/", ".")
           bin = bin.replace(".py", "")
           script = __import__(bin)
           try:   
             response = script.main()
           except:
             response = "Error: Check Syntax\n"
        else:
           response = "COMMAND NOT FOUND"

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\nAccess-Control-Allow-Origin: *\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')


