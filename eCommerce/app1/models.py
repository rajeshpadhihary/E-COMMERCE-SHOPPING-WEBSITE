from django.db import models
from django.contrib.auth.models import User
import random
from django.core.validators import MinValueValidator,MaxValueValidator

class Product(models.Model):
    P_CHOICES = (
        ("T-Shirts","T-Shirts"),
        ("Shirts","Shirts"),
        ("FormalMen","FormalMen"),
        ("FormalWomen","FormalWomen"),
        ("Groom","Groom"),
        ("Bridal","Bridal"),
        ("Jeans","Jeans"),
        ("FootWear","FootWear"),
        ("Watches","Watches"),
        ("Sun Glassess","Sun Glassess"),
    )
    GENDER_CHOICE = (
        ('Male','Male'),
        ('Female', 'Female'),
        ('Unisex', 'Unisex'),
    )
    title = models.CharField(max_length = 100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices = P_CHOICES,max_length = 50)
    forgender = models.CharField(choices = GENDER_CHOICE,max_length = 50)
    product_available = models.IntegerField(default=0)
    avg_rating = models.FloatField(default = 0)
    total_ratings_count = models.IntegerField(default = 0)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    
class CustomerAddress(models.Model):
    STATE_CHOICES = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh','Arunachal Pradesh'),
        ('Assam','Assam'),
        ('Bihar','Bihar'),
        ('Chandigarh','Chandigarh'),
        ('Delhi','Delhi'),
        ('Goa','Goa'),
        ('Gujarat','Gujarat'),
        ('Haryana','Haryana'),
        ('Jammu and Kashmir','Jammu and Kashmir'),
        ('Jharkhand','Jharkhand'),
        ('Karnataka','Karnataka'),
        ('Kerala','Kerala'),
        ('Madhya Pradesh','Madhya Pradesh'),
        ('Maharashtra','Maharashtra'),
        ('Manipur','Manipur'),
        ('Meghalaya','Meghalaya'),
        ('Mizoram','Mizoram'),
        ('Nagaland','Nagaland'),
        ('Odisha','Odisha'),
        ('Pondicherry','Puduchery'),
        ('Punjab','Punjab'),
        ('Rajasthan','Rajasthan'),
        ('Sikkim','Sikkim'),
        ('Tamil Nadu','Tamil Nadu'),
        ('Telangana','Telangana'),
        ('Tripura','Tripura'),
        ('Uttarakhand','Uttarakhand'),
        ('Uttar Pradesh','Uttar Pradesh'),
        ('West Bengal','West Bengal')
    )
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.IntegerField(default = "**********")
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField(null=True,blank=True)
    state = models.CharField(choices = STATE_CHOICES, max_length=100)



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)

    @property
    def total(self):
        return self.quantity * self.product.discounted_price
    
class DebitCardDetailsModel(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    name_on_card = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date_month = models.CharField(max_length=2)
    expiry_date_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)

class CreditCardDetailsModel(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    name_on_card = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiry_date_month = models.CharField(max_length=2)
    expiry_date_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    product = models.CharField(max_length = 800)
    quantity = models.CharField(max_length=800)
    total_price = models.FloatField(default=1)
    cash_on_delivery = models.BooleanField(default=False)
    debit_card = models.BooleanField(default = False)
    credit_card = models.BooleanField(default = False)
    ID = random.randint(999999,99999999999)
    transaction_id = models.PositiveIntegerField(default = ID,blank = True)
    order_status = models.BooleanField(default=False)


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    

class CustomerProfile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    name_for_profile = models.CharField(max_length = 100,null = True,blank = True)
    about = models.CharField(max_length = 400)
    profile_image = models.ImageField(upload_to='userprofileimages',null=True, blank=True)
    
class CustomerQuery(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    subject = models.CharField(max_length =  100)
    message = models.TextField()

class ReviewOfProduct(models.Model):
    review_user = models.ForeignKey(User,on_delete = models.CASCADE)
    review_user_name = models.CharField(max_length = 100,blank = True,null = True)
    rating = models.FloatField(validators = [MinValueValidator(1),MaxValueValidator(5)])
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text = models.TextField(default = None,blank = True)

class ReturnProduct(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    order = models.ForeignKey(Order,on_delete = models.SET_NULL,null = True)
    reason = models.TextField()
    return_product = models.CharField(max_length = 800)
    return_status = models.IntegerField(default = 0)