from django.db import migrations

from eventyay.helpers.placeholders import rename_placeholder


STORES = ('GlobalSettingsObject_SettingsStore', 'Organizer_SettingsStore', 'Event_SettingsStore')


def rename_organizer_placeholder(apps, schema_editor):
    for store in STORES:
        model = apps.get_model('base', store)
        for setting in model.objects.filter(key__startswith='mail_', value__contains='{organizer}'):
            setting.value = rename_placeholder(setting.value, 'organizer', 'organizer_name')
            setting.save(update_fields=['value'])


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0088_invoicevoucher_applies_to_platform_fees_budget_used'),
    ]

    operations = [
        migrations.RunPython(rename_organizer_placeholder, reverse_code=migrations.RunPython.noop),
    ]
