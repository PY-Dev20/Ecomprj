from django.urls import path
from . import views
app_name = "core"

urlpatterns = [
    
    path('', views.home, name='home'),
    
    #Product
    path('product/', views.product_list_view, name='product_list'),
    path('product/<pid>/', views.product_detail_view, name='product_detail'),
    
    
    #Category
    path('category/', views.category_list_view, name='category_list'),
    path('category/<cid>/', views.category_product_list_view, name='category_product_list'),
    
    #Vendor
    path('vendors/', views.vendor_list_view, name='vendor_list'),
    path('vendor/<vid>/', views.vendor_detail_view, name='vendor_detail'),
    
    #Tags
    path('products/tag/<slug:tag_slug>/', views.tag_list_view, name='tag_list'),
    
    #Add reviews
    path('ajax_add_review/<pid>/', views.ajax_add_review, name='ajax_add_review'), 
    
    #Search
    path('search/', views.search_view, name='search'),
    
    # products filter in product list
    path('filter-products/', views.filter_product_view, name='filter-products'),
    
    #add products to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    
    
]