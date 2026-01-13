from django.contrib.auth.models import User
from django.db import models

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    #SEO-friendly име за URL (например: "electronics-gadgets")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    #Картинка за категорията
    image = models.ImageField(upload_to='categories/', blank=True)
    #Дата и час на създаване
    created_at = models.DateTimeField(auto_now_add=True)


    #Как да се показва категорията в админ панела и други места
    def __str__(self):
        return self.name

    # Това ще промени името на модела в множествено число в админ панела
    class Meta:
        verbose_name_plural = 'Categories'

#----------------------------------------------------PRODUCT MODELS ----------------------------------------------------

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ВАЖНО: ВРЪЗКА КЪМ КАТЕГОРИЯ!
    # Това поле СВЪРЗВА продукта с категория
    category = models.ForeignKey(
        'products_and_categories.Category', # Към кой модел се свързва
        on_delete = models.CASCADE,# Ако изтрием категорията се изтриват и продуктите
        related_name='products' #Това позволява да достъпваме продуктите на категория чрез category.products
        )

    def get_final_price(self):
        return self.price


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'

#----------------------------------------------------CART MODELS -------------------------------------------------------
class Cart(models.Model):
    SHIPPING = 10.00
    # ВАЖНО: добави related_name='cart' за да работи user.cart
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def item_count(self):
        return self.items.count()

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    def total_price(self):
        total = 0
        for item in self.items.all():
            # КОРИГИРАНО: използвай item.quantity, НЕ product.stock!
            price = item.product.get_final_price()
            total += float(price) * item.quantity
        return total

    @property
    def total_with_shipping(self):
        """Връща общата сума с доставка"""

        return round(float(self.total_price()) + self.SHIPPING, 2)

    def __str__(self):
        return f'Cart of {self.user.username}'

class CartItem(models.Model):
     #CartItem - временна количка:
     #Запазва продуктите ДОКАТО пазаруваш
     #Може да добавяш/махаш/променяш количества
     #Свързано с Cart модела
     #Изтрива се след поръчката

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_item_total(self):
        return self.product.get_final_price() * self.quantity

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'


#----------------------------------------------------CHECKOUT MODELS ---------------------------------------------------

class Order(models.Model):
    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]

    PAYMENT_METHOD = [
        ('Cash_on_delivery', 'Cash On Delivery'),
        ('Bank_transfer', 'Bank Transfer'),
        ('Card', 'Card'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null = True)
    order_number = models.CharField(max_length = 100)
    email = models.EmailField()
    shipping_address = models.TextField()
    city = models.CharField(max_length = 100)
    postal_code = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)

    #Тук ще запазваме стойността на поръчката ако след това в уебсайта се променят цените
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='Cash_on_delivery')
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        """Връща пълното име или username"""
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.username
    def __str__(self):
      return  f'Order #{self.order_number} - {self.user.username}'

    def save(self, *args, **kwargs) -> None:
        if not self.order_number:
            import uuid
            self.order_number = f'ORD-{uuid.uuid4().hex[:8].upper()}'
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    #OrderItem - постоянен запис на поръчка:
    #Запазва КАКВО си поръчал
    #За всеки продукт пази: име, цена, количество
    #Свързано с Order модела
    #НИКОГА не се изтрива (история на поръчки)
    """Запазва информация за продуктите в поръчката"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
                                blank=True)  # Продуктът може да бъде изтрит
    product_name = models.CharField(max_length=250)  # Запазваме името
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Запазваме цената
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    @property
    def total_price(self):
        return float(self.product_price) * self.quantity