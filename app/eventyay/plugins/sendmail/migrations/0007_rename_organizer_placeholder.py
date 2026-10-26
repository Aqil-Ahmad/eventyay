from django.db import migrations
from i18nfield.strings import LazyI18nString

from eventyay.helpers.placeholders import rename_placeholder


FIELDS = {'TicketMailTemplate': ('subject', 'text'), 'EmailQueue': ('subject', 'message')}


def renamed(value):
    data = value.data if isinstance(value, LazyI18nString) else value
    if isinstance(data, dict):
        return LazyI18nString(
            {lang: rename_placeholder(text, 'organizer', 'organizer_name') for lang, text in data.items()}
        )
    if isinstance(data, str):
        return LazyI18nString(rename_placeholder(data, 'organizer', 'organizer_name'))
    return value


def rename_organizer_placeholder(apps, schema_editor):
    for model_name, fields in FIELDS.items():
        model = apps.get_model('sendmail', model_name)
        for row in model.objects.all().iterator():
            changed = []
            for field in fields:
                value = getattr(row, field)
                if value and '{organizer}' in str(value.data if isinstance(value, LazyI18nString) else value):
                    setattr(row, field, renamed(value))
                    changed.append(field)
            if changed:
                row.save(update_fields=changed)


class Migration(migrations.Migration):
    dependencies = [
        ('sendmail', '0006_ticketmailtemplate'),
    ]

    operations = [
        migrations.RunPython(rename_organizer_placeholder, reverse_code=migrations.RunPython.noop),
    ]
