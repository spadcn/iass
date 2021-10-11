#!/usr/bin/env python3

import re
from zipfile import ZipFile

class Izip():

    """提取zip中相应文件和新息"""
    def __init__(self, file):
        self.file = file
        self.za = self.__getza()

    def __getza(self):
        za = ZipFile(self.file)
        return za
        
    def getzfnlist(self, pattern):
        zfnlist = []
        for zf in self.za.filelist:
            if re.search(pattern, zf.filename):
                zfnlist.append(zf.filename)
        return zfnlist

    def readzf(self, zfn):
        try: 
           zfd = self.za.read(zfn)
        except KeyError:
            return
        return zfd

    def writefp(self, zfn, fp):
        open(fp, "wb").write(self.readzf(zfn))
        

