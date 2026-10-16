"""原02站机台排程看板；保留连接倍增、空机台和NULL任务文字。"""
from decimal import Decimal, ROUND_HALF_UP
from .source_quality_reports import rows, key
from .source_business_updates import matching
from .source_stock_services import raw
from .source_trial_steps import equal


def report(query=rows):
    assignments={}
    for schedule in query('ProcessSchedule','erp_production').order_by('pk'):
        for job in matching(query('JobSheet','erp_production'),SheetNo=raw(schedule,'JobSheetNo')).order_by('pk'):
            steps=matching(query('JobProcess','erp_production'),SheetSeries=raw(job,'SheetSeries')).filter(old_process_no=raw(schedule,'ProcessNo'))
            if not any(equal(raw(step,'WProcessNo') or '', '') for step in steps):continue
            customers=list(matching(query('PCustomer','erp_base'),CustomerID=raw(job,'CustomerID'))) or [None]
            grays=list(matching(query('PGray','erp_base'),GrayID=raw(job,'ProdID'))) or [None]
            amount=raw(job,'SumAssignedRolls')
            if amount is not None:
                amount=Decimal(str(amount)).quantize(Decimal('1'),rounding=ROUND_HALF_UP)
                if abs(amount)>=1000000:raise OverflowError('原看板decimal(6,0)匹数溢出。')
            for customer in customers:
                parts=[raw(schedule,'JobSheetNo'),'\n',None if customer is None else raw(customer,'ShortName'),'\n',
                       raw(job,'CustSelfProduct'),'\n',raw(job,'ColorNum'),raw(job,'ColorID'),raw(job,'CustColorNum'),
                       '(',None if amount is None else str(amount),'匹)']
                text=None if any(part is None for part in parts) else ''.join(parts)
                for gray in grays:
                    assignments.setdefault(key(raw(schedule,'MachineID')),[]).append({'Job':text,
                        'schedule_id':schedule.pk,'job_id':job.pk,'legacy_id':job.legacy_id,
                        'customer_id':None if customer is None else customer.pk,'gray_id':None if gray is None else gray.pk})
    machines=list(matching(query('PMachine','erp_base'),StationID='02').order_by('pk'))
    columns=[];output={};details=[];positions={}
    for machine in machines:
        column='machine_'+str(machine.pk)
        columns.append({'column':column,'MachineID':raw(machine,'MachineID'),'Name':raw(machine,'Name'),'record_id':machine.pk})
        for source in assignments.get(key(raw(machine,'MachineID')),[]) or [{'Job':None}]:
            identity=key(raw(machine,'MachineID'));positions[identity]=positions.get(identity,0)+1
            index=positions[identity]
            output.setdefault(index,{'ID':index})[column]=source['Job']
            details.append({'machine_record_id':machine.pk,'ID':index,**source})
    return {'report':'Led','rows':[{**{column['column']:None for column in columns},**row} for row in output.values()],
            'column_mapping':columns,'source_rows':details,
            'notes':['原无序ROW_NUMBER按项目ID稳定排序；机台列采用记录ID并另列原名称，重名、空名和标点名称均保留，不让动态列名导致看板失败或合并丢失。']}
