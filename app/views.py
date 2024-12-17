from django.http import JsonResponse
from django.shortcuts import redirect, render
from django import views

from app.forms import CompanyRegistrationForm
from django.contrib.auth.models import User

from app.models import Company, Contract, Employee, Service

import requests
from app import keycloak


class CompanyRegistrationView(views.View):
    def get(self, request):
        form = CompanyRegistrationForm()
        return render(request, "company_registration.html", {"form": form})

    def post(self, request):
        form = CompanyRegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, "company_registration.html", {"form": form})

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        company_name = form.cleaned_data["company_name"]
        contract_services = form.cleaned_data["contract_services"]

        user = User(username=username)
        user.set_password(password)
        user.save()
        
        company = Company.objects.create(name=company_name)
        Employee.objects.create(user=user, company=company)
        for service_code in contract_services:
            service = Service.objects.get(code=service_code)
            Contract.objects.create(company=company, service=service)
        
        # Keycloakにユーザー情報を登録する
        access_token = keycloak.get_access_token()
        requests.post(
            "http://auth_infra:8080/admin/realms/master/users",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "enabled": True,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        # Keycloakに企業名をグループとして登録する
        requests.post(
            "http://auth_infra:8080/admin/realms/master/groups",
            json={
                "name": company_name,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        # Keycloakにユーザーをグループに所属させる
        user_id = requests.get(
            f"http://auth_infra:8080/admin/realms/master/users?username={username}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        ).json()[0]["id"]
        group_id = requests.get(
            f"http://auth_infra:8080/admin/realms/master/groups?search={company_name}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        ).json()[0]["id"]
        requests.put(
            f"http://auth_infra:8080/admin/realms/master/users/{user_id}/groups/{group_id}",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

        return redirect("app:company_registration_complete")


class CompanyRegistrationCompleteView(views.View):
    def get(self, request):
        return render(request, "company_registration_complete.html")


class UserInfoAPIView(views.View):
    def get(self, request):
        access_token = request.headers.get("Authorization")
        print(access_token)
        # todo: 認証基盤にアクセスしてユーザー情報を取得する
        response = requests.get(
            "http://auth_infra:8080/realms/master/protocol/openid-connect/userinfo",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        print(response.content)
        return JsonResponse(
            {
                "username": "hoge",
            }
        )
