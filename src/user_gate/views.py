from django.shortcuts import render
from common.forms import UserForm
from project import settings
from django.views.generic import View, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


class Login(TemplateView):
    def __init__(self):
        self.template_name = 'user_gate/login.html'
        
        self.params = {
            "form": UserForm(),
            "fields": ["email", "password", "register_password"] # 表示するフィールド
        }
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.params)
        
    def post(self, request, *args, **kwargs):
        self.params["form"] = UserForm(data=request.POST)
        if self.params["form"].is_valid():
            cleaned_data = self.params["form"].cleaned_data
            backend = "animit.backends.AnimitBackend" # 認証方法
            animitUser = authenticate(email=cleaned_data.get('email'), password=cleaned_data.get('password'))
            
            if animitUser:
                animitUser.backend = backend
                login(request, animitUser)
                return redirect(settings.LOGIN_REDIRECT_URL)
            
        return render(request, self.template_name, self.params)
     
class LogOut(TemplateView):
        
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("user_gate:sign_up"))

class Home(LoginRequiredMixin, TemplateView):
    def __init__(self, **kwargs) -> None:
        self.template_name = "user_gate/home.html"
        self.login_url = settings.LOGIN_URL # ログインしていない状態でアクセスしようとしたときのリダイレクト先
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
