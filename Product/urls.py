from django.urls import path, include


from . import views


urlpatterns = (
    # urls for Product
    path('', views.ProductListView.as_view(), name='Product_product_list'),
    path('product/detail/<slug:slug>/', views.ProductDetailView.as_view(), name='Product_product_detail'),
    path('search', views.products_search, name="search"),

    # urls for order
    path('orders/', views.OrderListView.as_view(), name='Product_order_list'),
    path('order/confirmed/', views.order_confirm, name='Product_order_confirm'),
    path('order/create/<slug:slug>', views.OrderCreateView.as_view(), name='Product_order_create'),
    path('order/detail/<slug:slug>/', views.OrderDetailView.as_view(), name='Product_order_detail'),
)

