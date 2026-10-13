from plugins.erp_quality import services as quality
from plugins.erp_quality import models as q
from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from plugins.erp_base import models as base
from plugins.erp_base.business import write
from plugins.erp_production import models as production,services as planning,execution_services as actual,lifecycle_services as lifecycle
from plugins.erp_production import test_workflows as fixtures
from plugins.erp_sales import models as sales,fulfillment_services as fulfillment
from . import models as m,services as stock,packing_services as packing


class PackingDeliveryTests(TestCase):
    setUpTestData=classmethod(fixtures.ProductionPlanningTests.setUpTestData.__func__)
    setUp=fixtures.ProductionPlanningTests.setUp
    card=fixtures.ProductionPlanningTests.card
    allocate=fixtures.ProductionPlanningTests.allocate

    def output(self,quantity):return {'input_quantity':None,'input_unit':None,'output_quantity':Decimal(quantity),'output_unit':self.kg,
        'output_mass_kg':Decimal(quantity),'output_length_m':None,'output_pieces':None,'defect_quantity':None,'quality_note':None}

    def prepare(self):
        employee=base.Employee.objects.create(code='P',name='包装员工')
        process=base.Process.objects.create(code='GX98',name='实际包装')
        step=base.RouteStep.objects.create(route_version=self.version,sequence=4,process=process,is_required=True,predecessor=self.last)
        card=self.card();allocation=self.allocate(card)
        planning.prepare(card,self.actor,[self.first,self.last,step]);planning.release(card,self.actor,at=self.now+timedelta(minutes=1))
        for sequence,start,finish in [(1,1,2),(3,3,4)]:
            operation=production.WorkCardOperation.objects.get(work_card=card,sequence=sequence)
            actual.start(operation,self.actor,at=self.now+timedelta(hours=start),employee=employee,machine=self.machine)
            execution=production.OperationExecution.objects.get(operation=operation)
            actual.complete(execution,self.actor,at=self.now+timedelta(hours=finish),**self.output('80'))
        inspection=write(q.QualityInspection,{'number':'Q','work_card':card,'execution':execution,'kind':'final',
            'inspected_at':self.now+timedelta(hours=5),'inspected_quantity':Decimal('80'),'quantity_unit':self.kg},None,planning.POLICY)
        write(q.InspectionResultLine,{'inspection':inspection,'item_code':'COLOR','item_name_snapshot':'实际对色','result':'pass'},None,planning.POLICY)
        quality.judge(inspection,self.actor,result='pass',employee=employee)
        quality.dispose(inspection,self.actor,kind='release',quantity=Decimal('80'),unit=self.kg,reason='实际终检放行',employee=employee,at=self.now+timedelta(hours=6))
        disposition=q.QualityDisposition.objects.get()
        owner=base.Party.objects.create(code='OWN',name='本企业')
        lot=m.InventoryLot.objects.create(code='OUT',material=self.material,owner=owner)
        package=m.Package.objects.create(code='PK',barcode='BARCODE',lot=lot,work_card=card,source_execution=execution,
            piece_quantity=10,gross_mass_kg=81,tube_unit_tare_kg=Decimal('.01'),outer_tare_kg=Decimal('.9'),net_mass_basis='weighed_less_tare')
        m.PackageDispositionAllocation.objects.create(package=package,disposition=disposition,quantity=80,unit=self.kg)
        pkg_allocation=m.PackageOrderAllocation.objects.create(package=package,work_card_allocation=allocation,quantity=80,unit=self.kg)
        warehouse=base.Warehouse.objects.create(code='FIN',name='成品仓',kind='finished',factory=self.factory)
        location=base.StorageLocation.objects.create(code='BIN',name='成品库位',warehouse=warehouse,kind='bin')
        self.line.unit_price=Decimal('3.20');self.line.price_unit=self.kg;self.line.manual_price_reason='合同价格';self.line.save()
        return card,employee,package,pkg_allocation,disposition,warehouse,location

    def packed(self):
        values=self.prepare();card,employee,package,*_=values
        packing.pack(package,self.actor,at=self.now+timedelta(hours=7),employee=employee)
        lifecycle.complete_card(card,self.actor,at=self.now+timedelta(hours=8),reason='实际生产全部完成')
        return values

    def receive(self,package,warehouse,location,quantity,number):
        receipt=m.StockReceipt.objects.create(number=number,document_at=self.now+timedelta(hours=9),kind='finished_output',warehouse=warehouse)
        m.StockReceiptLine.objects.create(receipt=receipt,line_number=1,lot=package.lot,location=location,quantity=quantity,unit=self.kg,
            work_card=package.work_card,package=package,quality_state='released')
        stock.confirm(receipt,self.actor);stock.post(receipt,self.actor,self.now+timedelta(hours=10))
        return receipt

    def delivered(self):
        values=self.packed();card,employee,package,allocation,disposition,warehouse,location=values
        self.receive(package,warehouse,location,80,'IN')
        issue=m.StockIssue.objects.create(number='OUT',document_at=self.now+timedelta(hours=11),kind='delivery',warehouse=warehouse,destination_party=self.party)
        delivery=sales.Delivery.objects.create(number='DEL',document_at=self.now+timedelta(hours=11),customer=self.party,warehouse_issue=issue)
        line=sales.DeliveryLine.objects.create(delivery=delivery,line_number=1,order_line=self.line,package_allocation=allocation,quantity=80,unit=self.kg)
        row=m.StockIssueLine.objects.create(issue=issue,line_number=1,lot=package.lot,location=location,package=package,work_card=card,
            quantity=80,unit=self.kg,quality_state='released',delivery_line=line)
        fulfillment.confirm_delivery(delivery,self.actor);stock.confirm(issue,self.actor);stock.post(issue,self.actor,self.now+timedelta(hours=12))
        delivery.refresh_from_db();self.assertEqual(delivery.status,'issued')
        fulfillment.deliver(delivery,self.actor,at=self.now+timedelta(hours=13))
        return values,delivery,line,row

    def test_packing_exact_tare_scope_and_no_inventory_until_receipt(self):
        card,employee,package,allocation,disposition,warehouse,location=self.prepare()
        package.outer_tare_kg=None;package.save()
        with self.assertRaises(ValidationError):packing.pack(package,self.actor,at=self.now+timedelta(hours=7),employee=employee)
        package.outer_tare_kg=Decimal('.9');package.save()
        packing.pack(package,self.actor,at=self.now+timedelta(hours=7),employee=employee)
        package.refresh_from_db();self.assertEqual(package.net_mass_kg,Decimal('80'))
        self.assertEqual(m.InventoryMovement.objects.count(),0)
        self.assertEqual(package.packaging_execution.output_mass_kg,Decimal('80'))
        with self.assertRaises(ValidationError):quality.void(disposition.inspection,self.actor,reason='包装已采用',at=self.now+timedelta(hours=8))
        lifecycle.complete_card(card,self.actor,at=self.now+timedelta(hours=8),reason='实际完成')
        self.receive(package,warehouse,location,40,'IN1');self.receive(package,warehouse,location,40,'IN2')
        with self.assertRaises(ValidationError):self.receive(package,warehouse,location,1,'OVER')
        self.assertEqual(m.StockBalance.objects.get(package=package).quantity,80)

    def test_label_request_failure_and_reprint_keep_one_physical_package(self):
        card,employee,package,*_=self.packed()
        template=base.LabelTemplate.objects.create(code='LABEL',name='实用模板',version=2)
        package.refresh_from_db()
        package.label_template=template;package.save()
        packing.request_print(package,self.actor,at=self.now+timedelta(hours=9),employee=employee,copies=1)
        request=m.LabelPrint.objects.get();self.assertIsNone(request.printed_at);self.assertEqual(request.status,'requested')
        packing.confirm_print(request,self.actor,at=self.now+timedelta(hours=10),succeeded=False,reason='纸张未出')
        packing.request_print(package,self.actor,at=self.now+timedelta(hours=11),employee=employee,copies=1,previous=request,reason='更换纸张后重打')
        replacement=m.LabelPrint.objects.latest('pk');packing.confirm_print(replacement,self.actor,at=self.now+timedelta(hours=12),succeeded=True,reason='')
        request.refresh_from_db();self.assertEqual(request.status,'failed');self.assertIsNone(request.printed_at)
        self.assertEqual(m.Package.objects.count(),1);self.assertEqual(m.InventoryMovement.objects.count(),0)
        self.assertEqual(replacement.template_snapshot['template']['version'],2)

    def test_delivery_actual_stock_price_and_customer_return_pending(self):
        values,delivery,line,source=self.delivered()
        card,employee,package,allocation,disposition,warehouse,location=values
        line.refresh_from_db();delivery.refresh_from_db()
        self.assertEqual(line.unit_price_snapshot,Decimal('3.20'));self.assertEqual(delivery.status,'delivered')
        with self.assertRaises(ValidationError):stock.reverse(source.issue,self.actor,self.now+timedelta(hours=14),'先处理交付')
        receipt=m.StockReceipt.objects.create(number='RET-IN',document_at=self.now+timedelta(hours=14),kind='sales_return',warehouse=warehouse,source_party=self.party)
        receipt_row=m.StockReceiptLine.objects.create(receipt=receipt,line_number=1,lot=package.lot,location=location,package=package,
            work_card=card,quantity=10,unit=self.kg,quality_state='pending',original_issue_line=source)
        returned=sales.SalesReturn.objects.create(number='RET',customer=self.party,returned_at=self.now+timedelta(hours=14),reason='实际退回')
        sales.SalesReturnLine.objects.create(return_order=returned,original_delivery_line=line,original_issue_line=source,
            quantity=10,unit=self.kg,receipt_line=receipt_row,reopen_order_demand=True,reopen_reason='客户要求重新补交')
        fulfillment.confirm_return(returned,self.actor);stock.confirm(receipt,self.actor);stock.post(receipt,self.actor,self.now+timedelta(hours=15))
        returned.refresh_from_db();package.refresh_from_db()
        self.assertEqual(returned.status,'received');self.assertEqual(package.status,'returned')
        self.assertEqual(m.StockBalance.objects.get(package=package,quality_state='pending').quantity,10)
        self.assertEqual(fulfillment.reopened_quantity(self.line),10)
        with self.assertRaises(ValidationError):fulfillment.undo_delivery(delivery,self.actor,reason='已有真实退回')
        fulfillment.close_return(returned,self.actor,reason='实际退回已收完')
        with self.assertRaises(ValidationError):stock.reverse(receipt,self.actor,self.now+timedelta(hours=16),'须先重新办理退回')
        fulfillment.reopen_return(returned,self.actor,reason='更正原收回记录')
        stock.reverse(receipt,self.actor,self.now+timedelta(hours=17),'取消原实际收回')
        returned.refresh_from_db();self.assertEqual(returned.status,'confirmed')
        self.assertEqual(fulfillment.reopened_quantity(self.line),0)

    def test_api_pack_records_actual_package_and_legacy_id(self):
        card,employee,package,*_=self.prepare()
        response=self.client.post(f'/api/system/erp_warehouse_package/{package.pk}/pack/',
            {'at':(self.now+timedelta(hours=7)).isoformat(),'employee':employee.pk},format='json')
        self.assertEqual(response.status_code,200,response.data)
        self.assertEqual(response.data['data']['net_mass_kg'],'80.000000')
        self.assertIn('legacy_id',response.data['data'])

    def test_explicit_unfulfilled_demand_release_preserves_original_plan(self):
        card,employee,package,allocation,*_=self.packed()
        original=allocation.work_card_allocation
        with self.assertRaises(ValidationError):lifecycle.release_demand(original,self.actor,at=self.now+timedelta(hours=9),quantity=Decimal('21'),reason='超出未形成包装部分')
        lifecycle.release_demand(original,self.actor,at=self.now+timedelta(hours=9),quantity=Decimal('20'),reason='实际产出80，未完成20重新安排')
        original.refresh_from_db();self.assertEqual(original.allocated_quantity,100);self.assertEqual(original.released_unfulfilled_quantity,20)
        replacement=self.card(number='REPLACEMENT',quantity=20)
        self.assertEqual(self.allocate(replacement,20).allocated_quantity,20)

    def test_order_completion_requires_actual_delivery_and_close_keeps_shortfall(self):
        from plugins.erp_sales import services
        self.order.confirmed_at=self.now;self.order.save()
        values,delivery,line,source=self.delivered()
        with self.assertRaises(ValidationError):services.finish_order(self.order,self.actor,at=self.now+timedelta(hours=14),reason='仅交付80不能完成100')
        services.finish_order(self.order,self.actor,at=self.now+timedelta(hours=14),reason='客户终止未交付20',close=True)
        self.order.refresh_from_db();self.line.refresh_from_db();self.assertEqual(self.order.status,'closed');self.assertTrue(self.line.is_closed)
        self.assertEqual(self.line.ordered_quantity,100);self.assertEqual(line.quantity,80)
        services.reopen_order(self.order,self.actor,reason='客户恢复剩余需求')
        self.order.refresh_from_db();self.line.refresh_from_db();self.assertEqual(self.order.status,'running');self.assertFalse(self.line.is_closed)

    def test_reopen_completed_card_reopens_its_completed_batch(self):
        card,employee,package,*_=self.packed()
        batch=production.DyeBatch.objects.create(number='COMPLETE',factory=self.factory,status='completed')
        production.DyeBatchWorkCard.objects.create(batch=batch,work_card=card,sequence=1,quantity=100,unit=self.kg)
        lifecycle.reopen_card(card,self.actor,reason='原实际包装尚未入库，重新处理生产')
        card.refresh_from_db();batch.refresh_from_db()
        self.assertEqual(card.status,'running');self.assertEqual(batch.status,'running');self.assertIsNone(card.completed_at)

    def test_order_rework_inherits_source_demand_instead_of_adding_demand(self):
        card,employee,package,allocation,disposition,warehouse,location=self.prepare()
        quality.dispose(disposition.inspection,self.actor,kind='release',quantity=Decimal('60'),unit=self.kg,
            reason='更正实际可放行范围',employee=employee,at=self.now+timedelta(hours=7),supersedes=disposition)
        quality.dispose(disposition.inspection,self.actor,kind='rework',quantity=Decimal('20'),unit=self.kg,
            reason='其中20需要重新处理',employee=employee,at=self.now+timedelta(hours=7))
        rework_disposition=q.QualityDisposition.objects.get(kind='rework')
        order=production.ReworkOrder.objects.create(number='RW',original_work_card=card,disposition=rework_disposition,quantity=20,unit=self.kg,reason='原订单返修')
        with self.assertRaises(ValidationError):quality.release_rework(order,self.actor,number='RW-CARD',route_version=self.version,at=self.now+timedelta(hours=8))
        quality.release_rework(order,self.actor,number='RW-CARD',route_version=self.version,at=self.now+timedelta(hours=8),
            allocations=[{'original':allocation.work_card_allocation,'quantity':Decimal('20'),'unit':self.kg}])
        order.refresh_from_db()
        inherited=production.WorkCardOrderAllocation.objects.get(work_card=order.rework_work_card)
        self.assertEqual(inherited.original_allocation_id,allocation.work_card_allocation_id)
        self.assertEqual(inherited.order_line_id,self.line.pk)
        self.assertEqual(allocation.work_card_allocation.allocated_quantity,100)

    def test_rework_actual_execution_reinspection_and_completion_close(self):
        card,employee,package,allocation,disposition,warehouse,location=self.prepare()
        quality.dispose(disposition.inspection,self.actor,kind='rework',quantity=Decimal('20'),unit=self.kg,
            reason='整笔20实际返修',employee=employee,at=self.now+timedelta(hours=7),supersedes=disposition)
        source=q.QualityDisposition.objects.get(status='active')
        order=production.ReworkOrder.objects.create(number='RW',original_work_card=card,disposition=source,quantity=20,unit=self.kg,reason='重新松筒')
        route=base.Route.objects.create(code='RW',name='明确返修路线')
        version=base.RouteVersion.objects.create(route=route,version=1,status='active')
        base.RouteStep.objects.create(route_version=version,sequence=1,process=self.process,is_required=True)
        quality.release_rework(order,self.actor,number='RW-CARD',route_version=version,at=self.now+timedelta(hours=8),
            allocations=[{'original':allocation.work_card_allocation,'quantity':Decimal('20'),'unit':self.kg}])
        order.refresh_from_db();node=production.WorkCardOperation.objects.get(work_card=order.rework_work_card)
        actual.start(node,self.actor,at=self.now+timedelta(hours=9),employee=employee,machine=self.machine)
        execution=production.OperationExecution.objects.get(operation=node)
        actual.complete(execution,self.actor,at=self.now+timedelta(hours=10),**self.output('20'))
        inspection=write(q.QualityInspection,{'number':'RECHECK','work_card':order.rework_work_card,'execution':execution,'kind':'reinspection',
            'previous_inspection':disposition.inspection,'inspected_at':self.now+timedelta(hours=11),'inspected_quantity':Decimal('20'),'quantity_unit':self.kg},None,planning.POLICY)
        write(q.InspectionResultLine,{'inspection':inspection,'item_code':'RECHECK','item_name_snapshot':'实际复检','result':'pass'},None,planning.POLICY)
        quality.judge(inspection,self.actor,result='pass',employee=employee)
        quality.dispose(inspection,self.actor,kind='release',quantity=Decimal('20'),unit=self.kg,reason='实际复检放行',employee=employee,at=self.now+timedelta(hours=12))
        with self.assertRaises(ValidationError):quality.close_rework(order,self.actor,inspection=inspection,reason='生产未确认完成')
        lifecycle.complete_card(order.rework_work_card,self.actor,at=self.now+timedelta(hours=13),reason='返修实际全部完成')
        quality.close_rework(order,self.actor,inspection=inspection,reason='有效合格复检且生产已完成')
        order.refresh_from_db();self.assertEqual(order.status,'closed')
