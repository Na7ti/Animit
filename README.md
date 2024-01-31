# dbは以下をAnimit直下に配置
https://ite3-2022.slack.com/files/U03B17T2UCX/F06G7F7E4Q6/db.zip

# .gitkeepの削除
```rm db/dbdate/*/.gitkeep```

# 起動方法
```docker-compose up -d```

# ターミナルに接続
```docker-compose exec django /bin/bash```  
→root@(コンテナ名):/code#

# データベースの反映
```python manage.py makemigrations animit```  
```python manage.py migrate```

# 変更を反映される方法
```docker-compose restart```

# Django管理サイトLogin
ユーザー名: root  
Password: Temporary_password

# docker-compose.ymlメモ

1. version ········· docker-compose.yml のバージョンを指定する。
2. services ········ 起動するサービス群。ネストした要素でコンテナを定義する。
3. コンテナ名 ···· 任意の名前（例：mysample、busybox）
4. image ··········· イメージからコンテナ生成する場合、イメージ（リポジトリ:タグ）を指定する
5. command······· コンテナ起動時に実行するコマンドを設定する。
6. volumes········· ローカルとコンテナでファイルを同期する
7. environment··· 環境変数を設定する
8. build ············· Dockerfileのディレクトリを指定する
9. ports ············· ポート転送を指定する
10. depends_on···· 依存関係を設定する
