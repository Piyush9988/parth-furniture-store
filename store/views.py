from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Cart, Order


def home(request):
    return render(request, 'home.html')


def product_list(request):

    query = request.GET.get('q', '')

    products = Product.objects.filter(name__icontains=query)

    return render(request, 'products.html', {'products': products})


def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    Cart.objects.create(
        product=product,
        quantity=1
    )

    messages.success(request, f"{product.name} added to cart")

    return redirect('cart')


def cart_page(request):

    cart_items = Cart.objects.all()

    total_price = 0

    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total_price += item.subtotal

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def remove_from_cart(request, cart_id):

    cart_item = Cart.objects.get(id=cart_id)

    cart_item.delete()

    messages.warning(request, "❌ Item removed from cart")

    return redirect('/cart/')


def checkout(request):

    cart_items = Cart.objects.all()

    # 🚨 Prevent checkout if cart is empty
    if not cart_items.exists():
        messages.warning(request, "⚠️ Your cart is empty. Please add items before checkout.")
        return redirect('products')

    total_price = 0

    for item in cart_items:
        total_price += item.product.price * item.quantity

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")

        Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            total_price=total_price
        )

        Cart.objects.all().delete()

        return redirect('/order-success/')

    return render(request, 'checkout.html', {'total_price': total_price})


def order_success(request):
    return render(request, 'order_success.html')


# ---------- CATEGORY VIEWS ----------

def sofa_products(request):

    products = Product.objects.filter(category='sofa')

    return render(request, 'products.html', {'products': products})


def chair_products(request):

    products = Product.objects.filter(category='chair')

    return render(request, 'products.html', {'products': products})


def contact(request):
    return render(request, 'contact.html')


def cart_count(request):
    count = Cart.objects.count()
    return {'cart_count': count}


def increase_quantity(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrease_quantity(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')