"""原 Code128 字符集、校验位及自动模块；不改码、不截断异常内容。"""
from html import escape
from barcode import Code128
from barcode.charsets import code128
from barcode.errors import IllegalCharacterError
from django.core.exceptions import ValidationError


def issues(node):
    sym=node.find('Symbology');result=[]
    if sym.get('CharacterSet','CharsetA') not in ['CharsetA','CharsetB','CharsetC','CharsetAuto']:
        result.append('未对应Code128字符集')
    if node.get('AutoModule','false')!='true':result.append('Code128固定模块尺寸未对应')
    if node.get('Orientation','Normal')!='Normal':result.append('Code128旋转未对应')
    if any(k not in ['Ref','Name','CharacterSet'] for k in sym.attrib):result.append('Code128附加编码属性未对应')
    return result


def pattern(text,charset):
    if not text:raise ValidationError({'barcode':'Code128原内容为空；原记录保留，不编造条码。'})
    if charset=='CharsetAuto':
        if any(ord(c)>127 for c in text):
            raise ValidationError({'barcode':'Code128原内容含非ASCII字符；原模板没有FNC替代约定，不将文字解释成库的功能码占位。'})
        try:return Code128(text).build()[0]
        except IllegalCharacterError as error:raise ValidationError({'barcode':str(error)}) from error
    name=charset.removeprefix('Charset')
    if name=='C':
        if len(text)%2 or any(c not in '0123456789' for c in text):
            raise ValidationError({'barcode':'Code128 C原内容必须为偶数位ASCII数字；不补零、不截断。'})
        values=[int(text[i:i+2]) for i in range(0,len(text),2)]
    else:
        # 固定A/B只接收其原ASCII范围；库的特殊字符占位不自动替代业务文字。
        low,high=(0,95) if name=='A' else (32,127)
        if any(not low<=ord(c)<=high for c in text):
            raise ValidationError({'barcode':'Code128 '+name+'存在原字符集以外的内容；完整原值保留，不自动换码或删除字符。'})
        values=[getattr(code128,name)[c] for c in text]
    start=code128.START_CODES[name];checksum=(start+sum(i*v for i,v in enumerate(values,1)))%103
    return ''.join(code128.CODES[v] for v in [start,*values,checksum])+code128.STOP+'11'


def html(text,control):
    bits=pattern(text,control['symbology'].get('CharacterSet','CharsetA'))
    # 原控件Padding由外层保留；十模块静区随自动模块共同缩放。
    bars=''.join(f'<rect x="{i+10}" y="0" width="1" height="100"/>' for i,b in enumerate(bits) if b=='1')
    image=f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(text,quote=True)}" data-symbology="Code128" viewBox="0 0 {len(bits)+20} 100" preserveAspectRatio="none" style="width:100%;height:100%;min-height:0;flex:1" shape-rendering="crispEdges"><title>{escape(text)}</title>{bars}</svg>'
    attributes=control['attributes'];alignment=control['style'].get('TextAlignment','BottomLeft')
    label='' if attributes.get('ShowText','true')=='false' else '<span style="flex:none;text-align:'+('center' if 'Center' in alignment else 'right' if 'Right' in alignment else 'left')+'">'+escape(text)+'</span>'
    content=label+image if 'Top' in alignment else image+label
    return '<div style="display:flex;flex-direction:column;width:100%;height:100%;min-height:0">'+content+'</div>'
