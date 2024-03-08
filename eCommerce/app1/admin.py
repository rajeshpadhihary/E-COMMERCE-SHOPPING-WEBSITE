from django.contrib import admin
from .models import Product,CustomerAddress,Cart,DebitCardDetailsModel,CreditCardDetailsModel,Order,Wishlist,CustomerProfile,CustomerQuery,ReviewOfProduct,ReturnProduct

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','forgender','product_available','product_image']


@admin.register(CustomerAddress)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','phone','city','zipcode','state']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(DebitCardDetailsModel)
class DebitCardModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name_on_card','card_number','expiry_date_month','expiry_date_year','cvv']

@admin.register(CreditCardDetailsModel)
class CreditCardModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name_on_card','card_number','expiry_date_month','expiry_date_year','cvv']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['order_id','user','date','address','product','quantity','total_price','cash_on_delivery','debit_card','credit_card','transaction_id','order_status']


@admin.register(Wishlist)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user','name_for_profile','about','profile_image']

@admin.register(CustomerQuery)
class CustomerQueryAdmin(admin.ModelAdmin):
    list_display = ['id','user','fullname','email','phone','subject','message']

@admin.register(ReviewOfProduct)
class ReviewProductAdmin(admin.ModelAdmin):
    list_display = ['id','review_user','rating','product','review_text']

@admin.register(ReturnProduct)
class ReturnOrderAdmin(admin.ModelAdmin):
    list_display = ['id','reason', 'return_status','return_product']