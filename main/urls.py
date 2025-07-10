from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book_list/', views.book_list, name='book_list'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/<int:book_id>/', views.book_details, name='book_details'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('about/', views.about, name='Aboutus'),
     path('borrow_book/<int:book_id>/', views.borrow_book, name='borrow_book'),  
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
    path('return_book/<int:borrowed_id>/', views.return_book, name='return_book'),
]
