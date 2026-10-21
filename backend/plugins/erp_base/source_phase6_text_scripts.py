"""已核对原文的打印文字事件；不执行任意 C#，未对应脚本继续列为差异。"""
import hashlib

SCRIPTS={
    'ffd655f438663b666e2d9c2282e2e783cb5c87b1ece40fef3fcab655780a5cca':
        ('GrayInWaste','tableCell28','tableCell28_BeforePrint','original_job',('OriJobsheetNo','ReceSheetNo')),
    '617bb20bb362e601fa5d5b4161fdc92aa4f616b4443965eb7982aefe20af9923':
        ('TrialDyeRecipePhaseDetail','tableCell13','tableCell13_BeforePrint','recipe_unit',('RecipeUnit','RecipeUnit_R')),
    '63bec0f6baa41d307a4e1cd819fa6666b3089756605257db93a75050b17a2c5e':
        ('TrialDyeRecipePhaseDetail','tableCell13','tableCell13_BeforePrint','recipe_unit',('RecipeUnit','RecipeUnit_R')),
}


def plan(root):
    spec=SCRIPTS.get(hashlib.sha256(root.get('ScriptsSource','').encode()).hexdigest())
    return spec if spec is not None and root.get('DataMember')==spec[0] else None


def script_event(node,root):
    spec=plan(root)
    if spec is None:return False
    return any(control.get('Name')==spec[1] and control.find('Scripts') is node for control in root.iter()) and {
        k:v for k,v in node.attrib.items() if k!='Ref'}=={'OnBeforePrint':spec[2]}


def inputs(root):
    spec=active_plan(root)
    return spec[4] if spec is not None else ()


def active_plan(root):
    return plan(root) if any(script_event(node,root) for node in root.iter('Scripts')) else None


def text(spec,value):
    # 对应这三份原脚本的 Trim：NULL/DBNull 变空串；原始数据本身不改写。
    def trim(name):
        item=value(name)
        return '' if item is None else str(item).strip()
    if spec[3]=='original_job':
        original=trim('OriJobsheetNo')
        return original if original else trim('ReceSheetNo')
    unit=trim('RecipeUnit')
    return '%' if unit=='0' else 'g/l' if unit=='1' else trim('RecipeUnit_R')
