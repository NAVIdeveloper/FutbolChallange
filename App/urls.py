from django.urls import path
from .views import *

urlpatterns = [
    path("",HomePage,name='home'),
    path("turnirlar/",TurnamentPage,name='turnirlar'),
    path("jamoalar/",TeamsPage,name='jamoalar'),
    path("voqealar/<int:T>/<int:R>/",EventsPage,name='voqealar'),

    path('register/',RegisterPage,name='register'),
    path("kirish/",KirishPage,name='kirish'),
    path("chiqish/",ChiqishPage,name='chiqish'),
    path("qoshilish/<int:pk>/",QoshilishPage,name='qoshilish'),
    path("chiqibketish/<int:pk>/",ChiqibketishPage,name='chiqibketish'),
    path("detail/turnament/<int:pk>/",TurnamentDetailPage,name='detail-turnament'),

    path("add_point_turnament_team/<int:reg_id>/",Admin_add_point_turnament_team,name='add_point_turnament_team'),
    path("delete_turnament_team/<int:pk>/",Admin_delete_turnament_team,name='delete_turnament_team'),

    path("on_off_url/<int:pk>/",Admin_on_off_url,name='on_off_url'),
    path('detail-team/<int:pk>/',DetailTeamPage,name='detail-team'),
    path("add_turnament/",Admin_add_turnament,name='add_turnament'),
    path("end_turnament/<int:pk>/",Admin_end_turnament,name='end_turnament'),
    path("add-new-event/<int:pk>/",Admin_add_new_event,name='add-new-event'),
    path("delete-event/<int:pk>/",Admin_delete_event,name="delete-event"),
    path("follow/<int:pk>/",FollowPage,name='follow'),
    path("SelectTurnamentPage/",SelectTurnamentPage,name="SelectTurnamentPage"),
    path("filter-event/<int:pk>/",SelectRoundOfTurnamentPage,name='filter-event'),
]