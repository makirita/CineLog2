
# CineLog

TMDbのWebAPIを使用した映画の記録(レビュー、感想等)するアプリです。
ユーザーが、自分の感想だけを書き込むアプリとなっており、
他の人のレビューを見ることはできません。
レスポンシブに対応しているのでスマホからも記録することができます。

# 機能説明

ログイン・・・ユーザーログイン(アカウント名+パスワード)とgoogleログインがあります
映画検索・・・WebAPIで映画のタイトルを検索
マイリスト・・・検索したタイトルをマイリストに登録できます。またタグを付与することも可能です



# ライブラリ

Pillow 9.5.0
social-auth-app-django 5.2.0
neologdn 0.5.1

# インストール

```bash
pip install pillow
pip install social-auth-app-django
pip install neologdn
```


# 注意点

HTML上に表記の乱れ等あるので修正します。
またレスポンシブ対応のマイページでJSが予期しない動作をすることを確認しており
修正します。

# Author

* Hiroki Sakurai
* sa11kurarudan11@gmail.com