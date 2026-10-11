"""多轮打样、客户回复和版本冻结。"""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from plugins.erp_base.business import locked, persist, record, snapshot, require_state, require_rows
from . import models as m

PARENTS = {m.SampleLine: ('request', ''), m.SampleTrial: ('sample_line', ''),
           m.SampleConfirmation: ('sample_line', ''), m.RecipeVersion: ('recipe', ''),
           m.RecipeStage: ('version', ''), m.RecipeIngredient: ('stage', 'version'),
           m.ProcessCurveStep: ('curve_version', '')}
OWNED = {m.SampleRequest: {'status', 'received_at'}, m.SampleLine: {'status', 'assigned_employee'},
         m.SampleTrial: {'status', 'started_at', 'finished_at'},
         m.SampleConfirmation: {'result', 'sent_at', 'confirmed_at'}, m.Recipe: set(),
         m.RecipeVersion: {'status', 'approved_by', 'approved_at'}, m.RecipeStage: set(),
         m.RecipeIngredient: set(), m.ProcessCurveVersion: {'status'}, m.ProcessCurveStep: set()}


def editable(item):
    if isinstance(item, m.Recipe):
        if m.RecipeVersion.objects.filter(recipe=item).exclude(status='draft').exists():
            raise ValidationError({'recipe': '已有冻结版本，不能修改配方主体适用资料。'})
    elif isinstance(item, m.SampleLine):
        require_state(item.request, ['draft'])
    elif isinstance(item, m.SampleTrial):
        require_state(item, ['planned'])
    elif isinstance(item, m.SampleConfirmation):
        require_state(item, ['pending'], 'result')
        if item.sent_at is not None:
            raise ValidationError({'sent_at': '已送版记录通过客户回复操作维护。'})
    elif isinstance(item, m.RecipeStage):
        require_state(item.version, ['draft'])
    elif isinstance(item, m.RecipeIngredient):
        require_state(item.stage.version, ['draft'])
    elif isinstance(item, m.ProcessCurveStep):
        require_state(item.curve_version, ['draft'])
    else:
        require_state(item, ['draft'])


def parent_editable(model, root):
    if model in [m.SampleTrial, m.SampleConfirmation]:
        require_state(root, ['assigned', 'running', 'sent', 'rejected'])
    elif model is m.RecipeVersion:
        if not root.is_active:
            raise ValidationError({'recipe': '配方主体已停用。'})
    else:
        editable(root)


def validate(item):
    if isinstance(item, m.SampleTrial) and item.recipe_version_id is not None:
        version = item.recipe_version
        if version.recipe.material_id is not None and version.recipe.material_id != item.sample_line.material_id:
            raise ValidationError({'recipe_version': '试验配方物料不匹配。'})
        if version.recipe.customer_id is not None and version.recipe.customer_id != item.sample_line.request.customer_id:
            raise ValidationError({'recipe_version': '试验配方客户不匹配。'})
    if isinstance(item, m.RecipeStage) and item.curve_version_id is not None:
        require_state(item.curve_version, ['approved', 'active'])
    if isinstance(item, m.RecipeVersion) and item.original_version_id is not None:
        seen, cursor = {item.pk}, item.original_version
        while cursor is not None:
            if cursor.pk in seen:
                raise ValidationError({'original_version': '来源配方版本不能形成循环。'})
            seen.add(cursor.pk)
            cursor = cursor.original_version
    if isinstance(item, m.SampleLine) and item.original_sample_line_id == item.pk and item.pk is not None:
        raise ValidationError({'original_sample_line': '来源打样明细不能指向自身。'})


POLICY = {'parents': PARENTS, 'owned': OWNED, 'editable': editable,
          'parent_editable': parent_editable, 'validate': validate,
          'lock_root': lambda item: lock_line(item)[1] if isinstance(item, m.SampleLine) else locked(item),
          'deletable': editable}


def refresh_request(request, actor):
    statuses = set(m.SampleLine.objects.filter(request=request).values_list('status', flat=True))
    if statuses <= {'accepted', 'cancelled'}:
        request.status = 'confirmed'
    elif 'running' in statuses:
        request.status = 'running'
    elif 'sent' in statuses or 'rejected' in statuses:
        request.status = 'sent'
    elif 'assigned' in statuses or 'accepted' in statuses:
        request.status = 'assigned'
    else:
        request.status = 'received'
    persist(request, actor)


def lock_line(line):
    return locked(line.request), locked(line)


def refresh_line(line, actor):
    trial = m.SampleTrial.objects.filter(sample_line=line, status__in=['running', 'completed']).order_by('-trial_number').first()
    confirmation = m.SampleConfirmation.objects.filter(sample_line=line, trial=trial, sent_at__isnull=False).order_by('-sent_at', '-pk').first()
    line.status = 'running' if confirmation is None else 'sent' if confirmation.result == 'pending' else confirmation.result
    persist(line, actor)


@transaction.atomic
def receive(item, actor, at):
    item = locked(item)
    require_state(item, ['draft'])
    before = snapshot(item)
    require_rows(m.SampleLine.objects.filter(request=item))
    item.status, item.received_at = 'received', at
    persist(item, actor)
    record(item, 'receive', before, actor)
    return item


@transaction.atomic
def assign(item, actor, employee):
    request = locked(item.request)
    item = locked(item)
    require_state(request, ['received', 'assigned', 'running', 'sent'])
    require_state(item, ['pending', 'assigned', 'rejected'])
    before = snapshot(item)
    item.assigned_employee, item.status = employee, 'assigned'
    persist(item, actor)
    refresh_request(request, actor)
    record(item, 'assign', before, actor)
    return item


@transaction.atomic
def start_trial(item, actor, at):
    request, line = lock_line(item.sample_line)
    item = locked(item)
    require_state(line, ['assigned', 'running', 'rejected', 'sent'])
    require_state(item, ['planned'])
    if item.operator_id is None:
        raise ValidationError({'operator': '请明确本轮试验操作人员。'})
    before = snapshot(item)
    item.status, item.started_at = 'running', at
    persist(item, actor)
    line.status = 'running'
    persist(line, actor)
    refresh_request(request, actor)
    record(item, 'start', before, actor)
    return item


@transaction.atomic
def complete_trial(item, actor, at, result_text):
    request, line = lock_line(item.sample_line)
    item = locked(item)
    require_state(item, ['running'])
    before = snapshot(item)
    item.status, item.finished_at, item.result_text = 'completed', at, result_text
    persist(item, actor)
    record(item, 'complete', before, actor)
    return item


@transaction.atomic
def send(item, actor, at):
    request, line = lock_line(item.sample_line)
    item = locked(item)
    require_state(line, ['running', 'assigned', 'rejected', 'sent'])
    require_state(item, ['pending'], 'result')
    if item.sent_at is not None:
        raise ValidationError({'sent_at': '本记录已送版。'})
    if item.trial_id is None or item.trial.status != 'completed':
        raise ValidationError({'trial': '送版必须关联已完成的真实试验轮次。'})
    if at < item.trial.finished_at:
        raise ValidationError({'at': '送版时间不得早于试验完成时间。'})
    before = snapshot(item)
    item.sent_at = at
    persist(item, actor)
    refresh_line(line, actor)
    refresh_request(request, actor)
    record(item, 'send', before, actor)
    return item


@transaction.atomic
def reply(item, actor, result, at, customer_reply):
    request, line = lock_line(item.sample_line)
    item = locked(item)
    require_state(item, ['pending'], 'result')
    if item.sent_at is None or at < item.sent_at:
        raise ValidationError({'confirmed_at': '客户回复时间不得早于送版时间。'})
    before = snapshot(item)
    if result == 'accepted':
        if item.confirmed_recipe_id is None or item.confirmed_color_id is None:
            raise ValidationError({'confirmed_recipe': '确板必须明确确认色标准与配方版本。'})
        require_state(item.confirmed_recipe, ['approved', 'active'])
        if item.trial.recipe_version_id != item.confirmed_recipe_id:
            raise ValidationError({'confirmed_recipe': '确板配方必须对应所送试验的配方版本。'})
        color = locked(item.confirmed_color)
        if color.customer_id is not None and color.customer_id != line.request.customer_id:
            raise ValidationError({'confirmed_color': '确认色标准客户不匹配。'})
        if color.material_id is not None and color.material_id != line.material_id:
            raise ValidationError({'confirmed_color': '确认色标准物料不匹配。'})
        color.source_sample = line
        persist(color, actor)
    item.result, item.confirmed_at, item.customer_reply = result, at, customer_reply
    persist(item, actor)
    refresh_line(line, actor)
    refresh_request(request, actor)
    record(item, 'reply', before, actor, customer_reply)
    return item


@transaction.atomic
def version_transition(item, actor, target, employee=None):
    item = locked(item)
    require_state(item, {'approved': ['draft'], 'active': ['approved'], 'retired': ['approved', 'active']}[target])
    before = snapshot(item)
    if target == 'approved':
        if isinstance(item, m.RecipeVersion):
            for stage in require_rows(m.RecipeStage.objects.filter(version=item)):
                validate(stage)
                require_rows(m.RecipeIngredient.objects.filter(stage=stage))
            item.approved_by, item.approved_at = employee, timezone.now()
        else:
            require_rows(m.ProcessCurveStep.objects.filter(curve_version=item))
    item.status = target
    persist(item, actor)
    record(item, target, before, actor)
    return item


def copied_values(item):
    omitted = {'id', 'legacy_id', 'creator', 'modifier', 'dept_belong', 'create_datetime', 'update_datetime'}
    return {f.attname: f.value_from_object(item) for f in item._meta.fields if f.name not in omitted}


@transaction.atomic
def clone_version(item, actor):
    if isinstance(item, m.RecipeVersion):
        locked(item.recipe)
        item = locked(item)
        version = m.RecipeVersion.objects.filter(recipe=item.recipe).aggregate(value=Max('version'))['value'] + 1
        values = copied_values(item)
        values.update(version=version, status='draft', approved_by_id=None, approved_at=None,
                      original_version_id=item.pk, sample_trial_id=None, valid_from=None)
        clone = persist(m.RecipeVersion(**values), actor)
        for stage in m.RecipeStage.objects.filter(version=item).order_by('sequence'):
            values = copied_values(stage)
            values['version_id'] = clone.pk
            new_stage = persist(m.RecipeStage(**values), actor)
            for ingredient in m.RecipeIngredient.objects.filter(stage=stage).order_by('sequence'):
                values = copied_values(ingredient)
                values['stage_id'] = new_stage.pk
                persist(m.RecipeIngredient(**values), actor)
    else:
        list(m.ProcessCurveVersion.objects.select_for_update().filter(code=item.code).order_by('pk'))
        version = m.ProcessCurveVersion.objects.filter(code=item.code).aggregate(value=Max('version'))['value'] + 1
        values = copied_values(item)
        values.update(version=version, status='draft')
        clone = persist(m.ProcessCurveVersion(**values), actor)
        for step in m.ProcessCurveStep.objects.filter(curve_version=item).order_by('sequence'):
            values = copied_values(step)
            values['curve_version_id'] = clone.pk
            persist(m.ProcessCurveStep(**values), actor)
    record(clone, 'clone', snapshot(item), actor)
    return clone
