#!/usr/bin/env python3

import os
import re
from glob import glob
from utils import get_random_string,get_random_digits,get_ftime,change_workdir,get_img_ctime,get_img_mtime,get_value
from shutil import copy,move,rmtree

def rename_files(wd, pts, rps, timeprefixtype):
    wd = get_value(wd)
    pts = get_value(pts)
    rps = get_value(rps)
    timeprefixtype = get_value(timeprefixtype)
    if not change_workdir(wd):
        return False
    hassuffix = False
    hasprefix = False
    fnprefix = ""
    mrps = ""
    if '|' in rps:
        rps = rps.split('|')
        fnprefix = rps[0]
        if fnprefix != "":
            hasprefix = True
        try:
            fnsuffix = rps[2]
            hassuffix = True
        except IndexError:
            pass
        mrps = rps[1]

    files = glob("*.*")

    blacklist=['iass,py', 'iass.pyw']
    for ifile in blacklist:
        try:
            files.remove(ifile)
        except ValueError:
            pass

    for file in files:
        if  os.path.isdir(file):
            continue
        tprefix = ""
        fname, fext = os.path.splitext(file)
        if timeprefixtype == 1:
            tprefix = get_img_ctime(file)
            if tprefix == "" or tprefix == "0000:00:00 00:00:00":
                tprefix = get_ftime(file, "ctime")
            tprefix = tprefix + "-"
        elif timeprefixtype == 2:
            tprefix = get_img_mtime(file)
            if tprefix == "" or tprefix == "0000:00:00 00:00:00":
                tprefix = get_ftime(file, "mtime")
            tprefix = tprefix + "-"

        if hasprefix == True:
            nfname = re.sub(pts, mrps, fname)
            fnprefix = tprefix + rps[0] + "__"
        else:
            nfname = re.sub(pts, rps, fname)
            fnprefix = tprefix

        if fnprefix == None:
            fnprefix = ""

        if hassuffix == True:
            suffix = fnsuffix
            if m := re.search("@+", suffix):
                suffix = re.sub("@+", get_random_string(m.end() - m.start()), suffix)
            if m := re.search("#+", suffix):
                suffix = re.sub("#+", get_random_digits(m.end() - m.start()), suffix)
            suffix = "__" + suffix
            rep_file = fnprefix + nfname + suffix + fext
        else:
            rep_file = fnprefix + nfname + fext

        if file != rep_file:
            print(file + " -> " +  rep_file);
            move(file, rep_file)
