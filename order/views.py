from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from basic.models import Product, Category
from order.models import OrderForm, Shopcart, OrderProduct, Order, ShopcartForm
from user.models import Profile


@login_required(login_url='login')
def shopcart(request):
    user = Profile.objects.get(user=request.user)
    shopcart_ = Shopcart.objects.filter(user=user)
    total = 0
    for shop in shopcart_:
        total += shop.product.price * shop.quantity
    context = {
        'shopcart': shopcart_,
        'total': total,
    }
    return render(request, 'order/shopcart.html', context)


def addshopcart(request, slug):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(slug=slug)
    user = Profile.objects.get(user=request.user)
    data1, data2 = Shopcart.objects.get_or_create(user=user, product=product)

    if request.method == "POST":
        form = ShopcartForm(request.POST)
        if form.is_valid():
            data1.quantity += int(form.cleaned_data.get('quantity'))
            data1.save()
            return redirect(url)


@login_required(login_url='/login')  # check login
def deletefromcart(request, pk):
    Shopcart.objects.filter(id=pk).delete()
    messages.success(request, "Your item deleted from Shop Cart!")
    return redirect('shopcart')
#
#
# def orderproduct(request):
#     profile = Profile.objects.get(user=request.user)
#     shopcart_ = Shopcart.objects.filter(user=profile)
#     total_quantity = 0
#     total = 0
#     for rs in shopcart_:
#         total += rs.product.price * rs.quantity
#         total_quantity += rs.quantity
#     # return HttpResponse(str(total))
#
#     if request.method == 'POST':  # if there is a post
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             data = Order()
#             data.first_name = form.cleaned_data.get('first_name', None)  # get product quantity from form
#             data.last_name = form.cleaned_data.get('last_name', None)
#             data.last_name = form.cleaned_data.get('email', None)
#             data.last_name = form.cleaned_data.get('country', None)
#             data.user_id = request.user.id
#             data.total = total
#             data.total_quantity = total_quantity
#             data.ip = request.META.get('REMOTE_ADDR')
#             ordercode = get_random_string(10).upper()  # random code
#             data.code = ordercode
#             data.save()
#
#             # Move Shopcart items to Order Product items
#             profile = Profile.objects.get(user=request.user)
#             shopcart_ = Shopcart.objects.filter(user=profile)
#             for rs in shopcart_:
#                 detail = OrderProduct()
#                 detail.order_id = data.id  # Order id
#                 detail.product_id = rs.product_id
#                 detail.user = profile
#                 detail.quantity = rs.quantity
#                 detail.price = rs.product.price
#                 detail.amount = rs.amount
#                 detail.save()
#                 product = Product.objects.get(id=rs.product_id)
#                 product.count -= rs.quantity
#                 product.save()
#
#             Shopcart.objects.filter(user=profile).delete()
#             request.session['cart_items'] = 0
#             messages.success(request, "Your Order Has Been Completed! Thank you!")
#             return render(request, 'order/ordercomplete.html', {'ordercode': ordercode})
#         else:
#             messages.warning(request, form.errors)
#             return redirect('orderproduct')
#
#     form = OrderForm()
#     profile = Profile.objects.get(user=request.user)
#     shopcart_ = Shopcart.objects.filter(user_id=profile)
#     context = {
#         'shopcart': shopcart_,
#         'total': total,
#         'profile': profile,
#         'form': form,
#     }
#
#     return render(request, 'order/orderproduct.html', context)
#

def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = Shopcart.objects.filter(user_id=current_user.id)
    profile = Profile.objects.get(user=current_user)
    total_quantity = 0
    total = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        total_quantity += rs.quantity
    # return HttpResponse(str(total))

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        if form.is_valid():

            data = Order()
            data.first_name = form.cleaned_data.get('first_name', None)  # get product quantity from form
            data.last_name = form.cleaned_data.get('last_name', None)
            data.address = form.cleaned_data.get('address', None)
            data.city = form.cleaned_data.get('city', None)
            data.phone = form.cleaned_data.get('phone', None)
            data.user = profile
            data.total = total
            data.total_quantity = total_quantity
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(10).upper()  # random code
            data.code = ordercode
            data.save()

            # Move Shopcart items to Order Product items
            shopcart = Shopcart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id  # Order id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.product.count
                detail.save()
                # Reduce quantity of sold product from Amount of Product
                product = Product.objects.get(id=rs.product_id)
                product.count -= rs.quantity
                product.save()

            Shopcart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0
            messages.success(request, "Your Order Has Been Completed! Thank you!")
            return render(request, 'order/ordercomplete.html', {'ordercode': ordercode, 'category': category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm
    shopcart = Shopcart.objects.filter(user_id=current_user.id)
    profile = Profile.objects.get(user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'profile': profile,
        'form': form,
    }

    return render(request, 'order/orderproduct.html', context)
