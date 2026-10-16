from django.db import migrations
from ._source_provenance_20261016 import preserve_sources, remove_menu_columns

class Migration(migrations.Migration):
    dependencies = [('erp_base', '0027_foundation_platform_sources'), ('erp_production', '0021_shared_business_sources'), ('erp_purchase', '0010_legacy_collation_lookup_indexes'), ('erp_quality', '0012_shared_business_sources'), ('erp_sales', '0017_shared_business_sources'), ('erp_sampling', '0010_original_lookup_index_names'), ('erp_warehouse', '0015_original_lookup_index_names')]

    operations = [migrations.RunPython(preserve_sources,migrations.RunPython.noop),migrations.RunPython(remove_menu_columns,migrations.RunPython.noop)]
