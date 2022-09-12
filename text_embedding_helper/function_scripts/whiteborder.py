import photoshop.api as ps
import photoshop.api.action_manager as am
import sys,json

app = ps.Application()

def build_exec_desc(ref, desc):
    xdesc = ps.ActionDescriptor()
    xdesc.uput('target', ref)
    xdesc.uput('to', desc)
    return xdesc

def main_api(px):
    ref = ps.ActionReference.load([
        '!ref',
        am.ReferenceKey('textLayer', am.Enumerated('ordinal', 'targetEnum'))
    ])
    adict = {
        '_classID': 'layerFXVisible',
        'scale': am.UnitDouble('percentUnit', 100.000000),
        'frameFX': {
            '_classID': 'frameFX',
            'enabled': True,
            'style': am.Enumerated('frameStyle', 'outsetFrame'),
            'paintType': am.Enumerated('frameFill', 'solidColor'),
            'mode': am.Enumerated('blendMode', 'normal'),
            'opacity': am.UnitDouble('percentUnit', 100.000000),
            'size': am.UnitDouble('pixelsUnit', px),
            'color': {
                '_classID': 'grayscale',
                'gray': 0.0
            }
        }
    }
    adesc = ps.ActionDescriptor.load(adict)
    xdesc = build_exec_desc(ref, adesc)
    app.executeAction(am.str2id('set'), xdesc)
