# メール送信
from django.core.mail import send_mail
from django.conf import settings
import random

def certification_mail(email):

    print(email)

    """メール送信し認証コードを返す"""
    authentication_code = str(random.randint(100000, 999999)).zfill(6)
    
    send_mail(
        "認証コード",
        authentication_code,
        'CA01973085@st.kawahara.ac.jp',  # 送信元のメールアドレス
        [email],               # 受信者リスト
        fail_silently=False,
    )
    
    return authentication_code