#!/usr/bin/env python3 
import os.path
import platform
from glob import glob

installdir = os.path.split(__file__)[0]

class Settings():
    """对于各种文档的响应设定"""
    
    def __init__(self):
#        self.xl_meta_pt = "xl/drawings/drawing[0-9]+.xml"
#        self.xl_meta_pt = "xl/drawings/_rels/drawing[0-9]+.xml.rels"
        if platform.system() == 'Windows':
            self.workdir = "X:\X"
            self.clicmd = installdir + "/" + "asscli.pyw"
            self.pdfcmd = installdir + "/" + "poppler/bin/" + "pdfimages"
            self.convert = installdir + "/" + "ImageMagick/" + "convert"
            self.exiftool = installdir + "/" + "exiftool/" + "exiftool"
        else:
            self.workdir = "/data/projects/test/ixx"
            self.clicmd = installdir + "/" + "asscli.py"
            self.pdfcmd = "pdfimages"
            self.convert = "convert"
            self.exiftool = "exiftool"

        self.button_width = 10
        self.filepattern = "*.xlsx,*.XLSX,*.pptx,*.PPTX,*.pdf,*.PDF"
        self.imgpattern = "HEIC,heic|jpg"
        self.debug = False
        self.deltedir = True
        self.button_height = 1
        self.xlmediapath = "xl/media/"
        self.pptmediapath = "ppt/media/"
        self.type = {'.pdf': 'pdf', ".PDF": 'pdf',
                '.xlsx': 'xl', ".XLSX": "xl",
                '.pptx': 'ppt', '.PPTX': 'ppt',
                '.docx': 'doc', '.DOCX': 'docx'}
        self.mediatype = {'ppt': {'path': 'ppt/media/', 'imgpt': 'ppt/slides/_rels/slide[0-9]+.xml.rels'},
                'xl' : {'path': 'xl/media/', 'imgpt': 'xl/drawings/drawing[0-9]+.xml', 'rowpt': 'xdr:to/xdr:row', 'colpt': 'xdr:to/xdr:col', 'idpt': 'xdr:pic/xdr:blipFill/a:blip', 'elempt': '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed' },
                'pdf': {'path': 'pdf/path/', 'imgpt': '(Filter/(DCTDecode)/.*/Length (.*)>>\r\nstream\r\n),(Filter(\[/DCTDecode\]/).*/Length (.*)/Name/.*/Image/Type/XObject/Width.*>>stream\r\n),(Length (.*)/Type/XObject/Subtype/Image/.*/Filter/(JPXDecode)/.*/Interpolate true/ColorSpace/DeviceRGB>>stream\r\n),(/Filter \[/FlateDecode /(DCTDecode)\]\n.*\n.*\n.*\n/Length (.*)\n.*\nstream\n),Filter/(DCTDecode)/.*/Length (.*)/.*stream\r\n'}
                }

                    #(Filter\[/(FlateDecode)\]/Length (.*)>>stream\r\n),



    


