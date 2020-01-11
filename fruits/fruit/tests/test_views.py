from django.test import TestCase
from ..views import *
from ..forms import *
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.signing import dumps
from .factory import *


class TestItemList(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        res = self.client.get(reverse('fruit:item_list'))
        self.assertTemplateUsed(res, 'fruit/list.html')

    def test_pagination(self):
        """ページネーション機能が存在しているかを確認"""
        res = self.client.get(reverse('fruit:item_list'))
        self.assertTrue('is_paginated' in res.context)
        self.assertTrue(len(res.context['object_list']) == 0)

    def test_pagination_with_page_exist(self):
        """存在するページにアクセスした時に適切なレスポンスを返すかを確認"""
        res_exist = self.client.get(reverse('fruit:item_list') + '?page=1')
        self.assertEqual(res_exist.status_code, 200)

    def test_pagination_with_page_not_exist(self):
        """存在しないページにアクセスした時にエラーを返すかを確認"""
        res_not_exist = self.client.get(reverse('fruit:item_list') + '?page=10000')
        self.assertEqual(res_not_exist.status_code, 404)

    def test_pagination_with_invalid_page(self):
        """不適切なページを指定した場合にエラーを返すかを確認"""
        res_not_exist = self.client.get(reverse('fruit:item_list') + '?page=hogehoge')
        self.assertEqual(res_not_exist.status_code, 404)

    def test_pagination_with_query(self):
        """ページネーション機能と検索機能が同時に機能するかを確認"""
        product = FarmProductFactory()
        res = self.client.get(reverse('fruit:item_list') + '?q=りんご&page=1')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, product.product_name)

    def test_query_with_exist(self):
        """指定した語を検索した時、該当するオブジェクトが一覧画面に反映されていることを確認"""
        product = FarmProductFactory()
        res_apple = self.client.get(reverse('fruit:item_list') + '?q=美味しいりんご')
        self.assertEqual(res_apple.status_code, 200)
        self.assertContains(res_apple, product.product_name)

    def test_query_with_no_exist(self):
        """指定した語を検索した時、データベースに存在しない語の場合、一覧画面に結果が反映されないことを確認"""
        product = FarmProductFactory()
        res_orange = self.client.get(reverse('fruit:item_list') + '?q=不味いオレンジ')
        self.assertEqual(res_orange.status_code, 200)
        self.assertNotContains(res_orange, product.product_name)


class TestItemDetail(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        product = FarmProductFactory()
        res = self.client.get(reverse('fruit:item_detail', kwargs={'pk': product.pk}))
        self.assertTemplateUsed(res, 'fruit/detail.html')

    def test_object_exist(self):
        """指定した個別オブジェクトがページに存在するかを確認"""
        product = FarmProductFactory()
        res = self.client.get(reverse('fruit:item_detail', kwargs={'pk': product.pk}))
        self.assertContains(res, product.product_name)

    def test_comment_exist(self):
        """"該当商品のデータベースにコメント(スターのみは除く)がある場合、コメントが画面に反映されているか確認"""
        self.user = get_user_model().objects.create_user(
            email='comment_exist@aaa.com', name='aaa', password='aaa')
        product = FarmProductFactory()
        comment = ReviewFactory(user=self.user, product=product)
        res = self.client.get(reverse('fruit:item_detail', kwargs={'pk': product.pk}))
        self.assertContains(res, comment.comment)

    def test_comment_no_exist(self):
        """該当商品のデータベースにコメントがない場合、画面にその商品に対するコメントが存在しないことを確認"""
        self.user = get_user_model().objects.create_user(
            email='comment_exist@aaa.com', name='aaa', password='aaa')
        user_1 = User.objects.create(email='hoge@aaa.com', name='hoge', password='hoge')
        farm_1 = Farm.objects.create(user=user_1, farm_name='hoge農園')
        product_1 = FarmProductFactory(farm=farm_1)
        comment = ReviewFactory(user=self.user)
        res = self.client.get(reverse('fruit:item_detail', kwargs={'pk': product_1.pk}))
        self.assertNotContains(res, comment.comment)

    def test_comment_with_logged_in(self):
        """ログインしている場合POSTしてコメントが可能なことの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        product = FarmProductFactory()
        res = self.client.get(reverse('fruit:item_detail', kwargs={'pk': product.pk}))
        self.assertEqual(Review.objects.count(), 0)

        data = {'user': self.user.pk, 'product': product.pk, 'rating': 3,
                'comment': 'good', 'created': timezone.now(), 'updated': timezone.now()}
        self.client.post(reverse('fruit:item_detail', kwargs={'pk': product.pk}), data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().comment, 'good')

    def test_unable_to_comment_with_not_logged_in(self):
        """ログインしていない場合コメントフォームがテンプレートに表示されないことの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')

        product = FarmProductFactory()
        res = self.client.get(reverse('fruit:item_detail', kwargs={'pk': product.pk}))

        self.assertNotContains(res, res.context['form'])

    def test_POST_comment_with_valid(self):
        """有効なコメントをPOSTするとデータベースに1件反映されることの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        product = FarmProductFactory()
        self.client.get(reverse('fruit:item_detail', kwargs={'pk': product.pk}))
        self.assertEqual(Review.objects.count(), 0)

        data = {'user': self.user.pk, 'product': product.pk, 'rating': 3,
                'comment': 'good', 'created': timezone.now(), 'updated': timezone.now()}
        res_post = self.client.post(reverse('fruit:item_detail', kwargs={'pk': product.pk}), data)
        self.assertEquals(res_post.status_code, 302)

        self.assertEqual(Review.objects.count(), 1)

    def test_POST_comment_with_invalid(self):
        """有効でないコメントをPOSTしてもデータベースに反映されないことの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        product = FarmProductFactory()
        self.client.get(reverse('fruit:item_detail', kwargs={'pk': product.pk}))
        self.assertEqual(Review.objects.count(), 0)

        data = {}
        res_post = self.client.post(reverse('fruit:item_detail', kwargs={'pk': product.pk}), data)
        self.assertEquals(res_post.status_code, 200)

        form = res_post.context.get('form')
        self.assertTrue(form.errors)

        self.assertEqual(Review.objects.count(), 0)


class TestLogin(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        res = self.client.get(reverse('fruit:login'))
        self.assertTemplateUsed(res, 'fruit/login.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        res = self.client.get(reverse('fruit:login'))
        form = res.context.get('form')
        self.assertIsInstance(form, LoginForm)

    def test_csrf(self):
        """CSRF対策の確認"""
        res = self.client.get(reverse('fruit:login'))
        self.assertContains(res, 'csrfmiddlewaretoken')


class TestLogout(TestCase):
    def test_template_used(self):
        """ログアウト時、指定のページにリダイレクトされるか確認"""
        res = self.client.get(reverse('fruit:logout'))
        self.assertRedirects(res, reverse('fruit:item_list'))


class TestSignUp(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        res = self.client.get(reverse('fruit:sign_up'))
        self.assertTemplateUsed(res, 'fruit/sign_up.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        res = self.client.get(reverse('fruit:sign_up'))
        form = res.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_csrf(self):
        """CSRF対策の確認"""
        res = self.client.get(reverse('fruit:sign_up'))
        self.assertContains(res, 'csrfmiddlewaretoken')

    def test_redirection(self):
        """サインアップ成功時のリダイレクト先が正しいか確認"""
        url = reverse('fruit:sign_up')
        data = {
            'name': 'hoge',
            'email': 'hoge@hoge.com',
            'password1': 'hoge123456',
            'password2': 'hoge123456'
        }
        response = self.client.post(url, data)
        success_url = reverse('fruit:sign_up')

        self.assertRedirects(response, success_url)

    def test_user_num_increase(self):
        """新しいユーザーが登録される際、ユーザー数が1人分増加するかを確認"""
        self.assertFalse(User.objects.count(), 0)

        url = reverse('fruit:sign_up')
        data = {
            'name': 'hoge',
            'email': 'hoge@hoge.com',
            'password1': 'hoge123456',
            'password2': 'hoge123456'
        }
        self.client.post(url, data)
        self.assertEqual(User.objects.count(), 1)


class TestUserMyPage(TestCase):
    def test_redirect_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、ログインページにリダイレクトされるか確認"""
        res = self.client.get(reverse('fruit:user_mypage'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/user_mypage')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:user_mypage'))
        self.assertTemplateUsed(res, 'fruit/user_mypage.html')


class TestPasswordChange(TestCase):
    def test_redirect_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、ログインページにリダイレクトされるか確認"""
        res = self.client.get(reverse('fruit:password_change'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/password_change/')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:password_change'))
        self.assertTemplateUsed(res, 'fruit/password_change.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:password_change'))
        form = res.context.get('form')
        self.assertIsInstance(form, MyPasswordChangeForm)


class TestPasswordChangeDone(TestCase):
    def test_redirect_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、ログインページにリダイレクトされるか確認"""
        res = self.client.get(reverse('fruit:password_change_done'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/password_change/done/')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:password_change_done'))
        self.assertTemplateUsed(res, 'fruit/password_change_done.html')


class TestPasswordReset(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        res = self.client.get(reverse('fruit:password_reset'))
        self.assertTemplateUsed(res, 'fruit/password_reset.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        res = self.client.get(reverse('fruit:password_reset'))
        form = res.context.get('form')
        self.assertIsInstance(form, MyPasswordResetForm)

    def test_redirection(self):
        """パスワードリセット成功時のリダイレクト先が正しいか確認"""
        url = reverse('fruit:password_reset')
        data = {
            'email': 'hoge@hoge.com',
        }
        res = self.client.post(url, data)
        success_url = reverse('fruit:password_reset_done')

        self.assertRedirects(res, success_url)


class TestPasswordResetDone(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        res = self.client.get(reverse('fruit:password_reset_done'))
        self.assertTemplateUsed(res, 'fruit/password_reset_done.html')


class TestPasswordResetComplete(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        res = self.client.get(reverse('fruit:password_reset_complete'))
        self.assertTemplateUsed(res, 'fruit/password_reset_complete.html')


class TestEmailChange(TestCase):
    def test_redirect_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、ログインページにリダイレクトされるか確認"""
        res = self.client.get(reverse('fruit:email_change'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/email/change/')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:email_change'))
        self.assertTemplateUsed(res, 'fruit/email_change.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:email_change'))
        form = res.context.get('form')
        self.assertIsInstance(form, EmailChangeForm)

    def test_redirection(self):
        """アドレス変更成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        url = reverse('fruit:email_change')
        data = {
            'email': 'hoge@hoge.com',
        }
        res = self.client.post(url, data)
        success_url = reverse('fruit:email_change_done')

        self.assertRedirects(res, success_url)


class TestEmailChangeDone(TestCase):
    def test_redirect_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、ログインページにリダイレクトされるか確認"""
        res = self.client.get(reverse('fruit:email_change_done'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/email/change/done/')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:email_change_done'))
        self.assertTemplateUsed(res, 'fruit/email_change_done.html')


class TestEmailChangeComplete(TestCase):
    def test_template_used(self):
        """指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        token = dumps('login@login.com')
        res = self.client.get(reverse('fruit:email_change_complete', kwargs={'token': str(token)}))
        self.assertTemplateUsed(res, 'fruit/email_change_complete.html')


class TestFarmInfo(TestCase):
    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:farm_info_page', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(res, 'fruit/farm_info.html')


class TestShoppingCartItem(TestCase):
    def test_redirect_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、ログインページにリダイレクトされるか確認"""
        res = self.client.get(reverse('fruit:cart_item_list'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/cart_item_list/')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:cart_item_list'))
        self.assertTemplateUsed(res, 'fruit/cart.html')


class TestUserEdit(TestCase):
    def test_403_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、403 Forbiddenになるか"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        res = self.client.get(reverse('fruit:edit_user', kwargs={'pk': self.user.pk}))
        self.assertEqual(res.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:edit_user', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(res, 'fruit/user_edit.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:edit_user', kwargs={'pk': self.user.pk}))
        form = res.context.get('form')
        self.assertIsInstance(form, UserEditForm)

    def test_redirection(self):
        """ユーザー情報変更成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:edit_user', kwargs={'pk': self.user.pk})
        data = {
            'name': 'login',
            'email': 'login@login.com',
            'password': 'login',
            'first_name': 'hoge',
            'last_name': 'fuga',
            'next': 'create'
        }
        res = self.client.post(url, data)
        success_url = reverse('fruit:user_mypage')

        self.assertRedirects(res, success_url)

    def test_move_to_confirmation_page(self):
        """確認ボタンを押した際、確認ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:edit_user', kwargs={'pk': self.user.pk})
        data = {
            'name': 'login',
            'email': 'login@login.com',
            'password': 'login',
            'first_name': 'hoge',
            'last_name': 'fuga',
            'next': 'confirm'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/user_edit_confirm.html')

    def test_back_to_input_page(self):
        """戻るボタンを押した際、入力ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(
            email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:edit_user', kwargs={'pk': self.user.pk})
        data = {
            'name': 'login',
            'email': 'login@login.com',
            'password': 'login',
            'first_name': 'hoge',
            'last_name': 'fuga',
            'next': 'back'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/user_edit.html')

    def test_chage_user_info(self):
        """ユーザー情報変更時、変更内容がデータベースに反映されているか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:edit_user', kwargs={'pk': self.user.pk})
        data = {
            'name': 'login',
            'email': 'login@login.com',
            'password': 'login',
            'first_name': 'hoge',
            'last_name': 'fuga',
            'next': 'create'
        }
        res = self.client.post(url, data)
        self.assertEquals(res.status_code, 302)

        edited_user = get_user_model().objects.get(email='login@login.com')
        self.assertEquals('hoge', edited_user.first_name)


class TestUserDelete(TestCase):
    def test_403_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、403 Forbiddenになるか"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        res = self.client.get(reverse('fruit:delete_user', kwargs={'pk': self.user.pk}))
        self.assertEqual(res.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:delete_user', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(res, 'fruit/user_delete.html')

    def test_redirection(self):
        """ユーザー削除成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:delete_user', kwargs={'pk': self.user.pk})
        res = self.client.post(url)
        success_url = reverse('fruit:item_list')

        self.assertRedirects(res, success_url)

    def test_chage_user_info(self):
        """ユーザー削除成功時、内容がデータベースに反映されているか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        self.assertEqual(get_user_model().objects.count(), 1)

        url = reverse('fruit:delete_user', kwargs={'pk': self.user.pk})
        res = self.client.post(url)
        self.assertEquals(res.status_code, 302)

        self.assertEqual(get_user_model().objects.count(), 0)


class TestOrderHistory(TestCase):
    def test_403_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、403 Forbiddenになるか"""
        res = self.client.get(reverse('fruit:order_history'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/order_history/')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:order_history'))
        self.assertTemplateUsed(res, 'fruit/order_history.html')

    def test_no_object_in_template(self):
        """オーダー履歴がない場合、ページにオブジェクトが表示されないことを確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        res = self.client.get(reverse('fruit:order_history'))
        self.assertNotContains(res, res.context['orders'])

    def test_object_in_template(self):
        """オーダー履歴がある場合、ページにそのオブジェクトが表示されることを確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        OrderFactory(user=self.user)

        res = self.client.get(reverse('fruit:order_history'))
        self.assertQuerysetEqual(res.context['orders'], ['<Order: Order object (1)>'])


class TestFarmInfoRegister(TestCase):
    def test_403_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、403 Forbiddenになるか"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        res = self.client.get(reverse('fruit:farm_info_register', kwargs={'pk': self.user.pk}))
        self.assertEqual(res.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:farm_info_register', kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(res, 'fruit/farm_info_register.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        res = self.client.get(reverse('fruit:farm_info_register', kwargs={'pk': self.user.pk}))
        form = res.context.get('form')
        self.assertIsInstance(form, FarmInfoRegisterChangeForm)

    def test_redirection(self):
        """農場情報登録成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:farm_info_register', kwargs={'pk': self.user.pk})
        data = {
            'farm_name': 'hoge農園',
            'next': 'create'
        }
        res = self.client.post(url, data)
        success_url = reverse('fruit:farm_info_page', kwargs={'pk': self.user.pk})

        self.assertRedirects(res, success_url)

    def test_move_to_confirmation_page(self):
        """確認ボタンを押した際、確認ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:farm_info_register', kwargs={'pk': self.user.pk})
        data = {
            'farm_name': 'hoge農園',
            'next': 'confirm'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/farm_info_register_confirm.html')

    def test_back_to_input_page(self):
        """戻るボタンを押した際、入力ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:farm_info_register', kwargs={'pk': self.user.pk})
        data = {
            'farm_name': 'hoge農園',
            'next': 'back'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/farm_info_register.html')

    def test_register(self):
        """農場情報の登録が成功した際、データーベースに当該情報が1件増えていることを確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        self.assertEqual(Farm.objects.count(), 0)

        url = reverse('fruit:farm_info_register', kwargs={'pk': self.user.pk})
        data = {
            'farm_name': 'hoge農園',
            'next': 'create'
        }
        res = self.client.post(url, data)
        self.assertEquals(res.status_code, 302)

        self.assertEqual(Farm.objects.count(), 1)


class TestFarmInfoChange(TestCase):
    def test_403_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、403 Forbiddenになるか"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        farm = Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_info_change', kwargs={'farm_pk': farm.pk}))
        self.assertEqual(res.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_info_change', kwargs={'farm_pk': farm.pk}))
        self.assertTemplateUsed(res, 'fruit/farm_info_change.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)
        res = self.client.get(reverse('fruit:farm_info_change', kwargs={'farm_pk': farm.pk}))
        form = res.context.get('form')
        self.assertIsInstance(form, FarmInfoRegisterChangeForm)

    def test_redirection(self):
        """農場情報登録成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_info_change', kwargs={'farm_pk': farm.pk})
        data = {
            'farm_name': 'fugafuga農園',
            'next': 'create'
        }
        res = self.client.post(url, data)
        success_url = reverse('fruit:farm_info_page', kwargs={'pk': self.user.pk})

        self.assertRedirects(res, success_url)

    def test_move_to_confirmation_page(self):
        """確認ボタンを押した際、確認ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_info_change', kwargs={'farm_pk': farm.pk})
        data = {
            'farm_name': 'fugafuga農園',
            'next': 'confirm'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/farm_info_change_confirm.html')

    def test_back_to_input_page(self):
        """戻るボタンを押した際、入力ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_info_change', kwargs={'farm_pk': farm.pk})
        data = {
            'farm_name': 'fugafuga農園',
            'next': 'back'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/farm_info_change.html')

    def test_chage_farm_info(self):
        """農場情報変更時、変更内容がデータベースに反映されているか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_info_change', kwargs={'farm_pk': farm.pk})
        data = {
            'farm_name': 'fugafuga農園',
            'next': 'create'
        }
        res = self.client.post(url, data)
        self.assertEquals(res.status_code, 302)

        edited_farm = Farm.objects.get(user=self.user)
        self.assertEquals('fugafuga農園', edited_farm.farm_name)


class TestFarmInfoDelete(TestCase):
    def test_403_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、403に遷移されるか"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        farm = Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_info_delete', kwargs={'farm_pk': farm.pk}))
        self.assertEqual(res.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_info_delete', kwargs={'farm_pk': farm.pk}))
        self.assertTemplateUsed(res, 'fruit/farm_info_delete.html')

    def test_redirection(self):
        """農場情報削除成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_info_delete', kwargs={'farm_pk': farm.pk})
        res = self.client.post(url)
        success_url = reverse('fruit:farm_info_page', kwargs={'pk': self.user.pk})

        self.assertRedirects(res, success_url)

    def test_delete_farm_info(self):
        """農場情報削除成功時、内容がデータベースに反映されているか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        self.assertEqual(Farm.objects.count(), 1)

        url = reverse('fruit:farm_info_delete', kwargs={'farm_pk': farm.pk})
        res = self.client.post(url)
        self.assertEquals(res.status_code, 302)

        self.assertEqual(Farm.objects.count(), 0)


class TestFarmProductRegister(TestCase):
    def test_403_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、403 Forbiddenになるか"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        farm = Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_product_register', kwargs={'farm_pk': farm.pk}))
        self.assertEqual(res.status_code, 403)

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_product_register', kwargs={'farm_pk': farm.pk}))
        self.assertTemplateUsed(res, 'fruit/farm_product_register.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)
        res = self.client.get(reverse('fruit:farm_product_register', kwargs={'farm_pk': farm.pk}))
        form = res.context.get('form')
        self.assertIsInstance(form, FarmProductRegisterAndChangeForm)

    def test_redirection(self):
        """商品情報登録成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_product_register', kwargs={'farm_pk': farm.pk})
        data = {
            'product_name': '美味しいオレンジ',
            'product_category': 'オレンジ',
            'product_origin': '和歌山県産',
            'product_description': 'とれたてです。',
            'product_weight': '25',
            'product_stock': '10',
            'product_price': 7000,
            'created': timezone.now(),
            'updated': timezone.now(),
            'available': True,
            'farm': farm,
            'next': 'create'
        }
        res = self.client.post(url, data)
        success_url = reverse('fruit:farm_info_page', kwargs={'pk': self.user.pk})

        self.assertRedirects(res, success_url)

    def test_move_to_confirmation_page(self):
        """確認ボタンを押した際、確認ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_product_register', kwargs={'farm_pk': farm.pk})
        data = {
            'product_name': '美味しいオレンジ',
            'product_category': 'オレンジ',
            'product_origin': '和歌山県産',
            'product_description': 'とれたてです。',
            'product_weight': '25',
            'product_stock': '10',
            'product_price': 7000,
            'created': timezone.now(),
            'updated': timezone.now(),
            'available': True,
            'farm': farm,
            'next': 'confirm'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/farm_product_register_confirm.html')

    def test_back_to_input_page(self):
        """戻るボタンを押した際、入力ページにレンダリングされているかの確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        url = reverse('fruit:farm_product_register', kwargs={'farm_pk': farm.pk})
        data = {
            'product_name': '美味しいオレンジ',
            'product_category': 'オレンジ',
            'product_origin': '和歌山県産',
            'product_description': 'とれたてです。',
            'product_weight': '25',
            'product_stock': '10',
            'product_price': 7000,
            'created': timezone.now(),
            'updated': timezone.now(),
            'available': True,
            'farm': farm,
            'next': 'back'
        }
        res = self.client.post(url, data)

        self.assertTemplateUsed(res, 'fruit/farm_product_register.html')

    def test_register(self):
        """商品情報の登録が成功した際、データーベースに当該情報が1件増えていることを確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)

        self.assertEqual(FarmProduct.objects.count(), 0)

        url = reverse('fruit:farm_product_register', kwargs={'farm_pk': farm.pk})
        data = {
            'product_name': '美味しいオレンジ',
            'product_category': 'オレンジ',
            'product_origin': '和歌山県産',
            'product_description': 'とれたてです。',
            'product_weight': '25',
            'product_stock': '10',
            'product_price': 7000,
            'created': timezone.now(),
            'updated': timezone.now(),
            'available': True,
            'farm': farm,
            'next': 'create'
        }
        res = self.client.post(url, data)
        self.assertEquals(res.status_code, 302)

        self.assertEqual(FarmProduct.objects.count(), 1)


class TestFarmProductChange(TestCase):
    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = Farm.objects.create(user=self.user, farm_name='test農園')
        product = FarmProductFactory(farm=farm)
        res = self.client.get(
            reverse(
                'fruit:farm_product_change',
                kwargs={
                    'farm_product_pk': product.pk}))
        self.assertTemplateUsed(res, 'fruit/farm_product_change.html')

    def test_contains_form(self):
        """指定のフォームの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)
        product = FarmProductFactory(farm=farm)
        res = self.client.get(
            reverse(
                'fruit:farm_product_change',
                kwargs={
                    'farm_product_pk': product.pk}))
        form = res.context.get('form')
        self.assertIsInstance(form, FarmProductRegisterAndChangeForm)

    def test_redirection(self):
        """商品情報変更成功時のリダイレクト先が正しいか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)
        product = FarmProductFactory(farm=farm)

        url = reverse('fruit:farm_product_change', kwargs={'farm_product_pk': product.pk})
        data = {
            'product_name': '美味しいオレンジ',
            'product_category': 'オレンジ',
            'product_origin': '和歌山県産',
            'product_description': 'とれたてです。',
            'product_weight': '25',
            'product_stock': '10',
            'product_price': 7000,
            'created': timezone.now(),
            'updated': timezone.now(),
            'available': True,
            'farm': farm,
            'next': 'change'
        }
        res = self.client.post(url, data)
        success_url = reverse('fruit:farm_info_page', kwargs={'pk': self.user.pk})

        self.assertRedirects(res, success_url)


    def test_chage_farm_product(self):
        """商品情報変更時、変更内容がデータベースに反映されているか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        farm = FarmFactory(user=self.user)
        product = FarmProductFactory(farm=farm)

        url = reverse('fruit:farm_product_change', kwargs={'farm_product_pk': product.pk})
        data = {
            'product_name': '美味しいみかん',
            'product_category': 'みかん',
            'product_origin': '和歌山県産',
            'product_description': 'とれたてです。',
            'product_weight': '25',
            'product_stock': '10',
            'product_price': 7000,
            'created': timezone.now(),
            'updated': timezone.now(),
            'available': True,
            'farm': farm,
            'next': 'change'
        }
        res = self.client.post(url, data)
        self.assertEquals(res.status_code, 302)

        edited_farm_product = FarmProduct.objects.get(farm=farm)
        self.assertEquals('美味しいみかん', edited_farm_product.product_name)


class TestFarmProductsList(TestCase):
    def test_redirect_if_not_logged_in(self):
        """ログインしていない状態でアクセスした場合、ログインページにリダイレクトされるか確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_products_list'))
        self.assertRedirects(res, '/fruit/login?next=/fruit/farm_products_list/')

    def test_logged_in_uses_correct_template(self):
        """ログインした状態で指定のテンプレートの使用を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)
        Farm.objects.create(user=self.user, farm_name='test農園')
        res = self.client.get(reverse('fruit:farm_products_list'))
        self.assertTemplateUsed(res, 'fruit/farm_products_list.html')

    def test_post_and_get(self):
        """表示するデータを1件追加しその反映を確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        farm = FarmFactory(user=self.user)
        product = FarmProductFactory(farm=farm)

        res = self.client.get(reverse('fruit:farm_products_list'))
        self.assertContains(res, product.product_name)

    def test_post_and_template(self):
        """削除対象オブジェクトのリストをPOSTした際、表示されるテンプレートが意図したものかを確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        farm = FarmFactory(user=self.user)
        product = FarmProductFactory(farm=farm)

        url = reverse('fruit:farm_products_list')
        data = {'delete_flags': [product.pk]}
        res = self.client.post(url, data)
        self.assertTemplateUsed(res, 'fruit/farm_product_delete.html')
        self.assertNotContains(res, res.context['delete_farm_products'])

    def test_post_with_nothing_and_template(self):
        """空のリストをPOSTした際、テンプレートにオブジェクトが含まれないことを確認"""
        self.user = get_user_model().objects.create_user(
            email='login@login.com', name='login', password='login')
        logged_in = self.client.login(email='login@login.com', password='login')
        self.assertTrue(logged_in)

        url = reverse('fruit:farm_products_list')
        data = {'delete_flags': []}
        res = self.client.post(url, data)
        self.assertTemplateUsed(res, 'fruit/farm_product_delete.html')
        self.assertNotContains(res, res.context['delete_farm_products'])
