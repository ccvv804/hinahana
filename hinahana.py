# -*- coding: utf-8 -*-
import sys
import os
import io
import re
import shutil

def hinahana(r):
    nulldir = False
    nowdir = os.getcwd()
    filename = os.path.splitext(os.path.basename(r))[0]
    f=open(r,"rb")
    f.seek(0)
    nametest = f.read(4)
    if nametest != b'\x48\x41\x4E\x41':    
        print('File magic number NG')
        return None 
    elif nametest == b'\x48\x41\x4E\x41':  
        print('File magic number OK')
    else :
        print('Unknown NG')
        return None 
    try:
        os.mkdir(filename)
    except FileExistsError:
        print('warning! ' + filename + ' folder already exists')  
    os.chdir(filename)
    newdir = os.getcwd()
    
    f.seek(8)
    filenumbertest=f.read(4)
    filesizetest=f.read(4)
    filenumber=int.from_bytes(filenumbertest, byteorder='little')
    filesize=int.from_bytes(filesizetest, byteorder='little')
    filenumbercounter = filenumber
    while filenumbercounter > 0:
        f.seek(16+48*(filenumber-filenumbercounter))
        exfileinfo=f.read(48)
        exfilename = re.sub(b'\x00', b'', exfileinfo[0:14]).decode('ascii')
        exfiledisk = exfileinfo[14:16].decode('ascii')
        if exfiledisk != 'c:' :
            print(exfiledisk)
            print("Sorry I didn't make this feature.")
            print("Please contact the developer.")
            return None
        exfileaddress = re.sub(b'\x00', b'', exfileinfo[16:36]).decode('ascii')[1:-1]     
        exfilesize = int.from_bytes(exfileinfo[36:40], byteorder='little')
        exfilebinaddress = int.from_bytes(exfileinfo[40:44], byteorder='little')
        exfileunknowninfo = exfileinfo[44:48]
        if not exfileaddress == '' :
            try:
                os.mkdir(exfileaddress)
            except FileExistsError:
                pass 
            except FileNotFoundError:
                loopaddress = exfileaddress
                frontloopaddress = ''
                while loopaddress.find('\\') != -1:
                    try:
                        os.mkdir(frontloopaddress+loopaddress[0:loopaddress.find('\\')])
                    except FileExistsError:
                        pass    
                    frontloopaddress = frontloopaddress + loopaddress[0:loopaddress.find('\\')] + '\\'
                    loopaddress = loopaddress[loopaddress.find('\\')+1:] 
                os.mkdir(exfileaddress)
        else :
            nulldir = True
        if nulldir :
            nulldir = False
        else :   
            os.chdir(exfileaddress)  
        f.seek(exfilebinaddress)
        exfiledata=f.read(exfilesize) 
        if exfilename.find('.bin') != -1 and exfiledata[0:4] == b'\x48\x41\x4E\x41' or exfilename.find('.BIN') != -1 and exfiledata[0:4] == b'\x48\x41\x4E\x41':
            okdir = os.getcwd()
            os.chdir(nowdir)
            returnname = hinahanamini(exfiledata, exfilename, newdir, okdir)
            os.chdir(okdir)
        elif exfilename.find('.KBN') != -1 or exfilename.find('.kbn') != -1:
            xf=io.BytesIO(exfiledata)
            xf.seek(16) 
            xn1=xf.read(16) 
            xn=xn1.split(b'\0',1)[0] 
            xm=xn.decode('ascii') 
            xz=open(xm,'bw') 
            xf.seek(144)
            xdata=xf.read() 
            xz.write(xdata) 
            xz.close()
        else :
            z=open(exfilename,'bw')
            z.write(exfiledata)
            z.close
        os.chdir(newdir)     
        filenumbercounter = filenumbercounter-1    
    os.chdir(nowdir)    

def hinahanamini(data, name, nowdir, tellme):
    nulldir = False
    filename = os.path.splitext(name)[0]
    f=io.BytesIO(data)
    f.seek(0)
    nametest = f.read(4)
    if nametest != b'\x48\x41\x4E\x41':    
        print(filename)
        print('File magic number NG')
        return None 
    elif nametest == b'\x48\x41\x4E\x41':  
        print('File magic number OK')
    else :
        print('Unknown NG')
        return None  
    os.chdir(nowdir)
    newdir = os.getcwd()
    
    f.seek(8)
    filenumbertest=f.read(4)
    filesizetest=f.read(4)
    filenumber=int.from_bytes(filenumbertest, byteorder='little')
    filesize=int.from_bytes(filesizetest, byteorder='little')
    filenumbercounter = filenumber
    while filenumbercounter > 0:
        f.seek(16+48*(filenumber-filenumbercounter))
        exfileinfo=f.read(48)
        exfilename = re.sub(b'\x00', b'', exfileinfo[0:14]).decode('ascii')
        exfiledisk = exfileinfo[14:16].decode('ascii')
        if exfiledisk != 'c:' :
            print(exfiledisk)
            print("Sorry I didn't make this feature.")
            print("Please contact the developer.")
            return None
        exfileaddress = re.sub(b'\x00', b'', exfileinfo[16:36]).decode('ascii')[1:-1]     
        exfilesize = int.from_bytes(exfileinfo[36:40], byteorder='little')
        exfilebinaddress = int.from_bytes(exfileinfo[40:44], byteorder='little')
        exfileunknowninfo = exfileinfo[44:48]
        if not exfileaddress == '' :
            try:
                os.mkdir(exfileaddress)
            except FileExistsError:
                pass 
            except FileNotFoundError:
                loopaddress = exfileaddress
                frontloopaddress = ''
                while loopaddress.find('\\') != -1:
                    try:
                        os.mkdir(frontloopaddress+loopaddress[0:loopaddress.find('\\')])
                    except FileExistsError:
                        pass    
                    frontloopaddress = frontloopaddress + loopaddress[0:loopaddress.find('\\')] + '\\'
                    loopaddress = loopaddress[loopaddress.find('\\')+1:] 
                try:
                    os.mkdir(exfileaddress)
                except FileExistsError:
                        pass    
        else :
            nulldir = True
        if nulldir :
            nulldir = False
        else :   
            os.chdir(exfileaddress) 
        f.seek(exfilebinaddress)
        exfiledata=f.read(exfilesize)
        '''
        if exfilename.find('.bin') != -1 or exfilename.find('.BIN') != -1:
            okdir = os.getcwd()
            os.chdir(nowdir)
            hinahanamini(exfiledata, exfilename, nowdir, okdir)
            os.chdir(okdir)
        '''    
        if exfilename.find('.KBN') != -1 or exfilename.find('.kbn') != -1:
            xf=io.BytesIO(exfiledata)
            xf.seek(16) 
            xn1=xf.read(16) 
            xn=xn1.split(b'\0',1)[0] 
            xm=xn.decode('ascii') 
            xz=open(xm,'bw') 
            xf.seek(144)
            xdata=xf.read() 
            xz.write(xdata) 
            xz.close()
        else :
            z=open(exfilename,'bw')
            z.write(exfiledata)
            z.close
        os.chdir(newdir)     
        filenumbercounter = filenumbercounter-1     

try : 
    hina = sys.argv[1]
except IndexError:
    print('No file specified')
    exit()
hinahana(hina)