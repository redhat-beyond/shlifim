from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0011_alter_fields_question'),
    ]

    def generate_data(apps, schema_editor):
        from django.contrib.auth.models import User
        from home.models import Profile

        with transaction.atomic():
            # Create Blocked user profile
            user = User.objects.create_user(username='BlockedUser',
                                            password='BlockedUserBlockedUser',
                                            email='BlockedUser@gmail.com')
            blockedProfile = Profile(user=user)
            blockedProfile.is_blocked = True
            blockedProfile.save()

            # Create Admin superuser profile
            superuser = User.objects.create_superuser(username='Admin',
                                                      password='Admin',
                                                      email='Admin@gmail.com').save()
            Profile(user=superuser).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
