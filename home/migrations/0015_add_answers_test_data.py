from django.db import migrations, transaction
from datetime import datetime


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0014_auto_20210425_2055'),
    ]

    def create_answers_test_data(apps, schema_editor):
        from home.models import Profile, Question, Answer

        answer_test_data = [(2, 1, 'This is an old Answer',
                            datetime(2019, 5, 3), 1, 2, False),
                            (1, 1, 'This is an popular Answer',
                            datetime(2021, 1, 3), 100, 3, False),
                            (3, 1, 'The answer is 2 for sure. I have master degree in Math from Harvard',
                            datetime(2021, 2, 14), 5, 1, False),
                            (4, 1, '1+1 = 2. Simple algebra.',
                            datetime(2021, 4, 14), 5, 1, False),
                            (2, 14, 'Old Answer',
                            datetime(2019, 5, 3), 1, 2, False),
                            (1, 14, 'Popular Answer',
                            datetime(2021, 1, 3), 100, 3, False),
                            (3, 14, 'Answer A',
                            datetime(2021, 2, 14), 5, 1, False),
                            (4, 14, 'Answer B',
                            datetime(2021, 4, 14), 5, 1, False),
                            ]

        with transaction.atomic():

            for user_id, question, content, publish_date, likes_count, dislikes_count, is_edited in answer_test_data:
                curr_question = Question.objects.get(id=question)
                profile = Profile.objects.get(user=user_id)
                Answer(profile=profile, question=curr_question, content=content, publish_date=publish_date,
                       likes_count=likes_count, dislikes_count=dislikes_count, is_edited=is_edited).save()

    def create_tags_test_data(apps, schema_editor):
        from home.models import Tag, Question_Tag, Question
        question_tag_test_data = [
            ('Question', 'Pitagoras'),
            ('Question', '5th_Grade'),
            ('question from math course', '5th_Grade'),
            ('question from math course', 'Pitagoras'),
            ('question from bible course', 'Bagrut_Exam'),
            ('g forwards, it was even later than', 'Hebrew'),
            ('g forwards, it was even later than', 'Bagrut_Exam')
        ]

        with transaction.atomic():
            # Create Question_Tag objects
            for title, tag_name in question_tag_test_data:
                curr_tag = Tag.objects.filter(tag_name=tag_name)
                curr_question = Question.objects.filter(title=title)
                Question_Tag(question=curr_question[0], tag=curr_tag[0]).save()

    operations = [
        migrations.RunPython(create_answers_test_data),
        migrations.RunPython(create_tags_test_data),
    ]