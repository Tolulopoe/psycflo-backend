from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save, post_delete
from django.core.exceptions import ValidationError
from django.db.models import Count, F

class TimestampMixin(models.Model):
    """Base model with automatic timestamp tracking"""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimestampMixin):
    """Manages discussion categories visible in UI"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(
        validators=[MinLengthValidator(20)],
        help_text="Displayed under category name in UI"
    )
    icon = models.CharField(
        max_length=50, 
        default='forum',
        help_text="Material Design icon name"
    )
    color = models.CharField(
        max_length=7,
        default='#2196F3',
        help_text="Hex color for category cards"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order in category list"
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return f"{self.name} Category"

    def clean(self):
        """Automatically generate/update slug from name"""
        if not self.slug or (self.pk and Category.objects.get(pk=self.pk).name != self.name):
            self.slug = slugify(self.name)

class Event(TimestampMixin):
    """Handles both upcoming and past events"""
    EVENT_STATUS = (
        ('upcoming', 'Upcoming Event'),
        ('past', 'Past Event'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True, blank=True)
    description = models.TextField(
        validators=[MinLengthValidator(50)],
        help_text="Full event description"
    )
    status = models.CharField(
        max_length=20, 
        choices=EVENT_STATUS, 
        db_index=True
    )
    event_date = models.DateTimeField()
    thumbnail = models.URLField(
        help_text="URL for event card image",
        blank=True
    )
    location = models.CharField(
        max_length=200,
        help_text="Physical or virtual location",
        blank=True
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Highlight in featured section"
    )
    event_category = models.CharField(max_length=100, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)
    registration_deadline = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-event_date']
        indexes = [
            models.Index(fields=['status', '-event_date']),
            models.Index(fields=['slug']),
        ]

    @property
    def available_seats(self):
        return self.capacity - self.registrations.count()

    def clean(self):
        """Validate registration deadline"""
        if self.registration_deadline and self.registration_deadline > self.event_date:
            raise ValidationError("Registration deadline must be before event date")
        if not self.slug:
            self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        """Update status based on current time"""
        now = timezone.now()
        if self.event_date < now:
            self.status = 'past'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class PostManager(models.Manager):
    """Custom manager for post queries"""
    def trending(self):
        return self.get_queryset().annotate(
            engagement_score=Count('likes') * 2 +
                       F('comments_count') +
                       F('views') +
                       F('shares') * 3
        ).order_by('-engagement_score', '-created_at')[:20]

    def published(self):
        return self.filter(is_draft=False, scheduled_publish_time__lte=timezone.now())

class Post(TimestampMixin):
    """Main discussion post model with engagement tracking"""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(10)],
        help_text="Post title in lists"
    )
    slug = models.SlugField(max_length=210, unique=True, blank=True)
    content = models.TextField(
        validators=[MinLengthValidator(50)],
        help_text="Main post content"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    is_anonymous = models.BooleanField(
        default=False,
        help_text="Hide author identity"
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True,
        help_text="Users who liked this post"
    )
    views = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(
        default=False,
        help_text="Pin to top of discussions"
    )
    is_draft = models.BooleanField(default=False)
    scheduled_publish_time = models.DateTimeField(blank=True, null=True)
    engagement_score = models.IntegerField(default=0, db_index=True)
    thumbnail = models.URLField(
        help_text="URL for post card image",
        blank=True
    )

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'category']),
            models.Index(fields=['is_pinned', '-created_at']),
            models.Index(fields=['scheduled_publish_time']),
            models.Index(fields=['engagement_score']),
            models.Index(fields=['slug']),
        ]

    @property
    def is_published(self):
        return not self.is_draft and (
            self.scheduled_publish_time is None or 
            self.scheduled_publish_time <= timezone.now()
        )

    def calculate_engagement_score(self):
        """Calculate and update the engagement score"""
        self.engagement_score = (self.likes.count() * 2) + self.comments_count + self.views + (self.shares * 3)
        self.save(update_fields=['engagement_score'])

    def __str__(self):
        return f"Post: {self.title[:50]}"

class Comment(TimestampMixin):
    """Nested comments for discussion posts"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    content = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text="Comment text content"
    )
    is_anonymous = models.BooleanField(default=False)
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    is_edited = models.BooleanField(default=False)
    edit_history = models.JSONField(default=list, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_content = self.content

    def save(self, *args, **kwargs):
        """Track edits and update post's comment count"""
        if self.pk and self.content != self._original_content:
            self.edit_history.append({
                'previous_content': self._original_content,
                'edited_at': timezone.now().isoformat()
            })
            self.is_edited = True
        super().save(*args, **kwargs)
        self._original_content = self.content
        self.post.calculate_engagement_score()

    def delete(self, *args, **kwargs):
        """Update post's comment count when deleted"""
        post = self.post
        super().delete(*args, **kwargs)
        post.calculate_engagement_score()

    class Meta:
        ordering = ['created_at']
        verbose_name = "Post Comment"
        verbose_name_plural = "Post Comments"

    def __str__(self):
        return f"Comment by {self.author or 'Anonymous'} on {self.post}"

class UserProfile(TimestampMixin):
    """Extended user profile with community features"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.URLField(
        default='/static/images/default-profile.png'
    )
    bio = models.TextField(
        blank=True,
        validators=[MinLengthValidator(20)]
    )
    community_rank = models.PositiveIntegerField(default=0)
    notification_preferences = models.JSONField(default=dict)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('unverified', 'Unverified'),
            ('pending', 'Pending'),
            ('verified', 'Verified')
        ],
        default='unverified'
    )
    last_active = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username}'s Profile"

class EventRegistration(TimestampMixin):
    """Tracks event participation"""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def __str__(self):
        return f"{self.user} registered for {self.event}"

class Report(TimestampMixin):
    """Content moderation reporting system"""
    REPORT_TYPES = (
        ('spam', 'Spam'),
        ('abuse', 'Abusive Content'),
        ('inappropriate', 'Inappropriate'),
        ('other', 'Other'),
    )

    reporter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open'),
            ('reviewed', 'Reviewed'),
            ('resolved', 'Resolved')
        ],
        default='open'
    )
    resolution_details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(post__isnull=False) | models.Q(comment__isnull=False),
                name='content_required'
            )
        ]

    def __str__(self):
        return f"Report on {self.post or self.comment} ({self.report_type})"