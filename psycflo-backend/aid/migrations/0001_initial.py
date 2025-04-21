

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AidRequest',

            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=30)),
                ('email', models.EmailField(default='example@example.com', max_length=254)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('country', models.CharField(default='Nigeria', max_length=30)),
                ('state', models.CharField(default='Kwara', max_length=30)),
                ('local_government', models.CharField(default='Ilorin West', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='donors',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('brandname', models.CharField(default='', max_length=30)),
                ('message', models.TextField()),
                ('donated_at', models.DateTimeField(auto_now_add=True)),
                ('distributed', models.DateTimeField(auto_now_add=True)),
                ('website', models.URLField(blank=True)),

            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('localgovernment', models.CharField(max_length=255)),
                ('phoneno', models.IntegerField()),

            ],
        ),
    ]
