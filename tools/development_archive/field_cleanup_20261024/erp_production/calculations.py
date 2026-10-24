"""已明确计量基准的生产计算，未知事实保持为 None。"""
from decimal import Decimal

from django.core.exceptions import ValidationError

from plugins.erp_base.choices import DosageBasis


def calculate_adopted_dosage(original_dosage, adjustment_percent):
    if original_dosage is None or adjustment_percent is None:
        return None
    return original_dosage * (Decimal('1') + adjustment_percent / Decimal('100'))


def planned_chemical_mass_kg(dosage, basis, *, dry_mass_kg=None, bath_volume_l=None):
    """百分数以干料kg为基准；g/L以明确浴液体积L为基准。"""
    if basis == DosageBasis.OWF_PERCENT:
        if dosage is None or dry_mass_kg is None:
            return None
        return dry_mass_kg * dosage / Decimal('100')
    if basis == DosageBasis.G_PER_LITRE:
        if dosage is None or bath_volume_l is None:
            return None
        return dosage * bath_volume_l / Decimal('1000')
    raise ValidationError('必须明确选择剂量计算基准。')


def calculate_elapsed_minutes(started_at, ended_at):
    if started_at is None or ended_at is None:
        return None
    elapsed = ended_at - started_at
    if elapsed.total_seconds() < 0:
        raise ValidationError('结束时间不能早于开始时间。')
    seconds = Decimal(elapsed.days * 86400 + elapsed.seconds)
    seconds += Decimal(elapsed.microseconds) / Decimal('1000000')
    return seconds / Decimal('60')
