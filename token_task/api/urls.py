from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('info/', views.info_view, name='info'),
    path('latency/', views.latency_view, name='latency'),
    path('logout/', views.logout_view, name='token_blacklist'),
]