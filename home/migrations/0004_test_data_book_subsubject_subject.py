from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0003_book_sub_subject_subject"),
    ]

    def generate_data(apps, schema_editor):
        from home.models import Subject, Sub_Subject, Book

        subjects_test_data = [
            ("Bible"),
            ("Biology"),
            ("Chemistry"),
            ("English"),
            ("Geography"),
            ("Literature"),
            ("History"),
            ("Hebrew"),
            ("Math"),
            ("Physics"),
        ]
        sub_subjects_test_data = [
            ("Gensis", "Bible"),
            ("Kings in the Bible", "Bible"),
            ("Prophecies", "Bible"),
            ("Anatomy", "Biology"),
            ("Genetics", "Biology"),
            ("Cell Biology", "Biology"),
            ("Atomic Structure", "Chemistry"),
            ("Units and Measurement", "Chemistry"),
            ("Periodic Table", "Chemistry"),
            ("Essays", "English"),
            ("Grammer", "English"),
            ("English - Oral", "English"),
            ("Physical Geography", "Geography"),
            ("Human Geography", "Geography"),
            ("Atmosphere", "Geography"),
            ("Medieval", "Literature"),
            ("17th Century", "Literature"),
            ("20th Century", "Literature"),
            ("Writing", "Hebrew"),
            ("Text analysis", "Hebrew"),
            ("Grammer", "Hebrew"),
            ("Algebra", "Math"),
            ("Geometry", "Math"),
            ("Probability", "Math"),
            ("Classical mechanics", "Physics"),
            ("Thermodynamics", "Physics"),
            ("Quantum mechanics", "Physics"),
            ("Ancient history‎", "History"),
            ("Roman period", "History"),
            ("The Middle Ages", "History"),
        ]
        book_test_data = [
            ("The Atlas of the Human Body", "Biology"),
            ("Genesis", "Bible"),
            ("Exodus", "Bible"),
            ("Judges", "Bible"),
            ("All My Sons", "Literature"),
            ("1948", "Literature"),
            ("antigona", "Literature"),
            ("Sapiens: A Brief History of Humankind", "History"),
            ("Modern Hebrew for Beginners", "Hebrew"),
            ("Benny-Goren", "Math"),
            ("Fundamentals of Physics", "Physics"),
        ]

        with transaction.atomic():
            # Create Subject objects
            for subject_name in subjects_test_data:
                Subject(subject_name=subject_name).save()
            # Create Sub-Subject objects
            for name, related_subject in sub_subjects_test_data:
                curr_subject = Subject.objects.get(subject_name=related_subject)
                Sub_Subject(sub_subject_name=name, related_subject=curr_subject).save()
            # Create Books objects
            for name, related_subject in book_test_data:
                curr_subject = Subject.objects.get(subject_name=related_subject)
                Book(book_name=name, related_subject=curr_subject).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
