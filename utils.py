#!/usr/bin/env python3
import os
import re
import random
import string
import time
import subprocess
import tkinter as tk
from glob import glob
from tkinter import messagebox
import tkinter.font as tf
from PIL import Image
from datetime import datetime
from multiprocessing import Process
from settings import Settings
import platform
import threading


settings = Settings()

def imessage(title, message):
       tk.messagebox.showwarning(title, message)

def nmessage(title, message):
       tk.messagebox.showinfo(title, message)

def change_workdir(wd):
    wd = get_value(wd)
    try:
        os.chdir(wd)
        return True
    except FileNotFoundError:
        imessage("FileNotFoundError", wd + ": 目录不存在")
        return False

def get_installdir():
    installdir = os.path.split(__file__)[0]
    return installdir

def get_settings():
    return Settings()

def get_random_string(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))

def get_random_digits(length):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))

def imgconvert(wd, imgtypes, xprogressbar):
    wd = get_value(wd)
    imgtypes  = get_value(imgtypes)
    types = imgtypes.split('|')
    try:
        ttype = types[1]
    except IndexError:
        return
    stypes = []
    glob("*.*")
    stypes = types[0].split(',')
    if not change_workdir(wd):
        return False

    try:
        os.mkdir("output")
    except FileExistsError:
        pass
    files = []
    for stype in stypes:
        files.extend(glob("*." + stype))

    if not files:
        return
    xprogressbar.reset_progressbar()
    i = 0
    for file in files:
        loops = len(files)
        xprogressbar.update_progressbar(loops, i)
        i += 1
        fname, fext = os.path.splitext(file)
        print(file + " -> " + "output/" + fname + "." + ttype)
        if platform.system() == 'Windows':
            p = subprocess.run([settings.convert, file, "output/" + fname + "." + ttype], capture_output = False, shell=True)
        else:
            p = subprocess.run([settings.convert, file, "output/" + fname + "." + ttype])

def get_value(var):
    try:
        var = var.get()
    except AttributeError:
        pass
    return var

def get_ftime(fname, timetype):
    if timetype == "ctime":
        ftime = time.localtime(os.stat(fname).st_ctime)
    elif timetype == "mtime":
        ftime = time.localtime(os.stat(fname).st_mtime)
    return str(ftime.tm_year) + '{:02}'.format(int(ftime.tm_mon)) + '{:02}'.format(int(ftime.tm_mday))

def has_exif_info(file):
    if re.search("\.jpg$|\.png$", file, re.IGNORECASE):
        return True
    else:
        return False
 
def get_media_ctime(fname):
    if platform.system() == 'Windows':
        bctime = subprocess.run([settings.exiftool, '-d', '%Y%m%d', '-CreateDate', '-s', '-s', '-s', fname], capture_output=True, shell=True).stdout
    else:
        bctime = subprocess.run([settings.exiftool, '-d', '%Y%m%d', '-CreateDate', '-s', '-s', '-s', fname], capture_output=True).stdout
    return bctime.decode('ascii').rstrip()

def get_media_mtime(fname):
    if platform.system() == 'Windows':
        bmtime = subprocess.run([settings.exiftool, '-d', '%Y%m%d', '-ModifyDate', '-s', '-s', '-s', fname], capture_output=True, shell=True).stdout
    else:
        bmtime = subprocess.run([settings.exiftool, '-d', '%Y%m%d', '-ModifyDate', '-s', '-s', '-s', fname], capture_output=True).stdout
    return bmtime.decode('ascii').rstrip()

def get_img_mtime(fname):
    "returns the image date from image (if available)\nfrom Orthallelous"
    std_fmt = '%Y:%m:%d %H:%M:%S.%f'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
    try:
        exif = Image.open(fname).getexif()
    except Image.UnidentifiedImageError:
        return get_media_mtime(fname)

    # 有些照片的时间末尾会有”上午“或者”下午“等其他字符，从19位开始截断 
    dat = exif.get(306)
    if dat == None:
        return get_media_mtime(fname)

    if len(dat) > 19:
        dat = dat[0:19]
    sub = exif.get(37520)
    if sub == None:
        sub = 0

    if dat == "0000:00:00 00:00:00":
        return ""
    full = '{}.{}'.format(dat, sub)
    t = datetime.strptime(full, std_fmt)
    #T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
    return str(t.year) + '{:02}'.format(int(t.month)) + '{:02}'.format(int(t.day))

def get_img_ctime(fname):
    "returns the image date from image (if available)\nfrom Orthallelous"
    std_fmt = '%Y:%m:%d %H:%M:%S.%f'
    # https://exiv2.org/tags.html *** HEIF doesn't work yet ***
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeDigitized)
            (306, 37520), ]  # (DateTime, SubsecTime)
    try:
        exif = Image.open(fname).getexif()
    except Image.UnidentifiedImageError:
        return get_media_ctime(fname)

    # 有些照片的时间末尾会有”上午“或者”下午“等其他字符，从19位开始截断 
    dat = exif.get(36867)
    if dat == None:
        return get_media_ctime(fname)
        #return get_time(fname, 'mtime')

    if len(dat) > 19:
        dat = dat[0:19]
    sub = exif.get(37521)
    if sub == None:
        sub = 0

    if dat == "0000:00:00 00:00:00":
        return ""
    full = '{}.{}'.format(dat, sub)
    t = datetime.strptime(full, std_fmt)
   #T = time.mktime(time.strptime(dat, '%Y:%m:%d %H:%M:%S')) + float('0.%s' % sub)
    return str(t.year) + '{:02}'.format(int(t.month)) + '{:02}'.format(int(t.day))

def run_as_child(run_proc, parmas):
    p = Process(target=run_proc, args=parmas)
    p.start()

def run_as_thread(run_proc, args):
    t = threading.Thread(target=run_proc, args=args) 
    t.setDaemon(True) 
    t.start()
