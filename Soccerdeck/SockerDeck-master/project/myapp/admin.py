from django.contrib import admin

# Register your models here.
#user_login, user_details, user_query, player_info, player_club_history, player_match_history, country_master, club_master, club_games

from .models import user_login, user_details, user_query, player_info, player_club_history, player_match_history, country_master, club_master, club_games
from .models import club_player
admin.site.register(user_login)
admin.site.register(user_details)
admin.site.register(user_query)
admin.site.register(player_info)
admin.site.register(player_club_history)
admin.site.register(player_match_history)
admin.site.register(country_master)
admin.site.register(club_master)
admin.site.register(club_games)
admin.site.register(club_player)


