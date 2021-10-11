from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Style
from utils import run_as_thread
import time
  
class Iprogress():
    """ iass progress bar """

    def __init__(self, tkroot):
        self.tkroot = tkroot
        self.length = 485
        self.count = 20
        self.step = 100 / self.count
        self.orient = HORIZONTAL
        self.mode = 'determinate'
        self.pady = 10
        self.barstyle = self.set_progressbar_style()
        self.progressbar = self._gen_progressbar(self.tkroot, self.length, self.step)

    def _gen_progressbar(self, tkroot, length, step):
        progressbar = Progressbar(tkroot, orient = self.orient, 
              length = self.length, mode = self.mode, style="LabeledProgressbar")
        progressbar['value'] = 0
        return progressbar
    
    def enable_progressbar(self, num):
        #self.progressbar.pack(pady = self.pady)
        self.progressbar.grid(row=num, columnspan=2)

    def update_progressbar(self, loops, i):
            step = 100 / loops
            self.progressbar['value'] += step
            if self.progressbar['value'] < 100 and i < loops - 1:
                self.barstyle.configure("LabeledProgressbar", text="{0} %      ".format(int(self.progressbar['value'])), foreground='Black', background='LightGray')
            else:
                self.progressbar['value'] = 100
                self.barstyle.configure("LabeledProgressbar", text="{0} %      ".format(int(self.progressbar['value'])), foreground='Black', background='DeepSkyBlue')

    def reset_progressbar(self):
        self.progressbar['value'] = 0
        self.barstyle.configure("LabeledProgressbar", text="{0} %      ".format(int(self.progressbar['value'])), foreground='Black', background='LightGray')


#    def _update_progressbar(self):
#        for i in range(0, self.loops):
#            print(i % int(self.loops / self.count))
#            if i % int(self.loops / self.count) == 0:
#                if self.progressbar['value'] < 100:
#                    self.progressbar['value'] += self.step
#                    self.barstyle.configure("LabeledProgressbar", text="{0} %      ".format(int(self.progressbar['value'])))
#                    print(self.progressbar['value'])
#                    time.sleep(1)
#                else:
#                    self.progressbar['value'] = 100
#                    self.barstyle.configure("LabeledProgressbar", text="{0} %      ".format(int(self.progressbar['value'])))
#                    break
#            else:
#                continue
#
#    def update_progressbar(self):
#        run_as_thread(self._update_progressbar, ())

    def set_progressbar_style(self):
        style = Style(self.tkroot)
        style.layout("LabeledProgressbar",
                [('LabeledProgressbar.trough',
                    {'children': [('LabeledProgressbar.pbar',
                        {'side': 'left', 'sticky': 'ns'}),
                        ("LabeledProgressbar.label",   # label inside the bar
                            {"sticky": ""})],
                        'sticky': 'nswe'})])
        return style

