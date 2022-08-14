import photoshop.api as ps
import ActionManager as psAM
app = ps.Application()
psAM.psAM_settings['psapp'] = app
import sys,json

def mktxlr(text, pos, lineinfo, orientation, rgb=(0,0,0)):
  app.preferences.rulerUnits = ps.Units.Pixels
  doc = app.activeDocument
  text_color = ps.SolidColor()
  text_color.rgb.red = rgb[0]
  text_color.rgb.green = rgb[1]
  text_color.rgb.blue = rgb[2]
  newtlyr = doc.artLayers.add()
  newtlyr.kind = ps.LayerKind.TextLayer
  newtlyr.textItem.contents = text
  newtlyr.textItem.color = text_color
  namerefpy = psAM.ActionReferencePy('textLayer', 'Name', newtlyr.name)
  AMobj = psAM.ActionObjectPy(namerefpy)
  rangelist = []; last = 0
  while True:
    i = text.find('\r',last)
    if i == -1:
      break
    rangelist.append((last,i))
    last = i+1
  textStyleRange = psAM.ActionListPy([])
  for i in range(len(lineinfo)):
    styleobj = psAM.ActionDescriptorPy('textStyleRange',{ \
      'from': rangelist[i][0], \
      'to': rangelist[i][1], \
      'textStyle': psAM.ActionDescriptorPy('textStyle',{ \
        'autoLeading': False, \
        'size': psAM.psUnitDouble('pointsUnit',float(lineinfo[i][0])*1.1), \
        'leading': psAM.psUnitDouble('pointsUnit',float(lineinfo[i][1])), \
        'syntheticBold': True, \
        'fontPostScriptName': 'Sarasa-UI-SC-Regular', 
        'fontName': 'Sarasa UI SC', \
        'fontStyleName': 'Regular' \
      }) \
    })
    textStyleRange.append(styleobj)
  AMobj.merge( \
    psAM.ActionDescriptorPy('textLayer',{ \
      'textStyleRange': textStyleRange
    }) \
  )
  AMobj['/textKey/orientation'] = psAM.psEnumerated('orientation',orientation)
  start_ruler_units = app.preferences.rulerUnits
  newtlyr.textItem.position = list(pos)
  app.preferences.rulerUnits = start_ruler_units

app.load(sys.argv[1])
drawinfo = json.loads(sys.stdin.read())
for i in range(len(drawinfo)):
  pos = drawinfo[i]['pos']
  lineinfo = drawinfo[i]['lines']
  mktxlr('文字占位%d\r'%i*len(lineinfo), pos, lineinfo, 'vertical', rgb=(0,0,0))
