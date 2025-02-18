from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faculty',
            old_name='Trainee',
            new_name='trainee',
        ),
    ]
