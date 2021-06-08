from django.db import migrations, transaction
from django.utils import timezone


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0005_question"),
    ]

    def generate_data(apps, schema_editor):
        from django.contrib.auth.models import User
        from home.models import Profile, Subject, Sub_Subject, Book, Question

        question_test_data = [
            (
                "Rebecca",
                "question from math course",
                "Hey , Can someome help me solve the equation 1+1?",
                timezone.now(),
                "Math",
                "Algebra",
                "7",
                "Benny-Goren",
                14,
                True,
            ),
            (
                "Rebecca",
                "question from bible course",
                "Does god exist?",
                timezone.now(),
                "Bible",
                "Prophecies",
                "7",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                "Question",
                "Was Alessandro Volta a professor of chemistry?",
                timezone.now(),
                "Chemistry",
                "",
                "11",
                "",
                None,
                False,
            ),
            (
                "Aviv",
                "question about ants",
                "Do the ants eat plants, meats, or both?	both",
                timezone.now(),
                "Biology",
                "Cell Biology",
                "10",
                "Benny-Goren",
                50,
                False,
            ),
            (
                "Ido",
                "Need help",
                "Is Hebrew the largest member of the Semitic language family??",
                timezone.now(),
                "Hebrew",
                "Writing",
                "10",
                "Modern Hebrew for Beginners",
                23,
                False,
            ),
            (
                "Ido",
                "question",
                "Where is the Berliner Dom located?",
                timezone.now(),
                "Geography",
                "Atmosphere",
                "12",
                "",
                None,
                False,
            ),
            (
                "Rebecca",
                "Novel price",
                "Did Tesla win the Nobel Prize??",
                timezone.now(),
                "History",
                "Ancient history‎",
                "12",
                "Sapiens: A Brief History of Humankind",
                23,
                False,
            ),
            (
                "Danit",
                "Question from  Benny Goren Book",
                "Can you help me solve this equation 2X=8?",
                timezone.now(),
                "Math",
                "Algebra",
                "7",
                "Benny-Goren",
                100,
                False,
            ),
            (
                "Danit",
                "1948",
                "Who is the author of the book 1948?",
                timezone.now(),
                "Literature",
                "20th Century",
                "7",
                "1948",
                None,
                False,
            ),
        ]

        with transaction.atomic():
            for (
                username,
                title,
                content,
                publish_date,
                subject_name,
                sub_subject_name,
                grade,
                book_name,
                book_page,
                is_edited,
            ) in question_test_data:
                curr_subject = Subject.objects.get(subject_name=subject_name)
                if sub_subject_name != "":
                    curr_sub_subject = Sub_Subject.objects.get(
                        sub_subject_name=sub_subject_name
                    )
                if book_name != "":
                    curr_book = Book.objects.get(book_name=book_name)
                user = User.objects.get(username=username)
                profile = Profile.objects.get(user=user)
                Question(
                    profile=profile,
                    title=title,
                    content=content,
                    publish_date=publish_date,
                    subject=curr_subject,
                    sub_subject=curr_sub_subject,
                    grade=grade,
                    book=curr_book,
                    book_page=book_page,
                    is_edited=is_edited,
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
