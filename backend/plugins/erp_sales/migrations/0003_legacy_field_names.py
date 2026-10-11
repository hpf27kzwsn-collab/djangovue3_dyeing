from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('erp_sales', '0002_initial'),
    ]

    operations = [
        migrations.RenameField('salesorder', 'contact_name', 'brand_name'),
        migrations.RenameField('salesorderline', 'quality_requirements', 'intended_use'),
        migrations.RenameField('salesorderline', 'packaging_requirements', 'special_requirements'),
        migrations.RenameField('salesorderline', 'due_at', 'dyeing_due_at'),
    ]
