import json
import decimal

from datetime import timedelta

from django.views import View
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

from tracker.models import User, TimeTracker


class IndexView(View):
    def get(self, request: HttpRequest):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=(today.weekday() + 2) % 7)
        
        weekly_hours = []
        for i in range(7):
            day = start_of_week + timedelta(days=i)
            total = TimeTracker.objects.filter(
                user=request.user,
                date=day
            ).aggregate(Sum('hours_spent'))['hours_spent__sum'] or 0
            weekly_hours.append(float(total))
        
        daily_target = request.user.target_weekly_hours / 7
        
        context = {
            "users": User.objects.all(),
            'weekly_hours': weekly_hours,
            'daily_target': daily_target,
        }
        return render(request, "index.html", context=context)


class LoginView(View):
    def get(self, request: HttpRequest):
        return render(request, "login.html")

    def post(self, request: HttpRequest):
        content = json.loads(request.body)
        if not isinstance(content, dict):
            return JsonResponse({"error": "Invalid request format"}, status=400)
        
        username = content.get("username")
        password = content.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)


class DailyReportView(View, LoginRequiredMixin):
    def post(self, request: HttpRequest):
        number = request.POST.get("study_hours")
        if number is None:
            return HttpRequest(status=400)
        number = decimal.Decimal(number)
        user = request.user
        user.weekly_hours += number
        user.save()

        TimeTracker.objects.create(
            user=user,
            hours_spent=number,
        )

        return redirect("tracker:index")


class WeeklyTargetView(View, LoginRequiredMixin):
    def post(self, request: HttpRequest):
        number = request.POST.get("weekly_target")
        if number is None:
            return HttpRequest(status=400)
        
        number = int(number)
        user = request.user
        user.target_weekly_hours = number
        user.weekly_hours = 0
        user.save()
        return redirect("tracker:index")
