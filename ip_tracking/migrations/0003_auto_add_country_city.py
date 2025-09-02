from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('ip_tracking', '0002_blockedip'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestlog',
            name='country',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='requestlog',
            name='city',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]

