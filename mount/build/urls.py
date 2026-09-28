from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "building/add/",
        views.add_building,
        name="add_building",
    ),

    path(
        "building/<int:id>/",
        views.building_detail,
        name="building_detail",
    ),

    path(
        "building/edit/<int:id>/",
        views.edit_building,
        name="edit_building",
    ),

    path(
        "building/delete/<int:id>/",
        views.delete_building,
        name="delete_building",
    ),
]
