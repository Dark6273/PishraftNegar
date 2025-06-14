from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    target_weekly_hours = models.PositiveIntegerField(
        default=40,
        help_text=_("Number of hours the user works per week."),
    )
    weekly_hours = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.0,
        help_text=_("Number of hours the user worked per week."),
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username


class TimeTracker(models.Model):
    """
    Model to track time spent on tasks.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_trackers')
    hours_spent = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.0,
        help_text=_("Number of hours spent on the task.")
    )
    date = models.DateField(
        auto_now_add=True,
        help_text=_("Date when the time was tracked.")
    )

    class Meta:
        verbose_name = _("time tracker")
        verbose_name_plural = _("time trackers")

    def __str__(self):
        return f"{self.user.username} - {self.hours_spent} hours on {self.date}"
