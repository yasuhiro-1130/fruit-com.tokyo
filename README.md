# fruit.com  

## アプリ概要
果物の消費者と生産者のマッチングサービスです。  
生産者は自分が生産した果物をサイト上に出品し、消費者はそれを直接購入できる、という仮定で作りました。

## リンク先URL
https://fruit-com.tokyo/

## 画面サンプル
|トップ一覧画面|商品個別画面|
|:--:|:--:|
|<img src="https://user-images.githubusercontent.com/38691313/72244457-a7848a00-3631-11ea-9411-669b1cb1dc27.png" width="400px">|<img src="https://user-images.githubusercontent.com/38691313/72246174-845bd980-3635-11ea-833e-5c8e1552f069.png" width="400px">|
|検索機能|コメント入力・削除・編集機能, 商品評価機能|

|果物出品画面|果物出品/確認変更画面|
|:--:|:--:|
|<img src="https://user-images.githubusercontent.com/38691313/72246438-0ba94d00-3636-11ea-9b51-6f65c6e71af8.png" width="400px">|<img src="https://user-images.githubusercontent.com/38691313/72246467-1fed4a00-3636-11ea-9b77-d9d6ed20053e.png" width="400px">|
|画像アップロード機能, 商品内容投稿機能|画像変更機能, 商品内容変更機能|

|ショッピングカート画面|ショッピングカート確認画面|
|:--:|:--:|
|<img src="https://user-images.githubusercontent.com/38691313/72247691-c9cdd600-3638-11ea-8593-c834b8c4c016.png" width="400px">|<img src="https://user-images.githubusercontent.com/38691313/72247701-ccc8c680-3638-11ea-8e60-bf2dd988a358.png" width="400px">|
|数量変更機能, カート内アイテム削除機能(Ajax)|カート内アイテム確認機能|

|注文履歴画面|クレジット入力画面(Stripe)|
|:--:|:--:|
|<img src="https://user-images.githubusercontent.com/38691313/72247831-1b766080-3639-11ea-8ead-ede3a5dbc01a.png" width="400px">|<img src="https://user-images.githubusercontent.com/38691313/72249328-7c536800-363c-11ea-86da-c5ad19b4c640.png" width="400px">|
|注文履歴一覧表示機能|クレジット入力機能|

|商品個別画面/コメント編集・削除機能|ユーザー情報確認変更画面|
|:--:|:--:|
|<img src="https://user-images.githubusercontent.com/38691313/72248162-dacb1700-3639-11ea-874b-c54996417226.png" width="400px">|<img src="https://user-images.githubusercontent.com/38691313/72249257-5332d780-363c-11ea-9b15-bab67cbdd7a3.png" width="400px">|
|コメント編集・削除機能(Ajax)|メールアドレス変更機能, パスワード変更機能,  ユーザー情報変更機能|

|新規登録画面|ログイン画面|
|:--:|:--:|
|<img src="https://user-images.githubusercontent.com/38691313/72249511-deac6880-363c-11ea-8b99-be0dbcb3cfdd.png" width="400px">|<img src="https://user-images.githubusercontent.com/38691313/72249503-dc4a0e80-363c-11ea-8606-2f510c3ad988.png" width="400px">|
|新規ユーザー作成機能|ログイン機能, パスワード再発行機能|

## 使用技術
### フロント  
- HTML
- CSS
- JQuery
- Javascript
- スマホ対応(レスポンシブデザイン)

### バックエンド  
- python  3.7  
- django  2.2  

### インフラ  
- docker  
- docker-compose  
- nginx  

- AWS  
  - RDS(postgres  11.4)  
  - S3  
  - CloudFront  
  - Route53  
  - VPC  
  - IAM  
  - CloudWatch  
  - Certificate Manager  
  - ALB
  - ECR  
  - ECS  
  - EC2(RDS内調査用の踏み台サーバーとして)  

### CIツール  
- CircleCI  2.1  

### テスト  
- unittest  

### Linter  
- Flake8  

### 使用API  
- Stripe(クレジット決済)  
- Sendgrid(メール送信)

### ソースコード管理  
- Github  

### その他  
- お名前ドットコム  
- Cacoo

## クラウドアーキテクチャ
<img width="994" alt="スクリーンショット 2020-01-13 16 17 15" src="https://user-images.githubusercontent.com/38691313/72238139-40120e80-3620-11ea-9ae4-f5bd1edc6a9a.png">

## データベース図


