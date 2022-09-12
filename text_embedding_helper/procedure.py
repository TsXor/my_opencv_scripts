from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import click, json


@click.group() # 命令的总入口
def main():
    pass

@main.command()
@click.option('--op', help='input original picture file path', required=True)
@click.option('--xl', help='out excel file path', required=True)
def step1(inpath, xl):
    from function_scripts.textocr import main_api as textocr
    from function_scripts.textsort import main_api as textsort
    from lib_scripts.xloperate import py2xl
    
    Pim = Image.open(op)
    im = np.asarray(Pim)
    det = textocr(im)
    cover = np.where(det==255, 255, 0).astype('uint8')
    text = np.where(det==255, im, 255)
    xlsheet, markedtext = textsort(text)
    py2xl(xlsheet, xl, (20, 120, 30), extra=(('mask数据', cover),)) # xl is path
    Pmarkedtext = Image.fromarray(markedtext); Pmarkedtext.show()


@main.command()
@click.option('--op', help='input original picture file path', required=True)
@click.option('--xl', help='input excel file path', required=True)
@click.option('--psd', help='output psd file path', required=True)
def step2(op, xl, psd):
    import photoshop.api as ps
    from lib_scripts.psoperate import mktxlr, paste, moveto
    from lib_scripts.xloperate import xl2py
    import pathlib
    
    app = ps.Application()
    doc = app.open(op)
    xlinfo, cover = xl2py(xl, extra=('mask数据',))
    cover = tuple(cover)[0]
    for row in xlinfo:
        nul, text, jsont = row
        try:
            jsono = json.loads(jsont)
        except:
            continue
        if not text:
            rect = jsono["rect"]
            cv2.rectangle(cover, rect[0], rect[1], (0,0,0), -1)
            continue
        pos = jsono["pos"]
        linfo = jsono["lines"]
        lines = text.split('\n')
        lines = [(lines[i], *linfo[i]) for i in range(len(lines))]
        exitcode = mktxlr(lines, pos, 'vertical', rgb=(0,0,0))
    cover = np.expand_dims(cover, axis=2)
    cover = np.concatenate((cover, cover, cover, cover), axis=-1)
    # 在图片边角上加两个白色像素点，以防下一步粘贴时ps自动裁剪
    cover[0][0] = (255, 255, 255, 255)
    cover[cover.shape[0]-1][cover.shape[1]-1] = (255, 255, 255, 255)
    Pcover = Image.fromarray(cover)
    Pcover.save(psd+'.msk.png')
    mp = pathlib.Path(psd+'.msk.png')
    paste(app, mp)
    moveto(1)
    options = ps.PhotoshopSaveOptions()
    doc.saveAs(psd, options) # psd is path 
    doc.close()
    mp.unlink()


if __name__ == "__main__":
    main()