from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('msgboard', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from msgboard.models import Message

        test_data = [
            ('Dor', 'This is a simple question - you take 1 and add another 1. The answer is 11.'),
            ('Liron', 'I am not sure I understand the question. Can you give more details?'),
        ]

        with transaction.atomic():
            for author, text in test_data:
                Message(author=author, text=text).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
