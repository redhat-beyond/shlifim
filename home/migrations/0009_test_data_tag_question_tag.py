from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0008_question_tag')
    ]

    def generate_data(apps, schema_editor):
        from home.models import Tag, Question_Tag, Question
        tag_test_data = [
            ('Pitagoras'),
            ('5th_Grade'),
            ('Bagrut_Exam'),
            ('Hebrew')
        ]
        question_tag_test_data = [
            ('Question from  Benny Goren Book', 'Pitagoras'),
            ('Question from  Benny Goren Book', 'Bagrut_Exam'),
            ('question about ants', '5th_Grade'),
            ('Need help', 'Hebrew')
        ]

        with transaction.atomic():
            # Create Tag objects
            for tag_name in tag_test_data:
                Tag(tag_name=tag_name).save()
            # Create Question_Tag objects
            for title, tag_name in question_tag_test_data:
                curr_tag = Tag.objects.filter(tag_name=tag_name)
                curr_question = Question.objects.filter(title=title)
                Question_Tag(question=curr_question[0], tag=curr_tag[0]).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
