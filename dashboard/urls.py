from django.urls import path
from .views import *
from core.views import NotAllowed

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardIndexView.as_view(), name='index'),

    # Invoice
    path('invoices', InvoiceList.as_view(), name='invoices'),
    path('invoices/download/', DownloadExcel.as_view(),
         name='invoice_download_excel'),
    path('invoices/<int:pk>/edit/', UpdateInvoice.as_view(), name='invoice_edit'),
    path('invoices/<int:pk>/view/', ViewInvoice.as_view(), name='invoice_view'),

    # Invoice
    path('points', PointsList.as_view(), name='points'),
    path('points/upload', UploadPoints.as_view(), name='points_upload'),

    # Invoice
    path('picking', PickingForm.as_view(), name='picking'),
    path('picking/complete', PickingComplete.as_view(), name='picking_complete'),


    # Users
    path('users', UsersList.as_view(), name='users'),
    path('users/create', CreateUser.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', EditUser.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(), name='user_delete'),

    # Clients
    path('clients', ClientList.as_view(), name='clients'),
    path('clients/upload', UploadClients.as_view(),
         name='clients_upload_general'),

    # Orders
    path('orders', ClientOrdersList.as_view(), name='orders'),

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

    # Bottles
    path('bottles', BottleList.as_view(), name='bottles'),
    path('bottles/create', CreateBottle.as_view(), name='bottle_create'),
    path('bottles/<int:pk>/edit/', EditBottle.as_view(), name='bottle_edit'),
    path('bottles/<int:pk>/delete/', DeleteBottle.as_view(), name='bottle_delete'),

    # Bottle Rules
    path('bottle_rules', BottleRuleList.as_view(), name='bottle_rules'),
    path('bottle_rules/create', CreateBottleRule.as_view(),
         name='bottle_rule_create'),
    path('bottle_rules/<int:pk>/edit/',
         EditBottleRule.as_view(), name='bottle_rule_edit'),
    path('bottle_rules/<int:pk>/delete/',
         DeleteBottleRule.as_view(), name='bottle_rule_delete'),

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
    path('stocks/upload', UploadStockGeneral.as_view(),
         name='stock_upload_general'),


    # api
    path('verificar-celular', verificar_celular, name='verificar_celular'),


    # Extras
    path('not_allowed', NotAllowed, name='notAllowed'),
]
