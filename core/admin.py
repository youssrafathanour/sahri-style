from django.contrib import admin
from .models import (
    Category,
    Product,
    Customer,
    Order,
    OrderItem,
    StockMovement,
    Expense,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'promo_price',
        'stock',
        'is_available',
    )

    list_filter = (
        'category',
        'is_available',
    )

    search_fields = (
        'name',
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'full_name',
        'phone',
        'city',
        'created_at',
    )

    search_fields = (
        'full_name',
        'phone',
        'city',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'customer__full_name',
        'customer__phone',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'unit_price',
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'movement_type',
        'quantity',
        'stock_initial',
        'stock_after',
        'date',
    )

    list_filter = (
        'movement_type',
        'date',
    )

    search_fields = (
        'product__name',
        'note',
    )


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'label',
        'amount',
        'date',
    )

    list_filter = (
        'date',
    )