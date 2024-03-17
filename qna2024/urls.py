"""
URL configuration for qna2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . views import send_object, send_json, question_detection, deploy, drive_upload, split_paragraph, upload_for_active_learning;

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send_object/', send_object),
    path('send_json/', send_json),
    path('question', question_detection),
    path('deploy', deploy),
    path('drive_upload', drive_upload),
    path('split_paragraph', split_paragraph),
    path('upload_for_active_learning', upload_for_active_learning),
]
