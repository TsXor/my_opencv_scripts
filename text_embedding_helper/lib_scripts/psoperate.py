import photoshop.api as ps
import photoshop.api.action_manager as am
import pathlib

app = ps.Application()

def str2lines(text):
    rangelist = []; last = 0
    while True:
        i = text.find('\r',last)
        if i == -1:
            break
        rangelist.append((last,i))
        last = i+1
    return rangelist

def build_exec_desc(ref, desc):
    xdesc = ps.ActionDescriptor()
    xdesc.uput('null', ref)
    xdesc.uput('to', desc)
    return xdesc

def mktxlr(txtlines: [(str, int, int)], pos, orientation, rgb=(0,0,0)):
    txts = [l[0] for l in txtlines]
    if not txts[0]:
        return -1

    # DOM operation
    app.preferences.rulerUnits = ps.Units.Pixels
    doc = app.activeDocument
    text_color = ps.SolidColor()
    text_color.rgb.red, text_color.rgb.green, text_color.rgb.blue = rgb
    newtlyr = doc.artLayers.add()
    newtlyr.kind = ps.LayerKind.TextLayer
    newtlyr.textItem.contents = '\r'.join([l[0] for l in txtlines])
    newtlyr.textItem.color = text_color
    start_ruler_units = app.preferences.rulerUnits
    newtlyr.textItem.position = list(pos)
    app.preferences.rulerUnits = start_ruler_units
    
    # AM operation
    ref = ps.ActionReference.load([
        '!ref',
        am.ReferenceKey('textLayer', am.Enumerated('ordinal', 'targetEnum'))
    ])
    indexes = [len('\r'.join(txts[:i])) for i in range(len(txts)+1)]
    if indexes:
        indexes[0] = -1
    indexes = [(indexes[i]+1, indexes[i+1]) for i in range(len(txtlines))]
    layer_dict = {
        '_classID':'textLayer',
        'orientation':am.Enumerated('orientation',orientation),
        'textStyleRange':[
            {
                '_classID':'textStyleRange',
                'From': indexes[i][0],  # USE "From" instead of "from"
                'to': indexes[i][1],
                'textStyle': {
                    '_classID':'textStyle',
                    'size': am.UnitDouble('pointsUnit',float(txtlines[i][1])*1.1),
                    'syntheticBold': True,
                    'leading': am.UnitDouble('pointsUnit',float(txtlines[i][2])),
                    'autoLeading': False,
                    'fontPostScriptName': 'Sarasa-UI-SC-Regular',
                    'fontName': 'Sarasa UI SC',
                    'fontStyleName': 'Regular'
                }
            } for i in range(len(txtlines))
        ]
    }
    layer_desc = ps.ActionDescriptor.load(layer_dict)
    xdesc = build_exec_desc(ref, layer_desc)
    app.executeAction(am.str2id('set'), xdesc)
    return 0

def paste(app, path: pathlib.WindowsPath):
    import_dict = {
        "null": path,
        "freeTransformCenterState": am.Enumerated(type="quadCenterState", value="QCSAverage"),
        "offset": {
            "horizontal": am.UnitDouble(unit="distanceUnit", double=0),
            "vertical": am.UnitDouble(unit="distanceUnit", double=0),
            "_classID": "offset",
        },
        "_classID": None,
    }
    import_desc = ps.ActionDescriptor.load(import_dict)
    app.executeAction(am.str2id("placeEvent"), import_desc)

def moveto(index):
    mv_dict = {
        'null': [
            '!ref',
            am.ReferenceKey(desiredclass='layer', value=am.Enumerated(type='ordinal', value='targetEnum'))
        ],
        'to': [
            '!ref',
            am.ReferenceKey(desiredclass='layer', value=am.Index+index)
        ],
        'adjustment': False,
        'version': 5,
        '_classID': None
    }
    mv_desc = ps.ActionDescriptor.load(mv_dict)
    app.executeAction(am.str2id("move"), mv_desc)