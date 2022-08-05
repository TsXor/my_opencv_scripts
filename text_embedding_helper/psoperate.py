import photoshop.api as ps
import ActionManager as psAM
app = ps.Application()
psAM.psAM_settings['psapp'] = app
import sys,json

def mktxlr(text, pos, size, leading, orientation, rgb=(0,0,0)):
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
  AMobj.merge( \
    psAM.ActionDescriptorPy('textLayer',{ \
      'textStyleRange': psAM.ActionListPy([ \
        psAM.ActionDescriptorPy('textStyleRange',{ \
          'from': 0, \
          'to': len(list(text)), \
          'textStyle': psAM.ActionDescriptorPy('textStyle',{ \
            'autoLeading': False, \
            'size': psAM.psUnitDouble('pointsUnit',float(size)*1.1), \
            'leading': psAM.psUnitDouble('pointsUnit',float(leading)), \
            'syntheticBold': True, \
            'fontPostScriptName': 'Sarasa-UI-SC-Regular', 
            'fontName': 'Sarasa UI SC', \
            'fontStyleName': 'Regular' \
          }) \
        }) \
      ]) \
    }) \
  )
  AMobj['/textKey/orientation'] = psAM.psEnumerated('orientation',orientation)
  start_ruler_units = app.preferences.rulerUnits
  newtlyr.textItem.position = list(pos)
  app.preferences.rulerUnits = start_ruler_units

drawinfo = json.loads(sys.stdin.read())
for i in range(len(drawinfo)):
  a,b,c,d = drawinfo[i]
  mktxlr('文字占位'+str(i), (a-c/2,b), c, d, 'vertical', rgb=(0,0,0))
