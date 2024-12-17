from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("", views.CompanyRegistrationView.as_view(), name="company_registration"),
    path(
        "complete/",
        views.CompanyRegistrationCompleteView.as_view(),
        name="company_registration_complete",
    ),
    path("api/userinfo/", views.UserInfoAPIView.as_view(), name="userinfo"),
]
