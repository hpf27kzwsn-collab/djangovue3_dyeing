from datetime import timedelta
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from system.models import Users, Role, RoleMenuButtonPermission
from plugins.erp_base import models as base
from plugins.erp_sales import models as sales
from plugins.erp_sampling import models as sampling
from plugins.erp_base.business import write
from . import models as m, services as s


class ProductionPlanningTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('init_data', verbosity=0)
        cls.actor = Users.objects.get(username='superadmin')
        cls.kg = base.Unit.objects.create(code='kg',name='千克',dimension='mass',factor_to_base=1,decimal_places=6)
        cls.litre = base.Unit.objects.create(code='L',name='升',dimension='volume',factor_to_base=1,decimal_places=6)
        cls.gram = base.Unit.objects.create(code='g',name='克',dimension='mass',base_unit=cls.kg,factor_to_base=Decimal('.001'),decimal_places=3)
        cls.factory = base.Factory.objects.create(code='F',name='工厂')
        cls.material = base.Material.objects.create(code='Y',name='纱线',kind='yarn',stock_unit=cls.kg)
        cls.chemical = base.Material.objects.create(code='D',name='染料',kind='chemical',stock_unit=cls.gram)
        cls.party = base.Party.objects.create(code='C',name='客户')
        cls.process = base.Process.objects.create(code='GX01',name='松筒',is_active=True)
        cls.optional = base.Process.objects.create(code='GX02',name='翻松',is_active=True)
        cls.final = base.Process.objects.create(code='GX03',name='染色',is_active=True)
        route = base.Route.objects.create(code='RT01',name='路线')
        cls.version = base.RouteVersion.objects.create(route=route,version=1,status='active')
        cls.first = base.RouteStep.objects.create(route_version=cls.version,sequence=1,process=cls.process,is_required=True)
        cls.middle = base.RouteStep.objects.create(route_version=cls.version,sequence=2,process=cls.optional,is_required=False,predecessor=cls.first)
        cls.last = base.RouteStep.objects.create(route_version=cls.version,sequence=3,process=cls.final,is_required=True,predecessor=cls.middle)
        cls.machine = base.Machine.objects.create(code='M',name='机台',factory=cls.factory,is_active=True,load_capacity_kg=200)
        base.MachineProcess.objects.create(machine=cls.machine,process=cls.process,is_active=True)
        base.MachineProcess.objects.create(machine=cls.machine,process=cls.final,is_active=True)
        cls.now = timezone.now()
        cls.order = sales.SalesOrder.objects.create(number='SO',document_at=cls.now,customer=cls.party,status='confirmed')
        cls.line = sales.SalesOrderLine.objects.create(order=cls.order,line_number=1,material=cls.material,
            ordered_quantity=100,ordered_unit=cls.kg)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.actor)

    def card(self, number='WC',quantity=100,manual=False):
        return m.WorkCard.objects.create(number=number,document_at=self.now,factory=self.factory,material=self.material,
            route_version=self.version,planned_quantity=quantity,quantity_unit=self.kg,manual_creation_reason='人工授权独立加工' if manual else '')

    def allocate(self, card, quantity=100):
        return write(m.WorkCardOrderAllocation,{'work_card':card,'order_line':self.line,'allocated_quantity':Decimal(quantity),'unit':self.kg},None,s.POLICY)

    def release(self, card):
        s.prepare(card,self.actor,[self.first,self.last])
        return s.release(card,self.actor,at=self.now+timedelta(minutes=1))

    def batch(self,card,number='B'):
        batch=m.DyeBatch.objects.create(number=number,factory=self.factory,planned_mass_kg=100)
        member=write(m.DyeBatchWorkCard,{'batch':batch,'work_card':card,'sequence':1,'quantity':card.planned_quantity,'unit':self.kg},None,s.POLICY)
        for source in m.WorkCardOrderAllocation.objects.filter(work_card=card):
            write(m.DyeBatchAllocation,{'batch_work_card':member,'work_card_allocation':source,'quantity':source.allocated_quantity,'unit':self.kg},None,s.POLICY)
        return batch

    def recipe(self,basis='owf_percent',ratio_basis='volume_per_mass'):
        recipe=sampling.Recipe.objects.create(code='R',name='配方',material=self.material,is_active=True,purpose='standard')
        version=sampling.RecipeVersion.objects.create(recipe=recipe,status='approved')
        stage=sampling.RecipeStage.objects.create(version=version,sequence=1,bath_ratio=10,bath_ratio_basis=ratio_basis)
        sampling.RecipeIngredient.objects.create(stage=stage,sequence=1,material=self.chemical,dosage=2,dosage_basis=basis)
        return version,stage

    def inputs(self, stage, **extra):
        return [{'stage':stage,'water_amount':None,'water_unit':None,'density':None,'adjustment_percent':Decimal('0'),**extra}]

    def test_optional_step_bypass_and_frozen_parameter_snapshot(self):
        card=self.card()
        self.allocate(card)
        sales.SalesLineRequirement.objects.create(order_line=self.line,namespace='packing',requirement_code='P1',name='包装',value_text='袋装')
        self.line.special_requirements = '保留原特殊要求'
        self.line.save()
        self.release(card)
        operations=list(m.WorkCardOperation.objects.filter(work_card=card).order_by('sequence'))
        self.assertEqual([o.sequence for o in operations],[1,3])
        self.assertEqual(operations[1].predecessor_id,operations[0].pk)
        self.assertEqual(m.WorkCardRequirement.objects.get(work_card=card).value_text,'袋装')
        allocation = m.WorkCardOrderAllocation.objects.get(work_card=card)
        self.line.special_requirements = '后续变更'
        self.line.save()
        self.assertEqual(allocation.adopted_order_snapshot['special_requirements'], '保留原特殊要求')
        self.last.standard_minutes=99;self.last.save()
        self.assertIsNone(operations[1].planned_minutes)
        with self.assertRaises(ValidationError):
            write(m.OperationParameter,{'operation':operations[0],'sequence':1,'name':'温度'},None,s.POLICY)

    def test_order_split_allocation_and_cancel_releases_demand(self):
        first=self.card('W1',60);second=self.card('W2',50)
        self.allocate(first,60)
        with self.assertRaises(ValidationError):self.allocate(second,50)
        self.assertEqual(m.WorkCardOrderAllocation.objects.count(),1)
        s.cancel(first,self.actor,reason='取消原投产')
        self.allocate(second,50)

    def test_release_requires_complete_allocation_or_manual_reason(self):
        card=self.card()
        s.prepare(card,self.actor,[self.first,self.last])
        with self.assertRaises(ValidationError):s.release(card,self.actor,at=self.now+timedelta(minutes=1))
        self.allocate(card,50)
        with self.assertRaises(ValidationError):s.release(card,self.actor,at=self.now+timedelta(minutes=1))
        manual=self.release(self.card('M1',manual=True))
        self.assertEqual(manual.status,'released')

    def test_manual_schedule_replacement_keeps_history_and_adjacent_slots(self):
        first=self.release(self.card('W1',manual=True))
        second=self.release(self.card('W2',manual=True))
        op=m.WorkCardOperation.objects.get(work_card=first,sequence=1)
        op2=m.WorkCardOperation.objects.get(work_card=second,sequence=1)
        start=self.now+timedelta(hours=1);end=start+timedelta(hours=1)
        s.schedule(op,self.actor,machine=self.machine,planned_start=start,planned_end=end)
        with self.assertRaises(ValidationError):s.schedule(op2,self.actor,machine=self.machine,planned_start=start,planned_end=end)
        s.schedule(op2,self.actor,machine=self.machine,planned_start=end,planned_end=end+timedelta(hours=1))
        old=m.ScheduleAssignment.objects.get(operation=op)
        new=s.reschedule(old,self.actor,machine=self.machine,planned_start=start-timedelta(minutes=20),planned_end=start,reason='插单后前移')
        old.refresh_from_db()
        self.assertEqual((old.status,new.version,new.previous_assignment_id),('replaced',2,old.pk))
        s.publish(new,self.actor)
        s.cancel_schedule(new,self.actor,reason='取消紧筒排单')
        self.assertEqual(m.ScheduleAssignment.objects.filter(operation=op).count(),2)

    def test_combined_batch_has_one_physical_slot(self):
        first=self.release(self.card('W1',50,manual=True));second=self.release(self.card('W2',50,manual=True))
        batch=self.batch(first)
        write(m.DyeBatchWorkCard,{'batch':batch,'work_card':second,'sequence':2,'quantity':Decimal('50'),'unit':self.kg},None,s.POLICY)
        op=m.WorkCardOperation.objects.get(work_card=first,sequence=3)
        op2=m.WorkCardOperation.objects.get(work_card=second,sequence=3)
        start=self.now+timedelta(hours=1)
        s.schedule(op,self.actor,machine=self.machine,planned_start=start,planned_end=start+timedelta(hours=2),batch=batch)
        with self.assertRaises(ValidationError):s.schedule(op2,self.actor,machine=self.machine,planned_start=start+timedelta(hours=3),planned_end=start+timedelta(hours=4),batch=batch)
        self.assertEqual(m.ScheduleAssignment.objects.filter(batch=batch).count(),1)

    def test_recipe_adoption_calculates_units_and_preserves_replaced_snapshot(self):
        card=self.card();self.allocate(card);card=self.release(card);batch=self.batch(card)
        version,stage=self.recipe()
        s.adopt_recipe(batch,self.actor,recipe_version=version,at=self.now+timedelta(hours=1),dry_mass_kg=Decimal('100'),stages=self.inputs(stage))
        first=m.ProductionRecipe.objects.get(batch=batch)
        plan=m.MaterialPlanLine.objects.get(stage__production_recipe=first)
        self.assertEqual(plan.required_quantity,Decimal('2000'))
        self.assertEqual(Decimal(plan.calculation_snapshot['chemical_mass_kg']),Decimal('2'))
        s.adopt_recipe(batch,self.actor,recipe_version=version,at=self.now+timedelta(hours=2),dry_mass_kg=Decimal('100'),stages=self.inputs(stage,adjustment_percent=Decimal('10')))
        first.refresh_from_db();plan.refresh_from_db()
        self.assertEqual(first.status,'replaced');self.assertEqual(plan.required_quantity,Decimal('2000'))
        self.assertEqual(m.MaterialPlanLine.objects.get(stage__production_recipe__status='active').required_quantity,Decimal('2200'))
        with self.assertRaises(ValidationError):write(m.DyeBatchWorkCard,{'batch':batch,'work_card':card,'sequence':2,'quantity':1,'unit':self.kg},None,s.POLICY)

    def test_mass_bath_g_per_l_requires_density_and_rolls_back_adoption(self):
        card=self.release(self.card(manual=True));batch=self.batch(card)
        version,stage=self.recipe('g_per_litre','mass_per_mass')
        with self.assertRaises(ValidationError):s.adopt_recipe(batch,self.actor,recipe_version=version,at=self.now+timedelta(hours=1),dry_mass_kg=Decimal('100'),stages=self.inputs(stage))
        self.assertEqual(m.ProductionRecipe.objects.count(),0)
        s.adopt_recipe(batch,self.actor,recipe_version=version,at=self.now+timedelta(hours=1),dry_mass_kg=Decimal('100'),stages=self.inputs(stage,density=Decimal('1.25')))
        self.assertEqual(m.MaterialPlanLine.objects.get().required_quantity,Decimal('1600'))

    def test_api_typed_stage_input_and_owned_state(self):
        card=self.release(self.card(manual=True));batch=self.batch(card);version,stage=self.recipe()
        url=f'/api/system/erp_production_dyebatch/{batch.pk}/adopt_recipe/'
        response=self.client.post(url,{'recipe_version':version.pk,'at':(self.now+timedelta(hours=1)).isoformat(),'dry_mass_kg':'100',
            'stages':[{'stage':stage.pk,'adjustment_percent':'0'}]},format='json')
        self.assertEqual(response.status_code,200,response.data)
        response=self.client.patch(f'/api/system/erp_production_workcard/{card.pk}/',{'status':'completed'},format='json')
        self.assertEqual(response.status_code,400,response.data)

    def test_selected_nodes_respect_related_data_permissions(self):
        card=self.card(manual=True)
        role=Role.objects.get(key='erp_production_manager')
        user=Users.objects.create_user(username='planner',password='test-password',dept=self.actor.dept)
        user.role.add(role)
        RoleMenuButtonPermission.objects.filter(role=role,menu_button__menu__component_name='erp_base_routestep').delete()
        self.client.force_authenticate(user)
        response=self.client.post(f'/api/system/erp_production_workcard/{card.pk}/prepare/',{'steps':[self.first.pk,self.last.pk]},format='json')
        self.assertEqual(response.status_code,400,response.data)
        self.assertEqual(m.WorkCardOperation.objects.count(),0)


from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from django.db import close_old_connections, connections
from django.test import TransactionTestCase, skipUnlessDBFeature


class ProductionConcurrencyTests(TransactionTestCase):
    def setUp(self):
        self.actor=Users.objects.create(username='production-actor',is_superuser=True)
        self.kg=base.Unit.objects.create(code='kg',name='千克',dimension='mass',factor_to_base=1,decimal_places=6)
        self.factory=base.Factory.objects.create(code='F',name='工厂')
        material=base.Material.objects.create(code='Y',name='纱线',kind='yarn',stock_unit=self.kg)
        party=base.Party.objects.create(code='C',name='客户')
        self.process=base.Process.objects.create(code='GX01',name='松筒',is_active=True)
        route=base.Route.objects.create(code='RT',name='路线')
        version=base.RouteVersion.objects.create(route=route,status='active')
        step=base.RouteStep.objects.create(route_version=version,sequence=1,process=self.process,is_required=True)
        self.machine=base.Machine.objects.create(code='M',name='机台',factory=self.factory,is_active=True)
        base.MachineProcess.objects.create(machine=self.machine,process=self.process,is_active=True)
        order=sales.SalesOrder.objects.create(number='SO',document_at=timezone.now(),customer=party,status='confirmed')
        self.line=sales.SalesOrderLine.objects.create(order=order,line_number=1,material=material,ordered_quantity=100,ordered_unit=self.kg)
        self.cards=[]
        for index in [1,2]:
            card=m.WorkCard.objects.create(number=str(index),document_at=timezone.now(),factory=self.factory,material=material,
                route_version=version,planned_quantity=70,quantity_unit=self.kg,manual_creation_reason='独立加工')
            s.prepare(card,self.actor,[step])
            self.cards.append(card)

    def race(self, callback):
        gate=Barrier(2)
        def run(key):
            close_old_connections()
            try:
                gate.wait(timeout=15)
                try:
                    callback(key)
                    return 'saved'
                except ValidationError:
                    return 'rejected'
            finally:connections['default'].close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            return list(pool.map(run,[card.pk for card in self.cards]))

    @skipUnlessDBFeature('has_select_for_update')
    def test_two_cards_cannot_allocate_same_remaining_order_demand(self):
        def allocate(key):
            write(m.WorkCardOrderAllocation,{'work_card':m.WorkCard.objects.get(pk=key),'order_line':sales.SalesOrderLine.objects.get(pk=self.line.pk),
                'allocated_quantity':Decimal('70'),'unit':base.Unit.objects.get(pk=self.kg.pk)},None,s.POLICY)
        self.assertEqual(sorted(self.race(allocate)),['rejected','saved'])
        self.assertEqual(m.WorkCardOrderAllocation.objects.count(),1)

    @skipUnlessDBFeature('has_select_for_update')
    def test_two_cards_cannot_schedule_same_machine_interval(self):
        for card in self.cards:s.release(card,self.actor,at=timezone.now())
        start=timezone.now()+timedelta(hours=1)
        def schedule(key):
            s.schedule(m.WorkCardOperation.objects.get(work_card_id=key),Users.objects.get(pk=self.actor.pk),
                machine=base.Machine.objects.get(pk=self.machine.pk),planned_start=start,planned_end=start+timedelta(hours=1))
        self.assertEqual(sorted(self.race(schedule)),['rejected','saved'])
        self.assertEqual(m.ScheduleAssignment.objects.count(),1)
