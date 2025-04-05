


"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_country_master_add', views.admin_country_master_add, name='admin_country_master_add'),
    path('admin_country_master_view', views.admin_country_master_view, name='admin_country_master_view'),
    path('admin_country_master_delete', views.admin_country_master_delete, name='admin_country_master_delete'),

    path('admin_player_info_add', views.admin_player_info_add, name='admin_player_info_add'),
    path('admin_player_info_view', views.admin_player_info_view, name='admin_player_info_view'),
    path('admin_player_info_profile', views.admin_player_info_profile, name='admin_player_info_profile'),
    path('admin_player_info_edit/<int:player_id>/', views.admin_player_info_edit, name='admin_player_info_edit'),
    path('admin_player_info_delete', views.admin_player_info_delete, name='admin_player_info_delete'),

    path('admin_club_master_add', views.admin_club_master_add, name='admin_club_master_add'),
    path('admin_club_master_view', views.admin_club_master_view, name='admin_club_master_view'),
    path('admin_club_master_edit/<int:club_id>/', views.admin_club_master_edit, name='admin_club_master_edit'),
    path('admin_club_master_delete', views.admin_club_master_delete, name='admin_club_master_delete'),

    path('admin_user_details_view', views.admin_user_details_view, name='admin_user_details_view'),
    path('admin_user_detail_delete', views.admin_user_detail_delete, name='admin_user_detail_delete'),

    path('admin_player_club_history_add', views.admin_player_club_history_add, name='admin_player_club_history_add'),
    path('admin_player_club_history_view', views.admin_player_club_history_view, name='admin_player_club_history_view'),
    path('admin_player_club_history_delete', views.admin_player_club_history_delete, name='admin_player_club_history_delete'),

    path('admin_player_match_history_add', views.admin_player_match_history_add, name='admin_player_match_history_add'),
    path('admin_player_match_history_view', views.admin_player_match_history_view, name='admin_player_match_history_view'),
    path('admin_player_match_history_delete', views.admin_player_match_history_delete,name='admin_player_match_history_delete'),

    path('club_club_master_add', views.club_club_master_add, name='club_club_master_add'),
    path('club_login', views.club_login, name='club_login'),
    path('club_changepassword', views.club_changepassword, name='club_changepassword'),
    path('club_logout', views.club_logout, name='club_logout'),
    path('club_home', views.club_home, name='club_home'),

    path('club_player_add', views.club_player_add, name='club_player_add'),
    path('club_player_view', views.club_player_view, name='club_player_view'),
    path('club_player_view/profile', views.club_player_profile, name='club_player_profile'),
    path('club_player_delete', views.club_player_delete, name='club_player_delete'),
    path('club_player_request', views.club_player_request),
    path('club_notifications_view', views.club_notifications_view, name='club_notifications_view'),
    path('club_delete_notification', views.club_delete_notification),

    path('club_player_info_view', views.club_player_info_view, name='club_player_info_view'),
    path('club_player_info_profile', views.club_player_info_profile, name='club_player_info_profile'),
    path('club_player_club_history_view', views.club_player_club_history_view, name='club_player_club_history_view'),
    path('club_player_match_history_view', views.club_player_match_history_view,name='club_player_match_history_view'),

    path('club_query_add', views.club_query_add, name='club_query_add'),
    path('club_query_view', views.club_query_view, name='club_query_view'),
    path('club_query_delete', views.club_query_delete, name='club_query_delete'),

    path('club_games_add', views.club_games_add, name='club_games_add'),
    path('club_games_view', views.club_games_view, name='club_games_view'),
    path('club_games_delete', views.club_games_delete, name='club_games_delete'),

    path('user_login', views.user_login_check, name='user_login'),
    path('user_home', views.user_home, name='user_home'),
    path('user_notifications_view', views.user_notifications_view, name='user_notifications_view'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('user_player_info_view', views.user_player_info_view, name='user_player_info_view'),
    path('user_player_info_profile', views.user_player_info_profile, name='user_player_info_profile'),
    path('user_player_club_history_view', views.user_player_club_history_view, name='user_player_club_history_view'),
    path('user_player_match_history_view', views.user_player_match_history_view, name='user_player_match_history_view'),

    path('user_club_master_view', views.user_club_master_view, name='user_club_master_view'),
    path('user_club_player_view', views.user_club_player_view, name='user_club_player_view'),
    path('user_club_games_view', views.user_club_games_view, name='user_club_games_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
