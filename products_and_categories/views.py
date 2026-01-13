from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404,redirect

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
#Добавяме продуктите и категориите за да може да работим с тях
from .models import Product, Category, Cart, CartItem, Order, OrderItem


# Create your views here.

def home(request):

    """Начална страница с категории"""
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def category_products(request, category_slug):
    """Продукти в категория"""
    category = get_object_or_404(Category, slug=category_slug)
    products = category.products.all()
    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })

@login_required
def add_to_cart(request, product_id:int):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    """If the product is already in the cart we increase it, otherwise add it to the cart with quantity 1"""
    if not item_created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    """Return the use on the same page or to the cart"""
    return redirect(request.META.get('HTTP_REFERER', 'view_cart'))

@login_required
def view_cart(request):
    """Shows all products in cart """

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total': cart.total_price()
    }
    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, product_id:int):
    """Remove product from cart"""
    #Тук двойната долна играе ролята на join между cart and user, по този начин взимаме cart_item and user
    cart_item = get_object_or_404(CartItem, id=product_id, cart__user = request.user)
    product_name = cart_item.product.name
    if 'remove_all' in request.POST:
        cart_item.delete()
        msg = '🗑️ Removed all {product_name} from cart'
    elif cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        msg = f"➖ Reduced {product_name} to {cart_item.quantity}"
    else:
        cart_item.delete()
        msg = f"❌ Removed {product_name} from cart"

    messages.success(request, msg)

    return redirect(request.META.get('HTTP_REFERER','view_cart'))


@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.items.count() == 0:
        return redirect('view_cart')

    if request.method == 'POST':
        # Validation and processing the form
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')

        # Пресмятане на общата сума
        shipping_cost = 7 if payment_method == 'cash_on_delivery' else 5
        total_with_shipping = cart.total_price() + shipping_cost

        # Creating object order
        order = Order.objects.create(
            user=request.user,
            cart=cart,  # Важно: запазваме връзката с количката
            email=email,
            shipping_address=address,
            city=city,
            postal_code=postal_code,
            total_amount=total_with_shipping,
            payment_method=payment_method
        )

        #⭐⭐⭐ СТЪПКА 1: Запазване на продуктите в OrderItem модела ⭐⭐⭐
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,  # Връзка с продукта
                product_name=cart_item.product.name,
                product_price=cart_item.product.get_final_price(),
                quantity=cart_item.quantity
            )

        # ⭐⭐⭐ СТЪПКА 2: СЕГА изтриваме количката ⭐⭐⭐
        cart.items.all().delete()

        # Добавяме съобщение за успех
        messages.success(request, f"✅ Order #{order.order_number} placed successfully! Your cart has been cleared.")

        # Sending the confirmation email
        send_order_confirmation_email(order)

        # Reroute the user to checkout_success.html
        return redirect('checkout_success', order_id=order.id)

    context = {
        'cart': cart,
        'user': request.user
    }

    return render(request, 'checkout.html', context)

def checkout_success_view(request, order_id):
    order = get_object_or_404(Order, id = order_id, user=request.user)
    return render(request, 'checkout_success.html', {'order': order})


def send_order_confirmation_email(order):
    """Изпраща имейл за потвърждение - SSL FIXED версия"""
    try:
        subject = f'✅ Order Confirmation #{order.id} - QuestHaven'

        # HTML съдържание
        message = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #3498db;">🎮 Thank you for your order at QuestHaven!</h2>

            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h3>📦 Order Details</h3>
                <p><strong>Order Number:</strong> #{order.id}</p>
                <p><strong>Date:</strong> {order.created_at.strftime('%d.%m.%Y %H:%M')}</p>
                <p><strong>Total Amount:</strong> {order.total_amount:.2f} лв.</p>

                <h3>📍 Shipping Address</h3>
                <p>{order.shipping_address}<br>
                {order.city}, {order.postal_code}</p>
            </div>

            <p style="margin-top: 20px;">
                We will notify you when your order is shipped.<br>
                Best regards,<br>
                <strong>The QuestHaven Team</strong>
            </p>
        </body>
        </html>
        """

        # Plain text версия
        text_message = f"""
        Thank you for your order at QuestHaven!

        Order Details:
        - Order Number: #{order.id}
        - Date: {order.created_at.strftime('%d.%m.%Y %H:%M')}
        - Total Amount: {order.total_amount:.2f} лв.

        Shipping Address:
        {order.shipping_address}
        {order.city}, {order.postal_code}

        We will notify you when your order is shipped.

        Best regards,
        The QuestHaven Team
        """

        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings

        # Създаване на имейл
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )

        # Добавяне на HTML версия
        email.attach_alternative(message, "text/html")

        # Изпращане БЕЗ fail_silently, за да видим грешките
        email.send(fail_silently=False)

        print(f"✅ Email sent successfully to {order.email}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {type(e).__name__}: {e}")

        # Fallback - опитай с обикновен имейл
        try:
            from django.core.mail import send_mail
            send_mail(
                f'Order #{order.id} Confirmation',
                text_message,
                settings.DEFAULT_FROM_EMAIL,
                [order.email],
                fail_silently=False,
            )
            print(f"✅ Fallback email sent to {order.email}")
            return True
        except:
            print(f"❌ Fallback also failed for {order.email}")
            return False
