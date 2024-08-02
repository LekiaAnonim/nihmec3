from django.urls import path
from registration import views

app_name = 'registration'
urlpatterns = [
    path("", views.AttendantCreateView.as_view(), name='register'),
    path('visitor/<int:pk>/tag', views.AttendantDetail.as_view(), name='visitor-card'),
    path('visitors/list/', views.AttendantListView.as_view(), name='visitors-list'),
]