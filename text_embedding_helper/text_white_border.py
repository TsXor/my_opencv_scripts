import photoshop.api as ps
import ActionManager as psAM
app = ps.Application()
psAM.psAM_settings['psapp'] = app
import sys,json

def ctxlrframe(px):
  ctxlrrefpy = psAM.ActionReferencePy('textLayer', 'Enumerated', psAM.psEnumerated('ordinal', 'targetEnum'))
  ctxlrobjpy = psAM.ActionObjectPy(ctxlrrefpy)
  ctxlrobjpy.merge( \
    psAM.ActionDescriptorPy('layerFXVisible', { \
      'scale': psAM.psUnitDouble('percentUnit', 100.000000), \
      'frameFX': psAM.ActionDescriptorPy('frameFX', { \
        'enabled': True, \
        'style': psAM.psEnumerated('frameStyle', 'outsetFrame'), \
        'paintType': psAM.psEnumerated('frameFill', 'solidColor'), \
        'mode': psAM.psEnumerated('blendMode', 'normal'), \
        'opacity': psAM.psUnitDouble('percentUnit', 100.000000), \
        'size': psAM.psUnitDouble('pixelsUnit', 4.000000), \
        'color': psAM.ActionDescriptorPy('grayscale', {'gray': 0.0})
      }) \
    }) \
  )

while True:
  ipt = input('字体白边大小: ')
  ctxlrframe(ipt)
