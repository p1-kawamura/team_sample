from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index,hinban_enter,free,hinban_click,team_color_size_click,rental_now,rental_modal,rental_basket,rental_ok, \
        return_modal,return_ok,henshu_index,henshu_hinban_click,henshu_list_click,henshu_up,henshu_del, \
            size_index,size_num,size_name,size_new,size_del,size_sample,csv_index,csv_imp


app_name="sample"
urlpatterns = [
    path('', index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='sample/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('hinban_enter/', hinban_enter, name="hinban_enter"),
    path('hinban_click/', hinban_click, name="hinban_click"),
    path('team_color_size_click/', team_color_size_click, name="team_color_size_click"),
    path('rental_now/', rental_now, name="rental_now"),
    path('rental_basket/', rental_basket, name="rental_basket"),
    path('rental_modal/', rental_modal, name="rental_modal"),
    path('rental_ok/', rental_ok, name="rental_ok"),
    path('return_modal/', return_modal, name="return_modal"),
    path('return_ok/', return_ok, name="return_ok"),
    path('henshu_index/', henshu_index, name="henshu_index"),
    path('henshu_hinban_click/', henshu_hinban_click, name="henshu_hinban_click"),
    path('henshu_list_click/', henshu_list_click, name="henshu_list_click"),
    path('henshu_up/', henshu_up, name="henshu_up"),
    path('henshu_del/', henshu_del, name="henshu_del"),
    path('size_index/', size_index, name="size_index"),
    path('size_num/', size_num, name="size_num"),
    path('size_name/', size_name, name="size_name"),
    path('size_new/', size_new, name="size_new"),
    path('size_del/', size_del, name="size_del"),
    path('size_sample/', size_sample, name="size_sample"),
    path('csv_index/', csv_index, name="csv_index"),
    path('csv_imp/', csv_imp, name="csv_imp"),
    path('free/', free, name="free"),
]