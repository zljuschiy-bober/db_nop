from django.urls import path
from django.conf.urls import url
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('view_cat/', views.category_view, name='view_category'),
    path('view_region/', views.region_edit, name='edit_region'),
    # FIRM
    path('view_firm/', views.firm_view, name='firm_view'),
    url(r'^firm=(?P<pk>\d+)$', views.firm_detail, name='firm_detail'),
    # OBJECT
    path('view_obj/', views.object_view_all, name='object_view_all'),
    url(r'^obj=(?P<pk>\d+)$', views.object_detail, name='object_detail'),
    path('search/', views.search_object, name='search_object'),
    path('profile/', views.view_profile, name='view_profile'),
    # Documents
    path('view_doc/', views.doc_view_all, name='doc_view_all'),
    url(r'^doc=(?P<pk>\d+)$', views.doc_detail, name='doc_detail'),
    path('search_doc/', views.search_doc, name='search_doc'),

]
