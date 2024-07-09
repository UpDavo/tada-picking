from django.urls import path
from .views import *
from core.views import NotAllowed

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),
    
    # Invoice
    path('invoices', InvoiceList.as_view(), name='invoices'),
    
    # Invoice
    path('points', PointsList.as_view(), name='points'),
    path('points/upload', UploadPoints.as_view(), name='points_upload'),


    # Users
    path('users', UsersList.as_view(), name='users'),
    path('users/create', CreateUser.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', EditUser.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(), name='user_delete'),

    # Roles
    path('roles', RoleList.as_view(), name='roles'),
    path('roles/create', CreateRole.as_view(), name='role_create'),
    path('roles/<int:pk>/edit/', EditRole.as_view(), name='role_edit'),
    path('roles/<int:pk>/delete/', DeleteRole.as_view(), name='role_delete'),
    
    # Stores
    path('stores', StoreList.as_view(), name='stores'),
    path('stores/create', CreateStore.as_view(), name='store_create'),
    path('stores/<int:pk>/edit/', EditStore.as_view(), name='store_edit'),
    path('stores/<int:pk>/delete/', DeleteStore.as_view(), name='store_delete'),
    
    # Cities
    path('cities', CityList.as_view(), name='cities'),
    path('cities/create', CreateCity.as_view(), name='city_create'),
    path('cities/<int:pk>/edit/', EditCity.as_view(), name='city_edit'),
    path('cities/<int:pk>/delete/', DeleteCity.as_view(), name='city_delete'),

    # Products
    path('products', ProductList.as_view(), name='products'),
    path('products/create', CreateProduct.as_view(), name='product_create'),
    path('products/upload', UploadProduct.as_view(), name='product_upload'),
    path('products/<int:pk>/edit/', EditProduct.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/',
         DeleteProduct.as_view(), name='product_delete'),

    # Products
    path('stocks', StockList.as_view(), name='stocks'),
    path('stocks/create', CreateStock.as_view(), name='stock_create'),
    path('stocks/<int:pk>/edit/', EditStock.as_view(), name='stock_edit'),
    path('stocks/<int:pk>/delete/',
         DeleteStock.as_view(), name='stock_delete'),
    path('stocks/<int:pk>/upload', UploadStock.as_view(), name='stock_upload'),
    path('stocks/upload', UploadStockGeneral.as_view(), name='stock_upload_general'),


    # Extras
    path('not_allowed', NotAllowed, name='notAllowed'),
]
