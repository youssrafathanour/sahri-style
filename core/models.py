from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    promo_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    size = models.CharField(
        max_length=20,
        blank=True
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Customer(models.Model):
    full_name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20)

    address = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


class Order(models.Model):
    STATUS_CHOICES = [
        ('nouvelle', 'Nouvelle'),
        ('confirmee', 'Confirmée'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='nouvelle'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Commande #{self.id} - {self.customer.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product} x{self.quantity}"


class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='movements'
    )

    movement_type = models.CharField(
        max_length=10,
        choices=MOVEMENT_CHOICES
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    # Stock initial : reste fixe
    stock_initial = models.PositiveIntegerField(
        default=0
    )

    # Stock restant après le mouvement
    stock_after = models.PositiveIntegerField(
        default=0
    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    note = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.movement_type} - "
            f"{self.product} - "
            f"Initial: {self.stock_initial} - "
            f"Restant: {self.stock_after}"
        )


class Expense(models.Model):
    label = models.CharField(
        max_length=150
    )

    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    date = models.DateField()

    note = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.label