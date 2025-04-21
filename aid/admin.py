from django.contrib import admin
from.models import AidRequest,donors
# Register your models here.
admin.site.register(AidRequest)
admin.site.register(donors)
class MemberAdmin(admin.ModelAdmin):
  list_display = ("brandname",  "donated_at",)



