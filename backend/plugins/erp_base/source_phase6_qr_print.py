"""R153 原 UTF-8 字节二维码脚本的明确对应；保留原版本和纠错配置。"""
import hashlib
from django.core.exceptions import ValidationError
import qrcode
from qrcode.util import QRData, MODE_8BIT_BYTE
from qrcode.image.svg import SvgPathImage
from qrcode.exceptions import DataOverflowError

R153_SCRIPT='2ea47345606df9f82accdf7c6f3f1cdd9290ea49ee8112263040456e6d5cbb38'

def supported_script(root):
    return hashlib.sha256(root.get('ScriptsSource','').encode()).hexdigest()==R153_SCRIPT

def script_event(node,root):
    return supported_script(root) and {k:v for k,v in node.attrib.items() if k!='Ref'}=={'OnBeforePrint':'barCode1_BeforePrint'}

def issues(node,root):
    sym=node.find('Symbology')
    if sym is not None and sym.get('Name')=='Code128':
        from .source_phase6_linear_print import issues as linear_issues
        return linear_issues(node)
    if sym is None or sym.get('Name')!='QRCode':return ['尚未对应此条码制式']
    result=[]
    if not supported_script(root):result.append('二维码字节编码脚本未对应')
    if node.get('ShowText','true')!='false':result.append('二维码附加文字布局未对应')
    if node.get('AutoModule','false')!='true':result.append('二维码固定模块尺寸未对应')
    if sym.get('ErrorCorrectionLevel','L') not in ['L','M','Q','H']:result.append('二维码纠错级别未对应')
    return result

def svg(text,sym):
    version=sym.get('Version','AutoVersion')
    qr=qrcode.QRCode(version=None if version=='AutoVersion' else int(version.removeprefix('Version')),
        error_correction=getattr(qrcode.constants,'ERROR_CORRECT_'+sym.get('ErrorCorrectionLevel','L')),
        image_factory=SvgPathImage,border=4)
    qr.add_data(QRData(text.encode('utf8'),mode=MODE_8BIT_BYTE))
    try:qr.make(fit=version=='AutoVersion')
    except DataOverflowError as error:
        raise ValidationError({'barcode':'原指定二维码版本容量不足，原内容完整保留；需与旧客户端溢出行为对照。'}) from error
    import xml.etree.ElementTree as ET
    root=ET.fromstring(qr.make_image().to_string(encoding='unicode'))
    ET.register_namespace('','http://www.w3.org/2000/svg')
    root.set('width','100%');root.set('height','100%');root.set('preserveAspectRatio','xMinYMin meet')
    return ET.tostring(root,encoding='unicode')
