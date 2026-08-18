from django.shortcuts import render, get_object_or_404, redirect

from .models import (
    Product,
    Category,
    Customer,
    Order,
    OrderItem,
    StockMovement,
)


def home(request):
    return render(request, 'home.html')


def catalogue(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    return render(
        request,
        'catalogue.html',
        {
            'products': products,
            'categories': categories,
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product,
        }
    )


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        price = (
            product.promo_price
            if product.promo_price
            else product.price
        )

        subtotal = price * quantity

        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(
        request,
        'cart.html',
        {
            'products': products,
            'total': total,
        }
    )


def increase_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def checkout(request):

    cart_data = request.session.get('cart', {})

    if not cart_data:
        return redirect('cart')

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')

        if not full_name or not phone:

            return render(
                request,
                'checkout.html',
                {
                    'error': 'Veuillez remplir le nom et le téléphone.'
                }
            )

        customer = Customer.objects.create(
            full_name=full_name,
            phone=phone,
            address=address,
            city=city
        )

        order = Order.objects.create(
            customer=customer,
            status='nouvelle'
        )

        for product_id, quantity in cart_data.items():

            product = get_object_or_404(
                Product,
                id=product_id
            )

            # Stock actuel avant la vente
            stock_before = product.stock

            # Vérifier le stock disponible
            if quantity > stock_before:

                return render(
                    request,
                    'checkout.html',
                    {
                        'error': (
                            f'Le produit {product.name} '
                            f'ne possède que {stock_before} '
                            f'unités en stock.'
                        )
                    }
                )

            # Stock restant après la vente
            stock_after = stock_before - quantity

            # Prix utilisé pour la commande
            unit_price = (
                product.promo_price
                if product.promo_price
                else product.price
            )

            # Créer la ligne de commande
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price
            )

            # Mettre à jour le stock
            product.stock = stock_after

            # Si le stock arrive à zéro
            if product.stock == 0:
                product.is_available = False

            product.save()

            # Stock initial fixe
            stock_initial = 200

            # Enregistrer le mouvement
            StockMovement.objects.create(
                product=product,
                movement_type='sortie',
                quantity=quantity,
                stock_initial=stock_initial,
                stock_after=stock_after,
                note=f'Sortie pour la commande #{order.id}'
            )

        # Vider le panier
        request.session['cart'] = {}
        request.session.modified = True

        return render(
            request,
            'order_success.html',
            {
                'order': order
            }
        )

    products = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id
        )

        price = (
            product.promo_price
            if product.promo_price
            else product.price
        )

        subtotal = price * quantity

        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(
        request,
        'checkout.html',
        {
            'products': products,
            'total': total,
        }
    )
def dashboard(request):
    products = Product.objects.all().order_by('stock')
    orders = Order.objects.all().order_by('-created_at')[:15]
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(stock__lt=10)

    return render(request, 'dashboard.html', {
        'products': products,
        'orders': orders,
        'total_orders': total_orders,
        'total_products': total_products,
        'low_stock': low_stock,
    })
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.GET.get('status')
    valid_statuses = ['nouvelle', 'confirmee', 'expediee', 'livree', 'annulee']
    if new_status in valid_statuses:
        order.status = new_status
        order.save()
    return redirect('dashboard')