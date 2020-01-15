#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os, filecmp
import subprocess
import shutil
import datetime
import hashlib
import tkinter as Tkinter
import threading
import zipfile

##без коментариев
def zip_files_dirs(dir_dst):
    MMax=0
    k=0
    for root, dirs, files in os.walk(dir_dst):
        for name in files:
            MMax=MMax+1
    try:
        out_label['text']=("обнаружено"+str(MMax))##
    except BaseException:
        c=0

    for direc in os.listdir(dir_dst):
        direc_src=os.path.join(dir_dst,direc)
        for Yd in os.listdir(direc_src):
            Y_src=os.path.join(direc_src,Yd)
            try:
                k=k+1
                out_label['text']=("обработано "+str(k-1)+"/"+str(MMax)+"\n"+Y_src)##
            except BaseException:
                c=0
            ## в случае встречи рар без этого ифа создает пустые *.rar.zip
##            if Y_src.endswith('.rar') or Y_src.endswith('.RAR'):##вообшето можно можно довить обработку и рара
##                continue
##          сотрит(XD sotrit) зип ли файл если нет создает *.зип если да тогда возрашает "обьект" зипа
##            if Y_src.endswith('.zip'):
            if zipfile.is_zipfile(Y_src):
                Yzip=zipfile.ZipFile(str(Y_src),"a")
            else:
                Yzip=zipfile.ZipFile(str(Y_src+'.zip'),"a")
            for root, dirs, files in os.walk(Y_src):
                    for name in files:
                        if stop.is_set():##ЕСЛИ НАЖАТА КНОПКА ОТМЕНА
                            stop.clear()
                            log=open(logFiles,'a')
                            log.write(" stop zip ")
                            log.close()
                            Yzip.close()
                            sys.exit()
                        p=os.path.join(root,name)##не выкатаю зачем это
                        p=p[len(Y_src)+1:]
                        if not len(name)==len(p):
                            p=p[:-len(name)-1]+"/"+name
                        try:## ЕСЛИ ФАЙЛА НЕТ  ТО ПРИ СРАВНЕНИИИ ВЫКИНЕT ЕРРОр и запишит файл в зип
                            if Yzip.getinfo(p).file_size==os.stat(os.path.join(root,name)).st_size:
                                continue
                            else:##ЕСЛИ ФАЙЛ ЕСТЬ ТО В ТЕОРРИИ СОЗДАЕТ ЕГО КОПИИЮ
                                f_dst=0
                                p=p[:p.find('(')]+p[p.find(')'):]
                                try:
                                    i=0
                                    while True:
                                        i=i+1
                                        f_dst=p[:p.find('.')]+"("+str(i)+")"+p[p.find('.'):]
                                        Yzip.getinfo(f_dst)
                                except KeyError:
                                    p=f_dst
                                    Yzip.write(os.path.join(root,name),p, compress_type=zipfile.ZIP_DEFLATED)
                        except KeyError:
                            #print(p)
                            Yzip.write(os.path.join(root,name),p, compress_type=zipfile.ZIP_DEFLATED)
            Yzip.close()
##            ОПАСНАЯ СТРОКА ИБО УДАЛЯЕТ КАТОЛОГ
            shutil.rmtree(Y_src, ignore_errors=True)

def del_empty_dirs(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)
#                print(a, 'удалена')

def copyy(dir_src,dir_dst,zap=0):
    date=datetime.datetime.now();
    log=open(logFiles,'a')
    err=0
    k=0
    MMax=0
    Cf=0
    for root, dirs, files in os.walk(dir_src):
        for name in files:
            MMax=MMax+1
    try:
        out_label['text']=("обнаружено"+str(MMax))##
    except BaseException:
        c=0
    for direc in os.listdir(dir_src):
        direc_src=os.path.join(dir_src,direc)
#        print(direc_src)
        for root, dirs, files in os.walk(direc_src):
    #        print ("[-]"+dir_src+dir_dst+str(stop))
                for name in files:
        #            print ("[-]"+dir_src+dir_dst)
                    f_src = os.path.join(root, name)
                    temptime=datetime.datetime.fromtimestamp(os.path.getmtime(f_src))
                    if stop.is_set():
                        stop.clear()
                        temp=datetime.datetime.now()
                        log.write(""+str(temp.day)+"/"+str(temp.month)+"/"+str(temp.year)+" "+str(temp.hour)+":"+str(temp.minute)+":"+str(temp.second)+" stop "+str(k-1)+"/"+str(MMax)+"\n")   
                        log.close()
                        sys.exit()
                    try:
        #            print ("[-]"+dir_src+dir_dst)
                        k=k+1
                        out_label['text']=("обработано "+str(k-1)+"/"+str(MMax)+"\n"+f_src)##
                    except BaseException:
                        c=0
                    if temptime.year!=date.year:
                        #путь к файлу назначения
                        f_dst=dir_dst+"/"+direc+"/"+str(temptime.year)+"/"+(f_src[len(direc_src):len(root)])+"/"+name
    #                    f_dst=dir_dst+f_src[len(dir_src):len(root)]+"/"++"/"+name
                        #путь к папке назначения
                        p_dst=dir_dst+"/"+direc+"/"+str(temptime.year)+"/"+(f_src[len(direc_src):len(root)])
    #                    p_dst=dir_dst+f_src[len(dir_src):len(root)]+"/"+str(temptime.year)+"/"
                        if not os.path.exists(f_dst):
        #                    print ("[-] ", f_src)
                            temp=datetime.datetime.now()
                            log.write(""+str(temp.day)+"/"+str(temp.month)+"/"+str(temp.year)+" "+str(temp.hour)+":"+str(temp.minute)+":"+str(temp.second)+" copy "+f_src+" to "+f_dst+"\n")
                            #создание директории если отсутсвует
                            if not os.path.exists(p_dst):
                                os.makedirs(p_dst)
                            shutil.copy2(f_src,f_dst)
                            Cf=Cf+1
        #                    os.system("xcopy "+f_src+" "+p_dst+" /z /y /v /i")
        #                    log.write(str(subprocess.check_output("xcopy \""+f_src+"\" \""+p_dst+"\" /z /y /v")))
                        else:
                            if zap==0 and not filecmp.cmp(f_src, f_dst) and not compare_h(f_src)==compare_h(f_dst):
                                i=0
                                name=name[:name.find('(')]+name[name.find(')'):]
                                while os.path.exists(f_dst):
                                    i=i+1    
                                    f_dst=p_dst+"/"+name[:name.find('.')]+"("+str(i)+")"+name[name.find('.'):]
#                                print(f_dst)
                                shutil.copy2(f_src,f_dst)
                                Cf=Cf+1
                        while not filecmp.cmp(f_src, f_dst) and not compare_h(f_src)==compare_h(f_dst) and err<5:
                            #print ("измененый файл , перезапись ", f_src)
                            temp=datetime.datetime.now()
                            log.write(""+str(temp.day)+"/"+str(temp.month)+"/"+str(temp.year)+" "+str(temp.hour)+":"+str(temp.minute)+":"+str(temp.second)+" compare erro, rewrite "+f_src+" to "+f_dst+"\n")
        #                    log.write(str(subprocess.check_output("xcopy \""+f_src+"\" \""+p_dst+"\" /z /y /v")))
        #                    os.system("xcopy "+f_src+" "+p_dst+" /z /y /v /i")
        #                    subprocess.run(['xcopy', os.path.abspath(f_src), os.path.abspath(p_dst),'/s', '/e', '/z', '/y', '/v', '/i'],"log.log")
        
                            shutil.copy2(f_src,f_dst)
                            err=err+1
        #                    shutil.copy2(f_src,f_dst)
                        if err==5:
                            temp=datetime.datetime.now()
                            log.write(""+str(temp.day)+"/"+str(temp.month)+"/"+str(temp.year)+" "+str(temp.hour)+":"+str(temp.minute)+":"+str(temp.second)+" rewrite File: "+f_src+" failed\n")
                        else:
                            temp=datetime.datetime.now()
                            log.write(""+str(temp.day)+"/"+str(temp.month)+"/"+str(temp.year)+" "+str(temp.hour)+":"+str(temp.minute)+":"+str(temp.second)+" "+str(err)+" rewrite "+f_src+"\n")
                            os.remove(f_src)
                            log.write(" remove "+f_src+"\n")
                        err=0
    log.write("check/move/all:"+str(k)+"/"+str(Cf)+"/"+str(MMax)+".\n end")
    log.close()
    del_empty_dirs(dir_src)
    out_label['text']=("проверено/перемешено/всего:"+str(k)+"/"+str(Cf)+"/"+str(MMax)+".\nзакончено,начата архивация")
    try:
        if ZiP.get()==1:
            zip_files_dirs(dir_dst)
        message_button['state']=Tkinter.DISABLED
        otm_button['state']=Tkinter.DISABLED
        out_label['text']=("проверено/перемешено/всего:"+str(k)+"/"+str(Cf)+"/"+str(MMax)+".\nзакончено")##
    except BaseException:
        c=0

def removeOld(dir_to_search,f_type,dol):
    date=datetime.datetime.now();
    for dirpath, dirnames, filenames in os.walk(dir_to_search):
        for fIle in filenames:
            curpath = os.path.join(dirpath, fIle)
            if curpath.endswith(f_type):
                file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
                if datetime.datetime.now() - file_modified > datetime.timedelta(hours=dol*24):
                    os.remove(curpath)
#                    print("remove ",curpath)
                    temp=datetime.datetime.now()
                    log=open(logFiles,'a')
                    log.write(""+str(temp.day)+"/"+str(temp.month)+"/"+str(temp.year)+" "+str(temp.hour)+":"+str(temp.minute)+":"+str(temp.second)+" remove "+curpath+"\n")
                    log.close()

def compare_h(f_src):
    BUF_SIZE = 65536
    sha1 = hashlib.sha224()
    with open(f_src, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    f.close()
    return sha1

def start(dir_src,dir_dst,zap=0):
    copyy(dir_src,dir_dst,zap)

def checkPath():
    c=0
    try:
        if not os.path.exists(src.get()):
            message_button['state']=Tkinter.DISABLED
            out_label['text']=("путь не сушествует -откуда:\n "+src.get()+"\n")
            c=3
        if not os.path.exists(dft.get()):
            message_button['state']=Tkinter.DISABLED
            c=c+1
            out_label['text']=("путь не сушествует -куда:\n "+dft.get()+"\n")
            if c==4:
                out_label['text']=("пути НЕ сушествуют!!!: \n")
        if c==0:
            message_button['state']='normal'
            Zip_button['state']='normal'
            out_label['text']=("пути сушествуют, готов к работе\n")
    except BaseException:
        out_label['text']=("запись не верна\n(возмжно присуствуют русские символы)")
        c=4
    return c
    
def display_full_name():
    if not checkPath():
        otm_button['state']='normal'
        message_button['state']=Tkinter.DISABLED
        Zip_button['state']=Tkinter.DISABLED
        out_label['text']=("Из "+src.get()+" передвигаю в "+dft.get()+" Запуск произведен")
        dataF=open("data.txt","w")
        temp=""+src.get()+"\n"+dft.get()+"\n"+str(zap)
        dataF.write(temp)
        dataF.close()
        p2=threading.Thread(target=start,args=(src.get(),dft.get(),mode.get()))
        p2.start()
#        start(src.get(),dft.get())
        out_label['text']=("save in data.txt and run")
        removeOld(dir,".log",7)
        
def otmena():
    otm_button['state']=Tkinter.DISABLED
    stop.set()
#    message_button['state']='normal'

def UnZip_all():
    Zip_button['state']=Tkinter.DISABLED
    otm_button['state']='normal'
    check_button['state']=Tkinter.DISABLED
    try:
        if not os.path.exists(dft.get()):
            message_button['state']=Tkinter.DISABLED
            out_label['text']=("путь не сушествует -куда:\n "+dft.get()+"\n")
            otm_button['state']=Tkinter.DISABLED
            Zip_button['state']='normal'
            check_button['state']='normal'
            return 0
    except BaseException:
        out_label['text']=("запись не верна\n(возмжно присуствуют русские символы)")
        otm_button['state']=Tkinter.DISABLED
        Zip_button['state']='normal'
        check_button['state']='normal'
        return 0
    
    out_label['text']=("разархивация началась")
    Thr=threading.Thread(target=unzi,args=(dft.get(),0))
    Thr.start()
    
def unzi(dir_dft,k):
    for direc in os.listdir(dir_dft):
        direc_src=os.path.join(dir_dft,direc)
        for Yd in os.listdir(direc_src):
            Y_src=os.path.join(direc_src,Yd)
            if stop.is_set():
                stop.clear()
                otm_button['state']=Tkinter.DISABLED
                Zip_button['state']='normal'
                check_button['state']='normal'
                out_label['text']=("разархивация остановлено")
                sys.exit()
##            if Y_src.endswith('.zip'):
            if zipfile.is_zipfile(Y_src):
                Yzip=zipfile.ZipFile(str(Y_src),"a")
                Yzip.extractall(os.path.join(Y_src[:-4]))
                Yzip.close()
                try:
                    if zipfile.is_zipfile(Y_src):
##                    if Y_src.endswith('.zip'):
                        os.remove(Y_src)
                except BaseException:
                    c=0
    out_label['text']=("разархивация закончена")
    otm_button['state']=Tkinter.DISABLED
    Zip_button['state']='normal'
    check_button['state']='normal'

if __name__ == '__main__':
    os.popen('chcp').read()
    stop= threading.Event()
    dir = os.path.abspath(os.curdir)
    date=datetime.datetime.now();
    logFiles=("Log-"+str(date.day)+"."+str(date.month)+"."+str(date.year)+".log")
    if len(sys.argv)==3:##запуск скомандной строки
        src=str(sys.argv[1])
        dft=str(sys.argv[2])     
        if not os.path.exists(src):
            log=open(logFiles,'a')
            log.write(""+str(datetime.datetime.now())+" path no exist:"+src+"\n")
            log.close()
  #          print ("path no exist:"+src)
            sys.exit()
        if not os.path.exists(dft):
            log=open(logFiles,'a')
            log.write(""+str(datetime.datetime.now())+" path no exist:"+dft+"\n")
            log.close()
 #           print ("path no exist:"+dft)
            sys.exit()
            removeOld(dir,".log",0)
        date=datetime.datetime.now();
        start(src,dft)
    else:
        d_src=""
        d_dft=""
        zap=0
        try:
            removeOld(dir,".log",0)
        except BaseException:
            c=0
        #файл не сушетвует или пустой
        
        
        root = Tkinter.Tk()
        root.title("передвигаю файлы")
        root.geometry("420x300")
        
        src = Tkinter.StringVar()
        dft = Tkinter.StringVar()
        mode = Tkinter.IntVar()
        ZiP = Tkinter.IntVar()
        if not (not os.path.exists("data.txt") or os.stat("data.txt").st_size == 0):
            dataF=open("data.txt")
            temp=dataF.read().splitlines()
            try:
                src.set(str(temp[0]))
                dft.set(str(temp[1]))
                mode.set(int(temp[2]))
                ZiP.set(int(temp[3]))
            except BaseException:
                dataF.close()
            dataF.close()
        src_label = Tkinter.Label(text="откуда:")
        dft_label = Tkinter.Label(text="куда:")
        out_label = Tkinter.Label(text="")

        src_label.grid(row=0, column=0, sticky="w")
        dft_label.grid(row=1, column=0, sticky="w")
        out_label.grid(row=7, column=0, sticky="W"+"E"+"N"+"S",columnspan=8,rowspan=2)
        
        src_entry = Tkinter.Entry(textvariable=src,width=55)
        dft_entry = Tkinter.Entry(textvariable=dft,width=55)

        src_entry.grid(row=0,column=1, columnspan=2,pady=10, padx=10)
        dft_entry.grid(row=1,column=1, columnspan=2,pady=10, padx=10)

        check_mode=Tkinter.Checkbutton(text="файл перезаписывается",variable=mode).grid(row=2,column=1,columnspan=2,sticky="w")
        check_Ziip=Tkinter.Checkbutton(text="Zip",variable=ZiP).grid(row=2,column=0)
        
        check_button = Tkinter.Button(text="проверить пути", command=checkPath)
        check_button.grid(row=3,column=2, padx=5, pady=5, sticky="w")
        
        message_button = Tkinter.Button(text="начать",state=Tkinter.DISABLED, command=display_full_name)
        message_button.grid(row=5,column=0, padx=5, pady=5, sticky="W"+"E"+"N"+"S",columnspan=2)
        
        otm_button=Tkinter.Button(text="отменить",state=Tkinter.DISABLED,command=otmena)
        otm_button.grid(row=5,column=2, padx=5, pady=5,sticky="W"+"E"+"N"+"S",columnspan=2)

        Zip_button=Tkinter.Button(text="разархивировать все",command=UnZip_all)
        Zip_button.grid(row=6,column=2, padx=5, pady=5,sticky="W"+"E"+"N"+"S",columnspan=2)

        root.resizable(width=False, height=False)

        p1=threading.Thread(target=start,args=(src.get(),dft.get()))
        root.mainloop()
