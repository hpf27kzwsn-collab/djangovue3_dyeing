from plugins.erp_quality import services as quality
from plugins.erp_quality import models as q
from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from plugins.erp_base import models as base
from plugins.erp_warehouse import models as wh, services as stock
from plugins.erp_base.business import write
from . import test_workflows as planning_tests
from . import models as m, services as planning, execution_services as actual, weighing_services as weighing


class ActualProductionTests(TestCase):
    setUpTestData=classmethod(planning_tests.ProductionPlanningTests.setUpTestData.__func__)
    setUp=planning_tests.ProductionPlanningTests.setUp
    card=planning_tests.ProductionPlanningTests.card
    release=planning_tests.ProductionPlanningTests.release
    batch=planning_tests.ProductionPlanningTests.batch
    recipe=planning_tests.ProductionPlanningTests.recipe
    inputs=planning_tests.ProductionPlanningTests.inputs

    def employee(self):return base.Employee.objects.create(code='E',name='现场员工')

    def outputs(self,**extra):
        return {'input_quantity':None,'input_unit':None,'output_quantity':None,'output_unit':None,
            'output_mass_kg':None,'output_length_m':None,'output_pieces':None,'defect_quantity':None,'quality_note':None,**extra}

    def setup_execution(self):
        card=self.release(self.card(manual=True));employee=self.employee()
        operation=m.WorkCardOperation.objects.get(work_card=card,sequence=1)
        actual.start(operation,self.actor,at=self.now+timedelta(hours=1),employee=employee,machine=self.machine)
        return card,operation,m.OperationExecution.objects.get(operation=operation),employee

    def complete(self,execution,**values):
        return actual.complete(execution,self.actor,at=self.now+timedelta(hours=27),**self.outputs(**values))

    def warehouse(self,material,quantity=100,quality_state='released'):
        owner=base.Party.objects.create(code='OWN',name='本企业')
        warehouse=base.Warehouse.objects.create(code='W',name='仓库',kind='raw',factory=self.factory)
        location=base.StorageLocation.objects.create(code='B',name='库位',warehouse=warehouse,kind='bin')
        lot=wh.InventoryLot.objects.create(code='LOT',material=material,owner=owner)
        receipt=wh.StockReceipt.objects.create(number='IN',document_at=self.now,kind='opening',warehouse=warehouse)
        row=wh.StockReceiptLine.objects.create(receipt=receipt,line_number=1,lot=lot,location=location,
            quantity=self.kg.convert_quantity(Decimal(quantity),material.stock_unit),unit=material.stock_unit,quality_state=quality_state)
        stock.confirm(receipt,self.actor);stock.post(receipt,self.actor,self.now+timedelta(minutes=1))
        return warehouse,location,lot,row

    def test_actual_predecessor_machine_and_cross_day_completion(self):
        card=self.release(self.card(manual=True));employee=self.employee()
        last=m.WorkCardOperation.objects.get(work_card=card,sequence=3)
        with self.assertRaises(ValidationError):actual.start(last,self.actor,at=self.now+timedelta(hours=1),employee=employee,machine=self.machine)
        first=m.WorkCardOperation.objects.get(work_card=card,sequence=1)
        actual.start(first,self.actor,at=self.now+timedelta(hours=1),employee=employee,machine=self.machine)
        with self.assertRaises(ValidationError):actual.start(first,self.actor,at=self.now+timedelta(hours=1),employee=employee,machine=self.machine)
        execution=m.OperationExecution.objects.get(operation=first)
        self.complete(execution,output_quantity=Decimal('80'),output_unit=self.kg,output_mass_kg=Decimal('79'))
        execution.refresh_from_db();card.refresh_from_db()
        self.assertEqual(execution.elapsed_minutes,Decimal('1560'));self.assertEqual(card.status,'running')
        self.assertEqual(m.ExecutionWorker.objects.get(execution=execution).employee_id,employee.pk)
        actual.start(last,self.actor,at=self.now+timedelta(hours=28),employee=employee,machine=self.machine)

    def test_correction_keeps_original_and_distinguishes_omission_from_clear(self):
        self.now=self.now.replace(microsecond=123456)
        card,operation,execution,employee=self.setup_execution()
        self.complete(execution,output_quantity=Decimal('80'),output_unit=self.kg,output_mass_kg=Decimal('79'))
        actual.correct(execution,self.actor,reason='重量录入错误',at=self.now+timedelta(hours=28),employee=employee,changes={'output_mass_kg':None})
        execution.refresh_from_db()
        self.assertEqual(execution.output_mass_kg,Decimal('79'))
        self.assertIsNone(actual.effective(execution)['output_mass_kg'])
        from django.utils.dateparse import parse_datetime
        self.assertEqual(parse_datetime(actual.effective(execution)['started_at']),execution.started_at)
        self.assertEqual(parse_datetime(actual.effective(execution)['ended_at']),execution.ended_at)
        self.assertEqual(Decimal(actual.effective(execution)['output_quantity']),Decimal('80'))
        correction=m.ExecutionCorrection.objects.get(execution=execution)
        self.assertTrue(correction.changes_mass);self.assertFalse(correction.changes_quantity)
        with self.assertRaises(ValidationError):actual.correct(execution,self.actor,reason='无效',at=self.now+timedelta(hours=28),employee=employee,changes={'ended_at':None})

    def test_machine_history_and_abort_preserve_actual_start(self):
        card,operation,execution,employee=self.setup_execution()
        self.complete(execution,output_mass_kg=Decimal('80'))
        other=self.release(self.card('OTHER',manual=True))
        node=m.WorkCardOperation.objects.get(work_card=other,sequence=1)
        with self.assertRaises(ValidationError):actual.start(node,self.actor,at=self.now+timedelta(hours=2),employee=employee,machine=self.machine)
        actual.start(node,self.actor,at=self.now+timedelta(hours=28),employee=employee,machine=self.machine)
        running=m.OperationExecution.objects.get(operation=node)
        actual.abort(running,self.actor,at=self.now+timedelta(hours=29),reason='真实开工后中止本轮')
        running.refresh_from_db();self.assertEqual(running.status,'cancelled');self.assertIsNone(running.output_mass_kg)
        self.assertEqual(running.started_at,self.now+timedelta(hours=28))
        actual.start(node,self.actor,at=self.now+timedelta(hours=30),employee=employee,machine=self.machine)
        self.assertEqual(m.OperationExecution.objects.get(operation=node,status='running').execution_number,2)

    def test_semi_output_lineage_does_not_post_inventory_twice(self):
        card,operation,execution,employee=self.setup_execution()
        warehouse,location,lot,original=self.warehouse(self.material)
        issue=wh.StockIssue.objects.create(number='RAW-OUT',document_at=self.now+timedelta(minutes=30),kind='production',warehouse=warehouse)
        input_row=wh.StockIssueLine.objects.create(issue=issue,line_number=1,lot=lot,location=location,work_card=card,quantity=80,unit=self.kg,quality_state='released')
        stock.confirm(issue,self.actor);stock.post(issue,self.actor,self.now+timedelta(minutes=40))
        self.complete(execution,output_mass_kg=Decimal('80'))
        output_lot=wh.InventoryLot.objects.create(code='SEMI',material=self.material,owner=lot.owner)
        receipt=wh.StockReceipt.objects.create(number='SEMI-IN',document_at=self.now+timedelta(hours=28),kind='semi_output',warehouse=warehouse)
        output_row=wh.StockReceiptLine.objects.create(receipt=receipt,line_number=1,lot=output_lot,location=location,work_card=card,source_execution=execution,quantity=80,unit=self.kg,quality_state='released')
        stock.confirm(receipt,self.actor);stock.post(receipt,self.actor,self.now+timedelta(hours=29))
        lineage=wh.LotTransformation.objects.create(number='TRACE',work_card=card,execution=execution,occurred_at=self.now+timedelta(hours=28))
        wh.LotTransformationLine.objects.create(transformation=lineage,direction='input',lot=lot,quantity=80,unit=self.kg,issue_line=input_row)
        wh.LotTransformationLine.objects.create(transformation=lineage,direction='output',lot=output_lot,quantity=80,unit=self.kg,receipt_line=output_row)
        before=wh.InventoryMovement.objects.count()
        stock.confirm_transformation(lineage,self.actor,self.now+timedelta(hours=30))
        self.assertEqual(wh.InventoryMovement.objects.count(),before)
        with self.assertRaises(ValidationError):stock.reverse(receipt,self.actor,self.now+timedelta(hours=31),'先取消谱系采用')
        stock.void_transformation(lineage,self.actor,self.now+timedelta(hours=31),'产出收货更正')
        stock.reverse(receipt,self.actor,self.now+timedelta(hours=32),'冲销实际收货')
        lineage.refresh_from_db();self.assertTrue(lineage.is_confirmed);self.assertTrue(lineage.is_void)

    def test_shared_batch_one_physical_execution_and_member_total(self):
        first=self.release(self.card('W1',40,manual=True));second=self.release(self.card('W2',60,manual=True))
        batch=self.batch(first)
        write(m.DyeBatchWorkCard,{'batch':batch,'work_card':second,'sequence':2,'quantity':Decimal('60'),'unit':self.kg},None,planning.POLICY)
        operation=m.WorkCardOperation.objects.get(work_card=first,sequence=1)
        planning.schedule(operation,self.actor,machine=self.machine,planned_start=self.now+timedelta(hours=1),planned_end=self.now+timedelta(hours=3),batch=batch)
        planning.publish(m.ScheduleAssignment.objects.get(batch=batch),self.actor)
        actual.start_batch(batch,self.actor,process=self.process,machine=self.machine,at=self.now+timedelta(hours=1),employee=self.employee())
        physical=m.PhysicalBatchExecution.objects.get(batch=batch)
        members=[{'execution':row,**self.outputs(output_mass_kg=Decimal('40') if row.operation.work_card_id==first.pk else Decimal('60'))} for row in m.OperationExecution.objects.filter(physical_execution=physical)]
        with self.assertRaises(ValidationError):actual.complete_batch(physical,self.actor,at=self.now+timedelta(hours=2),output_mass_kg=Decimal('99'),members=members)
        self.assertEqual(m.OperationExecution.objects.filter(status='completed').count(),0)
        actual.complete_batch(physical,self.actor,at=self.now+timedelta(hours=2),output_mass_kg=Decimal('100'),members=members)
        self.assertEqual(m.PhysicalBatchExecution.objects.filter(status='completed').count(),1)
        self.assertEqual(m.OperationExecution.objects.filter(status='completed').count(),2)
        employee=base.Employee.objects.get(code='E')
        corrections=[{'execution':row,'output_mass_kg':Decimal('39') if row.operation.work_card_id==first.pk else Decimal('59')} for row in m.OperationExecution.objects.filter(physical_execution=physical)]
        with self.assertRaises(ValidationError):actual.correct_batch(physical,self.actor,at=self.now+timedelta(hours=4),employee=employee,
            reason='整缸重核',output_mass_kg=Decimal('99'),started_at=self.now+timedelta(hours=1),ended_at=self.now+timedelta(hours=2),members=corrections)
        actual.correct_batch(physical,self.actor,at=self.now+timedelta(hours=4),employee=employee,
            reason='整缸重核',output_mass_kg=Decimal('98'),started_at=self.now+timedelta(hours=1),ended_at=self.now+timedelta(hours=2),members=corrections)
        physical.refresh_from_db();self.assertEqual(physical.output_mass_kg,Decimal('100'))
        self.assertEqual(Decimal(actual.effective_physical(physical)['output_mass_kg']),Decimal('98'))
        self.assertEqual(m.ExecutionCorrection.objects.count(),2)

    def test_quality_scope_disposition_cap_and_explicit_concession(self):
        card,operation,execution,employee=self.setup_execution()
        self.complete(execution,output_mass_kg=Decimal('80'))
        inspection=write(q.QualityInspection,{'number':'Q','work_card':card,'execution':execution,'kind':'in_process',
            'inspected_at':self.now+timedelta(hours=28),'inspected_quantity':Decimal('50'),'quantity_unit':self.kg},None,planning.POLICY)
        write(q.InspectionResultLine,{'inspection':inspection,'item_code':'COLOR','item_name_snapshot':'实际对色','value_text':'偏深','result':'fail'},None,planning.POLICY)
        with self.assertRaises(ValidationError):quality.judge(inspection,self.actor,result='pass',employee=employee)
        quality.judge(inspection,self.actor,result='fail',employee=employee)
        with self.assertRaises(ValidationError):quality.dispose(inspection,self.actor,kind='release',quantity=Decimal('50'),unit=self.kg,reason='普通放行',employee=employee,at=self.now+timedelta(hours=29))
        quality.dispose(inspection,self.actor,kind='concession',quantity=Decimal('30'),unit=self.kg,reason='客户接受',employee=employee,at=self.now+timedelta(hours=29))
        with self.assertRaises(ValidationError):quality.dispose(inspection,self.actor,kind='rework',quantity=Decimal('30'),unit=self.kg,reason='超范围',employee=employee,at=self.now+timedelta(hours=29))
        self.assertEqual(q.QualityDisposition.objects.count(),1)
        with self.assertRaises(ValidationError):actual.correct(execution,self.actor,at=self.now+timedelta(hours=30),employee=employee,reason='改量',changes={'output_mass_kg':Decimal('70')})
        quality.void(inspection,self.actor,reason='实际检验来源录错',at=self.now+timedelta(hours=30))
        inspection.refresh_from_db();self.assertTrue(inspection.is_void);self.assertEqual(inspection.result,'fail')
        self.assertEqual(q.QualityDisposition.objects.get().status,'cancelled')
        actual.correct(execution,self.actor,at=self.now+timedelta(hours=31),employee=employee,reason='实绩重核',changes={'output_mass_kg':Decimal('70')})

    def test_incoming_quality_release_changes_quality_through_real_stock_adjustment(self):
        warehouse,location,lot,receipt=self.warehouse(self.material,100,'pending')
        employee=self.employee()
        inspection=write(q.QualityInspection,{'number':'IN-Q','lot':lot,'receipt_line':receipt,'kind':'incoming',
            'inspected_at':self.now+timedelta(hours=1),'inspected_quantity':Decimal('60'),'quantity_unit':self.kg},None,planning.POLICY)
        write(q.InspectionResultLine,{'inspection':inspection,'item_code':'A','item_name_snapshot':'实际来料检查','value_text':'符合','result':'pass'},None,planning.POLICY)
        quality.judge(inspection,self.actor,result='pass',employee=employee)
        quality.dispose(inspection,self.actor,kind='release',quantity=Decimal('60'),unit=self.kg,reason='实际合格范围',employee=employee,at=self.now+timedelta(hours=2))
        disposition=q.QualityDisposition.objects.get(inspection=inspection)
        adjustment=wh.StockAdjustment.objects.create(number='ADJ',document_at=self.now+timedelta(hours=2),warehouse=warehouse,reason='来料实际放行')
        wh.StockAdjustmentLine.objects.create(adjustment=adjustment,line_number=1,lot=lot,location=location,
            quality_state='pending',new_quality_state='released',quantity_delta=60,disposition=disposition)
        stock.confirm(adjustment,self.actor);stock.post(adjustment,self.actor,self.now+timedelta(hours=3))
        self.assertEqual(wh.StockBalance.objects.get(lot=lot,quality_state='pending').quantity,40)
        self.assertEqual(wh.StockBalance.objects.get(lot=lot,quality_state='released').quantity,60)

    def test_weighing_plan_measurement_and_issue_are_separate_facts(self):
        card=self.release(self.card(manual=True));batch=self.batch(card);version,stage=self.recipe()
        planning.adopt_recipe(batch,self.actor,recipe_version=version,at=self.now+timedelta(hours=1),dry_mass_kg=Decimal('100'),stages=self.inputs(stage))
        adoption=m.ProductionRecipe.objects.get(batch=batch)
        weighing.create_order(adoption,self.actor,number='WO',at=self.now+timedelta(hours=2),kind='normal',reason='')
        order=m.WeighingOrder.objects.get(batch=batch);weighing.confirm(order,self.actor)
        line=m.WeighingLine.objects.get(stage__order=order)
        self.assertEqual(line.planned_quantity,Decimal('2000'));self.assertEqual(m.WeighingRecord.objects.count(),0)
        weighing.weigh(line,self.actor,quantity=Decimal('1000'),unit=self.gram,source='manual',at=self.now+timedelta(hours=3),employee=self.employee())
        measured=m.WeighingRecord.objects.get(line=line)
        warehouse,location,lot,receipt=self.warehouse(self.chemical,10)
        issue=wh.StockIssue.objects.create(number='CH',document_at=self.now+timedelta(hours=4),kind='chemical',warehouse=warehouse)
        row=wh.StockIssueLine.objects.create(issue=issue,line_number=1,lot=lot,location=location,quantity=Decimal('1001'),unit=self.gram,
            quality_state='released',weighing_line=line,measurement_record=measured,quantity_source='manual')
        with self.assertRaises(ValidationError):stock.confirm(issue,self.actor)
        row.quantity=Decimal('1000');row.unit=self.gram;row.full_clean();row.save()
        extra=wh.StockIssueLine.objects.create(issue=issue,line_number=2,lot=lot,location=location,quantity=Decimal('1'),unit=self.gram,
            quality_state='released',weighing_line=line,measurement_record=measured,quantity_source='manual')
        with self.assertRaises(ValidationError):stock.confirm(issue,self.actor)
        extra.delete()
        stock.confirm(issue,self.actor);stock.post(issue,self.actor,self.now+timedelta(hours=5))
        self.assertEqual(weighing.issued_quantity(line),Decimal('1000'))
        self.assertEqual(weighing.measured_quantity(line),Decimal('1000'))
        order.refresh_from_db();self.assertEqual(order.status,'partial_issued')
        with self.assertRaises(ValidationError):weighing.void(measured,self.actor,reason='已领不可直接作废',at=self.now+timedelta(hours=6))

    def test_rework_creates_independent_card_without_rewriting_original(self):
        card,operation,execution,employee=self.setup_execution();self.complete(execution,output_mass_kg=Decimal('80'))
        inspection=q.QualityInspection.objects.create(number='Q',work_card=card,execution=execution,kind='in_process',result='fail',
            inspected_at=self.now+timedelta(hours=28),inspected_quantity=80,quantity_unit=self.kg)
        quality.dispose(inspection,self.actor,kind='rework',quantity=Decimal('20'),unit=self.kg,reason='重新加工',employee=employee,at=self.now+timedelta(hours=29))
        disposition=q.QualityDisposition.objects.get()
        order=m.ReworkOrder.objects.create(number='RW',original_work_card=card,disposition=disposition,quantity=20,unit=self.kg,reason='重新加工')
        quality.release_rework(order,self.actor,number='WC-RW',route_version=self.version,at=self.now+timedelta(hours=30))
        order.refresh_from_db();execution.refresh_from_db()
        self.assertEqual(order.rework_work_card.original_work_card_id,card.pk)
        self.assertEqual(order.rework_work_card.status,'released');self.assertEqual(execution.status,'completed')

    def test_api_actual_member_labels_and_effective_decimal_strings(self):
        card,operation,execution,employee=self.setup_execution();self.complete(execution,output_mass_kg=Decimal('80.123456'))
        url=f'/api/system/erp_production_operationexecution/{execution.pk}/'
        response=self.client.get(url)
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(response.data['data']['work_card_number'],card.number)
        self.assertEqual(response.data['data']['effective_facts']['output_mass_kg'],'80.123456')
        response=self.client.post(url+'correct/',{'at':(self.now+timedelta(hours=28)).isoformat(),'employee':employee.pk,
            'reason':'更正','changes':{'output_mass_kg':'79.123456'}},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(response.data['data']['effective_facts']['output_mass_kg'],'79.123456')

    def test_actual_project_item_api_accepts_actual_results(self):
        card,operation,execution,employee=self.setup_execution()
        response=self.client.post('/api/system/erp_production_executionmeasurement/',{'execution':execution.pk,
            'name':'实测温度','value_text':'60'},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.complete(execution,output_mass_kg=Decimal('80'))
        inspection=write(q.QualityInspection,{'number':'Q','work_card':card,'execution':execution,'kind':'in_process',
            'inspected_at':self.now+timedelta(hours=28),'inspected_quantity':Decimal('80'),'quantity_unit':self.kg},None,planning.POLICY)
        response=self.client.post('/api/system/erp_quality_inspectionresultline/',{'inspection':inspection.pk,
            'item_code':'A','item_name_snapshot':'实测检验','value_text':'符合','result':'pass'},format='json')
        self.assertEqual(response.status_code,200,response.data)
