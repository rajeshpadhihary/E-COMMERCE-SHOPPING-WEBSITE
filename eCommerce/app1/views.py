from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.views import View
from .models import (
    Product,
    CustomerAddress,
    Cart,
    Order,
    DebitCardDetailsModel,
    CreditCardDetailsModel,
    Wishlist,
    CustomerProfile,
    CustomerQuery,
    ReviewOfProduct,
    ReturnProduct
)
from .forms import UserRegistrationform, ProfileForm,CustomerProfileForm,AddProducts,ReviewProductForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
import json


def home(request):
    products = Product.objects.all().order_by('-id')[:8]
    first_4_products = products[:4]
    last_4_products = products[4:]
    return render(request,"home.html",locals())


def about(request):
    return render(request,"about.html")


def contact(request):
    return render(request,"contact.html")


class CategoryVIEW(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values("title")
        return render(request, "category.html", locals())


class CategoryTitleView(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values("title")
        return render(request, "category.html", locals())


class ProductDetailsVIEW(View):
    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(id=pk)
        reviews = ReviewOfProduct.objects.filter(product = product)
        
        top_reviews_list = []
        for i in reviews:
            if i.rating > 3:
                top_reviews_list.append(i)
        top_five_reviews = top_reviews_list[:5]
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product = product) & Q(user = request.user))
        return render(request, "product_details.html", locals())


class CustomerRegistrationVIEW(View):
    def get(self, request):
        form = UserRegistrationform()
        return render(request, "registration.html", locals())

    def post(self, request):
        form = UserRegistrationform(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congrats ! User Registration Successfully.")
        else:
            messages.warning(
                request, "Invalid Input Data !!! Please Check Your Entries Again."
            )
        return render(request, "registration.html", locals())

class UserProfile(View):
    def get(self,request):
        user = request.user
        customer = User.objects.get(username = user.username)

        try:
            profile = CustomerProfile.objects.get(user = user)
            address = CustomerAddress.objects.filter(user=user)
            address_count = CustomerAddress.objects.filter(user=user).count()
            orders = Order.objects.filter(user = user).order_by('-date')
            recent_orders = orders[0:4]
            orders_count = Order.objects.filter(user = user).count()

            return render(request,'profile.html',locals())
        except Exception:
            address = CustomerAddress.objects.filter(user=user)
            address_count = CustomerAddress.objects.filter(user=user).count()
            orders = Order.objects.filter(user = user).order_by('-date')
            recent_orders = orders[0:4]
            orders_count = Order.objects.filter(user = user).count()
            return render(request,'profile2.html',locals())


class UserProfileAddress(View):
    def get(self, request):
        user_obj = User.objects.get(username=request.user.username)
        form = ProfileForm()
        return render(request, "add_address.html", locals())

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            city = form.cleaned_data["city"]
            zipcode = form.cleaned_data["zipcode"]
            state = form.cleaned_data["state"]

            user_obj = CustomerAddress(
                user=user,
                full_name=full_name,
                email=email,
                phone=phone,
                city=city,
                zipcode=zipcode,
                state=state,
            )
            user_obj.save()
            messages.success(request, "Data Added Successfully.")
        else:
            messages.warning(request, "Please check your data again")
        return render(request, "add_address.html", locals())


class UserAddressView(View):
    def get(self, request):
        user = request.user
        user_obj = CustomerAddress.objects.filter(user=user)
        return render(request, "address.html", locals())


class UpdateAddressView(View):
    def get(self, request, id):
        customer_user = CustomerAddress.objects.get(id=id)
        form = ProfileForm()
        form.fields["full_name"].initial = customer_user.full_name
        form.fields["city"].initial = customer_user.city
        form.fields["email"].initial = customer_user.email
        form.fields["phone"].initial = customer_user.phone
        form.fields["zipcode"].initial = customer_user.zipcode
        form.fields["state"].initial = customer_user.state

        return render(request, "updateaddress.html", locals())

    def post(self, request, id):
        address_object = CustomerAddress.objects.get(id=id)
        form = ProfileForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            city = form.cleaned_data["city"]
            zipcode = form.cleaned_data["zipcode"]
            state = form.cleaned_data["state"]

            address_object.full_name = full_name
            address_object.email = email
            address_object.phone = phone
            address_object.city = city
            address_object.zipcode = zipcode
            address_object.state = state
            address_object.save()

            messages.success(request, "Your Address has been updated successfully!")
        else:
            messages.warning(request, "Please correct the following error.")
            return self.get(request, id)

        return render(request, "updateaddress.html", locals())


class DeleteAddressView(View):
    def get(self, request, id):
        c_user = CustomerAddress.objects.get(id=id)
        c_user.delete()
        return redirect(reverse("address"))


def AddToCart(request, prod_id):
    user = request.user
    product = Product.objects.get(id=prod_id)
    cart_obj = Cart.objects.filter(product__id=product.id)
    if len(cart_obj) > 0:
        qty = int(cart_obj[0].quantity) + 1
        obj = cart_obj[0]
        obj.quantity = qty
        obj.save()
    else:
        cart_item = Cart(user=user, product=product, quantity=1)
        cart_item.save()

    return redirect(reverse("show_cart"))


def Show_Cart(request):
    user = request.user
    add_user = CustomerAddress.objects.filter(user=user)
    cartItems = Cart.objects.filter(user=user)
    total = sum([i.total for i in cartItems])
    shipping_charge = round(total * (5 / 100), 2)
    tax = round(total * (2 / 100), 2)
    grand_total = round(float((tax + shipping_charge + total)), 2)
    return render(request, "showcart.html", locals())


def Remove_Cart_Item(request, id):
    item = Cart.objects.get(id=id)
    if item.quantity > 1:
        qty = int(item.quantity) - 1
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect(reverse("show_cart"))


def Buy_Now(request,id):
    user = request.user
    add_user = CustomerAddress.objects.filter(user=user)
    product_obj = Product.objects.get(id = id)
    total = product_obj.discounted_price
    shipping_charge = round(total * (5 / 100), 2)
    tax = round(total * (2 / 100), 2)
    grand_total = round(float((tax + shipping_charge + total)), 2)
    return render(request,'buynow.html',locals())


class Order_DetailsView(View):
    def post(self, request):
        try:
            user = request.user
            customer_name = request.POST.get("nameoncard")
            payment_method = request.POST.get("radioNoLabel")
            expary = request.POST.get("expary")
            cardnumber = request.POST.get("cardnumber")
            cvv = request.POST.get("cvv")
            address = request.POST.get("addressNoLabel")

            address_obj = CustomerAddress.objects.get(id=address)
            import random
            otp = str(random.randint(1000,9999))
            request.session['otp'] = otp
            
            subject = "Your One Time Password"
            message = f"Your one time password is: {otp}"
            from_email = "verification@gmail.com"
            try:
                email_for_verify = address_obj.email
                cart_obj = Cart.objects.filter(user=user)
                total_price = sum([i.total for i in cart_obj])
                shipping_charge = round(total_price * (5 / 100), 2)
                tax = round(total_price * (2 / 100), 2)

                grand_total = round(float((tax + shipping_charge + total_price)), 2)

                product_titles = []

                for i in cart_obj:
                    product_titles.append(i.product.title)

                product_quantity = {}
                for x in product_titles:
                    cnts = Cart.objects.get(product__title=x)
                    product_quantity[cnts.product.title] = cnts.quantity

                send_mail(subject, message, from_email,[email_for_verify], fail_silently=False)

                if payment_method == "debit_card":
                    ex_month = expary.split("/")[0]
                    ex_year = expary.split("/")[1]
                    card_obj = DebitCardDetailsModel(
                        user=user,
                        name_on_card=customer_name,
                        card_number=cardnumber,
                        expiry_date_month=ex_month,
                        expiry_date_year=ex_year,
                        cvv=cvv,
                    )
                    card_obj.save()
                    order_obj = Order(
                        user=user,
                        address=address_obj,
                        product=product_titles,
                        quantity=json.dumps(product_quantity),
                        total_price=grand_total,
                        cash_on_delivery=False,
                        debit_card=True,
                        credit_card=False,
                        order_status=True,
                    )
                    order_obj.save()
                elif payment_method == "credit_card":
                    ex_month = expary.split("/")[0]
                    ex_year = expary.split("/")[1]
                    card_obj = CreditCardDetailsModel(
                        user=user,
                        name_on_card=customer_name,
                        card_number=cardnumber,
                        expiry_date_month=ex_month,
                        expiry_date_year=ex_year,
                        cvv=cvv,
                    )
                    card_obj.save()
                    order_obj = Order(
                        user=user,
                        address=address_obj,
                        product=product_titles,
                        quantity=json.dumps(product_quantity),
                        total_price=grand_total,
                        cash_on_delivery=False,
                        debit_card=False,
                        credit_card=True,
                        order_status=True,
                    )
                    order_obj.save()
                elif payment_method == "cash_on_delevery":
                    order_obj = Order(
                        user=user,
                        address=address_obj,
                        product=product_titles,
                        quantity=json.dumps(product_quantity),
                        total_price=grand_total,
                        cash_on_delivery=True,
                        debit_card=False,
                        credit_card=False,
                        order_status=True,
                    )
                    order_obj.save()
                order_products_obj = Cart.objects.filter(product__title__in = product_titles)
                for i in order_products_obj:
                    product_obj = Product.objects.get(title = i.product.title)
                    product_obj.product_available -= i.quantity
                    product_obj.save()
                return redirect('verification')
            
            except Exception as e:
                messages.error(request,"Eror while sending otp")
                # return HttpResponseServerError("Failed to send email: {}".format(e))
                return redirect(reverse("show_cart"))
            
        except Exception as e:
            messages.error(request, "Error Occurred While Fetching")
            return redirect(reverse("show_cart"))


class Direct_Buy_Order_DetailsView(View):
    def post(self, request,id):
        try:
            user = request.user
            customer_name = request.POST.get("nameoncard")
            payment_method = request.POST.get("radioNoLabel")
            expary = request.POST.get("expary")
            cardnumber = request.POST.get("cardnumber")
            cvv = request.POST.get("cvv")
            address = request.POST.get("addressNoLabel")

            address_obj = CustomerAddress.objects.get(id=address)
        
            import random
            otp = str(random.randint(1000,9999))
            request.session['otp'] = otp
            
            subject = "Your One Time Password"
            message = f"Your one time password is: {otp}"
            from_email = "verification@gmail.com"
            try:
                email_for_verify = address_obj.email
                prd_obj = Product.objects.get(pk=id)
                total_price = prd_obj.discounted_price
                shipping_charge = round(total_price * (5 / 100), 2)
                tax = round(total_price * (2 / 100), 2)

                grand_total = round(float((tax + shipping_charge + total_price)), 2)

                product_title = prd_obj.title
                product_quantity = {}
                product_quantity[product_title] = 1
                send_mail(subject, message, from_email,[email_for_verify], fail_silently=False)

                if payment_method == "debit_card":
                    ex_month = expary.split("/")[0]
                    ex_year = expary.split("/")[1]
                    card_obj = DebitCardDetailsModel(
                        user=user,
                        name_on_card=customer_name,
                        card_number=cardnumber,
                        expiry_date_month=ex_month,
                        expiry_date_year=ex_year,
                        cvv=cvv,
                    )
                    card_obj.save()
                    order_obj = Order(
                        user=user,
                        address=address_obj,
                        product=product_title,
                        quantity=json.dumps(product_quantity),
                        total_price=grand_total,
                        cash_on_delivery=False,
                        debit_card=True,
                        credit_card=False,
                        order_status=True,
                    )
                    order_obj.save()
                elif payment_method == "credit_card":
                    ex_month = expary.split("/")[0]
                    ex_year = expary.split("/")[1]
                    card_obj = CreditCardDetailsModel(
                        user=user,
                        name_on_card=customer_name,
                        card_number=cardnumber,
                        expiry_date_month=ex_month,
                        expiry_date_year=ex_year,
                        cvv=cvv,
                    )
                    card_obj.save()
                    order_obj = Order(
                        user=user,
                        address=address_obj,
                        product=product_title,
                        quantity=json.dumps(product_quantity),
                        total_price=grand_total,
                        cash_on_delivery=False,
                        debit_card=False,
                        credit_card=True,
                        order_status=True,
                    )
                    order_obj.save()
                elif payment_method == "cash_on_delevery":
                    order_obj = Order(
                        user=user,
                        address=address_obj,
                        product=product_title,
                        quantity=json.dumps(product_quantity),
                        total_price=grand_total,
                        cash_on_delivery=True,
                        debit_card=False,
                        credit_card=False,
                        order_status=True,
                    )
                    order_obj.save()

                product_obj = Product.objects.get(title = product_title)
                product_obj.product_available -= 1
                product_obj.save()
                return redirect('verification')
            except Exception as e:
                messages.error(request,"Eror while sending otp")
                # return HttpResponseServerError("Failed to send email: {}".format(e))
                return redirect(reverse("buynow"))
            
        except Exception as e:
            messages.error(request, "Error Occurred While Fetching")
            return redirect(reverse("buynow"))

def SuccessOrder(request):
    return render(request, "orderedsuccessfull.html")


def orderReciptView(request):
    user_obj = Order.objects.filter(user=request.user).order_by("-order_id")
    recent_order = user_obj[0]
    dict_val = json.loads(recent_order.quantity)
    order_det = {}
    for i in range(len(dict_val)):
        key = list(dict_val.keys())[i]
        products = Product.objects.get(title=key)
        product_img = products.product_image
        value = dict_val[key]
        order_det[key] = [value, product_img]
    adrs = recent_order.address
    c_address = CustomerAddress.objects.get(id=adrs.id)
    dict_addrs = {}
    dict_addrs["Name"] = c_address.full_name
    dict_addrs["Ph.No."] = c_address.phone
    dict_addrs["City"] = c_address.city
    dict_addrs["Zipcode"] = c_address.zipcode
    dict_addrs["State"] = c_address.state


    return render(request, "order_details.html", locals())


class OrdersView(View):
    def get(self, request):
        user = request.user
        return_obj = ReturnProduct.objects.filter(user = user)
        orders = Order.objects.filter(user=user)
        returns = ReturnProduct.objects.filter(order__in = orders)
        for i in returns:
            if i.return_status == 1:
                order_obj = Order.objects.get(order_id = i.order.order_id)
                productoq = order_obj.quantity
                product_and_quantity = json.loads(productoq)
                email_for_verify = order_obj.address.email
                subject = "Return Successfull."
                message = f"\nDear Sir/Madam,\n\tYour Order having order id {order_obj.order_id} has returned successfully.\nItem Name & Quantity : {order_obj.quantity}\nYour payment will be credited to your bank account after products recived from you.\nSo please co-operate.\nThank You"
                from_email = "verification@gmail.com"
                send_mail(subject, message, from_email,[email_for_verify], fail_silently=False)
                for i,j in product_and_quantity.items():
                    product_obj = Product.objects.get(title=i)
                    product_obj.product_available += j
                    product_obj.save()
                print(order_obj)
                order_obj.delete()
        return render(request, "orders.html", locals())

def otp_verification(request):
    if request.method == 'POST':
        otp_ = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if int(otp_) != int(session_otp):
            del session_otp
            messages.error(request,"Invalid OTP")
            return redirect(reverse('show_cart'))
        else:
            return redirect(reverse('ordersuccess')) 
    return render(request,'verification_page.html',locals())

def plus_wishlist(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        Wishlist(user = user, product = product).save()
        data={'status':'Product added to wishlist'}
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id = prod_id)
        Wishlist.objects.get(user = user, product = product).delete()
        data={'status':'Product removed from wishlist'}
        return JsonResponse(data)
    
def WishList(request):
    user = request.user
    wishlist_obj = Wishlist.objects.filter(user = user)
    return render(request,'wishlist.html',locals())


def search_items(request):
    if request.method == 'POST':
        user = request.user
        search_title = request.POST.get("search-box")
        all_searh_items = []
        product = Product.objects.filter(title__icontains = search_title)
        for i in product:
            all_searh_items.append(i)
        category = Product.objects.filter(category__icontains=search_title)
        for j in category:
            if j not in all_searh_items:
                all_searh_items.append(j)
        return render(request,'search_item.html',locals())
    

class ProfileData(View):
    def get(self, request):
        user_obj = User.objects.get(username=request.user.username)
        form = CustomerProfileForm()
        return render(request, "profile_data.html", locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST,request.FILES)
        user = request.user
        print(form.is_valid())
        if form.is_valid():
            name = form.cleaned_data["name_for_profile"]
            about = form.cleaned_data["about"]
            profile_pic = request.FILES.get("profile_image")

            user_obj = CustomerProfile(
                user=user,
                name_for_profile=name,
                about=about,
                profile_image=profile_pic,
            )
            user_obj.save()
            messages.success(request, "Data Added Successfully.")
        else:
            messages.warning(request, "Please check your data again")
        return render(request, "add_address.html", locals())

class UpdateProfileData(View):
    def get(self, request, id):
        customer_user = CustomerProfile.objects.get(id=id)
        form = CustomerProfileForm()
        form.fields["name_for_profile"].initial = customer_user.name_for_profile
        form.fields["about"].initial = customer_user.about

        return render(request, "updateprofile.html", locals())

    def post(self, request, id):
        profile_object = CustomerProfile.objects.get(id=id)
        form = CustomerProfileForm(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            name = form.cleaned_data["name_for_profile"]
            about = form.cleaned_data["about"]
            profile_pic = request.FILES.get("profile_image")
            if profile_pic == None:
                picture = profile_object.profile_image
            else:
                picture = profile_pic
                
            profile_object.name_for_profile = name
            profile_object.about = about
            profile_object.profile_image = picture
            profile_object.save()

            messages.success(request, "Your Profile has been updated successfully!")
        else:
            messages.warning(request, "Please correct the following error.")
            return self.get(request, id)

        return render(request, "updateprofile.html", locals())


def CustomerQuerySave(request):
    user = request.user
    if request.method == "POST":
        try:
            fullname = request.POST.get("fullname")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            subject = request.POST.get("subject")
            message = request.POST.get("message")

            C_Query = CustomerQuery(user = user,fullname = fullname,email = email,phone = phone,subject = subject,message = message)
            C_Query.save()
                    
        except Exception as e:
            return redirect(reverse("contact"))

    return render(request,'querysubmit.html')


class AddProductView(View):
    def get(self, request):
        user = request.user
        user_obj = User.objects.get(username=request.user.username)
        form = AddProducts()
        return render(request, "add_product.html", locals())

    def post(self, request):
        form = AddProducts(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            title = form.cleaned_data["title"]
            selling_price = form.cleaned_data["selling_price"]
            discounted_price = form.cleaned_data["discounted_price"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            forgender = form.cleaned_data["forgender"]
            product_available = form.cleaned_data["product_available"]
            product_image = request.FILES.get("product_image")

            user_obj = Product(
                title=title,
                selling_price=selling_price,
                discounted_price=discounted_price,
                description = description,
                category = category,
                forgender = forgender,
                product_available = product_available,
                product_image=product_image,
            )
            user_obj.save()
            messages.success(request, "Product Added Successfully.")
        else:
            messages.warning(request, "Please check your data again")
        return render(request, "add_product.html", locals())

def ViewProducts(request):
    products = Product.objects.all()
    print(products)
    return render(request,"view_products.html",locals())



class UpdateProducts(View):
    def get(self, request, id):
        customer_user = Product.objects.get(id=id)
        form = AddProducts()
        form.fields["title"].initial = customer_user.title
        form.fields["selling_price"].initial = customer_user.selling_price
        form.fields["discounted_price"].initial = customer_user.discounted_price
        form.fields["description"].initial = customer_user.description
        form.fields["category"].initial = customer_user.category
        form.fields["forgender"].initial = customer_user.forgender
        form.fields["product_available"].initial = customer_user.product_available
        form.fields["product_image"].initial = customer_user.product_image

        return render(request, "update_product.html", locals())

    def post(self, request, id):
        product_object = Product.objects.get(id=id)
        form = AddProducts(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            title = form.cleaned_data["title"]
            selling_price = form.cleaned_data["selling_price"]
            discounted_price = form.cleaned_data["discounted_price"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            forgender = form.cleaned_data["forgender"]
            product_available = form.cleaned_data["product_available"]
            product_image = request.FILES.get("product_image")

            if product_image == None:
                picture = product_object.product_image
            else:
                picture = product_image

            product_object.title = title
            product_object.selling_price = selling_price
            product_object.discounted_price = discounted_price
            product_object.description = description
            product_object.category = category
            product_object.forgender = forgender
            product_object.product_available = product_available
            product_object.product_image = picture
            product_object.save()
            return redirect(reverse('view_products'))
        else:
            messages.warning(request, "Please check your data again")
            return self.get(request, id)

def ProductDelete(request, id):
    obj = Product.objects.get(id = id)
    obj.delete()
    return redirect(reverse('view_products'))


def productsForMen(request):
    products_for_men = Product.objects.filter(Q(forgender="Male") | Q(forgender="Unisex"))
    products_for_men_count = products_for_men.count()
    return render(request,"mens_product.html",locals())

def mensProductFilter(request,type):
    products_for_men = Product.objects.filter(Q(forgender="Male") | Q(forgender="Unisex"))
    filter_products_obj = []
    for i in products_for_men:
        if i.category == type:
            filter_products_obj.append(i)
    products_for_men_count = len(filter_products_obj)
    return render(request,'mens_product_filter.html', locals())


def productsForwoMen(request):
    products_for_women = Product.objects.filter(Q(forgender="Female") | Q(forgender="Unisex"))
    products_for_women_count = products_for_women.count()
    return render(request,"womens_product.html",locals())

def womensProductFilter(request,type):
    products_for_women = Product.objects.filter(Q(forgender="Female") | Q(forgender="Unisex"))
    filter_products_obj = []
    for i in products_for_women:
        if i.category == type:
            filter_products_obj.append(i)
    products_for_women_count = len(filter_products_obj)
    return render(request,'womens_product_filter.html', locals())



class AddProductReviewView(View):
    def get(self, request,id):
        user_obj = User.objects.get(username=request.user.username)
        form = ReviewProductForm()
        product_obj = Product.objects.get(id = id)
        return render(request, "review_form.html", locals())

    def post(self, request,id):
        form = ReviewProductForm(request.POST)
        if form.is_valid():
            user = request.user
            product_obj = Product.objects.get(id = int(id))
            review_by_user = ReviewOfProduct.objects.filter(Q(review_user = user) & Q(product = product_obj))
            if len(review_by_user)>0 :
                messages.error(request, 'You have already given a review')
                return redirect('addreview',id = int(id))
            product = Product.objects.get(id = id)
            rating = form.cleaned_data["rating"]
            review_user_name = form.cleaned_data["review_user_name"]
            if float(rating) > 5:
                messages.error(request,"Rating must be in between 1-5. Please try again.")
                return redirect('addreview',id = int(id))
            review_text = form.cleaned_data["review_text"]

            review_obj = ReviewOfProduct(
                review_user=user,
                review_user_name = review_user_name,
                rating=rating,
                product=product,
                review_text=review_text,
            )
            review_obj.save()
            product_review = ReviewOfProduct.objects.filter(product = product)
            print(product_review)
            ratings = []
            for i in product_review:
                ratings.append(i.rating)
            print(ratings)
            avarage_rating = sum(ratings)/len(ratings)
            print(avarage_rating)
            product.avg_rating = round(avarage_rating, 1)
            product.total_ratings_count += 1
            product.save()
            messages.success(request, "Review Added Successfully.")
        else:
            messages.warning(request, "Please check your data again")
        return render(request, "review_form.html", locals())


def AllReviewsOfAProductView(request,id):
    user = request.user

    reviews = ReviewOfProduct.objects.filter(product__id=id)
    reviews_to_show = reviews[:20]

    rating_label_list = ["4 < rating <= 5","3 < rating <= 4","2 < rating <= 3","1 < rating <= 2"]
    rating_count_in_product = []

    rating_greater_than_four = ReviewOfProduct.objects.filter(Q(product__id=id) & Q(rating__gt = 4) & Q(rating__lte = 5)).count()
    rating_count_in_product.append(rating_greater_than_four)

    rating_greater_than_three = ReviewOfProduct.objects.filter(Q(product__id=id) & Q(rating__gt = 3) & Q(rating__lte = 4)).count()
    rating_count_in_product.append(rating_greater_than_three)

    rating_greater_than_two = ReviewOfProduct.objects.filter(Q(product__id=id) & Q(rating__gt = 2) & Q(rating__lte = 3)).count()
    rating_count_in_product.append(rating_greater_than_two)

    rating_greater_than_one = ReviewOfProduct.objects.filter(Q(product__id=id) & Q(rating__gt = 1) & Q(rating__lte = 2)).count()
    rating_count_in_product.append(rating_greater_than_one)

    print(rating_count_in_product)
    return render(request,"allreviewsofaproduct.html",locals())


def ProductReturnFormView(request):
    if request.method == 'POST':
        reason = request.POST.get('message')
        id = request.POST.get('order_id')
        email_for_verify = request.POST.get('email')
        print(reason,id,email_for_verify)

        order = Order.objects.get(order_id=id)
        product_and_quantity = json.loads(order.quantity)
        try:
            subject = "Regarding Your Return Process. Please Check Below."
            message = f"\nDear Sir/Madam,\n\tWe have successfully received your request for the following item.\nItem Name & Quantity : {order.quantity}\nOrder ID : {order.order_id}.\nIt is under processing you will informed in your return history after this process completed."
            from_email = "verification@gmail.com"
            send_mail(subject, message, from_email,[email_for_verify], fail_silently=False)
            return_obj = ReturnProduct(user = request.user,order = order,reason = reason,return_status = 0,return_product = product_and_quantity)
            return_obj.save()

            return redirect(reverse("orderview"))
        except Exception as e:
            messages.error(request,"Error Whle Returning The Product : "+str(e))
            return redirect(reverse("orderview"))
    

def add_Review_After_buying(request,id):
    order_obj_id = id
    order_obj = Order.objects.get(order_id = id)
    order_products = order_obj.product.split(",")
    product_review_objs = []
    single_order_products = []
    for i in order_products:
        p = i.strip('[]')
        x = p.strip().replace("'","")
        product_obj = Product.objects.filter(title = x)
        product_review_objs.append(product_obj)
    for m in product_review_objs:
        for j in m:
            single_order_products.append(j)
    for item in single_order_products:
        print(item.title,item.product_available)
    return render(request,"afterbuyingaddreview.html",locals())
