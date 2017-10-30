from django.contrib import admin

from data.models import *


class ResultInline(admin.TabularInline):
    model = Result01
    extra = 0


class RecordAdmin(admin.ModelAdmin):
    inlines = [ResultInline]
    list_display = ('title', 'post_time')


admin.site.register(Group01)
admin.site.register(RawRecord01, RecordAdmin)
admin.site.register(Result01)
