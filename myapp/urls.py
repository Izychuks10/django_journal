from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import blog_detail, home, your_login_view, your_logout_view
from .views import delete_comment


urlpatterns = [
    path('', views.index, name='index'),
    path('journals/', views.journals, name='journals'),
    path('blog/', views.blog, name='blog'),  # New URL for adding journal
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('blog/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('home/', home, name='home'),
    path('logout/', your_logout_view, name='your_logout'),
    path('login/', your_login_view, name='login'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

]