from django.db import models
from users.models import WebsiteUser
from products.models import Product


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()

    def __str__(self):
        return self.name


class CategorySubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}->{self.subcategory}'


class SubCategory(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    category_id = models.ManyToManyField(Category, through=CategorySubCategory)
    image = models.ImageField(upload_to='img', null=True)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.user}, {self.product}, {self.quantity}'


class ProductOrder(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.user}, {self.product}, {self.order}'


class Order(models.Model):
    user = models.ForeignKey(WebsiteUser, on_delete=models.CASCADE)
    product_ordered = models.ManyToManyField(Product, through=ProductOrder)
    datetime_ordered = models.DateTimeField(auto_now_add=True)
    amount_paid = models.IntegerField(null=True)
    status_choices = (
        (1, 'Information about the order received'),
        (2, 'Order packaging in progress'),
        (3, 'Order sent to customer'),
        (4, "Order finished")
    )
    status = models.IntegerField(choices=status_choices, null=True, default=1)
    delivery_choices = (
        (1, 'Pickup in person'),
        (2, 'Home shipping')
    )
    shipping_type = models.IntegerField(choices=delivery_choices, default='1')
    payment_choices = (
        (1, 'Cash'),
        (2, 'Credit card'),
        (3, 'Bank transfer'),
        (4, 'Wallet')
    )
    payment_type = models.IntegerField(choices=payment_choices, null=True)
    address = models.CharField(max_length=250, null=True)
    phone_number = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.user}, {self.datetime_ordered}'