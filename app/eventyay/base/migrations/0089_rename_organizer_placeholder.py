from django.db import migrations

from eventyay.helpers.placeholders import rename_placeholder


STORES = ('GlobalSettingsObject_SettingsStore', 'Organizer_SettingsStore', 'Event_SettingsStore')


def rename(apps, old, new):
    for store in STORES:
        model = apps.get_model('base', store)
        for setting in model.objects.filter(key__startswith='mail_', value__contains=old):
            value = rename_placeholder(setting.value, old, new)
            if value != setting.value:
                setting.value = value
                setting.save(update_fields=['value'])


def forwards(apps, schema_editor):
    rename(apps, 'organizer', 'organizer_name')


def backwards(apps, schema_editor):
    rename(apps, 'organizer_name', 'organizer')


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0088_invoicevoucher_applies_to_platform_fees_budget_used'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=backwards),
    ]
