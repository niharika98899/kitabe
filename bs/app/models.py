from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES=(
    ('Maharashtra', 'Maharashtra'),
    ('TN', 'TN'),
    ('MP', 'MP'),
)
'''
STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way','On The Way'),
        ('Delivered','Delivered'),
        ('Cancel','Cancel'),
        ('Pending''Pending'), 
    )

class Payment(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=1000,blank=True,null=True)
    paid = models.BooleanField(default=False)
    
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_Price        '''


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_Price = models.FloatField()
    publisher = models.TextField()
    description = models.TextField(default='')
    #prodapp = models.TextField(default='')
    #category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, limit_choices_to={'category':models.F('category')})
    product_image = models.ImageField(upload_to = 'product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	@property
	def total_cost(self):
		return self.quantity * self.product.discounted_price

class Upload(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    publisher = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    
    CATEGORY_CHOICES = [
        ('1', '1st to 4th grade'),
        ('2', '5th to 7th grade'),
        ('3', '8th to 10th grade'),
        ('4', 'Junior College'),
        ('5', 'Under Graduate'),
        ('6', 'Post Graduate'),
        ('7', 'PHD'),
        ('8', 'Miscellaneous'),
    ]
    
    SUBCATEGORY_CHOICES = [
        ('1', 'English'),
        ('2', 'Maths'),
        ('3', 'Science'),
        ('4', 'History'),
        ('5', 'Geography'),
        ('6', 'Marathi'),
        ('7', 'Hindi'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=20, choices=SUBCATEGORY_CHOICES)
    product_image = models.ImageField(upload_to='images/')