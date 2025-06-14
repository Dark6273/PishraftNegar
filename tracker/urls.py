from django.urls import path

from tracker import views


app_name = "tracker"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("daily-report/", views.DailyReportView.as_view(), name="daily_report"),
    path("weekly-target/", views.WeeklyTargetView.as_view(), name="weekly_target"),
]

