from django.urls import path, include
from .views import account_login, account_logout, member_dashboard

urlpatterns = [

    path( '', account_login, name='account_login' ),
    path( 'logout/', account_logout, name='account_logout' ),
    path( 'admin/', include('super.urls') ),
    # path( 'member/', member_dashboard, name='member_dashboard' ),

]