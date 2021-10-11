#!/usr/bin/env python3

import os
import re
import glob
from izip import Izip
import argparse
import xml.etree.ElementTree as ET
from tempfile import mkdtemp
from shutil import copy,move,rmtree
from utils import get_settings

xmlsettings = get_settings()

class Ixml():
    """处理xml"""

    def __init__(self, file):
        self.file = file
        (filepath, fullname) = os.path.split(file)
        filename, fileextension = os.path.splitext(fullname)
        self.path = filepath
        self.name = filename
        self.ext = fileextension

    def build_idic(self, xmli, mtype, idic):
        tree = ET.parse(xmli)
        root = tree.getroot()
        for child in root: 
            id = child.attrib.get('Id')
            fp = child.attrib.get('Target')
            if child.attrib.get('Type') == "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image":
                (p, f) = os.path.split(fp)
                idic[id] = xmlsettings.mediatype[mtype]['path'] + f

    #This is for Excel document only
    def build_xl_xdic(self, xmlx, xdic):
        tree = ET.parse(xmlx)
        root = tree.getroot()
        namespaces = dict([node for _, node in ET.iterparse(xmlx, events=['start-ns'])])
        for pic in root.findall('.//xdr:twoCellAnchor', namespaces):
            row  = pic.find("xdr:to/xdr:row", namespaces)
            col  = pic.find("xdr:to/xdr:col", namespaces)
            id_elem = pic.find("xdr:pic/xdr:blipFill/a:blip", namespaces)
            try:
                id = id_elem.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                xdic[id] = [row.text, col.text]
            except AttributeError:
                if xmlsettings.debug == True:
                    print("Ignoring empty elem at row: " + row.text + " col: " + col.text)

    def extract_xl_image(self, xz, idic, xdic, usenamefile, sheet):
        for id in xdic.keys():
            (imagepath, imagefullname) = os.path.split(idic[id])
            imagename, imageextension = os.path.splitext(imagefullname)
            if imageextension == ".jpeg":
                imageextension = ".jpg"
            fixed_row = '{:04}'.format(int(xdic[id][0]))
            fixed_col = '{:04}'.format(int(xdic[id][1]))
            name = ""
            if usenamefile == True:
                textnamefile = self.path + self.name + ".txt"
                with open(textnamefile, mode='r', encoding='UTF-8') as nf:
                    names = nf.read().splitlines()
                    name = names[int(xdic[id][0])]
                    if name != "":
                        name = "_" + name
                    else:
                        name = ""
            sheet = '{:02}'.format(int(sheet))
            targetpath = self.path + self.name + "/"
            try:
                os.stat(targetpath)
            except:
                os.mkdir(targetpath)  
            targetfile = targetpath + sheet + "_" + fixed_row + "_" + fixed_col + name + imageextension
            sourcefile = idic[id]

            if not os.path.exists(targetfile):
                xz.writefp(sourcefile, targetfile)
            
    def extract_image(self, xz, idic, page):
        for id in sorted(idic.keys()):
            (imagepath, imagefullname) = os.path.split(idic[id])
            imagename, imageextension = os.path.splitext(imagefullname)
            name = re.search(r'[0-9]', id).group()
            name = '{:03}'.format(int(name))
            if imageextension == ".jpeg":
                imageextension = ".jpg"
            page = '{:03}'.format(int(page))
            targetpath = self.path + self.name + "/"
            try:
                os.stat(targetpath)
            except:
                os.mkdir(targetpath)  
            targetfile = targetpath + page + "_" + name + imageextension
            sourcefile = idic[id]

            if not os.path.exists(targetfile):
                xz.writefp(sourcefile, targetfile)
            
