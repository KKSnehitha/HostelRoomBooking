from django.contrib import admin
from django.urls import path
from bookapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('book/',views.student_info,name='student_info'),
    path('select/',views.select_room,name='select_room'),
    path('rooms/', views.dashboard, name='dashboard'),
    path("create/", views.create_rooms),
    path('roommates/<int:room_no>/', views.know_roommates, name='know_roommates'),
]
