from django.db import migrations, transaction
from home.models import Tag, Question_Tag, Question


class Migration(migrations.Migration):
    dependencies = [("home", "0017_alter_question_content")]

    def generate_data(apps, schema_editor):

        tag_test_data = [
            "benny_goren",
            "need_help",
            "algebra",
            "java",
            "god",
            "python",
            "c#",
            "geometry",
            "all_my_sons",
            "israel",
            "the_holocaust",
            "urgent",
            "trigonometry",
            "Bagrut",
            "1948_book",
            "novel",
        ]
        question_tag_test_data = [
            ("8", "algebra"),
            ("1", "Bagrut"),
            ("3", "urgent"),
            ("5", "urgent"),
            ("6", "all_my_sons"),
            ("6", "urgent"),
            ("6", "israel"),
            ("7", "novel"),
            ("9", "1948_book"),
            ("10", "c#"),
            ("10", "the_holocaust"),
            ("11", "geometry"),
            ("11", "urgent"),
            ("11", "benny_goren"),
            ("13", "all_my_sons"),
            ("14", "java"),
            ("14", "all_my_sons"),
            ("15", "israel"),
            ("16", "israel"),
            ("20", "benny_goren"),
            ("20", "all_my_sons"),
            ("22", "need_help"),
            ("22", "java"),
            ("22", "algebra"),
            ("25", "algebra"),
            ("25", "geometry"),
            ("26", "python"),
            ("28", "python"),
            ("28", "trigonometry"),
            ("29", "the_holocaust"),
            ("29", "algebra"),
            ("29", "israel"),
            ("31", "the_holocaust"),
            ("31", "java"),
            ("31", "c#"),
            ("32", "israel"),
            ("33", "Bagrut"),
            ("33", "algebra"),
            ("34", "c#"),
            ("36", "god"),
            ("38", "israel"),
            ("38", "c#"),
            ("40", "trigonometry"),
            ("40", "python"),
            ("40", "israel"),
            ("41", "java"),
            ("42", "java"),
            ("42", "god"),
            ("43", "java"),
            ("43", "algebra"),
            ("44", "c#"),
            ("44", "java"),
            ("45", "trigonometry"),
            ("45", "python"),
            ("48", "urgent"),
            ("48", "Bagrut"),
            ("48", "java"),
            ("49", "god"),
            ("49", "c#"),
            ("49", "python"),
            ("51", "java"),
            ("54", "the_holocaust"),
            ("58", "god"),
            ("59", "python"),
        ]

        with transaction.atomic():
            # Create Tag objects
            for tag_name in tag_test_data:
                Tag(tag_name=tag_name).save()
            # Create Question_Tag objects
            for id, tag_name in question_tag_test_data:
                curr_tag = Tag.objects.get(tag_name=tag_name)
                curr_question = Question.objects.get(id=id)
                Question_Tag(question=curr_question, tag=curr_tag).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
