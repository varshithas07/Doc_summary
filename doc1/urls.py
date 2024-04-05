from django.urls import path,re_path
from django.contrib import admin
from doc1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
path('doc/', views.doc_view, name='doc'),
path('split_pdf/', views.split_pdf, name='split_pdf'),]