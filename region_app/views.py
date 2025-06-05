from django.shortcuts import render
import requests
import logging
import json
import os
import time
from urllib.parse import urljoin
from requests.exceptions import RequestException
from django.contrib.auth import logout
from bs4 import BeautifulSoup
import random
from accounts.models import Product,ShoppingCart,WrittenReview,Order,BankDetails
# from accounts.form import ReviewForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import base64
from io import BytesIO
from PIL import Image










def home_view(request):
    # helper to build a list of products with a `resized_image` data-URI
    def get_resized_products(qs):
        resized = []
        for p in qs:
            data_uri = ''  # Default placeholder

            try:
                if p.image and p.image.path and os.path.isfile(p.image.path):
                    # open, convert, resize
                    img = Image.open(p.image.path)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img = img.resize((348, 328), Image.LANCZOS)

                    # write to buffer as high-quality JPEG
                    buf = BytesIO()
                    img.save(buf, format="JPEG", quality=90)
                    buf.seek(0)

                    # encode to base64 and form data URI
                    b64 = base64.b64encode(buf.read()).decode()
                    data_uri = f"data:image/jpeg;base64,{b64}"
            except (FileNotFoundError, UnidentifiedImageError, ValueError):
                # Log or silently pass on error (image missing, corrupt, etc.)
                data_uri = None  # Or keep as '' if preferred

            # attach it to the product instance
            p.resized_image = data_uri
            resized.append(p)
        return resized

    # Queries
    featured_products = Product.objects.filter(product_tag=Product.FEATURED)
    bestsellers       = Product.objects.filter(product_tag='Bestsellers')
    New_arrivals      = Product.objects.filter(product_tag='New Arrivals')
    Top_rated         = Product.objects.filter(product_tag='Top Rated')
    On_sale           = Product.objects.filter(product_tag='Sale')
    all_products_qs   = Product.objects.all()

    Amplifies     = Product.objects.filter(product_category='Amplifiers')
    Digital       = Product.objects.filter(product_category='Digital')
    Loudspeakers  = Product.objects.filter(product_category='Loudspeakers')
    Turntables    = Product.objects.filter(product_category='Turntables')

    # Resize for display
    Amplifies     = get_resized_products(Amplifies)
    Digital       = get_resized_products(Digital)
    Loudspeakers  = get_resized_products(Loudspeakers)
    Turntables    = get_resized_products(Turntables)
    all_products  = get_resized_products(all_products_qs)

    return render(request, 'home/index.html', {
        'Amplifies': Amplifies,
        'Digital': Digital,
        'Loudspeakers': Loudspeakers,
        'Turnatables': Turntables,
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'New_arrivals': New_arrivals,
        'Top_rated': Top_rated,
        'on_sale': On_sale,
        'all_products': all_products,
    })


def resize_product(product):
    """
    Resize a single Product instance’s image to 348×328px,
    encode it as a base64 data URI, and attach it as product.resized_image.
    """
    data_uri = ''
    if product.image and hasattr(product.image, 'path'):
        try:
            img = Image.open(product.image.path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img = img.resize((348, 328), Image.LANCZOS)

            buf = BytesIO()
            img.save(buf, format="JPEG", quality=90)
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode('utf-8')
            data_uri = f"data:image/jpeg;base64,{b64}"
        except Exception:
            data_uri = ''  # fallback on any error

    product.resized_image = data_uri
    return product


def get_resized_products(queryset):
    """
    Given a Product queryset, return a list of those Product instances
    each annotated with .resized_image.
    """
    return [resize_product(p) for p in queryset]


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # GET request: render product details
    related_qs = Product.objects.filter(product_category=product.product_category).exclude(id=product.id)
    reviews = WrittenReview.objects.filter(product=product)

    product = resize_product(product)
    related_products = get_resized_products(related_qs)

    return render(request, 'home/product_details.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    })



def submit_reviews(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            content = data.get('message')  # 'message' comes from the textarea

            if not all([name, email, content]):
                return JsonResponse({
                    'success': False,
                    'message': 'Name, email, and review content are required.'
                }, status=400)

            # You must pass the product ID in the URL or the body
            product_id = data.get('product_id')
            if not product_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Product ID is required.'
                }, status=400)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Product not found.'
                }, status=404)

            WrittenReview.objects.create(
                product=product,
                name=name,
                email=email,
                content=content
            )

            return JsonResponse({
                'success': True,
                'message': 'Review submitted successfully!',
                'redirect_url': request.path
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Server error occurred.'}, status=500)




def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
       return JsonResponse({"error": "Login is required to add items to the cart."}, status=401)

    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)  # Fetch the product
            user = request.user  # Get the logged-in user
            
            # Check if the product is already in the cart
            cart_item, created = ShoppingCart.objects.get_or_create(
                user=user, product=product,shipping_fee=product.shipping_fee,
                defaults={'quantity': 1}
            )
            if not created:
                # If the item exists, increase the quantity
                cart_item.quantity += 1
                cart_item.save()
            
            return JsonResponse({"message": "Product added to cart successfully!"}, status=200)
        
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)


@login_required(login_url='authenticate')
def get_cart_count(request):
    if request.user.is_authenticated:
        cart_count = ShoppingCart.objects.filter(user=request.user).count()  # Get the number of items in the cart
        return JsonResponse({"cart_count": cart_count})
    else:
        return JsonResponse({"cart_count": 0})




@login_required(login_url='authenticate')
def cart_view(request):
    # Fetch cart items for the logged-in user
    cart_items = ShoppingCart.objects.filter(user=request.user)
    
    # Initialize total variables
    subtotal = 0
    total = 0
    shipping_total = 0
    
    # Loop through each item to calculate subtotal and shipping fee
    for item in cart_items:
        # Calculate the subtotal (product price * quantity)
        item_subtotal = item.product.price * item.quantity
        subtotal += item_subtotal
        
        # Calculate the shipping fee for the item (example logic)
        shipping_fee = item.product.shipping_fee * item.quantity  # You can adjust this logic based on the product
        
        # Add shipping fee to the total
        shipping_total += shipping_fee
        
        # Add the item total (subtotal + shipping) to the total
        total += item_subtotal + shipping_fee

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_total': shipping_total,
        'total': total,
    }
    return render(request, 'home/cart.html', context)


def get_cart_total(user):
    cart_items = ShoppingCart.objects.filter(user=user)
    total = sum(item.total_price() for item in cart_items)
    return total



def calculate_shipping_fee(cart_total):
    # Example: Flat $10 shipping if cart total is below $100, free otherwise
    return  cart_total 


@login_required(login_url='authenticate')
# Function to increase item quantity
def increase_quantity(request, item_id):
    cart_item = ShoppingCart.objects.get(id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    # Calculate updated totals
    cart_total = get_cart_total(request.user)
    shipping_fee = calculate_shipping_fee(cart_total)
    total_amount = cart_total + shipping_fee

    return JsonResponse({
        'new_quantity': cart_item.quantity,
        'new_total': cart_item.total_price(),
        'new_cart_total': cart_total,
        'new_shipping_total': shipping_fee,
        'new_total_amount': total_amount,
    })

# Function to decrease item quantity
def decrease_quantity(request, item_id):
    cart_item = ShoppingCart.objects.get(id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    # Calculate updated totals
    cart_total = get_cart_total(request.user)
    shipping_fee = calculate_shipping_fee(cart_total)
    total_amount = cart_total + shipping_fee

    return JsonResponse({
        'new_quantity': cart_item.quantity,
        'new_total': cart_item.total_price(),
        'new_cart_total': cart_total,
        'new_shipping_total': shipping_fee,
        'new_total_amount': total_amount,
    })

@login_required(login_url='authenticate')
# Function to remove item from cart
def remove_from_cart(request, item_id):
    cart_item = ShoppingCart.objects.get(id=item_id, user=request.user)
    cart_item.delete()

    # Calculate updated totals
    cart_total = get_cart_total(request.user)
    shipping_fee = calculate_shipping_fee(cart_total)
    total_amount = cart_total + shipping_fee

    return JsonResponse({
        'message': 'Item removed successfully',
        'new_cart_total': cart_total,
        'new_shipping_total': shipping_fee,
        'new_total_amount': total_amount,
    })






def authenticate_view(request):
    return render(request,'auth/authenticate.html')


@login_required(login_url='authenticate')
def checkout_view(request):
    cart_items = ShoppingCart.objects.filter(user=request.user)
    # Calculate cart total and shipping fee
    cart_total = sum(item.total_price() for item in cart_items)
    shipping_fee = sum(item.shipping_fee for item in cart_items)  
    total_with_shipping = cart_total + shipping_fee
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_fee': shipping_fee,
        'total_with_shipping': total_with_shipping,
    }
    return render(request,'home/checkout.html',context)    



def get_bank_details(request):
    try:
        bank_details = BankDetails.objects.first()  # Fetch the first bank details record
        if not bank_details:
            return JsonResponse({"error": "Bank details not found"}, status=404)

        return JsonResponse({
            "bank_name": bank_details.bank_name,
            "branch_name": bank_details.branch_name,
            "account_number": bank_details.account_number,
            "account_holder": bank_details.account_holder,
            "swift_code": bank_details.swift_code,
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  

@login_required(login_url='authenticate')
def create_order(request):
    if request.method == "POST":
        try:
            # Parse the request body
            data = json.loads(request.body)

            billing_details = data.get("billingDetails")
            cart_details = data.get("cartDetails")

            # Validate data
            if not billing_details or not cart_details:
                return JsonResponse({"success": False, "error": "Invalid request data."}, status=400)

            # Create a list to hold order IDs for the response
            order_ids = []

            # Iterate over each product in the cart
            for product in cart_details["products"]:
                # Calculate total price for the individual product order
                total_price = float(product["quantity"]) * float(product["price"])

                # Calculate shipping fee (this is a placeholder; adjust as needed)
                shipping_fee = cart_details.get("shipping_fee", 0.0)  # Ensure this is set correctly

                # Create a new order instance for each product
    
                order = Order(
                    user=request.user,
                    street_address=billing_details["street_address"],
                    city=billing_details["city"],
                    state=billing_details["state"],
                    postcode=billing_details["postcode"],
                    email=billing_details["email"],
                    phone=billing_details["phone"],
                    product_details=json.dumps({"products": [product]}),  # Store only the current product
                    total_price=total_price,
                    shipping_fee=shipping_fee,
                )

                # Assign an image to the order from the product
                product_id = product["id"]
                try:
                    product_instance = Product.objects.get(id=product_id)
                    if product_instance.image:
                        order.order_image = product_instance.image  # Assign product's image to order_image
                except Product.DoesNotExist:
                    pass  # Handle the case where the product does not exist

                # Save the order instance
                order.save()
                order_ids.append(order.id)  # Store the order ID for the response

            # Clear the shopping cart for the user
            ShoppingCart.objects.filter(user=request.user).delete()

            return JsonResponse({"success": True, "order_ids": order_ids})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)




def order_success(request):
    return render(request, 'home/order.html')



@login_required(login_url='authenticate')
def myorders(request):
    """
    Fetch and display all orders for the currently logged-in user.
    """
    # Fetch orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Parse product details for each order
    for order in orders:
        try:
            order.product_details_parsed = json.loads(order.product_details).get('products', [])
        except json.JSONDecodeError:
            order.product_details_parsed = []  # Default to empty list if JSON is invalid

    return render(request, 'home/my_orders.html', {
        'orders': orders,
    })



def about_us_view(request):
    return render(request,'home/about.html')



def contact_view(request):
    return render(request,'home/contact.html')




def product_search(request):
    query = request.GET.get('search', '').strip()  # Trim whitespace
    print(f"Search query: '{query}'")  # Debugging line

    if query:
        # Check if the query length is less than 3
        if len(query) < 3:
            # If less than 3 characters, we can still search for products that contain the query
            products = Product.objects.filter(name__icontains=query)
        else:
            # If 3 or more characters, perform a more comprehensive search
            products = Product.objects.filter(name__icontains=query)

        print(f"Found products: {products}")  # Debugging line
    else:
        products = Product.objects.none()

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home/search_results.html', {
        'Search_products': page_obj,
        'Search_count': products.count(),
        'search_query': query,
    })




def terms_view(request):
    return render(request,'home/terms_conditions.html')

def refund_view(request):
    return render(request,'home/refund_policy.html')




def product_by_category_view(request, category_name):
    # Fetch products by category
    products = Product.objects.filter(product_category=category_name)

    # Pagination
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate start and end indices
    start_index = (page_obj.number - 1) * paginator.per_page + 1
    end_index = start_index + len(page_obj) - 1
    total_products = products.count()

    # Pass to template
    return render(request, f'home/products/{category_name.replace(" ", "_")}.html', {
        'products': page_obj,
        'start_index': start_index,
        'end_index': end_index,
        'total_products': total_products,
        'category_name': category_name,
    })  




def product_search(request):
    query = request.GET.get('search', '').strip()  # Trim whitespace
    print(f"Search query: '{query}'")  # Debugging line

    # Basic search logic
    if query:
        products = Product.objects.filter(name__icontains=query)
        print(f"Found products: {products}")  # Debugging line
    else:
        products = Product.objects.none()

    # Pagination
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate start and end indices
    start_index = (page_obj.number - 1) * paginator.per_page + 1
    end_index = start_index + len(page_obj) - 1
    total_products = products.count()

    return render(request, 'home/search_results.html', {
        'products': page_obj,
        'start_index': start_index,
        'end_index': end_index,
        'total_products': total_products,
        'query': query,  # Send query back for use in the template
        'category_name' : query,
    })









