

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=110, unique=True)),
                ('description', models.TextField(help_text='Displayed under category name in UI', validators=[django.core.validators.MinLengthValidator(20)])),
                ('icon', models.CharField(default='forum', help_text='Material Design icon name', max_length=50)),
                ('color', models.CharField(default='#2196F3', help_text='Hex color for category cards', max_length=7)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order in category list')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['order', 'name'],
                'indexes': [models.Index(fields=['slug'], name='community_c_slug_777ae5_idx')],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=210, unique=True)),
                ('description', models.TextField(help_text='Full event description', validators=[django.core.validators.MinLengthValidator(50)])),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming Event'), ('past', 'Past Event')], db_index=True, max_length=20)),
                ('event_date', models.DateTimeField()),
                ('thumbnail', models.URLField(blank=True, help_text='URL for event card image')),
                ('location', models.CharField(blank=True, help_text='Physical or virtual location', max_length=200)),
                ('is_featured', models.BooleanField(default=False, help_text='Highlight in featured section')),
                ('event_category', models.CharField(blank=True, max_length=100, null=True)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('registration_deadline', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-event_date'],
                'indexes': [models.Index(fields=['status', '-event_date'], name='community_e_status_6e6f52_idx'), models.Index(fields=['slug'], name='community_e_slug_d55c21_idx')],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text='Post title in lists', max_length=200, validators=[django.core.validators.MinLengthValidator(10)])),
                ('slug', models.SlugField(blank=True, max_length=210, unique=True)),
                ('content', models.TextField(help_text='Main post content', validators=[django.core.validators.MinLengthValidator(50)])),
                ('is_anonymous', models.BooleanField(default=False, help_text='Hide author identity')),
                ('views', models.PositiveIntegerField(default=0)),
                ('shares', models.PositiveIntegerField(default=0)),
                ('comments_count', models.PositiveIntegerField(default=0)),
                ('is_pinned', models.BooleanField(default=False, help_text='Pin to top of discussions')),
                ('is_draft', models.BooleanField(default=False)),
                ('scheduled_publish_time', models.DateTimeField(blank=True, null=True)),
                ('engagement_score', models.IntegerField(db_index=True, default=0)),
                ('thumbnail', models.URLField(blank=True, help_text='URL for post card image')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='community.category')),
                ('likes', models.ManyToManyField(blank=True, help_text='Users who liked this post', related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(help_text='Comment text content', validators=[django.core.validators.MinLengthValidator(10)])),
                ('is_anonymous', models.BooleanField(default=False)),
                ('is_edited', models.BooleanField(default=False)),
                ('edit_history', models.JSONField(blank=True, default=list)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='community.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='community.post')),
            ],
            options={
                'verbose_name': 'Post Comment',
                'verbose_name_plural': 'Post Comments',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('report_type', models.CharField(choices=[('spam', 'Spam'), ('abuse', 'Abusive Content'), ('inappropriate', 'Inappropriate'), ('other', 'Other')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('reviewed', 'Reviewed'), ('resolved', 'Resolved')], default='open', max_length=20)),
                ('resolution_details', models.TextField(blank=True, null=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.comment')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='community.post')),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile_picture', models.URLField(default='/static/images/default-profile.png')),
                ('bio', models.TextField(blank=True, validators=[django.core.validators.MinLengthValidator(20)])),
                ('community_rank', models.PositiveIntegerField(default=0)),
                ('notification_preferences', models.JSONField(default=dict)),
                ('verification_status', models.CharField(choices=[('unverified', 'Unverified'), ('pending', 'Pending'), ('verified', 'Verified')], default='unverified', max_length=20)),
                ('last_active', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='community.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event Registration',
                'verbose_name_plural': 'Event Registrations',
                'unique_together': {('event', 'user')},
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created_at', 'category'], name='community_p_created_b1914c_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['is_pinned', '-created_at'], name='community_p_is_pinn_af6e2b_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['scheduled_publish_time'], name='community_p_schedul_5d89ff_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['engagement_score'], name='community_p_engagem_30ea84_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['slug'], name='community_p_slug_614d88_idx'),
        ),
        migrations.AddConstraint(
            model_name='report',
            constraint=models.CheckConstraint(condition=models.Q(('post__isnull', False), ('comment__isnull', False), _connector='OR'), name='content_required'),
        ),
    ]
