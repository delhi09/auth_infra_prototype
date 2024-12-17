from django import forms


class CompanyRegistrationForm(forms.Form):
    username = forms.CharField(label="ユーザー名", max_length=100)
    password = forms.CharField(label="パスワード", max_length=100)
    company_name = forms.CharField(label="会社名", max_length=100)
    contract_services = forms.MultipleChoiceField(
        label="契約サービス",
        choices=[
            ("service1", "Service 1"),
            ("service2", "Service 2"),
            ("service3", "Service 3"),
        ],
        widget=forms.CheckboxSelectMultiple,
    )
