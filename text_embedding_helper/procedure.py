from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import click, json
from lib_scripts.cvutils import immask


@click.group() # 命令的总入口
def main():
    pass


step1_loaded = False

def step1_load():
    global textocr, textsort, py2xl
    from function_scripts.textocr import main_api as textocr
    from function_scripts.textsort import main_api as textsort
    from lib_scripts.xloperate import py2xl
    global step1_loaded
    step1_loaded = True

def step1_api(op, xl):
    if not step1_loaded:
        step1_load()
    
    Pim = Image.open(op)
    im = np.asarray(Pim)
    data = textocr(im)
    texts, covers, colors = list(zip(*data))
    xlsheets, markedtexts = list(zip(*[textsort(text, im) for text in texts]))
    xlsheets = [[(*r, c[0]) for r in x] for x, c in zip(xlsheets, colors)]
    header = (
        "文字图片",
        "翻译填这里（行数不得大于原文，无意义就留空）",
        "文字位置信息（不懂勿动！）",
        "文字颜色信息（不懂勿动！）",
    )
    xlsheet = sum([[header], *xlsheets], [])
    erasers = list(zip(*colors))[1]
    maskdat = list(zip(covers, erasers))
    py2xl(xlsheet, xl, (20, 120, 30, 30), extra=(('mask数据', maskdat),)) # xl is path
    for markedtext in markedtexts:
        Pmarkedtext = Image.fromarray(markedtext); Pmarkedtext.show()

@main.command()
@click.option('--op', help='input original picture file path', required=True)
@click.option('--xl', help='out excel file path', required=True)
def step1(*args, **kwargs):
    step1_api(*args, **kwargs)


step2_loaded = False

def step2_load():
    global ps, mktxlr, paste, moveto, xl2py, pathlib
    import photoshop.api as ps
    from lib_scripts.psoperate import mktxlr, paste, moveto
    from lib_scripts.xloperate import xl2py
    import pathlib
    global step2_loaded
    step2_loaded = True

def step2_api(op, xl, psd):
    if not step2_loaded:
        step2_load()
    
    app = ps.Application()
    doc = app.open(op)
    Pim = Image.open(op)
    im = np.asarray(Pim)
    xlinfo, maskdat = xl2py(xl, extra=('mask数据',))
    maskdat = tuple(maskdat)[0]
    tmask = np.ones(im.shape, dtype=np.uint8)
    for row in xlinfo:
        nul, text, jsont, tcolor = row
        try:
            jsono = json.loads(jsont)
        except:
            continue
        if (not text) or text=='IGNORE':
            continue
        rect = jsono["rect"]
        cv2.rectangle(tmask, rect[0], rect[1], (255,255,255), -1)
        if text=='ERASE':
            continue
        pos = jsono["pos"]
        linfo = jsono["lines"]
        lines = text.split('\n')
        lines = [(lines[i], *linfo[i]) for i in range(len(lines))]
        exitcode = mktxlr(lines, pos, 'vertical', rgb=(0,0,0))
    for cover, mcolor in maskdat:
        cover = immask(cover, tmask)
        cover = np.expand_dims(cover, axis=2)
        chnl = np.ones(cover.shape, dtype=np.uint8)*mcolor
        cover = np.concatenate((chnl, chnl, chnl, cover), axis=-1)
        # 在图片边角上加两个白色像素点，以防下一步粘贴时ps自动裁剪
        cover[0][0] = (255, 255, 255, 255)
        cover[cover.shape[0]-1][cover.shape[1]-1] = (255, 255, 255, 255)
        Pcover = Image.fromarray(cover)
        Pcover.save(psd+'.msk.png')
        mp = pathlib.Path(psd+'.msk.png')
        paste(app, mp)
        moveto(1)
        mp.unlink()
    options = ps.PhotoshopSaveOptions()
    doc.saveAs(psd, options) # psd is path 
    doc.close()

@main.command()
@click.option('--op', help='input original picture file path', required=True)
@click.option('--xl', help='input excel file path', required=True)
@click.option('--psd', help='output psd file path', required=True)
def step2(*args, **kwargs):
    step2_api(*args, **kwargs)


if __name__ == "__main__":
    main()