from django.urls import path
from .views import register, login_view, logout_view, seller_dashboard, buyer_dashboard,view_property,update_property,delete_property

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard'),
    path('buyer_dashboard/', buyer_dashboard, name='buyer_dashboard'),
    path('property/<int:property_id>/', view_property, name='view_property'),
    path('property/update/<int:property_id>/', update_property, name='update_property'),
    path('property/delete/<int:property_id>/', delete_property, name='delete_property'),
]

