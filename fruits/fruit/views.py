from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView,
    TemplateView, RedirectView, UpdateView,
    DeleteView, FormView
	)
from django.contrib.auth.views import (
    LoginView, PasswordChangeView,
    PasswordChangeDoneView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
	)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import ModelFormMixin

from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.contrib.auth import login
from django.conf import settings
from django.core.files.storage import default_storage
import os
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class OnlyTheUserMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk']


class OnlyTheFarmMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.farm.pk == self.kwargs['farm_pk']


class OnlyTheCartMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.cart.pk == self.kwargs['cart_pk']


class ItemList(ListView):
    model = FarmProduct
    template_name = 'fruit/list.html'
    paginate_by = 12

    def get_queryset(self):
        products = FarmProduct.objects.all().order_by('-updated')
        if 'q' in self.request.GET and self.request.GET['q'] is not None:
            query_objects = self.request.GET['q']
            products = products.filter(product_name__icontains=query_objects)
        return products


class ItemDetail(ModelFormMixin, DetailView):
    model = FarmProduct
    template_name = 'fruit/detail.html'
    form_class = ReviewForm

    def form_valid(self, form):
        review = form.save(commit=False)
        review.product = self.get_object()
        review.user = self.request.user
        review.save()
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['pk']
        context['comments'] = Review.objects.exclude(
            comment='').filter(product=product_id)[:5]
        context['review_counts'] = Review.objects.filter(
            product=product_id).count()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = self.get_object()
            return self.form_invalid(form)


@login_required
def delete_comment(request):
    comment_pk = request.POST.get('comment_pk')
    if comment_pk is None:
        return JsonResponse({'error': 'invalid parameter'})
    try:
        comment = Review.objects.get(pk=comment_pk)
        comment.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})


@login_required
def read_comment(request):
    comment_pk = request.POST.get('comment_pk')
    if comment_pk is None:
        return JsonResponse({'error': 'invalid parameter'})
    try:
        comment = Review.objects.get(pk=comment_pk)
        str_comment = str(comment.comment)
        str_comment_pk = str(comment.pk)
        return JsonResponse(
            {'comment': str_comment, 'comment_pk': str_comment_pk})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})


@login_required
def overwrite_comment(request):
    comment_pk = request.POST.get('comment_pk')
    textarea_content = request.POST.get('textarea_content')
    if comment_pk is None:
        return JsonResponse({'error': 'invalid parameter'})
    try:
        comment = Review.objects.get(pk=comment_pk)
        comment.comment = textarea_content
        comment.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})


class Login(LoginView):
    form_class = LoginForm
    template_name = 'fruit/login.html'


class SignUp(CreateView):
    template_name = 'fruit/sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }
        subject_template = get_template(
            'fruit/mail_template/sign_up/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template(
            'fruit/mail_template/sign_up/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        messages.success(self.request, 'ご登録のメールアドレスに本登録用リンクを送付しました')
        return HttpResponseRedirect(reverse('fruit:sign_up'))


class SignUpDone(TemplateView):
    template_name = 'fruit/sign_up_done.html'
    timeout_seconds = getattr(
        settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)

    def get(self, request, **kwargs):
        token = kwargs.get('token')

        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
        except SignatureExpired:
            return HttpResponseBadRequest()
        except BadSignature:
            return HttpResponseBadRequest()
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()

                    his_cart = ShoppingCart()
                    his_cart.user = user
                    his_cart.save()

                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')
                    return super().get(request, **kwargs)
        return HttpResponseBadRequest()


class UserMyPage(LoginRequiredMixin, TemplateView):
    template_name = 'fruit/user_mypage.html'


class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('fruit:password_change_done')
    template_name = 'fruit/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'fruit/password_change_done.html'


class PasswordReset(PasswordResetView):
    subject_template_name = 'fruit/mail_template/password_reset/subject.txt'
    email_template_name = 'fruit/mail_template/password_reset/message.txt'
    template_name = 'fruit/password_reset.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('fruit:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'fruit/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url = reverse_lazy('fruit:password_reset_complete')
    template_name = 'fruit/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'fruit/password_reset_complete.html'


class EmailChange(LoginRequiredMixin, FormView):
    template_name = 'fruit/email_change.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }
        subject = render_to_string(
            'fruit/mail_template/email_change/subject.txt', context)
        message = render_to_string(
            'fruit/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('fruit:email_change_done')


class EmailChangeDone(LoginRequiredMixin, TemplateView):
    template_name = 'fruit/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, TemplateView):
    template_name = 'fruit/email_change_complete.html'
    timeout_seconds = getattr(
        settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)

    def get(self, request, **kwargs):
        token = kwargs.get('token')

        try:
            new_email = loads(token, max_age=self.timeout_seconds)
        except SignatureExpired:
            return HttpResponseBadRequest()
        except BadSignature:
            return HttpResponseBadRequest()
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)


class FarmInfo(LoginRequiredMixin, TemplateView):
    template_name = 'fruit/farm_info.html'


@login_required
def ShoppingCartItemList(request):

    if request.method == 'GET':
        return render(request, 'fruit/cart.html')
    else:
        user = request.user
        product_pk = request.POST.get('product_pk')
        product = FarmProduct.objects.get(pk=product_pk)
        amount = request.POST.get('cart_amount')

        # 商品の選択数量と当該商品の現存在庫数量との比較
        current_product_stock = product.product_stock
        new_product_stock = int(current_product_stock) - int(amount)

        # 商品の選択数量と当該商品の現存在庫数量との比較で条件分岐
        if new_product_stock >= 0:
            product.product_stock = str(new_product_stock)
            product.save()
            # そのユーザーのカートに既にその商品があるか確認
            is_exist = ShoppingCartItem.objects.filter(
                cart__user=user).filter(product=product)
            if is_exist:
                current_amount = is_exist[0].amount
                new_amount = int(current_amount) + int(amount)

                if new_amount <= 20:
                    is_exist[0].amount = str(new_amount)
                    is_exist[0].save()
                else:
                    is_exist[0].amount = str(20)
                    is_exist[0].save()
            else:
                new_cart_item = ShoppingCartItem()
                new_cart_item.cart = request.user.cart
                new_cart_item.product = product
                new_cart_item.amount = amount
                new_cart_item.save()
            return redirect('fruit:cart_item_list')
        else:
            product.product_stock = str(0)
            product.save()

            is_exist = ShoppingCartItem.objects.filter(
                cart__user=user).filter(product=product)
            if is_exist:
                current_amount = is_exist[0].amount
                new_amount = int(current_amount) + int(current_product_stock)

                if new_amount <= 20:
                    is_exist[0].amount = str(new_amount)
                    is_exist[0].save()
                else:
                    is_exist[0].amount = str(20)
                    is_exist[0].save()
                    remain = int(new_amount) - 20
                    product.product_stock = str(remain)
                    product.save()
            else:
                new_cart_item = ShoppingCartItem()
                new_cart_item.cart = request.user.cart
                new_cart_item.product = product
                new_cart_item.amount = current_product_stock
                new_cart_item.save()
            return redirect('fruit:cart_item_list')


@login_required
def delete_cart_item(request):
    cart_item_pk = request.POST.get('cart_item_pk')

    if cart_item_pk is None:
        return JsonResponse({'error': 'invalid parameter'})

    try:
        cart_item = ShoppingCartItem.objects.get(pk=cart_item_pk)
        # 削除するカートアイテムの数量分、在庫数量を戻す処理
        cart_item_amount = cart_item.amount
        cart_item_product = cart_item.product
        new_amount = int(cart_item_amount) + \
            int(cart_item_product.product_stock)

        if new_amount <= 20:
            cart_item_product.product_stock = str(new_amount)
            cart_item_product.save()
            # カートアイテムの削除
            cart_item.delete()
            return JsonResponse({'success': True})
        else:
            # 出品者の追加と重なってカートアイテムの数量を在庫数量に戻し入れると20セット以上になる場合
            cart_item_product.product_stock = str(20)
            cart_item_product.save()
            # カートアイテムの削除
            cart_item.delete()
            return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})


@login_required
def plus_cart_item(request):
    cart_item_pk = request.POST.get('cart_item_pk')

    if cart_item_pk is None:
        return JsonResponse({'error': 'invalid parameter'})
    try:
        cart_item = ShoppingCartItem.objects.get(pk=cart_item_pk)
        new_amount = int(cart_item.amount) + 1
        # カートにある商品の数量を追加する分、その商品の在庫数量を減少させる
        cart_item_product = cart_item.product
        new_stock = int(cart_item_product.product_stock) - 1

        if new_amount <= 20 and new_stock >= 0:
            cart_item.amount = str(new_amount)
            cart_item.save()
            cart_item_product.product_stock = str(new_stock)
            cart_item_product.save()
        elif new_amount <= 20 and new_stock < 0:
            cart_item_product.product_stock = str(0)
            messages.error(request, '現在追加可能な最大数量です')
            cart_item_product.save()
        elif new_amount > 20 and new_stock >= 0:
            cart_item.amount = str(20)
            messages.error(request, '20セット以上は追加できません')
            cart_item.save()
        elif new_amount > 20 and new_stock < 0:
            cart_item.amount = str(20)
            cart_item.save()
            cart_item_product.product_stock = str(0)
            cart_item_product.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})


@login_required
def minus_cart_item(request):
    cart_item_pk = request.POST.get('cart_item_pk')

    if cart_item_pk is None:
        return JsonResponse({'error': 'invalid parameter'})
    try:
        cart_item = ShoppingCartItem.objects.get(pk=cart_item_pk)
        new_amount = int(cart_item.amount) - 1
        # カートにある商品の数量を減少させる分、その商品の在庫数量を増加させる
        cart_item_product = cart_item.product
        new_stock = int(cart_item_product.product_stock) + 1

        if new_amount >= 1 and new_stock <= 20:
            cart_item.amount = str(new_amount)
            cart_item.save()
            cart_item_product.product_stock = str(new_stock)
            cart_item_product.save()
        elif new_amount >= 1 and new_stock > 20:
            cart_item.amount = str(new_amount)
            cart_item.save()
            cart_item_product.product_stock = str(20)
            cart_item_product.save()
        elif new_amount < 1 and new_stock <= 20:
            cart_item.amount = str(1)
            cart_item.save()
        elif new_amount < 1 and new_stock > 20:
            cart_item.amount = str(1)
            cart_item.save()
            cart_item_product.product_stock = str(20)
            cart_item_product.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e.args)})


class ShoppingCartConfirm(LoginRequiredMixin, OnlyTheCartMixin, DetailView):
    model = ShoppingCart
    pk_url_kwarg = 'cart_pk'
    template_name = "fruit/cart_confirm.html"

    def get(self, request, *args, **kwargs):
        if request.user.postal_code_dlv1 == '' or request.user.postal_code_dlv2 ==\
            '' or request.user.tel_number_dlv1 == '' or request.user.tel_number_dlv2 ==\
            '' or request.user.tel_number_dlv3 == '' or request.user.address_dlv1 ==\
                '' or request.user.address_dlv2 == '':
            messages.error(self.request, "お届け先住所・郵便番号・電話番号を入力して下さい")
            return redirect(reverse_lazy('fruit:edit_user', 
			                              kwargs={'pk': request.user.pk}))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        cart = self.get_object()
        token = request.POST['stripeToken']
        user = request.user

        try:
            charge = stripe.Charge.create(
                amount=cart.total_amount,
                currency='jpy',
                source=token,
                description='メール:{}'.format(request.user.email),)
        except stripe.error.CardError:
            context = self.get_context_data()
            context['message'] = 'Your payment cannot be completed. The card has been declined.'
            messages.error(self.request, "カード使用不可のため決済処理が行えませんでした")
            return render(request, "fruit/cart_confirm.html", context)
        else:
            order = Order.objects.create(user=user, stripe_id=charge.id)

        try:
            # ショッピングカートアイテムインスタンスからオーダーアイテムインスタンスを作った後、前者を削除
            user_cart_items_list = ShoppingCartItem.objects.filter(
                cart__user=user)
            for item in user_cart_items_list:
                OrderedItem.objects.create(
                    order=order, product=item.product, amount=item.amount)
            ShoppingCartItem.objects.filter(cart__user=user).delete()
        except Exception:
            messages.error(self.request, "エラーが発生し処理を途中で終了しました")
            return render(request, "fruit/cart_confirm.html", context)

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'user': user,
        }
        subject_template = get_template(
            'fruit/mail_template/purchase_complete/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template(
            'fruit/mail_template/purchase_complete/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)

        messages.success(self.request, "注文処理が完了しました")
        return redirect('fruit:item_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publick_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class UserEdit(LoginRequiredMixin, OnlyTheUserMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'fruit/user_edit.html'

    def form_valid(self, form):
        ctx = {'form': form}

        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'fruit/user_edit_confirm.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'fruit/user_edit.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('fruit:user_mypage'))

    def form_invalid(self, form):
        messages.warning(self.request, "入力に誤りがあります")
        return render(self.request, 'fruit/user_edit.html', {'form': form})

    def get_success_url(self, **kwargs):
        messages.success(self.request, "ユーザー情報を更新しました")
        return reverse('fruit:user_mypage')


class UserDelete(LoginRequiredMixin, OnlyTheUserMixin, DeleteView):
    model = User
    template_name = 'fruit/user_delete.html'
    success_url = reverse_lazy('fruit:item_list')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, "ユーザー情報を削除しました")
        return result


class OrderHistory(LoginRequiredMixin, ListView):
    context_object_name = 'orders'
    template_name = 'fruit/order_history.html'

    def get_queryset(self):
        return Order.objects.filter(
               user=self.request.user).order_by('-created_at')


class FarmInfoRedirect(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        messages.warning(self.request, "出品前に農場基本情報の登録が必要です")
        return redirect(reverse_lazy('fruit:farm_info_register', 
		                              kwargs={'pk': request.user.pk}))
        

class FarmInfoRegister(LoginRequiredMixin, OnlyTheUserMixin, CreateView):
    form_class = FarmInfoRegisterChangeForm
    template_name = 'fruit/farm_info_register.html'

    def form_valid(self, form):
        ctx = {'form': form}

        if self.request.POST.get('next', '') == 'confirm':
            farm_image = form.cleaned_data.get('farm_image')
            if farm_image:
                temp_image = default_storage.save(
                    'temp_images/' + farm_image.name, farm_image)
                self.request.session['temp_farm_image_path'] = temp_image
            return render(self.request, 
			              'fruit/farm_info_register_confirm.html', ctx)

        if self.request.POST.get('next', '') == 'back':
            temp_image = self.request.session.pop('temp_farm_image_path', '')
            if temp_image:
                default_storage.delete(temp_image)
            return render(self.request, 'fruit/farm_info_register.html', ctx)

        if self.request.POST.get('next', '') == 'create':
            user = self.request.user
            farm = form.save(commit=False)
            farm.user = user

            temp_image = self.request.session.pop('temp_farm_image_path', '')
            if temp_image:
                image_file_name = os.path.basename(temp_image)
                image_obj = default_storage.open(temp_image)
                farm_image = default_storage.save(
                    'farm_images/' + image_file_name, image_obj)

                farm.farm_image = farm_image
                default_storage.delete(temp_image)
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('fruit:farm_info_page'))

    def form_invalid(self, form):
        messages.warning(self.request, "入力に誤りがあります")
        return render(self.request,
                      'fruit/farm_info_register.html',
                      {'form': form})

    def get_success_url(self, **kwargs):
        messages.success(self.request, "農場基本情報の登録が完了しました")
        return reverse(
            'fruit:farm_info_page', kwargs={
                'pk': self.request.user.pk})


class FarmInfoChange(LoginRequiredMixin, OnlyTheFarmMixin, UpdateView):
    model = Farm
    form_class = FarmInfoRegisterChangeForm
    pk_url_kwarg = 'farm_pk'
    template_name = 'fruit/farm_info_change.html'

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            farm_image = form.cleaned_data.get('farm_image')
            # 画像をクリアするチェックが付いているか
            if self.request.POST.get('farm_image-clear') == 'on':
                self.request.session['farm_image_delete_flag'] = 'on'
            else:
                self.request.session.pop('farm_image_delete_flag', '')

            if farm_image:
                temp_image = default_storage.save(
                    'temp_images/' + farm_image.name, farm_image)
                self.request.session['temp_farm_image_path'] = temp_image
            return render(self.request, 
			              'fruit/farm_info_change_confirm.html', ctx)

        if self.request.POST.get('next', '') == 'back':
            temp_image = self.request.session.pop('temp_farm_image_path', '')
            if temp_image:
                default_storage.delete(temp_image)
            return render(self.request, 'fruit/farm_info_change.html', ctx)

        if self.request.POST.get('next', '') == 'create':
            temp_image = self.request.session.pop('temp_farm_image_path', '')
            farm_info = form.save(commit=False)

            if temp_image:
                image_file_name = os.path.basename(temp_image)
                image_obj = default_storage.open(temp_image)
                farm_image = default_storage.save(
                    'farm_images/' + image_file_name, image_obj)

                farm_info.farm_image = farm_image
                farm_info.save()
                default_storage.delete(temp_image)

            image_delete_flag = self.request.session.pop(
                'farm_image_delete_flag', '')

            if image_delete_flag:
                farm_info.farm_image = None
                farm_info.save()
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('fruit:farm_info_page'))

    def get_success_url(self, **kwargs):
        messages.success(self.request, "農場基本情報の変更が完了しました")
        return reverse(
            'fruit:farm_info_page', kwargs={
                'pk': self.request.user.pk})


class FarmInfoDelete(LoginRequiredMixin, OnlyTheFarmMixin, DeleteView):
    model = Farm
    pk_url_kwarg = 'farm_pk'
    template_name = 'fruit/farm_info_delete.html'

    def get_success_url(self, **kwargs):
        messages.success(self.request, "農場基本情報の削除が完了しました")
        return reverse('fruit:farm_info_page', 
		                kwargs={'pk': self.request.user.pk})


class FarmProductRegister(LoginRequiredMixin, OnlyTheFarmMixin, CreateView):
    template_name = 'fruit/farm_product_register.html'
    form_class = FarmProductRegisterAndChangeForm
    pk_url_kwarg = 'farm_pk'

    def form_valid(self, form):
        ctx = {'form': form}

        if self.request.POST.get('next', '') == 'confirm':
            product_image = form.cleaned_data.get('product_image')
            if product_image:
                temp_image = default_storage.save(
                    'temp_images/' + product_image.name, product_image)
                self.request.session['temp_image_path'] = temp_image
            return render(self.request, 
			              'fruit/farm_product_register_confirm.html', ctx)

        if self.request.POST.get('next', '') == 'back':
            temp_image = self.request.session.pop('temp_image_path', '')
            if temp_image:
                default_storage.delete(temp_image)
            return render(self.request, 'fruit/farm_product_register.html', 
			              ctx)

        if self.request.POST.get('next', '') == 'create':
            user = self.request.user
            farm_product = form.save(commit=False)
            farm_product.farm = user.farm

            temp_image = self.request.session.pop('temp_image_path', '')

            if temp_image:
                image_file_name = os.path.basename(temp_image)
                image_obj = default_storage.open(temp_image)
                rsv_image = default_storage.save(
                    'rsv_images/' + image_file_name, image_obj)

                farm_product.product_image = rsv_image
                default_storage.delete(temp_image)
            return super().form_valid(form)

        else:
            return redirect(reverse_lazy('fruit:farm_info_page', 
			                kwargs={'pk': self.request.user.pk}))

    def form_invalid(self, form):
        messages.warning(self.request, "入力に誤りがあります")
        return render(self.request,
                      'fruit/farm_product_register.html',
                      {'form': form})

    def get_success_url(self, **kwargs):
        messages.success(self.request, "出品果物の登録が完了しました")
        return reverse('fruit:farm_info_page', 
		                kwargs={'pk': self.request.user.pk})


class FarmProductChange(LoginRequiredMixin, UpdateView):
    model = FarmProduct
    form_class = FarmProductRegisterAndChangeForm
    pk_url_kwarg = 'farm_product_pk'
    template_name = 'fruit/farm_product_change.html'

    def get(self, request, *args, **kwargs):
        url_param = self.kwargs.get('farm_product_pk')

        if url_param:
            request.session['url_param'] = url_param
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ctx = {'form': form}

        if self.request.POST.get('next', '') == 'confirm':
            product_image = form.cleaned_data.get('product_image')

            if self.request.POST.get('product_image-clear') == 'on':
                self.request.session['image_delete_flag'] = 'on'
            else:
                self.request.session.pop('image_delete_flag', '')

            if product_image:
                temp_image = default_storage.save(
                    'temp_images/' + product_image.name, product_image)
                self.request.session['temp_image_path'] = temp_image
            return render(self.request, 
			              'fruit/farm_product_change_confirm.html',ctx)

        if self.request.POST.get('next', '') == 'back':
            temp_image = self.request.session.pop('temp_image_path', '')
            if temp_image:
                default_storage.delete(temp_image)
            return render(self.request, 'fruit/farm_product_change.html', ctx)

        if self.request.POST.get('next', '') == 'change':
            self.request.session.pop('url_param', '')

            farm_product = form.save(commit=False)
            farm = self.request.user.farm
            farm_product.farm = farm
            farm_product.available = True

            temp_image = self.request.session.pop('temp_image_path', '')

            if temp_image:
                image_file_name = os.path.basename(temp_image)
                image_obj = default_storage.open(temp_image)
                rsv_image = default_storage.save(
                    'rsv_images/' + image_file_name, image_obj)

                farm_product.product_image = rsv_image
                farm_product.save()
                default_storage.delete(temp_image)

            image_delete_flag = self.request.session.pop(
                'image_delete_flag', '')
            if image_delete_flag:
                farm_product.product_image = None
                farm_product.save()
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('fruit:farm_info_page'),
			                kwargs={'pk': self.request.user.pk})

    def form_invalid(self, form):
        messages.warning(self.request, "入力に誤りがあります")
        return render(self.request,
                      'fruit/farm_product_change.html',
                      {'form': form})

    def get_success_url(self, **kwargs):
        messages.success(self.request, "出品果物の変更が完了しました")
        return reverse('fruit:farm_info_page',
		                kwargs={'pk': self.request.user.pk})


class FarmProductsList(LoginRequiredMixin, ListView):
    model = FarmProduct
    template_name = 'fruit/farm_products_list.html'

    def get_queryset(self):
        return FarmProduct.objects.filter(farm=self.request.user.farm.pk)

    def post(self, request):
        delete_list = request.POST.getlist('delete_flags')
        request.session['delete_farm_products_list'] = delete_list

        delete_farm_products = FarmProduct.objects.filter(pk__in=delete_list)
        context = {'delete_farm_products': delete_farm_products}
        return render(request, 'fruit/farm_product_delete.html', context)


@login_required
def FarmProductsDelete(request):
    delete_farm_products_list = request.session.pop(
        'delete_farm_products_list', '')

    if delete_farm_products_list:
        FarmProduct.objects.filter(pk__in=delete_farm_products_list).delete()
        messages.success(request, "削除が完了しました")
        return redirect(reverse_lazy('fruit:farm_info_page', 
		                kwargs={'pk': request.user.pk}))
    else:
        messages.error(request, "もう一度やり直して下さい")
        return redirect(reverse_lazy('fruit:farm_products_list'))
