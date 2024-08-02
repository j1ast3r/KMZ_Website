from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.home, name='home'),
                  path('hall', views.concerts_view, name='hall'),
                  path('events/', views.events_view, name='events_list'),
                  path('event/<int:event_id>/', views.event_detail, name='event_detail'),
                  path('about/', views.about_view, name='about_us'),
                  path('profile/', views.profile, name='profile'),
                  path('cart/', views.cart_view, name='shopping_cart'),
                  path('signup/', views.signup_view, name='signup'),
                  path('login/', views.login_view, name='login'),
                  path('cart/', views.cart_view, name='cart'),
                  path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
                  path('remove-from-cart/<int:ticket_id>/', views.remove_from_cart, name='remove_from_cart'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

print(urlpatterns)  # Add this line for debugging
