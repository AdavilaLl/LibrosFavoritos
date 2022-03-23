from django.urls import path     
from . import views_forms
from django.conf import settings
from django.conf.urls.static import static

app_name = 'baby'

urlpatterns = [
    path('login/', views_forms.login, name='login' ),
    path('logout/', views_forms.logout, name='logout' ),
    path('register/', views_forms.register, name='register' ),
    path('', views_forms.mainPage, name='mainPage' ),
    path('products/<str:size> ', views_forms.productBySize, name='productBySize'),
    path('products/<str:size>/<str:category> ', views_forms.productBySizeByCat, name='productBySizeByCat'),

    path('products/addToShoppingCart/<int:id>', views_forms.addToShoppingCart, name='addToShoppingCart'),
    path('shoppingCart/empty', views_forms.shoppingCartempty, name='shoppingCartempty'),
    path('shoppingCart/', views_forms.shoppingCart, name='shoppingCart'),
    path('shoppingCart/buy', views_forms.buy, name='buy'),

    path('products/', views_forms.productGrid, name='productGrid'),
    #Admin
    path('adminPage/', views_forms.adminMainPage, name='adminPage' ),
    path('adminPage/users', views_forms.showUsers, name='showUsers' ),
    path('adminPage/users/add', views_forms.addUserAdmin, name='addUser' ),
    path('adminPage/users/editUser/<int:id>', views_forms.editUser, name='editUser' ),
    path('adminPage/users/deleteUser/<int:id>', views_forms.deleteUser, name='deleteUser' ),
    path('adminPage/products', views_forms.adminShowProductsPage, name='showProducts' ),
    path('adminPage/products/add', views_forms.addProduct, name='addProduct' ),
    path('adminPage/products/edit/<int:id>', views_forms.editProd, name='editProd' ),
    path('adminPage/products/delete/<int:id>', views_forms.deleteProd, name='deleteProd' ),
    path('adminPage/products/detail/<int:id>', views_forms.showProductDetail, name='showProductDetail' ),
    path('adminPage/products/addCategory', views_forms.addCategory, name='addCategory' ),
    path('adminPage/products/editCat/<int:id>', views_forms.editCat, name='editCat' ),
    path('adminPage/products/deleteCat/<int:id>', views_forms.deleteCat, name='deleteCat' ),
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)