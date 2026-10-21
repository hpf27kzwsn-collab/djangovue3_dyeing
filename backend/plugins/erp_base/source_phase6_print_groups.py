"""原 Level 越大越外层；同 Level 的组头、组尾共享同一组行。"""
from itertools import groupby
from django.core.exceptions import ValidationError


def level(band):return int(band['attributes'].get('Level','0'))


def report_headers(headers,footers):
    """无分组定义的组尾作用于整份报表；只建立运行范围，不改原 XML。"""
    if headers:return headers
    return [{'kind':'GroupHeaderBand','name':'','height':0,'controls':[],
             'attributes':{'Level':str(level(band))},'whole_report':True} for band in footers]


def arrange(rows,headers,root,columns):
    from .source_phase6_layouts import kind
    fields={int(n.get('Level','0')):list(n.findall('./GroupFields/*')) for n in root.iter() if kind(n)=='GroupHeaderBand'}
    fields.update({level(b):[] for b in headers if b.get('whole_report')})
    ordered=sorted(headers,key=level,reverse=True);positions={}
    for band in ordered:
        positions[level(band)]=[]
        for field in fields[level(band)]:
            candidates=columns.get(field.get('FieldName').lower(),[])
            if len(candidates)!=1:raise ValidationError({'group':'分组字段无法唯一定位：'+field.get('FieldName')})
            positions[level(band)].append(candidates[0])
    # 从内向外稳定排序；既保留重复行，也不合并 NULL 与空串。
    for band in reversed(ordered):
        for field,pos in reversed(list(zip(fields[level(band)],positions[level(band)]))):
            rows.sort(key=lambda r:(r[pos] is not None,r[pos]),reverse=field.get('SortOrder','Ascending')=='Descending')
    scopes={};starts={};ends={};parent_positions=[]
    for band in ordered:
        current=level(band);parent_positions.extend(positions[current]);start=0
        for _,members in groupby(rows,key=lambda r:tuple(r[p] for p in parent_positions)):
            end=start+len(list(members));starts.setdefault(start,[]).append(band)
            ends.setdefault(end,[]).append(current)
            for index in range(start,end):scopes[index,current]=(start,end)
            start=end
    return ordered,scopes,starts,ends
