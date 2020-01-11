from . import views
from django.urls import path
from django.contrib.auth import views as django_auth_views

app_name = 'fruit'

urlpatterns = [
    # 一覧/個別ページ
    path('', views.ItemList.as_view(), name='item_list'),
    path('item/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),

    # コメント機能
    path('ajax_comment_delete/', views.delete_comment, name='delete_comment'),
    path('ajax_comment_read/', views.read_comment, name='read_comment'),
    path('ajax_comment_overwrite/', views.overwrite_comment, name='overwrite_comment'),

    # ログイン/サインアップ/パスワード変更・再設定/メールアドレス変更
    path(
        'login',
        views.Login.as_view(),
        name='login'),
    path(
        'logout',
        django_auth_views.LogoutView.as_view(),
        name='logout'),
    path(
        'sign_up/',
        views.SignUp.as_view(),
        name='sign_up'),
    path(
        'sign_up/done/<token>',
        views.SignUpDone.as_view(),
        name='sign_up_done'),
    path(
        'password_change/',
        views.PasswordChange.as_view(),
        name='password_change'),
    path(
        'password_change/done/',
        views.PasswordChangeDone.as_view(),
        name='password_change_done'),
    path(
        'password_reset/',
        views.PasswordReset.as_view(),
        name='password_reset'),
    path(
        'password_reset/done/',
        views.PasswordResetDone.as_view(),
        name='password_reset_done'),
    path(
        'password_reset/cofirm/<uidb64>/<token>/',
        views.PasswordResetConfirm.as_view(),
        name='password_reset_confirm'),
    path('password_reset/complete/',
         views.PasswordResetComplete.as_view(),
         name='password_reset_complete'),
    path(
        'email/change/',
        views.EmailChange.as_view(),
        name='email_change'),
    path(
        'email/change/done/',
        views.EmailChangeDone.as_view(),
        name='email_change_done'),
    path(
        'email/change/complete/<str:token>/',
        views.EmailChangeComplete.as_view(),
        name='email_change_complete'),

    # ユーザーマイページ/CRUD
    path('user_mypage', views.UserMyPage.as_view(), name='user_mypage'),
    path('edit_user/<int:pk>', views.UserEdit.as_view(), name='edit_user'),
    path('delete_user/<int:pk>', views.UserDelete.as_view(), name='delete_user'),
    path('order_history/', views.OrderHistory.as_view(), name='order_history'),

    # 果物農場ページ/CRUD
    path(
        'farm_info/<int:pk>',
        views.FarmInfo.as_view(),
        name='farm_info_page'),
    path(
        'farm_info_redirect/<int:pk>',
        views.FarmInfoRedirect.as_view(),
        name='farm_info_redirect'),
    path(
        'farm_info_register/<int:pk>',
        views.FarmInfoRegister.as_view(),
        name='farm_info_register'),
    path(
        'farm_info_change/<int:farm_pk>',
        views.FarmInfoChange.as_view(),
        name='farm_info_change'),
    path(
        'farm_info_delete/<int:farm_pk>',
        views.FarmInfoDelete.as_view(),
        name='farm_info_delete'),

    # 果物出品ページ/CRUD
    path(
        'farm_products_list/',
        views.FarmProductsList.as_view(),
        name='farm_products_list'),
    path(
        'farm_product_register/<int:farm_pk>',
        views.FarmProductRegister.as_view(),
        name='farm_product_register'),
    path(
        'farm_product_change/<int:farm_product_pk>',
        views.FarmProductChange.as_view(),
        name='farm_product_change'),
    path(
        'farm_product_delete/',
        views.FarmProductsDelete,
        name='farm_product_delete'),

    # ショッピングカート
    path('cart_item_list/', views.ShoppingCartItemList, name='cart_item_list'),
    path('cart_confirm/<int:cart_pk>', views.ShoppingCartConfirm.as_view(), name='cart_confirm'),
    path('ajax_cart_delete/', views.delete_cart_item, name='delete_cart_item'),
    path('ajax_cart_plus/', views.plus_cart_item, name='plus_cart_item'),
    path('ajax_cart_minus/', views.minus_cart_item, name='minus_cart_item'),
]
