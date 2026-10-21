"""原版式逐行条件、算术、字符串与日期算式；跨关系和未支持函数明确列差异。"""
import ast
import re
from decimal import Decimal, ROUND_HALF_EVEN
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from .source_phase6_print_rules import calculation_usage


TOKEN=re.compile(r"\s+|'(?:[^']|'')*'|\[[^\]]+\]|(?:\d+(?:\.\d*)?|\.\d+)|[A-Za-z_][A-Za-z_0-9]*|<>|!=|==|<=|>=|[=<>+*/(),%-]")


def reference_names(text):
    tokens=[m[0] for m in TOKEN.finditer(text) if not m[0].isspace()]
    return {token[1:-1] if token.startswith('[') else token for i,token in enumerate(tokens)
        if token.startswith('[') or re.fullmatch('[A-Za-z_][A-Za-z_0-9]*',token)
        and token.lower() not in ['true','false','null','and','or','not','in']
        and (i+1==len(tokens) or tokens[i+1]!='(')}


def expression(text):
    parts=[];position=0
    matches=list(TOKEN.finditer(text))
    for index,match in enumerate(matches):
        if match.start()!=position:raise ValueError('未实现表达式片段：'+text[position:match.start()])
        position=match.end();token=match[0]
        if token.isspace():continue
        if token.startswith("'"):parts.append(repr(token[1:-1].replace("''", "'")))
        elif token.startswith('['):parts.append('field('+repr(token[1:-1])+')')
        elif re.fullmatch('[A-Za-z_][A-Za-z_0-9]*',token):
            lower=token.lower()
            if lower in ['true','false','null']:parts.append({'true':'True','false':'False','null':'None'}[lower])
            elif lower in ['and','or','not','in']:parts.append(lower)
            elif next((m[0] for m in matches[index+1:] if not m[0].isspace()),None)=='(':parts.append(token)
            else:parts.append('field('+repr(token)+')')
        else:parts.append({'=':'==','<>':'!='}.get(token,token))
    if position!=len(text):raise ValueError('未实现表达式片段：'+text[position:])
    parsed=ast.parse(' '.join(parts),mode='eval').body
    def check(node):
        if isinstance(node,ast.Constant) and (node.value is None or isinstance(node.value,(str,int,float,bool))):return
        if isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
            check(node.left);check(node.right);return
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub,ast.Not)):check(node.operand);return
        if isinstance(node,ast.BoolOp) and isinstance(node.op,(ast.And,ast.Or)):
            for value in node.values:check(value)
            return
        if isinstance(node,ast.Compare) and len(node.ops)==1 and isinstance(node.ops[0],(ast.Eq,ast.NotEq,ast.Lt,ast.LtE,ast.Gt,ast.GtE,ast.In,ast.NotIn)):
            check(node.left);check(node.comparators[0]);return
        if isinstance(node,ast.Tuple):
            for value in node.elts:check(value)
            return
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and not node.keywords:
            name=node.func.id.lower();count=len(node.args)
            if name=='field' and count==1 and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):return
            valid={'abs':[1],'isnull':[1,2],'len':[1],'substring':[2,3],'round':[1,2],
                'today':[0],'now':[0],'getdate':[1],'adddays':[2]}
            if count in valid.get(name,[]) or name=='iif' and count>=1 and count%2==1:
                for arg in node.args:check(arg)
                return
        raise ValueError('未实现此计算表达式：'+text)
    check(parsed)
    return parsed


def references(tree):
    return {n.args[0].value for n in ast.walk(tree) if isinstance(n,ast.Call) and n.func.id=='field'}


def plan(root):
    definitions={n.get('Name').lower():n for n in root.findall('./CalculatedFields/*')}
    active=calculation_usage(root)['active'];ordered=[];visiting=set();done=set()
    def visit(name):
        key=name.lower()
        if key in visiting:raise ValueError('计算字段循环引用：'+name)
        if key in done:return
        node=definitions[key]
        if node.get('DataMember',root.get('DataMember'))!=root.get('DataMember'):
            raise ValueError('计算字段缺跨表关系：'+name)
        if node.get('FieldType','None') not in ['None','String','Decimal','DateTime']:
            raise ValueError('未实现计算字段类型：'+str(node.get('FieldType')))
        tree=expression(node.get('Expression',''))
        visiting.add(key)
        for ref in sorted(references(tree)):
            if ref.lower() in definitions:visit(ref)
        visiting.remove(key);done.add(key);ordered.append((node,tree))
    for name in active:visit(name)
    return ordered


def issues(root):
    try:plan(root)
    except (ValueError,SyntaxError) as error:return ['未实现原计算字段：'+str(error)]
    return []


def evaluate(tree,values,at=None):
    def value(node):return evaluate(node,values,at)
    if isinstance(tree,ast.Constant):
        if isinstance(tree.value,bool):return tree.value
        return Decimal(str(tree.value)) if isinstance(tree.value,(int,float)) else tree.value
    if isinstance(tree,ast.Tuple):return tuple(value(node) for node in tree.elts)
    if isinstance(tree,ast.Compare):
        left,right=value(tree.left),value(tree.comparators[0]);op=tree.ops[0]
        if isinstance(op,(ast.In,ast.NotIn)):
            # 单成员IN在Python语法树为标量，按原IN列表处理。
            candidates=right if isinstance(right,tuple) else (right,)
            answer=left in candidates
            return not answer if isinstance(op,ast.NotIn) else answer
        # 原表达式引擎明确把与数值比较的NULL按0比较；字符串/日期不猜测转换。
        if left is None and isinstance(right,(int,float,Decimal)):left=0
        if right is None and isinstance(left,(int,float,Decimal)):right=0
        if isinstance(op,ast.Eq):return left==right
        if isinstance(op,ast.NotEq):return left!=right
        if isinstance(op,ast.Lt):return left<right
        if isinstance(op,ast.LtE):return left<=right
        if isinstance(op,ast.Gt):return left>right
        return left>=right
    if isinstance(tree,ast.BoolOp):
        return all(bool(value(n)) for n in tree.values) if isinstance(tree.op,ast.And) else any(bool(value(n)) for n in tree.values)
    if isinstance(tree,ast.Call):
        name=tree.func.id.lower()
        if name=='field':
            v=values[tree.args[0].value.lower()]
            return Decimal(str(v)) if isinstance(v,float) else v
        if name=='iif':
            for i in range(0,len(tree.args)-1,2):
                if value(tree.args[i]):return value(tree.args[i+1])
            return value(tree.args[-1])
        if name=='now':return at
        if name=='today':return at.replace(hour=0,minute=0,second=0,microsecond=0)
        first=value(tree.args[0])
        if name=='isnull':
            if len(tree.args)==1:return first is None
            return value(tree.args[1]) if first is None else first
        if first is None:return None
        if name=='abs':return abs(first)
        if name=='len':return len(first)
        if name=='substring':
            start=int(value(tree.args[1]));length=int(value(tree.args[2])) if len(tree.args)==3 else len(first)-start
            if start<0 or start>len(first) or length<0 or start+length>len(first):raise ValueError('Substring起点或长度超出范围')
            return first[start:start+length]
        if name=='round':
            digits=int(value(tree.args[1])) if len(tree.args)==2 else 0
            return Decimal(str(first)).quantize(Decimal(1).scaleb(-digits),rounding=ROUND_HALF_EVEN)
        if name=='getdate':return first.replace(hour=0,minute=0,second=0,microsecond=0)
        if name=='adddays':return first+timedelta(days=float(value(tree.args[1])))
    if isinstance(tree,ast.UnaryOp):
        first=value(tree.operand)
        if isinstance(tree.op,ast.Not):return not first
        return None if first is None else -first if isinstance(tree.op,ast.USub) else first
    left,right=value(tree.left),value(tree.right)
    if left is None or right is None:return None
    if isinstance(tree.op,ast.Add):return left+right
    if isinstance(tree.op,ast.Sub):return left-right
    if isinstance(tree.op,ast.Mult):return left*right
    return Decimal(str(left))/Decimal(str(right))


def apply(root,result,at=None):
    if at is None:at=timezone.localtime(timezone.now())
    ordered=plan(root)
    if not ordered:return result
    columns=list(result['columns']);rows=[list(row) for row in result['rows']]
    for node,tree in ordered:
        names=[c['name'].lower() for c in columns];name=node.get('Name')
        if name.lower() in names:raise ValidationError({'calculation':'计算字段与查询投影重名：'+name})
        for ref in references(tree):
            if names.count(ref.lower())!=1:raise ValidationError({'calculation':'计算来源无法唯一定位：'+ref})
        for index,row in enumerate(rows):
            try:
                value=evaluate(tree,dict(zip(names,row)),at)
                if value is not None and node.get('FieldType')=='String':value=str(value)
                elif value is not None and node.get('FieldType')=='Decimal':value=Decimal(str(value))
            except (ArithmeticError,TypeError,ValueError) as error:
                raise ValidationError({'calculation':f'原行{index+1}，字段{name}无法计算：{error}；未跳过原行或补0。'}) from error
            row.append(value)
        columns.append({'name':name})
    return {**result,'columns':columns,'rows':rows,'calculated_fields':[n.get('Name') for n,_ in ordered]}
