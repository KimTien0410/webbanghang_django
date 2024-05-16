from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

STATUS_CHOICES = (
    ('NEW', 'NEW'),
    ('CONFIRMED', 'CONFIRMED'),
)

RESULT_CHOICES = (
    ('VNPAY_00', 'VNPAY SUCCESS'),
    ('VNPAY_05', 'VNPAY BAD_PASSWORD_EXCEEDING'),
    ('VNPAY_06', 'VNPAY WRONG_PASSWORD'),
    ('VNPAY_07', 'VNPAY SUSPICIOUS_TRANSACTION'),
    ('VNPAY_12', 'VNPAY CARD_IS_LOCKED'),
    ('VNPAY_09', 'VNPAY NO_INTERNET_BANKING'),
    ('VNPAY_10', 'VNPAY VERIFICATION_EXCEEDING'),
    ('VNPAY_11', 'VNPAY TIMEOUT_PAYMENT'),
    ('VNPAY_24', 'VNPAY CUSTOMER_CANCEL'),
    ('VNPAY_51', 'VNPAY NOT_ENOUGH_BALANCE'),
    ('VNPAY_65', 'VNPAY TRANSACTION_PER_DAY_EXCEEDING'),
    ('VNPAY_75', 'VNPAY BANK_MAINTENANCE'),
    ('VNPAY_99', 'VNPAY OTHER_ERRORS'),
)

STATE_CHOICES=(
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Ladakh','Ladakh'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal')
)
CATEGORY_CHOICES=(
    ("ML",'Milo'),
    ("VM",'Vinamilk'),
    ("DL",'Dalat Milk'),
    ("DT",'Dutch Lady'),
    ("BV",'Ba Vì'),
    ("SH",'Sữa Hạt'),
    ("YK",'Yakult'),
    ("FM",'Fami'),
    ("TH",'TH True Milk'),
    ("NF",'Nutifood'),
)
# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices= CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
class Customer(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    zipcode = models.IntegerField()
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending')
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    vnpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    vnpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    vnpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

    payment_method = models.CharField(max_length=100)  # Make sure to update this field when storing VNPay payments
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.amount} via {self.payment_method}"

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="Pending")
    payment= models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

