#!/usr/bin/env python3.8

import os
import re
from izip import *
import subprocess
from ixml import *
from io import BytesIO, StringIO
import argparse
import xml.etree.ElementTree as ET
from tempfile import mktemp
from shutil import copy,move,rmtree
from utils import get_settings

parser = argparse.ArgumentParser(description='This program extracts pictures from Excel file(s).')
parser.add_argument('file', type=str, nargs='+', help='Path to Excel file(s)')
#parser.add_argument('-f', '--file', type=str, help='Path to Excel file(.xlsx)', required=True)
parser.add_argument('-u', '--usenamefile', help='use name file to rename images', action='store_true')
parser.add_argument('-d', '--debug', help='enable debug message', action='store_true')
args = parser.parse_args()

settings = get_settings()
xmliprefix="iass" + "_xmli_"
xmlxprefix="iass" + "_xmlx_"

def mkxmltemp(tprefix):
    return mktemp(suffix='', prefix=tprefix)

for file in args.file:
    f, ext = os.path.splitext(file)
    mtype = settings.type[ext]
    print("Extract images from " + file + "...")
    if mtype == "pdf" or mtype == "PDF":
        prefix = f + "/" + "pdf"
        try:
            os.mkdir(f)
        except FileExistsError:
            pass
        subprocess.Popen([settings.pdfcmd, "-p", "-png", file, prefix], stdout = subprocess.DEVNULL, stdin = subprocess.DEVNULL, stderr = subprocess.PIPE)
        continue

    iz = Izip(file)

    # for xl, the filexs is for generating xdic, for others, it generate idic
    xfiles = iz.getzfnlist(settings.mediatype[mtype]['imgpt'])
    for xfile in xfiles:
        count = re.search(r'[0-9]+', xfile).group()
        ix = Ixml(file)

        if mtype == "xl":
            (p, n) = os.path.split(xfile)
            filei = p + "/_rels/" + n + ".rels"
            xmlx = mkxmltemp(xmlxprefix)
            xmli = mkxmltemp(xmliprefix) 
            try:
                iz.writefp(xfile, xmlx)
            except TypeError:
                continue
            try:
                iz.writefp(filei, xmli)
            except TypeError:
                continue
            idic = {}
            xdic = {}
            ix.build_idic(xmli, mtype, idic)
            ix.build_xl_xdic(xmlx, xdic)
            sheet = count
            ix.extract_xl_image(iz, idic, xdic, args.usenamefile, sheet)
            os.unlink(xmli)
            os.unlink(xmlx)
        else:
            xmli = mkxmltemp(xmliprefix) 
            try:
                iz.writefp(xfile, xmli)
            except TypeError:
                continue
            idic = {}
            ix.build_idic(xmli, mtype, idic)
            page = count
            ix.extract_image(iz, idic, page)
            os.unlink(xmli)

