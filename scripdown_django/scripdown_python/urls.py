from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_script, name='upload_script'),
    path('analyze/<int:script_id>/', views.analyze_script, name='analyze_script'),
    path('adjust-budget/<int:script_id>/', views.adjust_budget, name='adjust_budget'),
]