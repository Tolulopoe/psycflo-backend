from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import *
import json
from django.urls import reverse
from django.utils import timezone

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('content', 'author', 'is_anonymous', 'created_at', 'is_edited')
    readonly_fields = ('created_at', 'is_edited')
    show_change_link = True

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'truncated_content', 'author', 'category',
                    'engagement_score', 'is_pinned', 'published_status')
    list_filter = ('category', 'is_anonymous', 'is_pinned', 'is_draft', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    list_select_related = ['author', 'category']
    inlines = [CommentInline]
    readonly_fields = ('engagement_score', 'slug', 'views', 'shares')
    date_hierarchy = 'created_at'
    autocomplete_fields = ['author', 'category']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'author', 'category')
        }),
        ('Visibility', {
            'fields': ('is_anonymous', 'is_pinned', 'is_draft')
        }),
        ('Timing', {
            'fields': ('scheduled_publish_time',)
        }),
        ('Engagement', {
            'fields': ('engagement_score', 'likes', 'views', 'shares')
        }),
    )

    def truncated_content(self, obj):
        return format_html('<span title="{}">{}</span>',
                           obj.content,
                           obj.content[:50] + '...' if len(obj.content) > 50 else obj.content)
    truncated_content.short_description = 'Content Preview'

    def published_status(self, obj):
        return "Published" if obj.is_published else "Draft"
    published_status.admin_order_field = 'is_draft'

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'status', 'available_seats',
                    'registration_status', 'is_featured')
    list_filter = ('status', 'event_category', 'is_featured')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('available_seats', 'slug')
    date_hierarchy = 'event_date'
    autocomplete_fields = [] # Remove or correct this line

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'status')
        }),
        ('Details', {
            'fields': ('event_date', 'registration_deadline', 'capacity',
                       'thumbnail', 'location')
        }),
        ('Metadata', {
            'fields': ('is_featured', 'event_category')
        }),
    )

    def registration_status(self, obj):
        now = timezone.now()
        if obj.registration_deadline and obj.registration_deadline < now:
            return "Closed"
        return "Open" if obj.available_seats > 0 else "Full"
    registration_status.short_description = 'Registration'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_status', 'community_rank',
                    'last_active', 'post_count')
    search_fields = ('user__username', 'bio')
    list_filter = ('verification_status', 'community_rank')
    list_select_related = ['user']
    readonly_fields = ('last_active',)

    def post_count(self, obj):
        return obj.user.posts.count()
    post_count.short_description = 'Posts'

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created_at')
    list_filter = ('event__status',)
    search_fields = ('event__title', 'user__username')
    autocomplete_fields = ['event', 'user']

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'content_object', 'report_type', 'status', 'created_at')
    list_filter = ('report_type', 'status')
    search_fields = ('reporter__username', 'description')
    readonly_fields = ('reporter', 'created_at')
    actions = ['mark_as_resolved']

    def content_object(self, obj):
        return obj.post or obj.comment
    content_object.short_description = 'Reported Content'

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'post_count', 'color_preview')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('color_preview',)

    def post_count(self, obj):
        return obj.posts.count()
    post_count.admin_order_field = 'posts_count'

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(posts_count=Count('posts'))

class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'post_link', 'author', 'is_edited', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('edit_history_preview', 'post_link')
    list_select_related = ['author', 'post']

    def post_link(self, obj):
        return format_html('<a href="{}">{}</a>',
                           reverse('admin:community_post_change', args=[obj.post.id]),
                           obj.post.title)
    post_link.short_description = 'Post'

    def edit_history_preview(self, obj):
        return format_html('<pre>{}</pre>', json.dumps(obj.edit_history, indent=2))
    edit_history_preview.short_description = 'Edit History'

    def truncated_content(self, obj): # Added this method
        return format_html('<span title="{}">{}</span>',
                           obj.content,
                           obj.content[:50] + '...' if len(obj.content) > 50 else obj.content)
    truncated_content.short_description = 'Content Preview'

# Register all models with their custom admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
admin.site.register(Report, ReportAdmin)