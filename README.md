# auth_infra_prototype

## 起動
```sh
docker compose up -d
```

- TOP: http://localhost:18000/
- ADMIN: http://localhost:18000/admin/
- Keycloak: http://localhost:18080/

## ユーザー作成
```sh
docker compose exec billing_infra python manage.py createsuperuser
```

## マイグレーション
```sh
docker compose exec billing_infra python manage.py migrate
```

## ユーザー認証

### エンドポイント一覧の確認
http://localhost:18080/realms/master/.well-known/openid-configuration にブラウザでアクセス

### 認証リクエスト
- `http://localhost:18080/realms/master/protocol/openid-connect/auth?response_type=code&scope=openid&client_id={client_id}&state=abcdefgh&redirect_uri=http://localhost:18000/callback/&nonce=hijklmno` にKeycloakログイン済みのブラウザでアクセスする
- `client_id`はKeycloakの管理画面から確認する
- 事前にKeycloakのClientの`redirect_uri`に`http://localhost:18000/callback/`を登録しておく必要あり

### トークンリクエスト

- 認証リクエストのリダイレクト先URLのクエリーストリングから`code`をコピーして控える
- `client_id`と`client_secret`はKeycloakの管理画面から確認する

```sh
curl -X POST "http://localhost:18080/realms/master/protocol/openid-connect/token" -d "redirect_uri=http://localhost:18000/callback/" -d "grant_type=authorization_code" -d "code={code}" -d "client_id={client_id}" -d "client_secret={client_secret}"| jq -r ".access_token"
```
→ アクセストークンを取得できる

### ユーザーインフォリクエスト

```sh
curl -X GET "http://localhost:18000/api/userinfo/" -H "Authorization: {アクセストークン}"
```
