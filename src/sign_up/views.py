from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from common.forms import UserForm
from django.urls import reverse, reverse_lazy
from django.views.generic import View, TemplateView
from common.models import AnimitUser,Animal
from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, logout
from project import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import certification_mail
import jaconv
from django.http import JsonResponse
from django.views import View

class SignUp_Base(TemplateView):
    """サインイン時の最初のページ"""
    def __init__(self):
        self.template_name = 'sign_up/base.html'
        
        self.params = {
            "form": UserForm(sign_up=True),
            "fields": ["email", "username",  "userid", "password", "register_password"] # 表示するフィールド
        }

    def get(self, request, *args, **kwargs):

        print("get")

        return render(request, self.template_name, self.params)
    
    def post(self, request, *args, **kwargs):
        """サインアップの最初のページを表示、フォームデータをpostで受け取ると、バリデーションチェックを行う"""
        
        self.params["form"] = UserForm(data=request.POST, sign_up=True) # POSTで送信されたcsrf_token以外のデータを取得し、userformクラスのフィールドにそれぞれ代入

        # 送信されたデータのバリデーションチェック
        if self.params["form"].is_valid():
            sign_up_data = request.POST.copy() # request.POSTはQueryDictというオブジェクトで、書き換え不可になっている為コピーを取る
            sign_up_data["authentication_code"] = certification_mail(sign_up_data["email"]) # 認証コードを生成し、メールに保存
            request.session["sign_up_data"] = sign_up_data # セッションにUserFormクラスを保存
            return HttpResponseRedirect(reverse("sign_up:certification"))
        
        return render(request, self.template_name, self.params)

class SignUp_Certification(TemplateView):
    """サインイン時の2段階認証ページ"""
    def __init__(self):
        self.template_name = 'sign_up/certification.html'
        self.params = {
            "form": UserForm(sign_up=True),
            "fields": ["authentication_code"] # 表示するフィールド
        }
        
    def get(self, request, *args, **kwargs):
        """メール送信"""
        self.params["authentication_code"] = request.session.get("sign_up_data")["authentication_code"]
        return render(request, self.template_name, self.params)
    
    
    def post(self, request, *args, **kwargs):
        """認証の判断"""
        self.params["form"] = UserForm(data=request.POST, sign_up=True)
        
        if self.params["form"].is_valid():
            sign_up_data  = request.session.get('sign_up_data')
            if sign_up_data["authentication_code"] == request.POST['authentication_code']:
                # 認証成功
                
                    return HttpResponseRedirect(reverse("sign_up:set_animal"))
            else:
                custom_error = {"custom_error" : "認証コードが違います"}
                context = {**self.params, **custom_error}
                return render(request, self.template_name, context)
                
        
        return render(request, self.template_name, self.params)


class SignUp_SetAnimal(TemplateView):
    """動物を選択するページ"""
    def __init__(self):
        self.template_name = 'sign_up/set_animal.html'
        self.params = {
            "form": UserForm(sign_up=True),
            # "fields": ["authentication_code"] # 表示するフィールド
        }
        
    def get(self, request, *args, **kwargs):
        """動物選択"""
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        # リクエストがAjaxリクエストかどうかのチェック
        # Ajaxリクエストを確認するためにヘッダーを使用
        # HTTPヘッダーに「X-Requested-With」が含まれ、
        # その値が「XMLHttpRequest」であるかどうかを確認
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # クエリパラメータから「term」を取得(ユーザが検索ボックスに入力したテキスト)
            # termが存在しないなら、空の文字列を使用
            query = request.POST.get('term', '')
            # ひらがなをカタカナに変換
            query_kana = jaconv.hira2kata(query)
            # Animalモデルを使用してデータベース検索
            # icontainsは大文字小文字を区別しないfilterの条件
            animals = Animal.objects.filter(animal_name__icontains=query_kana)
            # QuerySetをリストに変換してソート
            # findメソッドにより、文字列が見つかった最初のインデックスを返す
            # これを使って、クエリが名前の先頭に近い動物がリストの上位に来るようにする
            # keyはソートの際に各要素に適用される関数を指定
            # ラムダ式はanimalオブジェクトのanimal_name属性に対してfindメソッドを実行
            animals = sorted(list(animals), key=lambda animal: animal.animal_name.find(query_kana))
            # animalsから動物名だけを抜き出して新しいリスト「result」を作成
            results = [animal.animal_name for animal in animals]
            # 結果のリストをJSON形式でレスポンスとして返す
            # 「safe=False」はレスポンスが辞書型ではなく、リスト型である場合に設定する必要があるらしい
            return JsonResponse(results, safe=False)
        # もしリクエストがAjaxでない場合は、エラーメッセージを含むJSONレスポンスを返す
        return JsonResponse({'error': 'Not Ajax request'})
    
    

    
