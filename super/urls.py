from django.urls import path
from . import views

urlpatterns = [
    path( '', views.admin_dashboard , name='admin_dashboard' ),
    path( 'admin-products', views.products , name='admin_products' ),
    path( 'admin-products/<int:product_id>', views.products , name='admin_product_show' ),
    path( 'admin-products-update/<int:product_id>', views.product_edit , name='admin_product_update' ),
    path( 'admin-products-delete/<int:product_id>', views.product_delete , name='admin_product_delete' ),


    path( 'admin-category', views.category , name='admin_category' ),
    path( 'admin-category/<int:category_id>', views.category , name='admin_category_show' ),
    path( 'admin-category-update/<int:category_id>', views.category_edit , name='admin_category_update' ),
    path( 'admin-category-delete/<int:category_id>', views.category_delete , name='admin_category_delete' ),
]