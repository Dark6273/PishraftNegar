from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

from tracker.models import User, TimeTracker


# admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'first_name', 'weekly_hours', 'target_weekly_hours', 'reach_target')

    def reach_target(self, obj):
        """
        Returns a boolean indicating whether the user has reached their weekly target.
        """
        return obj.weekly_hours >= obj.target_weekly_hours


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(TimeTracker)
class TimeTrackerAdmin(ModelAdmin):
    list_display = ('user', 'hours_spent', 'date')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)
    date_hierarchy = 'date'
    ordering = ('-date',)
