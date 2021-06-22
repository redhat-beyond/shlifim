from django.db import migrations, transaction
from django.utils import timezone
from datetime import datetime
import pytz


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0004_test_data_question"),
        ("users", "0002_users_test_data"),
    ]

    def generate_data(apps, schema_editor):
        from home.models import Question, Answer
        from users.models import Profile

        answer_test_data = [
            (
                1,
                1,
                "pretty sure its 2 but I suggesting you to check with another resources ",
                timezone.now(),
                [1, 2],
                [3, 4],
                False,
            ),
            (2, 2, "IDK", timezone.now(), [1], None, False),
            (
                2,
                1,
                "This is an old Answer",
                datetime(2019, 5, 3, tzinfo=pytz.UTC),
                [1],
                [2, 3],
                False,
            ),
            (
                1,
                1,
                "This is an popular Answer",
                datetime(2021, 1, 3, tzinfo=pytz.UTC),
                [1, 2, 3, 4, 5, 6],
                [],
                False,
            ),
            (
                3,
                1,
                "The answer is 2 for sure. I have master degree in Math from Harvard",
                datetime(2021, 2, 14, tzinfo=pytz.UTC),
                [],
                [],
                False,
            ),
            (
                4,
                1,
                "1+1 = 2. Simple algebra.",
                datetime(2021, 4, 14, tzinfo=pytz.UTC),
                [3, 4],
                [1],
                False,
            ),
            (
                2,
                14,
                "Old Answer",
                datetime(2019, 5, 3, tzinfo=pytz.UTC),
                [1],
                [],
                False,
            ),
            (
                1,
                14,
                "Popular Answer",
                datetime(2021, 1, 3, tzinfo=pytz.UTC),
                [1, 2, 3, 4, 5, 6],
                [],
                False,
            ),
            (
                3,
                14,
                "Answer A",
                datetime(2021, 2, 14, tzinfo=pytz.UTC),
                [4],
                [1, 2, 3],
                False,
            ),
            (
                4,
                14,
                "Answer B",
                datetime(2021, 4, 14, tzinfo=pytz.UTC),
                [1, 2, 3],
                [5],
                False,
            ),
        ]

        with transaction.atomic():

            for (
                user_id,
                question,
                content,
                publish_date,
                likes_profiles,
                dislike_profiles,
                is_edited,
            ) in answer_test_data:
                curr_question = Question.objects.get(id=question)
                profile = Profile.objects.get(user=user_id)
                answer = Answer(
                    profile=profile,
                    question=curr_question,
                    content=content,
                    publish_date=publish_date,
                    is_edited=is_edited,
                )
                answer.save()

                if likes_profiles is not None:
                    for profile_id in likes_profiles:
                        answer.likes.add(profile_id)

                if dislike_profiles is not None:
                    for profile_id in dislike_profiles:
                        answer.dislikes.add(profile_id)

    operations = [
        migrations.RunPython(generate_data),
    ]
