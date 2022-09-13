import pathlib
import pygubu
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import subprocess, itertools

from procedure import step1_api as step1
from procedure import step2_api as step2

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "procedure_gui.ui"


class ProcedureGuiApp:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("guitop", master)
        self.s1btn = builder.get_object("s1_doit")
        self.s2btn = builder.get_object("s2_doit")
        self.logbox = builder.get_object("logbox")
        self.logbox.config(state=tk.DISABLED)

        self.step1_in = None
        self.step1_out = None
        self.step2_in_pic = None
        self.step2_in_xl = None
        self.step2_out = None
        builder.import_variables(
            self, ["step1_in", "step1_out", "step2_in_pic", "step2_in_xl", "step2_out"]
        )

        builder.connect_callbacks(self)

    def writelog(self, line):
        self.logbox.config(state=tk.NORMAL)
        self.logbox.insert(tk.END, line+'\n')
        self.logbox.update()
        self.logbox.config(state=tk.DISABLED)

    def run(self):
        self.mainwindow.mainloop()

    def do_step1(self):
        self.s1btn.config(state=tk.DISABLED)
        paras = [x.get() for x in (self.step1_in, self.step1_out)]
        self.worker('step1', paras, ('', '.xlsx'))
        self.s1btn.config(state=tk.NORMAL)

    def do_step2(self):
        self.s2btn.config(state=tk.DISABLED)
        paras = [x.get() for x in (self.step2_in_pic, self.step2_in_xl, self.step2_out)]
        self.worker('step2', paras, ('', '.xlsx', '.psd'))
        self.s2btn.config(state=tk.NORMAL)

    def worker(self, name, paras, suffixes):
        if False in (bool(x) for x in paras):
            tkmsgbox.showwarning('警告','路径没选好！')
            return
        self.writelog('开始执行%s'%name)
        paras = [pathlib.Path(x) for x in paras]
        pics = [*list(paras[0].glob('*.jpg')), *list(paras[0].glob('*.png'))]
        elses = [[paras[n]/(pic.stem+suffixes[n]) for pic in pics] for n in range(1, len(paras))]
        sparas = zip(pics, *elses)
        for spara in sparas:
            spara = [str(p) for p in spara]
            self.writelog('处理%s'%spara[0])
            globals()[name](*spara)
        self.writelog('结束执行%s'%name)

if __name__ == "__main__":
    app = ProcedureGuiApp()
    app.run()
