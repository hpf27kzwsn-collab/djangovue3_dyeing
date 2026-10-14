import json
from pathlib import Path

ENTRY_RULES = json.loads(Path(__file__).with_name('source_entry_rules.json').read_text(encoding='utf8'))['models']


def entry_options(model):
    return [{'value': name, 'label': rule['title']} for name, rule in ENTRY_RULES.get(model._meta.label, {}).items()]
