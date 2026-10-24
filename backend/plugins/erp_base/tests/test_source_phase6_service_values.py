from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from plugins.erp_base import source_services as services
from plugins.erp_base.source_phase3_operations import model
from plugins.erp_base.source_phase6_service_values import RULES
from plugins.erp_base.source_phase6_auto_values import generated_fields
from plugins.erp_base.source_entry_registry import ENTRY_RULES
from plugins.erp_base.models import BusinessAction
from .source_fixtures import historical_batch


class ServiceValuesTests(TestCase):
    def setUp(self):self.actor=get_user_model().objects.create(username='service-values',is_superuser=True)

    def save(self,table,entry=None,parent=None,**values):
        m=model(table);data={m.SOURCE_FIELDS[k]:v for k,v in values.items()}
        if entry is not None:data['_entry']=entry
        if parent is not None:data['source_parent_1']=parent
        return services.write(m,data,actor=self.actor)

    def edit(self,item,**values):
        return services.write(type(item),{item.SOURCE_FIELDS[k]:v for k,v in values.items()},item,self.actor)

    def recipe(self,entry):
        head_entry=ENTRY_RULES[model('DyeRecipeDetail')._meta.label][entry]['master_entry']
        number='R'+str(list(RULES['DyeRecipeDetail']).index(entry))
        head=self.save('DyeRecipe',head_entry,SheetSeries=number,SheetNo=number)
        phase=self.save('DyeRecipePhase',entry,head,PhaseNo=1,BathRatio=7)
        detail=self.save('DyeRecipeDetail',entry,phase,StuffNo=1,Price=-2,Dosage=3,RecipeUnit=1,StuffType='A')
        return head,phase,detail

    def test_all_eight_recipe_entries_and_existing_cost_service(self):
        for entry in RULES['DyeRecipeDetail']:
            head,phase,detail=self.recipe(entry)
            expected=-42 if entry in ['BulkDyeRecipePhaseDetail','StandardDyeRecipePhaseDetail','FinishDyeRecipePhaseDetail'] else -6
            self.assertEqual(detail.old_amount,expected)
            head.refresh_from_db();self.assertEqual(head.old_cost,expected)
            detail=self.edit(detail,Dosage=-1,Amount=None)
            self.assertIsNone(detail.old_amount)
            head.refresh_from_db();self.assertIsNone(head.old_cost)
            if entry=='DyeRecipePhaseDetail':
                detail=self.edit(detail,RecipeUnit=0,StuffType='Z')
                self.assertIsNone(detail.old_amount)

    def test_parent_bath_ratio_refreshes_exact_link_and_keeps_duplicate_rows(self):
        head,phase,first=self.recipe('BulkDyeRecipePhaseDetail')
        second=self.save('DyeRecipeDetail','BulkDyeRecipePhaseDetail',phase,StuffNo=1,Price=2,Dosage=1,RecipeUnit=1)
        independent=self.save('DyeRecipeDetail','BulkDyeRecipePhaseDetail',phase,StuffNo=1,Price=2,Dosage=1,RecipeUnit=0)
        unrelated=self.save('DyeRecipePhase','BulkDyeRecipePhaseDetail',head,PhaseNo=2,BathRatio=9)
        other=self.save('DyeRecipeDetail','BulkDyeRecipePhaseDetail',unrelated,StuffNo=1,Price=2,Dosage=1,RecipeUnit=1)
        self.edit(phase,BathRatio=5)
        for row in [first,second,independent,other]:row.refresh_from_db()
        self.assertEqual([r.old_amount for r in [first,second,independent,other]],[-30,10,20,18])
        self.assertEqual(type(first).objects.filter(source_parent_1=phase,old_stuff_no=1).count(),3)
        head.refresh_from_db();self.assertEqual(head.old_cost,18)
        self.assertEqual(BusinessAction.objects.filter(action='entry_parent_formula_refresh').count(),2)

    def test_duplicate_phase_original_cost_multiplicity_is_retained(self):
        head,phase,first=self.recipe('DyeRecipePhaseDetail')
        duplicate=self.save('DyeRecipePhase','DyeRecipePhaseDetail',head,PhaseNo=1,BathRatio=4)
        second=self.save('DyeRecipeDetail','DyeRecipePhaseDetail',duplicate,StuffNo=1,Price=2,Dosage=1)
        head.refresh_from_db()
        self.assertEqual(head.old_cost,-8)  # 原SheetSeries+PhaseNo连接：每阶段均汇总-6+2。
        from plugins.erp_base.source_entry_calculations import entry_values
        self.assertEqual(entry_values(head,'BulkDyeRecipe')['old_cost'],-8)
        self.assertEqual(entry_values(head,'FinishDyeRecipe')['old_cost'],-8)
        self.assertEqual(entry_values(head,'TrialDyeRecipe')['old_cost'],-8)
        from tools.development_archive.customer_boundary_20261024.backend.source_phase6_expressions import evaluate
        from .test_source_phase6 import reader
        self.assertEqual(evaluate(head,'BulkDyeRecipe',reader)['changes']['old_cost'],-8)
        limited=lambda name,module:reader(name,module).exclude(pk=duplicate.pk) if name=='DyeRecipePhase' else reader(name,module)
        self.assertEqual(evaluate(head,'BulkDyeRecipe',limited)['changes']['old_cost'],-4)
        self.assertEqual(type(phase).objects.filter(source_parent_1=head).count(),2)
        self.assertEqual(type(first).objects.count(),2)

    def test_orphan_parent_formula_retains_row_then_explicit_link_calculates(self):
        row=self.save('DyeRecipeDetail','BulkDyeRecipePhaseDetail',SheetSeries='ORPHAN',PhaseNo=1,StuffNo=1,Price=2,Dosage=3,RecipeUnit=1)
        self.assertIsNone(row.old_amount)
        self.assertTrue(BusinessAction.objects.filter(object_id=row.pk,entity=row._meta.label,action='entry_formula_source_pending').exists())
        head=self.save('DyeRecipe','BulkDyeRecipe',SheetSeries='ORPHAN',SheetNo='ORPHAN')
        phase=self.save('DyeRecipePhase','BulkDyeRecipePhaseDetail',head,PhaseNo=1,BathRatio=4)
        row=services.write(type(row),{'source_parent_1':phase},row,self.actor)
        self.assertEqual(row.old_amount,24)

    def test_two_curve_entries_parent_change_and_explicit_null(self):
        for entry,parent_entry in [('p_DyeCurveDetail','p_DyeCurve'),('p_DyeCurveDetailJJ','p_DyeCurveJJ')]:
            head=self.save('p_DyeCurve',parent_entry,CurveID=parent_entry[-2:],MaxValue=3)
            detail=self.save('p_DyeCurveDetail',entry,head,StepNo=1,DefaultValue=-2)
            duplicate=self.save('p_DyeCurveDetail',entry,head,StepNo=1,DefaultValue=-2)
            self.assertEqual(detail.old_price,-6)
            self.edit(head,MaxValue=4)
            detail.refresh_from_db();duplicate.refresh_from_db()
            self.assertEqual((detail.old_price,duplicate.old_price),(-8,-8))
            detail=self.edit(detail,DefaultValue=7,Price=None);self.assertIsNone(detail.old_price)
            self.edit(head,MaxValue=None)
            duplicate.refresh_from_db();self.assertIsNone(duplicate.old_price)

    def test_five_job_quantity_variants_preserve_null_and_unusual_unit(self):
        for entry in RULES['JobGrayRecord']:
            row=self.save('JobGrayRecord',entry,SheetSeries=entry,GrayBarCode='SAME',WeightQty=-10,GUnit=None)
            self.assertEqual((row.old_kg,row.old_pound),(Decimal('-4.54'),Decimal('-22.05')))
            row=self.edit(row,GUnit=3)
            self.assertEqual((row.old_kg,row.old_pound),(Decimal('-4.54'),Decimal('-10')))
            row=self.edit(row,GUnit=9,Kg=None)
            self.assertIsNone(row.old_kg);self.assertEqual(row.old_pound,Decimal('-22.05'))

    def test_defective_units_have_original_distinct_null_defaults(self):
        row=self.save('DefectiveOutRecord','DefectiveOutRecord',GrayQty=-10,WeightQty=-10,GUnit=None,PUnit=None)
        self.assertEqual((row.old_gkg,row.old_gpound,row.old_pkg,row.old_ppound),(-10,-10,Decimal('-4.54'),Decimal('-22.05')))
        row=self.edit(row,GrayQty=None,WeightQty=None)
        self.assertEqual((row.old_gkg,row.old_gpound,row.old_pkg,row.old_ppound),(None,None,None,None))

    def test_fixed_price_detail_sum_no_unrelated_recalculation(self):
        row=self.save('QuoteDetail','FixedPriceDetail',SheetSeries='Q',DetailNo='DUP',Width=1,Weight=1,Price=-2,ProcessPrice=3)
        self.assertEqual(row.old_pricesum,1)
        row=self.edit(row,Price=4,Pricesum=None);self.assertIsNone(row.old_pricesum)
        row=self.edit(row,Remarks='保持空值');self.assertIsNone(row.old_pricesum)
        row=self.edit(row,ProcessPrice=2);self.assertEqual(row.old_pricesum,6)

    def test_historical_child_is_not_rewritten_by_parent_edit(self):
        head=self.save('p_DyeCurve','p_DyeCurve',CurveID='H',MaxValue=2)
        child=model('p_DyeCurveDetail').objects.create(source_parent_1=head,old_curve_id='H',old_step_no=1,old_default_value=3,old_price=-99,source_batch=historical_batch(),source_row=1)
        self.edit(head,MaxValue=4)
        child.refresh_from_db();self.assertEqual(child.old_price,-99)

    def test_parent_refresh_failure_rolls_back_all_rows_without_clipping(self):
        head=self.save('p_DyeCurve','p_DyeCurve',CurveID='OVERFLOW',MaxValue=1)
        first=self.save('p_DyeCurveDetail','p_DyeCurveDetail',head,StepNo=1,DefaultValue=2)
        second=self.save('p_DyeCurveDetail','p_DyeCurveDetail',head,StepNo=1,DefaultValue=999999)
        with self.assertRaises(ValidationError):self.edit(head,MaxValue=2)
        for row in [head,first,second]:row.refresh_from_db()
        self.assertEqual((head.old_max_value,first.old_price,second.old_price),(1,2,999999))
        self.assertFalse(BusinessAction.objects.filter(action='entry_parent_formula_refresh').exists())

    def test_registry_targets_exist_on_correct_physical_model(self):
        for table,entries in RULES.items():
            m=model(table)
            for entry,fields in entries.items():
                for target,inputs in fields.items():
                    self.assertIn(target,ENTRY_RULES[m._meta.label][entry]['formula_fields'])
                    self.assertIn(target,generated_fields(entry,m.__name__))
                    self.assertTrue(set(inputs)<=set(m.SOURCE_FIELDS))
        self.assertNotIn('Amount',generated_fields('BulkDyeRecipePhaseDetail','SourceDyeDyeRecipePhase'))
