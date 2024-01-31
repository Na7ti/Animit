from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import AnimitUser
from django import forms


class AnimitBackend(BaseBackend):
    def authenticate(self, request, email, password):
            print("EmailAuthBackendが呼び出されている")
            print(request, email, password)
            if email and password:
                try:
                    user = AnimitUser.objects.get(email=email)
                except AnimitUser.DoesNotExist:
                    raise forms.ValidationError('ユーザーが存在しません。メールアドレスを確認してください')
                    
                else:
                    if user.check_password(password) and self.user_can_authenticate(user):
                        print("認証成功！！！")
                        return user
                    else:
                        raise forms.ValidationError('パスワードが違います。再入力してください')
            return None
        
    def user_can_authenticate(self, user):
        """
        userがis_active属性を持っていない、またはis_active属性がTrueのときTrueを返す
        """
        is_active = getattr(user, 'is_active', None) # getattr関数は、オブジェクトから属性の値を取得する
        return is_active or is_active is None
    
    def get_user(self, user_id):
        try:
            print(f"ユーザーid {user_id}")
            return AnimitUser.objects.get(pk=user_id)
        except AnimitUser.DoesNotExist:
            return None