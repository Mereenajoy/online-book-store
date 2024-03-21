from django.db.models import Max
from django.shortcuts import render , redirect ,get_object_or_404
from .models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . forms import checkoutform
from django.contrib import messages
from .forms import OrderStatusForm
from django.db.models import Count
from datetime import datetime, timedelta
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponseNotAllowed

from django.db.models import F

# Create your views here.


def index(request):
    return render(request, 'index.html')



# def signup(request):
#     if request.method == "POST":
#         fname = request.POST["fname"]
#         email = request.POST["email"]
#         password = request.POST["password"]
#         va = User_reg(fname=fname, email=email,
#                       password=password)
#         va.save()
#         return render(request, 'login.html')
#     else:
#         return render(request, 'signup.html')

    
def signup(request):
    if request.method=="POST":
        fname=request.POST["fname"]
        email=request.POST["email"]
        password=request.POST['password']
       
        if User_reg.objects.filter(email=email):
            context={'msg':'Email Already Exists!'}
            return render(request,'signup.html',context)
        elif User_reg.objects.filter(fname=fname):
            context={'msg':'Username Already Exists!'}
            return render(request,'signup.html',context)
        else:
            va=User_reg(fname=fname , email=email,password=password)
            va.save()
            # return render(request,'login.html')
            return redirect('login')
    else:
        return render(request,'signup.html')




def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User_reg.objects.filter(email=email, password=password, usertype="A").exists():
            

            return redirect('admin_dashboard')
        
        elif User_reg.objects.filter(email=email, password=password, usertype="U").exists():
            user=User_reg.objects.filter(email=email, password=password, usertype="U")
            print(user)
            request.session['id'] = user[0].uid
            print(request.session['id'])
            return render(request, "homepage.html")

        else:
            return render(request, "invalid.html")
    else:
        return render(request, "login.html")
    
def admin_home(request):
    viewproducts = Book.objects.all()

    vp = {'detail': viewproducts}
    return render(request, 'admin_home.html', vp)

from django.http import Http404
def homepage(request):
    u = request.session.get('id')
    if u is None:
        raise Http404("Session data is missing")

    v = get_object_or_404(User_reg, uid=u)
    context = {'na': [v]}  # Wrap the object in a list to make it iterable
    return render(request, 'homepage.html', context)

def admin_add_product(request):
    if request.method== 'POST':
        file = request.FILES['image']
        fs = FileSystemStorage()
        path = fs.save(file.name ,file)

        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        # publidate = request.POST.get('publidate')
        quantity = request.POST.get('quantity') 
        # language = request.POST.get('language')
        # publisher = request.POST.get('publisher')

        max_bid = Book.objects.all().aggregate(Max('bid'))['bid__max']
        new_bid = max_bid + 1 if max_bid is not None else 1
        b = Book(bid=new_bid,title=title,author=author,genre=genre,desc=desc ,price=price,quantity=quantity,image=path )
        b.save()
        p = Book.objects.all()
        context = {'msg': 'Product added', 'p': p}

        return render(request, 'admin_add_product.html', context)
    else:
        return render(request, 'admin_add_product.html')


def admin_view_products(request):
    viewproducts = Book.objects.all()

    vp = {'detail': viewproducts}
    return render(request, 'admin_view_product.html', vp)

def view_product(request):
    viewproducts = Book.objects.filter(isdelete=False)
    # viewproducts = Book.objects.all()
    context = {'detail': viewproducts}
    return render(request, 'prdt.html', context)


def product_details(request, product_id):
    product = get_object_or_404(Book, pk=product_id)
    return render(request, 'product_details.html', {'product': product})

def productdetails(request, product_id):
    product = get_object_or_404(Book, pk=product_id)
    return render(request, 'productdetails.html', {'product': product})


def t(request):
    return render(request , 't.html')

def admin_update_pro(request):
    if request.method == 'POST':
        id = request.POST.get('p_id')
        up = Book.objects.get(bid=int(id))
        title = request.POST.get('title')
        author = request.POST.get('author')        
        genre = request.POST.get('genre')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        desc = request.POST.get('desc')
        
        up.title = title
        up.author = author
        up.genre = genre
        up.price = price
        up.quantity = quantity
        up.desc = desc
        up.save()
        msg = 'Product updated'
        up_l = Book.objects.all()
        context = {'detail': up_l, 'msg': msg}
        return render(request, 'admin_view_product.html', context)
    else:
        id = request.GET.get('id')
        up = Book.objects.get(bid=int(id))
        context = {'up': up}
        return render(request, 'admin_update_pro.html', context)
    

    
def admin_delete_product(request):
    if request.method == 'POST':
        id = request.POST.get('id')  # Use POST to pass data
        # Retrieve the product by its ID
        product = Book.objects.get(bid=id)
        
        # Deactivate the product instead of deleting it
        product.isdelete = True
        product.save()

        # Redirect to the view that displays the list of products
        return redirect('admin_view_products')  # Use the view function name
    elif request.method == 'GET':
        # Handle the GET request to display the confirmation page
        id = request.GET.get('id')  # Define 'id' for the GET request
        # Retrieve the product for confirmation
        product = Book.objects.get(bid=id)
        return render(request, 'admin_delete_product.html', {'product': product})

def toggle_product_activation(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Book, bid=product_id)
        action = request.POST.get('action')
        
        if action == 'activate':
            product.isdelete = True
        elif action == 'deactivate':
            product.isdelete = False
        
        product.save()
        
        return redirect('admin_view_products')
    else:
        return HttpResponseNotAllowed(['POST'])



def adminviewusers(request):
    viewuser = User_reg.objects.all()
    context = {'details': viewuser}
    return render(request, 'adminviewusers.html', context)


# def add_to_wishlist(request, bid):
#     book = Book.objects.get(pk=bid)

#     Wishlist.objects.create(
#         title=book.title,
#         price=book.price,
#         desc=book.desc,
#     )

#     return redirect('view_product')

# def wishlist(request):
#     wishlist_items = Wishlist.objects.all()
#     context = {'wishlist_items': wishlist_items}
#     return render(request, 'wishlist.html', context)




def admin_add_category(request):
    return render(request , 'admin_add_category.html')



def mycart(request):
    # Retrieve the user ID from the session
    user_id = request.session['id']
     # Get the user object based on the user ID
    up = User_reg.objects.get(uid=int(user_id))

     # Check if there is a cart associated with the session
    cart_id = request.session.get('cart_id')
    if cart_id:
         # If there is a cart ID in the session, retrieve the cart object
        cart1 = cart.objects.get(id=cart_id)
    else:
        # If there is no cart ID in the session, set cart1 to None
        cart1 = None
     # Prepare the context to be passed to the template   
    context = {'cart': cart1,'u':up}


    return render(request, 'cart.html', context)

def addtocart(request, id):
    product_obj = get_object_or_404(Book, bid=id)

    # Check if the cart exists
    cart_id = request.session.get('cart_id')
    if cart_id:
         # If the cart exists, retrieve the cart object
        cart_obj = cart.objects.get(id=cart_id)
    else:
        # If the cart doesn't exist, create a new cart object and save it in the session
        user_id = request.session.get('id')
        up = User_reg.objects.get(uid=int(user_id))
        cart_obj = cart.objects.create(customer=up, total=0)
        request.session['cart_id'] = cart_obj.id

    # Check if the book is in stock
    if product_obj.quantity <= 0:
        return HttpResponse("Out of Stock")
   
    # Check if the book is already in the cart
    product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)

    # If the book is in the cart
    if product_in_cart.exists():
        cartproduct = product_in_cart.first()
        # Check if adding more exceeds the available quantity
        if cartproduct.quantity + 1 > product_obj.quantity:
            return HttpResponse("Out of Stock")
        else:
            # Increase the quantity and update the subtotal
            cartproduct.quantity += 1
            cartproduct.subtotal += product_obj.price
            cartproduct.save()
            product_obj.quantity -= 1
            product_obj.save()
    else:
        # Create a new CartProduct instance
        cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price,
                                                 quantity=1, subtotal=product_obj.price)

    # Update cart total
    cart_obj.total += product_obj.price
    cart_obj.save()
    product_obj.quantity -= 1
    product_obj.save()

    return redirect("/view_product")

def managecart(request, id):
    print("im in manage cart")
    action = request.GET.get("action")
    cp_obj = CartProduct.objects.get(id=id)
    cart_obj = cp_obj.cart

    if action == "inc":
        cp_obj.quantity += 1
       

        cp_obj.subtotal += cp_obj.rate
        cp_obj.save()
        cart_obj.total += cp_obj.rate
        cart_obj.save()
        cp_obj.product.quantity -= 1  # Decrease book quantity
        cp_obj.product.save()
    elif action == "dcr":
        cp_obj.quantity -= 1
        cp_obj.subtotal -= cp_obj.rate
        cp_obj.save()
        cart_obj.total -= cp_obj.rate
        cart_obj.save()
        cp_obj.product.quantity += 1  # Increase book quantity
        cp_obj.product.save()
        if cp_obj.quantity == 0:
            cp_obj.delete()
            del request.session['cart_id']


    elif action == 'rmv':
        cart_obj.total -= cp_obj.subtotal
        cart_obj.save()
        cp_obj.product.quantity += cp_obj.quantity  # Add removed quantity back to book quantity
        cp_obj.product.save()
        cp_obj.delete()
    else:
        pass

    return redirect('/my-cart')

def emptycart(request):
    cart_id = request.session.get("cart_id", None)
    if cart_id:
        cart_obj = cart.objects.get(id=cart_id)
        for cart_product in cart_obj.cartproduct_set.all():
            book = cart_product.product
            book.quantity += cart_product.quantity  # Increase book quantity
            book.save()
        cart_obj.cartproduct_set.all().delete()
        cart_obj.total = 0
        cart_obj.save()

    return redirect('/my-cart')


def checkout(request):
    user_id=request.session['id']
    user=User_reg.objects.get(uid=user_id)
    cart_id = request.session.get("cart_id")
    cart_obj = cart.objects.get(id=cart_id)
    form = checkoutform(request.POST)
    print()
    if request.method == "POST":
        order_status = "Order recived"

        address = request.POST["address"]

        mobile =request.POST["contact"]
        total = request.POST["total"]
        new_order = Orders.objects.create(cart=cart_obj, customer=user, address=address, mobile=mobile,
                                              total=total, order_status=order_status)
        new_order.save()
        del request.session['cart_id']
        messages.info(request,"Order Placed")
        
        return redirect('user_orders')
    else:
        context = {'cart': cart_obj, 'form': form,'user': user}
        return render(request, 'checkout.html', context)



def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        print("Received query:", query)  # Debugging statement
        if query:
            products = Book.objects.filter(title__icontains=query)
        else:
            products = None

        return render(request, 'search.html', {'products': products, 'query': query})
    

def contact(request):
    return render(request , 'contact.html')




def profile(request):
    # Check if the user is logged in
    if 'id' in request.session:
        # Retrieve the user's ID from the session
        user_id = request.session['id']
        # Fetch the user's profile based on the user ID
        user_profile = User_reg.objects.get(uid=user_id)
        # Pass the user's profile to the template context
        context = {'user_profile': user_profile}
        # Render the profile.html template with the context
        return render(request, 'profile.html', context)
    else:
        # Handle the case when the user is not logged in
        return HttpResponse("Please log in to view your profile.")
    
def updateprofile(request):
    if request.method == 'POST':
        user_id = request.session.get('id')  # Retrieve user's ID from session
        if user_id is not None:
            up = User_reg.objects.get(uid=user_id)  # Query User_reg using uid
            xemail = up.email
            xpassword = up.password
            fname = request.POST.get('fname')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if fname:
                up.fname = fname
            if email:
                up.email = email
            if password:
                up.password = password

            up.save()

            if xemail != up.email or xpassword != up.password:
                return redirect('login')

            context = {'msg': 'User Details Updated', 'up': up}
            return redirect('profile')
        else:
            return redirect('login')
    else:
        user_id = request.session.get('id')
        if user_id is not None:
            up = User_reg.objects.get(uid=user_id)
            context = {'up': up}
            return render(request, 'updateprofile.html', context)
        else:
            return redirect('login')





def admin_view_orders(request):
    # Retrieve all orders ordered by created_at in ascending order
    # orders = Orders.objects.all().order_by(F('created_at').desc())
    orders = Orders.objects.all()
    
    # Prepare data to pass to the template
    orders_data = []
    for order in orders:
        order_info = {
            'id': order.id,
            'customer_name': order.customer.fname,
            'products': order.cart.cartproduct_set.all(),  # Retrieve all products in the cart
            'subtotal': order.total,
            'date_created': order.created_at,
            'order_status': order.order_status,  # Include the order_status field
        }
        orders_data.append(order_info)
    
    # Pass the orders data and ORDER_STATUS to the template for rendering
    context = {'orders': orders_data, 'ORDER_STATUS': ORDER_STATUS}
    return render(request, 'admin_view_orders.html', context)





def user_orders(request):
    # Retrieve the user ID from the session
    user_id = request.session.get('id')
    
    # Filter orders based on the user ID
    user_orders = Orders.objects.filter(customer_id=user_id).order_by(F('created_at').desc())
    
    # Pass the user's orders to the template context
    context = {'user_orders': user_orders}
    
    # Render the template with the user's orders
    return render(request, 'user_orders.html', context)




# def update_order_status(request, order_id):
#     if request.method == 'POST':
#         try:
#             new_status = request.POST.get('order_status')
#             order = get_object_or_404(Orders, id=order_id)
#             order.order_status = new_status
#             order.save()
#             messages.success(request, 'Order status updated successfully.')
#         except Exception as e:
#             messages.error(request, f'An error occurred: {e}')
#     return redirect('admin_view_orders')

def update_order_status(request, order_id):
    if request.method == 'POST':
        # Fetch the order object or return 404 if not found
        order = get_object_or_404(Orders, id=order_id)

        # Get the new status from the submitted form data
        new_status = request.POST.get('order_status')

        # Update the order status and save the order
        order.order_status = new_status
        order.save()

        # Optionally, add a success message
        messages.success(request, "Order status updated successfully.")

        # Redirect to the same page or to any other page
        return HttpResponseRedirect(reverse('admin_view_orders'))
    else:
        # If not a POST request, just redirect to orders list or another appropriate page
        messages.error(request, "Invalid request")
        return HttpResponseRedirect(reverse('admin_view_orders'))




def admin_dashboard(request):
    # Get the total count of users
    total_users = User_reg.objects.count()

    # Get the count of orders
    total_orders = Orders.objects.count()

    # Pass the counts to the template
    context = {
        'total_users': total_users,
        'total_orders': total_orders
    }
    return render(request, 'admin_dashboard.html', context)

def demo(request):
    return render(request , 'demo.html')


# def review(request, book_id):
#     book = get_object_or_404(Book, pk=book_id)
#     reviews = Review.objects.filter(book=book)
#     user_id = request.session.get('id')
#     user=User_reg.objects.get(uid=user_id)
#     if request.method == 'POST':
#         print("inside post")
#         rating=request.POST['rating']
#         comment=request.POST['comment']  
#         new=Review.objects.create(rating=rating,comment=comment,book=book,reviewer=user)
#         new.save()
#         print(new)
#         f=f"http://127.0.0.1:8000/review/{book_id}/"  
#         return redirect(f)
    
#     return render(request, 'review.html', {'book': book, 'reviews': reviews})


