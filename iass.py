#!/usr/bin/env python3

import os
import re
from glob import glob
import random
import string
import platform
from time import sleep
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tf
from tkinter import filedialog as fd
from functools import partial
from progressbar import *
from utils import imessage,nmessage,change_workdir,imgconvert,run_as_child,get_settings,run_as_thread,get_value
from rename import rename_files
from shutil import copy,move,rmtree
from ttkthemes import ThemedTk,ThemedStyle

iass_settings = get_settings()

debug = False
dlayout = {"workdir_entry_width": [67, 69],
        "archivelist_entry_width": [60, 61],
        "pattern_entry_width": [40, 41],
        "replacement_entry_width": [40, 41],
        "imgconvert_entry_width": [60, 61]
        }

#iassfont = 'Courier'
iassfont = 'Arial'
iassfontsize = 9
iassfontstyle = 'normal'

if platform.system() == 'Windows':
    # frames
    workdir_frame_padx = 3
    workdir_frame_pady = 3
    imgextractor_frame_padx = 3
    imgextractor_frame_pady = 3
    rename_frame_padx = 3
    rename_frame_pady = 3
    imgconvert_frame_padx = 3
    imgconvert_frame_pady = 3

    workdir_entry_padx = 0
    select_dir_button_padx = 0
    filetype_checkbuttons_padx = 0
    archivelist_label_padx = 0
    archivelist_entry_padx = 0
    extractrename_button_padx = 0
    extract_button_padx = 0
    fileprefix_label_padx = 0
    pattern_label_padx = 1
    pattern_entry_padx = 0
    replacement_label_padx = 1
    replacement_entry_padx = 0
    rename_button_padx = 0
    imgconvert_label_padx = 0
    imgconvert_entry_padx = 0
    imgconvert_button_padx = 0
    quit_button_padx = 0
    lsystem = 1
else:
    # frames
    workdir_frame_padx = 5
    workdir_frame_pady = 5
    imgextractor_frame_padx = 5
    imgextractor_frame_pady = 5
    rename_frame_padx = 5
    rename_frame_pady = 5
    imgconvert_frame_padx = 5
    imgconvert_frame_pady = 5
    workdir_entry_padx = 2
    select_dir_button_padx = 0
    filetype_checkbuttons_padx = 0
    archivelist_label_padx = 0
    archivelist_entry_padx = 0
    extractrename_button_padx = 0
    extract_button_padx = 0
    fileprefix_label_padx = 0
    pattern_label_padx = 3
    pattern_entry_padx = 0
    replacement_label_padx = 3
    replacement_entry_padx = 0
    rename_button_padx = 0
    imgconvert_label_padx = 0
    imgconvert_entry_padx = 0
    imgconvert_button_padx = 0
    quit_button_padx = 0
    lsystem = 0

def extract(wd, archivefiles, rename=False, fromxl=None, fromppt=None, frompdf=None):
    wd = get_value(wd)
    archivefiles = get_value(archivefiles)
    fromxl = get_value(fromxl)
    fromppt = get_value(fromppt)
    frompdf = get_value(frompdf)
    if not change_workdir(wd):
        return False
    if not fromxl:
        archivefiles = re.sub("\*.xlsx,*", "", archivefiles, flags=re.IGNORECASE)
    if not fromppt:
        archivefiles = re.sub("\*.pptx,*", "", archivefiles, flags=re.IGNORECASE)
    if not frompdf:
        archivefiles = re.sub("\*.pdf,*", "", archivefiles, flags=re.IGNORECASE)
    fpatterns = archivefiles.split(',')
    files = []
    for fpt in fpatterns:
        files.extend(glob(fpt))
    for file in files:
        if rename == True:
            if platform.system() == 'Windows':
                p = subprocess.Popen(["python", iass_settings.clicmd, "-u", file])
            else:
                p = subprocess.Popen([iass_settings.clicmd, "-u", file])
            #p = subprocess.Popen([iass_settings.clicmd, "-u", file], stdout= subprocess.PIEP, stdin =  subprocess.PIPE, stderr = subprocess.PIPE)
        else:
            if platform.system() == 'Windows':
                p = subprocess.Popen(["python", iass_settings.clicmd, file])
            else:
                p = subprocess.Popen([iass_settings.clicmd, file])

            #p = subprocess.Popen([iass_settings.clicmd, file], stdout= subprocess.PIPE, stdin =  subprocess.PIPE, stderr = subprocess.PIPE)


fields = {'pattern': '文件名串',
        'replacement': '新文件名',
        'imgext': '图像转换',
        'archivefiles': '文件列表',
        'directory': '工作目录'}

def askdirectory_on_button(var):
    directory = fd.askdirectory()
    if directory != () and directory != "":
        var.set(directory)

    return var

#iassroot = tk.Tk()
iassroot = ThemedTk(theme="breeze")
#style = ThemedStyle(iassroot)
#style.set_theme("plastik")
iassroot.resizable(False, False)
#if "nt" == os.name:
#    iassroot.wm_iconbitmap(bitmap = "./iass.ico")
#    iassroot.iconbitmap("./iass.ico")
#else:
#    iassroot.wm_iconbitmap(bitmap = "@./iass.xbm")
#    iassroot.iconbitmap("@./iass.xbm")
# https://stackoverflow.com/questions/11176638/tkinter-tclerror-error-reading-bitmap-file

iassroot.title("艾辟谷")
iassroot['padx'] = 6
iassroot['pady'] = 6
#iassroot.geometry("600x420")

s = ttk.Style()
#s.theme_use('alt')

s.configure('.', font=(iassfont, iassfontsize, iassfontstyle))
s.configure('TLabelframe.Label', foreground ='grey')
#s.configure('TLabelframe', font=(iassfont, iassfontsize, iassfontstyle))
#s.configure('TLabelframe.Label', background='blue')

# 工作目录
workdir_frame = ttk.LabelFrame(iassroot, text="工作目录", relief=tk.RIDGE)
workdir_frame.grid(row=1, column=0, columnspan=3, sticky=tk.E + tk.W + tk.N + tk.S, padx=workdir_frame_padx, pady=workdir_frame_pady)
workdir = tk.StringVar(workdir_frame, value=iass_settings.workdir)
workdir_entry = ttk.Entry(workdir_frame, textvariable=workdir, width=dlayout["workdir_entry_width"][lsystem])
workdir_entry.grid(row=1, column=0, columnspan=3, sticky=tk.E + tk.W, padx=workdir_entry_padx)
#https://stackoverflow.com/questions/16224368/tkinter-button-commands-with-lambda-in-python
select_dir_button = ttk.Button(workdir_frame, text="选择", command=lambda:askdirectory_on_button(workdir))
#  用partial的解决方案
#select_dir_button = ttk.Button(workdir_frame, text="选择", command=patrial(askdirectory_on_button, workdir))
select_dir_button.grid(row=1, column=4, sticky=tk.E + tk.W, padx=select_dir_button_padx)

#filepatterns = "*.xlsx,*.pdf,*.pptx"
#图片提取
fromxlfile = tk.BooleanVar(value=True)
frompptfile = tk.BooleanVar(value=True)
frompdffile = tk.BooleanVar(value=True)
imgextractor_frame = ttk.LabelFrame(iassroot, text="图片提取", relief=tk.RIDGE)
imgextractor_frame.grid(row=2, column=0, columnspan=3, sticky=tk.E + tk.W + tk.N + tk.S, padx=imgextractor_frame_padx, pady=imgextractor_frame_pady)
filetype_checkbuttons = ttk.Label(imgextractor_frame, text="文件类型")
filetype_checkbuttons.grid(row=1, rowspan=3, sticky=tk.W + tk.E, padx=filetype_checkbuttons_padx)
xl_checkbutton = ttk.Checkbutton(imgextractor_frame, text="XLSX", variable=fromxlfile, width=6)
xl_checkbutton.grid(row=1, column=1, sticky= tk.W)
ppt_checkbutton = ttk.Checkbutton(imgextractor_frame, text="PPTX", variable=frompptfile, width=6)
ppt_checkbutton.grid(row=2, column=1, sticky=tk.W)
pdf_checkbutton = ttk.Checkbutton(imgextractor_frame, text="PDF", variable=frompdffile, width=6)
pdf_checkbutton.grid(row=3, column=1, sticky=tk.W)
archivelist_label = ttk.Label(imgextractor_frame, text="文件列表")
archivelist_label.grid(row=4, column=0, padx=archivelist_label_padx)
filepattern = tk.StringVar(imgextractor_frame, value=iass_settings.filepattern)
archivelist_entry = ttk.Entry(imgextractor_frame, textvariable=filepattern, width=dlayout["archivelist_entry_width"][lsystem])
archivelist_entry.grid(row=4, column=1, columnspan=2, padx=archivelist_entry_padx)
extractrename_button = ttk.Button(imgextractor_frame, text="提取改名", command=partial(extract, workdir, filepattern, rename=True, fromxl=fromxlfile, fromppt=frompptfile, frompdf=frompdffile))
extractrename_button.grid(row=3, column=3, padx=extractrename_button_padx)
extract_button = ttk.Button(imgextractor_frame, text="文件提取", command=partial(extract, workdir, filepattern, rename=False, fromxl=fromxlfile, fromppt=frompptfile, frompdf=frompdffile))
extract_button.grid(row=4, column=3, padx=extract_button_padx)

# ========== 批量改名 ===========
rename_frame = ttk.LabelFrame(iassroot, text="批量改名", relief=tk.RIDGE)
rename_frame.grid(row=3, column=0, columnspan=3, sticky=tk.E + tk.W + tk.N + tk.S, padx=rename_frame_padx, pady=rename_frame_pady)
# radio buttons
fileprefix_label = ttk.Label(rename_frame, text="文件前缀")
fileprefix_label.grid(row=1, rowspan=3, column=0, sticky=tk.W + tk.N, padx=fileprefix_label_padx)
timeprefix = tk.IntVar(value=0)
notimeprefix = ttk.Radiobutton(rename_frame, text="没有时间", variable=timeprefix, value=0)
notimeprefix.grid(row=1, column=1, sticky=tk.W)
ctimeprefix = ttk.Radiobutton(rename_frame, text="创建时间", variable=timeprefix, value=1)
ctimeprefix.grid(row=2, column=1, sticky=tk.W)
mtimeprefix = ttk.Radiobutton(rename_frame, text="修改时间", variable=timeprefix, value=2)
mtimeprefix.grid(row=3, column=1, sticky=tk.W)
# 正则表达式匹配 

pattern_label = ttk.Label(rename_frame, text="正则匹配", )
pattern_label.grid(row=1, column=3, padx=pattern_label_padx)
pattern = tk.StringVar(rename_frame)
pattern_entry = ttk.Entry(rename_frame, textvariable=pattern, width=dlayout["pattern_entry_width"][lsystem])
pattern_entry.grid(row=1, column=4, columnspan=2, padx=pattern_entry_padx)
replacement_label = ttk.Label(rename_frame, text="新文件名", )
replacement_label.grid(row=2, column=3, padx=replacement_label_padx)
replacement = tk.StringVar(rename_frame)
replacement_entry = ttk.Entry(rename_frame, textvariable=replacement, width=dlayout["replacement_entry_width"][lsystem])
replacement_entry.grid(row=2, column=4, columnspan=2, padx=replacement_entry_padx)
rename_button = ttk.Button(rename_frame, text="批量改名", command=partial(rename_files, workdir, pattern, replacement, timeprefix))
rename_button.grid(row=3, column=8, padx=rename_button_padx)


#图片转换
imgconvert_frame = ttk.LabelFrame(iassroot, text="图片转换", relief=tk.RIDGE)
imgconvert_frame.grid(row=4, column=0, columnspan=3, sticky=tk.E + tk.W + tk.N + tk.S, padx=imgconvert_frame_padx, pady=imgconvert_frame_pady)
xprogress = Iprogress(imgconvert_frame)

imgconvert_label = ttk.Label(imgconvert_frame, text="格式转换")
imgconvert_label.grid(row=1, column=0, padx=imgconvert_label_padx)
imgpattern = tk.StringVar(imgextractor_frame, value=iass_settings.imgpattern)
imgconvert_entry = ttk.Entry(imgconvert_frame, textvariable=imgpattern, width=dlayout["imgconvert_entry_width"][lsystem])
imgconvert_entry.grid(row=1, column=1, columnspan=2, padx=imgconvert_entry_padx)
imgconvert_button = ttk.Button(imgconvert_frame, text="开始转换", command=partial(run_as_thread, imgconvert, (workdir, imgpattern, xprogress)))
imgconvert_button.grid(row=1, column=8, padx=imgconvert_button_padx)
xprogress.enable_progressbar(2)

quit_button = ttk.Button(imgconvert_frame, text="退出程序", command=iassroot.destroy)
quit_button.grid(row=2, column=8, padx=quit_button_padx)

for widget in iassroot.winfo_children():
    for cwidget in widget.winfo_children():
        if isinstance(cwidget, tk.Label):
            cwidget['font'] = (iassfont, iassfontsize)
        if isinstance(cwidget, tk.Entry):
            cwidget['font'] = (iassfont, iassfontsize)
        if isinstance(cwidget, tk.Button):
            cwidget['font'] = (iassfont, iassfontsize)
        if isinstance(cwidget, tk.Checkbutton):
            cwidget['font'] = (iassfont, iassfontsize)
        if isinstance(cwidget, tk.Radiobutton):
            cwidget['font'] = (iassfont, iassfontsize)
# main loop
iassroot.mainloop()
