from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('categories/', views.CategoryListCreate.as_view(), name='category-list-create'),
    path('subcategories/', views.SubCategoryListCreate.as_view(), name='subcategory-list-create'),
    path('products/', views.ProductListCreate.as_view(), name='product-list-create'),
    path('attributes/', views.AttributeListCreate.as_view(), name='attribute-list-create'),
    path('subattributes/', views.SubAttributeListCreate.as_view(), name='subattribute-list-create'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
