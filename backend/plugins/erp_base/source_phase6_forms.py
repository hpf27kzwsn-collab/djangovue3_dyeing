"""旧入口字段展示配置；原表完整录入仍保留，公式执行继续在服务层。"""
import re
from .source_phase6_entries import definition
from .source_entry_registry import ENTRY_RULES
from .source_phase6_auto_values import generated_fields
from .source_ownership import OWNERS
from .source_transfer_numbers import NUMBER_INPUTS


def field_key(name):
    words=re.sub(r'([a-z0-9])([A-Z])',r'\1_\2',name)
    return 'old_'+re.sub(r'\W','_',words.lower()).strip('_')


def extend(resources):
    for model,options in resources.items():
        options['workflow']['parent_bindings']=[{'relation':rule['field'],'fields':[
            {'field':field_key(old),'parent_original_field':parent_old}
            for old,parent_old in zip(rule['source_fields'],rule['target_fields'])]}
            for label,rules in OWNERS.items() if label.split('.')[1]==model for rule in rules]
        if model in ['SourceDyeArrivalNoticeDetail','SourceDyePurDetail','SourceDyeArticleOutDetail','SourceDyePriceAdjustDetail','SourceDyeOrderMain','SourceDyeOrderColor','SourceDyeProdIn','SourceDyeProdInRecord']:
            options['crud_fields'].insert(1,'transfer_retained')
            options.setdefault('fields',{})['transfer_retained']={'title':'转单状态','column':{'width':120,'sortable':False}}
            options['workflow'].setdefault('freeze_when',[]).append('transfer_retained')
        if model in ['SourceDyeOrderMain','SourceDyeProdIn']:
            options['workflow']['actions'].append({'key':'phase6_reverse_head_transfer','title':'撤回转入整单（原单留档）',
                'states':['draft',None],'inputs':[
                    {'key':'at','title':'撤回时间','kind':'datetime','required':True,'options':[]},
                    {'key':'reason','title':'撤回原因','kind':'text','required':True,'options':[]}]})
        if model in ['SourceDyeArrivalNoticeDetail','SourceDyePurDetail','SourceDyeArticleOutDetail']:
            options['workflow']['actions'].append({'key':'phase6_reverse_line_transfer','title':'撤回本次转入明细（保留来源）',
                'states':['draft',None],'inputs':[
                    {'key':'at','title':'撤回时间','kind':'datetime','required':True,'options':[]},
                    {'key':'reason','title':'撤回原因','kind':'text','required':True,'options':[]}]})
        if model=='SourceDyePriceAdjustDetail':
            options['workflow']['actions'].append({'key':'phase6_reverse_quote_adjustment','title':'撤回报价转调价（原删除回写并留档）',
                'states':['draft',None],'inputs':[
                    {'key':'at','title':'撤回时间','kind':'datetime','required':True,'options':[]},
                    {'key':'reason','title':'撤回原因','kind':'text','required':True,'options':[]}]})
        if model in ['SourceDyeArticleDeptApplyDetail','SourceDyeStuffDeptApplyDetail']:
            article=model=='SourceDyeArticleDeptApplyDetail';prefix='article' if article else 'stuff'
            source_module='erp_warehouse' if article else 'erp_production'
            options['workflow']['actions'].append({'key':'phase6_department_apply_to_purchase','title':'部门申请转采购（明确原行）',
                'states':['draft','confirmed','approved',None],'inputs':[
                    {'key':key,'title':title,'kind':'select','required':True,'options':[],
                     'remote':{'entity':entity,'pk':'id','label':'old_sheet_no',
                         'columns':[{'field':'id','title':'记录ID'},{'field':'old_sheet_no','title':'原单号'},
                                    {'field':'old_sheet_series','title':'流水号'}]}}
                    for key,title,entity in [('application','采用的部门申请表头',source_module+'_sourcedye'+prefix+'deptapply'),
                        ('head','目标采购单','erp_purchase_sourcedye'+prefix+'purmain')]]+
                    [{'key':key,'title':title,'kind':'number','required':True,'options':[]}
                        for key,title in [('quantity','本次采购原数量'),('price','本次采购单价')]]})
        if model=='SourceDyeMachineCarePlanDetail':
            options['workflow']['actions'].append({'key':'phase6_care_plan_to_article_out','title':'保养配件领料（明确来源）',
                'states':['draft','confirmed','approved',None],'inputs':[
                    {'key':'head','title':'目标配件出库单','kind':'select','required':True,'options':[],
                     'remote':{'entity':'erp_warehouse_sourcedyearticleout','pk':'id','label':'old_sheet_no',
                        'columns':[{'field':'id','title':'记录ID'},{'field':'old_sheet_no','title':'出库单号'},{'field':'old_ware_house_id','title':'仓库'}]}},
                    {'key':'article','title':'采用的配件资料（明确单位）','kind':'select','required':True,'options':[],
                     'remote':{'entity':'erp_base_sourcedyeparticle','pk':'id','label':'old_name',
                        'columns':[{'field':'id','title':'记录ID'},{'field':'old_article_id','title':'配件代码'},{'field':'old_unit','title':'单位'}]}},
                    *[{'key':key,'title':title,'kind':kind,'required':kind=='number','options':[]} for key,title,kind in [
                        ('quantity','本次领用原数量','number'),('price','本次单价','number'),
                        ('in_detail_no','入库明细原编号（未知可设为空）','text'),('storage_unit_ids','实际库位原代码（未知可设为空）','text')]]]})
        if model=='SourceDyePurDetail':
            options['workflow']['actions'].append({'key':'phase6_purchase_to_product','title':'采购转成品入库（明确来源）',
                'states':['draft','confirmed','approved',None],'inputs':[
                    {'key':'purchase','title':'采用的采购表头','kind':'select','required':True,'options':[],
                     'remote':{'entity':'erp_purchase_sourcedyepurmain','pk':'id','label':'old_sheet_no',
                        'columns':[{'field':'id','title':'记录ID'},{'field':'old_sheet_no','title':'采购单号'},
                                   {'field':'old_sheet_series','title':'流水号'},{'field':'old_supplier_id','title':'供应商'}]}},
                    {'key':'quantity_basis','title':'采购数量口径','kind':'select','required':True,
                     'options':[{'value':'weight','label':'重量原数值'},{'value':'length','label':'长度原数值'}]},
                    *[{'key':key,'title':title,'kind':kind,'required':True,'options':[]} for key,title,kind in [
                        ('sheet_kind','入库类别原代码','number'),('stock_unit','库存单位原代码','number'),
                        ('warehouse_id','仓库原代码','text'),('customer_id','客户原代码','text'),('prod_id','本厂规格原代码','text')]]]})
        if model == 'SourceDyeQuoteDetail':
            options['workflow']['actions'].append({'key':'phase6_quote_to_price_adjustment','title':'报价转调价（保存回写关联报价）',
                'states':['draft','confirmed','approved',None],'inputs':[
                    {'key':key,'title':title,'kind':'select','required':True,'options':[],
                     'remote':{'entity':'erp_sales_sourcedye'+entity,'pk':'id','label':'old_sheet_no',
                        'columns':[{'field':'id','title':'记录ID'},{'field':'old_sheet_no','title':'单号'},
                                   {'field':'old_sheet_series','title':'流水号'}]}}
                    for key,title,entity in [('quote','采用的报价头','quote'),('head','目标调价单（采用加价金额）','priceadjust')]]})
            options['workflow']['actions'].append({'key':'phase6_quote_to_order','title':'报价转新订单（明确来源）',
                'states':['draft','confirmed','approved',None], 'inputs':[
                    {'key':'quote','title':'本次采用的报价表头','kind':'select','required':True,'options':[],
                     'remote':{'entity':'erp_sales_sourcedyequote','pk':'id','label':'old_sheet_no',
                        'columns':[{'field':'id','title':'记录ID'},{'field':'old_sheet_no','title':'报价单号'},
                                   {'field':'old_sheet_series','title':'流水号'},{'field':'old_customer_id','title':'客户'}]}},
                    {'key':'fabric_id','title':'订单客户规格代码（未知可留空）','kind':'text','required':False,'options':[]}]})
        if model == 'SourceDyeArrivalNotice':
            options['workflow']['actions'].append({'key':'phase6_purchase_to_arrival','title':'采购转到货通知',
                'states':['draft',None], 'inputs':[{'key':'selected','title':'采购明细','kind':'multi',
                'remote':{'entity':'erp_purchase_sourcedyepurdetail','pk':'id','label':'old_detail_no',
                    'columns':[{'field':'id','title':'记录ID'},{'field':'old_detail_no','title':'采购明细号'},
                               {'field':'old_fabric_id','title':'物料'},{'field':'old_qty','title':'数量'}]},
                'required':True,'options':[]}]})
        for action in options['workflow']['actions']:
            for key,table,old,title in NUMBER_INPUTS.get(action['key'],[]):
                action['inputs'].append({'key':key,'title':title+'（留空自动编号）','kind':'text','required':False,'options':[]})
        rules={name:rule for label,entries in ENTRY_RULES.items() if label.split('.')[1]==model for name,rule in entries.items()}
        options['workflow']['entries']=[{'value':name,'label':rule['title'],
            'generated_fields':[field_key(old) for old in [*rule['number_fields'],*rule['default_fields']]]} for name,rule in rules.items()]
        formulas=[{'value':name,'label':rule['title']} for label,rules in ENTRY_RULES.items() if label.split('.')[1]==model for name,rule in rules.items() if rule['formula_fields']]
        if formulas:options['workflow']['actions'].append({'key':'phase6_formula','title':'旧入口公式试算与采用','states':['draft','confirmed','approved',None],
            'inputs':[{'key':'entry','title':'原计算入口','kind':'select','required':True,'options':formulas},
                      {'key':'apply','title':'采用可计算结果（关闭为只试算）','kind':'boolean','default':False,'options':[]}]})
        options['workflow']['print_entries']=[{'value':e['value'],'label':e['label']} for e in options['workflow'].get('entries',[])]
        if model=='SourceDyeDyeDipsRecord':options['workflow']['print_entries'].append({'value':'DyeDipsRecordStuffDosage','label':'试样记录染料份量'})
        for entry in options['workflow'].get('entries',[]):
            entry['generated_fields'].extend(field_key(target) for target in generated_fields(entry['value'],model))
            entry['copy_fields'] = [field_key(f['FieldName']) for f in definition(entry['value'])['fields']
                if f['FieldKind'] in ['CopyPrevRow', 'CopyLastRow'] and field_key(f['FieldName']) in options['crud_fields']]
            entry['field_rules']={field_key(f['FieldName']):{
                'title':f['FieldCaption'],'old_name':f['FieldName'],'readonly':f['IsReadOnly'],'required':f['IsRequired'],
                'display_format':f['DisplayFormat'],'editor_kind':f['EditorKind'],'editor_id':f['EditorID'],
                'generate_time':f['GenerateTime'],'expression':f['Express'],'kind':f['FieldKind']}
                for f in definition(entry['value'])['fields'] if field_key(f['FieldName']) in options['crud_fields']}
