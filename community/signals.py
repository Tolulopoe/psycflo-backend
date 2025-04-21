from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.db import transaction
from .models import Category, Event, Post, Comment, User, UserProfile

@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, **kwargs):
    if not instance.slug or (instance.pk and Category.objects.get(pk=instance.pk).name != instance.name):
        instance.slug = slugify(instance.name)

@receiver(pre_save, sender=Event)
def event_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    if instance.event_date < timezone.now():
        instance.status = 'past'

@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    instance.profile.save()

@receiver([post_save, post_delete], sender=Comment)
@transaction.atomic
def update_comment_count(sender, instance, **kwargs):
    post = instance.post
    post.comments_count = post.comments.count()
    post.save(update_fields=['comments_count'])
    # The engagement score will be updated by the post_save signal on Post

@receiver(pre_save, sender=Comment)
def track_comment_edits(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = Comment.objects.get(pk=instance.pk)
            if original.content != instance.content:
                instance.edit_history = instance.edit_history or []
                instance.edit_history.append({
                    'previous_content': original.content,
                    'edited_at': timezone.now().isoformat()
                })
                instance.is_edited = True
        except Comment.DoesNotExist:
            pass

@receiver(m2m_changed, sender=Post.likes.through)
def post_likes_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    """Update engagement score when likes are added or removed."""
    if action in ["post_add", "post_remove"]:
        instance.engagement_score = instance.calculate_engagement_score()
        instance.save(update_fields=['engagement_score'])

@receiver(post_save, sender=Post)
def update_post_engagement_on_comment_change(sender, instance, **kwargs):
    """Update engagement score when comments_count changes."""
    if not kwargs.get('created', False): # Avoid infinite loop on post creation
        if 'comments_count' in instance.tracker.changed():
            instance.engagement_score = instance.calculate_engagement_score()
            instance.save(update_fields=['engagement_score'])

