"""
URL configuration for memoly_drf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from assessment import views
from assessment.grading.scenario import GradeScenario

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("assessment/", views.AssessmentView.as_view(), name="assessment"),
    path("assessment/grade-short-answer/", views.GradeShortAnswer.as_view(), name="grade-short-answer"),
    path("assessment/grade-scenario/", GradeScenario.as_view(), name="grade-scenario"),
    path("admin/", admin.site.urls),
]
