#!/usr/bin/env python3.8

import re
import os
import zlib
from PIL import Image 
from io import BytesIO
from utils import get_settings

pdf_settings = get_settings()

class Ipdf():
    """ extract images from PDF"""
    def __init__(self, pdfile, folder):
        self.pdfile = pdfile
        self.folder = folder
    def formatpt(self, pt):
        pts = re.sub(r'(\[|\])', r'\\\1', pt.decode('ascii'))
        ptb = pts.encode('ascii')
        return ptb


    def extractimg(self):
        f = open(self.pdfile, "rb")
        fb = f.read()

        pts = pdf_settings.mediatype['pdf']['imgpt'].split(',')
        count=0
        for pt in pts:
            ext = ".jpg"
            if re.search('JPXDecode', pt):
                isjpx = True
                ext = ".jpx"
            else:
                isjpx = False

            if re.search('FlateDecode', pt):
                isflate = True
            else:
                isflate = False

            if re.search('DCTDecode', pt):
                isdct = True
            else:
                isdct = False

            ptb = re.compile(pt.encode('ascii'))
            objs = re.findall(ptb, fb)
            for obj in objs:
                spt = re.compile(self.formatpt(obj[0]))
                try:
                    pos_ss = re.search(spt, fb).end()
                except AttributeError:
                    continue

                if isjpx == True:
                    obj_len = int(obj[1].decode('ascii'))
                else:
                    obj_len = int(obj[2].decode('ascii'))

                f.seek(pos_ss)

                if isflate == True:
                    ttbf = f.read(obj_len)
                    tbf = zlib.decompress(ttbf)
                else:
                    tbf = f.read(obj_len)

                filename = self.folder + "/" + '{:03}'.format(int(count)) + ".jpg"
                    
                try:
                    os.stat(self.folder)
                except:
                    os.mkdir(self.folder)
                if isjpx == True:
                    im = Image.open(BytesIO(tbf))
                    img = im.convert("RGB")
                    img.save(filename)
                else:
                   with open(filename, "wb") as img:
                       img.write(tbf)
                count += 1
    
