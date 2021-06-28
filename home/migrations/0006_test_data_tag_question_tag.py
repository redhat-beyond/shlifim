from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [("home", "0005_test_data_answer")]

    def generate_data(apps, schema_editor):
        from home.models import Tag, Question_Tag, Question

        tag_test_data = [
            "Pitagoras",
            "5th_Grade",
            "Bagrut_Exam",
            "Hebrew",
            "benny_goren",
            "need_help",
            "algebra",
            "java",
            "god",
            "python",
            "csharp",
            "geometry",
            "all_my_sons",
            "israel",
            "the_holocaust",
            "urgent",
            "trigonometry",
            "Bagrut",
            "1984_book",
            "novel",
        ]

        question_tag_test_data = [
            ("8", "Pitagoras"),
            ("8", "5th_Grade"),
            ("2", "5th_Grade"),
            ("2", "Pitagoras"),
            ("2", "Bagrut_Exam"),
            ("14", "Hebrew"),
            ("14", "Bagrut_Exam"),
            ("8", "algebra"),
            ("1", "Bagrut"),
            ("3", "urgent"),
            ("5", "urgent"),
            ("6", "all_my_sons"),
            ("6", "urgent"),
            ("6", "israel"),
            ("7", "novel"),
            ("9", "1984_book"),
            ("10", "csharp"),
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
            ("31", "csharp"),
            ("32", "israel"),
            ("33", "Bagrut"),
            ("33", "algebra"),
            ("34", "csharp"),
            ("36", "god"),
            ("38", "israel"),
            ("38", "csharp"),
            ("40", "trigonometry"),
            ("40", "python"),
            ("40", "israel"),
            ("41", "java"),
            ("42", "java"),
            ("42", "god"),
            ("43", "java"),
            ("43", "algebra"),
            ("44", "csharp"),
            ("44", "java"),
            ("45", "trigonometry"),
            ("45", "python"),
            ("48", "urgent"),
            ("48", "Bagrut"),
            ("48", "java"),
            ("49", "god"),
            ("49", "csharp"),
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
            for question_id, tag_name in question_tag_test_data:
                curr_tag = Tag.objects.filter(tag_name=tag_name)
                curr_question = Question.objects.filter(id=question_id)
                Question_Tag(question=curr_question[0], tag=curr_tag[0]).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
