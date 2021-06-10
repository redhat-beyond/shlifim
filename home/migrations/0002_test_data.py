from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    def generate_data(apps, schema_editor):
        from django.contrib.auth.models import User
        from home.models import Profile

        user_test_data = [
            ("Rebecca", "RebeccaRebecca", "Rebecca@gmail.com", "F"),
            ("Danit", "DanitDanit", "Danit@gmail.com", "F"),
            ("Aviv", "AvivAviv", "Aviv@gmail.com", "M"),
            ("Ido", "IdoIdo", "Ido@gmail.com", None),
        ]

        with transaction.atomic():
            # Test: Create a User and Profile from a User via username.
            for username, password, email, gender in user_test_data:
                user = User.objects.create_user(
                    username=username, password=password, email=email
                )
                if gender:
                    Profile(user=user, gender=gender).save()
                else:
                    Profile(user=user).save()
            # Test: Create a Profile with user who was updated to superuser (admin)
            user = User.objects.create_superuser(
                username="Lior", password="LiorLior", email="Lior@gmail.com"
            ).save()
            Profile(user=user).save()
            # Test: Update a profile to be blocked.
            profile = Profile.objects.get(user=User.objects.get(username="Rebecca"))
            profile.is_blocked = True
            profile.save()

    operations = [
        migrations.RunPython(generate_data),
    ]
