from django.contrib import admin
from django.urls import path
from Buyer import views as buy
from seller import views as seller
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/view',seller.view_all_product.as_view()),
    path('product/add',seller.Add_product.as_view()),
    path('account/add',buy.CustomerRegistration.as_view()),
    path('account/login',buy.CustomerLoginView.as_view()),
    path('profile-view',buy.CustomerProfileView.as_view()),
    path('change-password',buy.CustomerChangePassword.as_view()),
    path('password-reset-token',buy.SendPasswordRestEmailView.as_view()),
    path('rest-password/<uid>/<token>',buy.CustomerPasswordResetView.as_view()),
    path('search_product/<str:qu>',seller.search_product.as_view()),
    path('category',seller.add_Category.as_view()),
    path('search-category/<str:que>',seller.list_of_product_by_Categeory.as_view()),
    path('category-list',seller.Category_list.as_view()),
    path('add-cart/<int:pid>',seller.add_cart.as_view()),
    path('cart-list',seller.listing_of_cart.as_view()),
    path('add-tags',seller.tag_products.as_view()),
    path('list-tags/<int:id>',seller.listing_of_tages_products.as_view()),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
