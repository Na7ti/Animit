from django import forms
from .models import AnimitUser
from django.contrib.auth import authenticate

class UserForm(forms.ModelForm):
    
    password = forms.CharField(max_length=15, widget=forms.PasswordInput) # フォームの入力時にinput:passwordを使用するためにpasswordフィールドをオーバーライド(AnimitUserモデルには影響しない)
    register_password = forms.CharField(max_length=15, widget=forms.PasswordInput) # データベースには追加されないフィールド
    authentication_code = forms.IntegerField(help_text="入力できる数字は6桁です")
    
    class Meta:
        model = AnimitUser
        fields = ["id", "email", "username", "userid", "password", "register_password", "authentication_code"]
    
    def __init__(self, *args, **kwargs):
        self.sign_up = kwargs.pop('sign_up', None)
        
        super(UserForm, self).__init__(*args, **kwargs)
        
        if self.data:  # フォームがデータを受け取った場合
            # POSTされたフィールドのみを必須に設定
            for field in list(self.fields):
                if field not in self.data:
                    # POSTデータに含まれていないフィールドは削除
                    self.fields.pop(field)
        
    def clean_email(self):
        """
        ユーザーがサインアップ時に、既にしようされているメアドでサインアップをしよとした時に、エラーを出す
        """
        email = self.cleaned_data.get('email')
        if self.sign_up:
            knownUser = AnimitUser.objects.filter(email=email).first()
            if knownUser:
                raise forms.ValidationError("このメールアドレスは既に使用されています")
            
        return email
    
    def clean_authentication_code(self):
        """送信されたコードのバリデーションをチェック"""
        authentication_code = self.cleaned_data.get('authentication_code')
        
        if 6 != len(str(authentication_code)):
            raise forms.ValidationError('6桁の数字を入力してください')

        
    def clean(self):
        """passwordとregister_passwordが空でなく、等しいとき、バリデーションをチェックしたデータを返す。そうでなければエラーを出す
        """
        password = self.cleaned_data.get('password')
        register_password = self.cleaned_data.get('register_password')
        if password and register_password and password != register_password:
            raise forms.ValidationError('passwordとregister_passwordが不一致です')
        
        return self.cleaned_data

    def save(self, commit=True):
        """
        パスワードをハッシュ化してデータを保存
        """
        animitUser = super().save(commit=False) # データベースにはまだ保存せずに、モデルのインスタンスを作成して返す
        # パスワードをハッシュ化して設定
        animitUser.set_password(self.cleaned_data["password"])

        if commit:
            animitUser.save()
        return animitUser


        
    
