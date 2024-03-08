from django import forms
from .models import CustomerAddress,CustomerProfile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User

class UserRegistrationform(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'autofocus':True,'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your Email Address', 'class':"form-control"}))
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password','class':'form-control'}))
    password2 = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password To Confirm','class':'form-control'}))


    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password','class':'form-control'}))


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs= {'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Cofirm Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model= CustomerAddress
        fields=['full_name','email','phone','city','zipcode','state']
        widgets = {
            'full_name':forms.TextInput(attrs={'placeholder':'Enter Full Name','class':'form-control'}),
            'email':forms.EmailInput(attrs={'placeholder':'Enter Email Address','class':'form-control'}),
            'phone':forms.NumberInput(attrs={'placeholder':'Enter Mobile Number','class':'form-control'}),
            'city': forms.TextInput(attrs={'placeholder':'Enter City Name','class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'placeholder':'Enter ZipCode','class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'})
        }


class CustomerProfileForm(forms.Form):
    name_for_profile = forms.CharField(label="Enter Full Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter First Name'}))
    about = forms.CharField(label="About Yourself.",max_length=250,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter About Yourself.'}))
    profile_image = forms.FileField(label="Profile Pic",required=False,widget=forms.FileInput(attrs={"class":"form-control"}))


class AddProducts(forms.Form):
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
    title = forms.CharField(label="Product Name",max_length=150,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter Product Name'}))
    selling_price = forms.IntegerField(label="Selling Price",widget=forms.NumberInput(attrs={"class":"form-control"}))
    discounted_price = forms.IntegerField(label="Discounted Price",widget=forms.NumberInput(attrs={"class":"form-control"}))
    description = forms.CharField(label="Description",max_length=250,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Description About the Product.'}))
    category = forms.ChoiceField(choices = P_CHOICES,label="Category",widget=forms.Select(attrs={"class":"form-control",'placeholder': 'Choice Product Category'}))
    forgender = forms.ChoiceField(choices = GENDER_CHOICE,label="For",widget=forms.Select(attrs={"class":"form-control",'placeholder': 'Choice Product For'}))
    product_available = forms.IntegerField(label="Products Available",widget=forms.NumberInput(attrs={"class":"form-control"}))
    product_image = forms.FileField(label="Product Picture",required=False,widget=forms.FileInput(attrs={"class":"form-control"}))
    
class ReviewProductForm(forms.Form):
    review_user_name = forms.CharField(label="Enter your Name",max_length=100,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter Your Name'}))
    rating = forms.CharField(label="Ratings You Want to Give",widget=forms.NumberInput(attrs={"class":"form-control",'placeholder': 'Number Must be in bettwen 1 to 5.','min':1,'max': '5',}))
    review_text = forms.CharField(label="Enter About This Product",max_length=250,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter Your opinion'}))
