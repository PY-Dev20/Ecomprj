from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from core.models import Category, Vendor, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, Wishlist, Address
from django.db.models import Count, Avg
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.template.loader import render_to_string



app_name = "core"
# Create your views here.
def home(request):
    products = Product.objects.filter(product_status="published", featured=True)
    categories = Category.objects.all().order_by('-id')
    vendors = Vendor.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'vendors': vendors,
        
    }
    return render(request, 'core/home.html', context)

def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    
    
    context = {
        'products': products,
        
    }
    return render(request, 'core/product_list.html', context)

def category_list_view(request):
    categories = Category.objects.all().order_by('-id')
    #categories = Category.objects.all().annotate(product_count=Count("product"))
    
    context = {
        'categories': categories
    
    }
    return render(request, 'core/category_list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'core/category_product_list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    
    context = {
        'vendors': vendors,
    }
    return render(request, 'core/vendor_list.html', context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    
    context = {
        'vendor': vendor,
        'products': products,
    }
    return render(request, 'core/vendor_detail.html', context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    
    #Getting All Reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    
    #Getting Avverage Reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating =Avg('rating'))
    
    # Product reviews form
    review_form = ProductReviewForm()    
    
    
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
    
    p_image = product.p_images.all()
    context = {
       
        'p': product,
        'p_image': p_image,
        'products': products,
        'reviews': reviews,
        'make_review': make_review,
        'average_rating': average_rating,
        'review_form': review_form,
    }
    return render(request, 'core/product_detail.html', context)


def tag_list_view(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by('-id')
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        
    context = {
        'products': products,
        'tag': tag,
        
    }
    return render(request, 'core/tag_list.html', context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user, 
        product=product, 
        review=request.POST['review'],
        rating=request.POST['rating'],
        
    )
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }
    
    avarage_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {
          'bool': True,
          'context': context,
          'avarage_reviews': avarage_reviews,
        }
        
    )
    
def search_view(request):
    query = request.GET.get("q")
    
    products = Product.objects.filter(title__icontains=query).order_by('-date')
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'core/search.html', context)
    
def filter_product_view(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    
    
    min_price = request.GET['min_price']
    max_price = request.GET['max_price']
    
    
    products = Product.objects.filter(product_status="published").order_by('-id').distinct()
    
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()
        
    context = {
        'products': products,
    }
        
    data = render_to_string("core/async/product_filter_list.html", context)
    
    return JsonResponse({'data': data})

def add_to_cart(request):
    # Retrieve product data from the query string
    product_id = request.GET.get('id')
    product_title = request.GET.get('title')
    product_price = float(request.GET.get('price', 0))
    quantity = int(request.GET.get('qty', 0))

    # Create a dictionary to hold the product data
    cart_product = {
        'title': product_title,
        'qty': quantity,
        'price': product_price,
    }

    # Update the cart data in the session
    cart_data = request.session.get('cart_data_obj', {})
    if product_id in cart_data:
        cart_data[product_id]['qty'] = quantity
    else:
        cart_data[product_id] = cart_product
    request.session['cart_data_obj'] = cart_data

    # Return a JSON response
    data = {'data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])}
    return JsonResponse(data)
        
    

