from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignupForm
from .models import Book, BorrowedBook
from .forms import BookForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse


def home(request):
    return render(request, 'home.html', {'is_admin': request.user.is_superuser})


User = get_user_model()
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            role = form.cleaned_data.get('role')
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False

            user.save()
            messages.success(request, f'🎉 Welcome to Biblionet! Your account has been created successfully. Please log in to start your reading journey.')
            return redirect('login')
        # If form is invalid, do NOT set a message, just show errors in the template
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': '❌ User not found. Please check your email or sign up for a new account.'})

        user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'👋 Welcome back, {user.username}! Ready to explore our collection of books?')
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '❌ Invalid password. Please try again.'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, '👋 You have been successfully logged out. Thank you for using Biblionet! Come back soon for more great reads.')
    return redirect('login')


def book_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        books = Book.objects.filter(title__icontains=search_query) | Book.objects.filter(
            author__icontains=search_query) | Book.objects.filter(category__icontains=search_query)
    else:
        books = Book.objects.all()
    
    # Get user's currently borrowed books
    user_borrowed_books = set()
    if request.user.is_authenticated:
        user_borrowed_books = set(BorrowedBook.objects.filter(
            user=request.user, 
            returned=False
        ).values_list('book_id', flat=True))
    
    # Prefetch borrowed books information and calculate status
    books_with_status = []
    for book in books:
        # Only count non-returned books for availability
        active_borrows = BorrowedBook.objects.filter(book=book, returned=False).count()
        available_copies = book.quantity - active_borrows
        
        books_with_status.append({
            'book': book,
            'active_borrows': active_borrows,
            'available_copies': available_copies,
            'is_borrowed_by_user': book.id in user_borrowed_books
        })
    
    return render(request, 'book_list.html', {
        'books_with_status': books_with_status,
        'is_admin': request.user.is_superuser
    })


from .forms import BookForm  # تأكدي إنك مستوردة الفورم

@login_required
def add_book(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  
        if form.is_valid():
            book = form.save()
            messages.success(request, f'📚 Book Added: "{book.title}" by {book.author} has been successfully added to the library collection with {book.quantity} copy(ies).')
            return redirect('book_list')
    else:
        form = BookForm()  

    books = Book.objects.all().prefetch_related('borrowedbook_set')
    books_with_info = []
    for book in books:
        current_borrowers = book.borrowedbook_set.filter(returned=False)
        borrower_count = current_borrowers.count()
        books_with_info.append({
            'book': book,
            'borrower_count': borrower_count,
            'is_borrowed': borrower_count > 0
        })

    return render(request, 'add_book.html', {
        'form': form,
        'books_info': books_with_info
    })


def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Calculate book availability
    active_borrows = BorrowedBook.objects.filter(book=book, returned=False).count()
    available_copies = book.quantity - active_borrows
    
    # Check if user has borrowed this book
    user_borrowed_books = set()
    borrowed_id = None
    if request.user.is_authenticated:
        borrowed_qs = BorrowedBook.objects.filter(user=request.user, book=book, returned=False)
        user_borrowed_books = set(BorrowedBook.objects.filter(
            user=request.user, 
            returned=False
        ).values_list('book_id', flat=True))
        if borrowed_qs.exists():
            borrowed_id = borrowed_qs.first().id
    
    context = {
        'book': book,
        'available_copies': available_copies,
        'user_borrowed_books': user_borrowed_books,
        'borrowed_id': borrowed_id,
    }
    
    return render(request, 'book_details.html', context)


@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'✏️ Book Updated: "{book.title}" by {book.author} has been successfully updated in the library.')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book_title = book.title
        book_author = book.author
        book.delete()
        messages.success(request, f'🗑️ Book Removed: "{book_title}" by {book_author} has been successfully removed from the library.')
        return redirect('book_list')
    return render(request, 'confirm_delete.html', {'book': book})


def about(request):
    return render(request, 'Aboutus.html')


# views.py

@login_required
def borrowed_books(request):

    # Prevent admins from accessing borrowed books page
    if request.user.is_superuser:
        messages.warning(request, '📚 Admin Access: This page is for regular users only. Admins manage the library, not borrow books.')
        return redirect('book_list')
    
    borrowed_books = BorrowedBook.objects.filter(user=request.user, returned=False)
    
    # Add a message if user has no borrowed books
    if not borrowed_books.exists():
        messages.info(request, f'📖 No Books Borrowed: You haven\'t borrowed any books yet. Browse our collection and start your reading journey!')
    
    return render(request, 'borrowed_books.html', {'borrowed_books': borrowed_books})


@login_required
def return_book(request, borrowed_id):
    # Prevent admins from returning books
    if request.user.is_superuser:
        msg = '🔒 Admin Restriction: Only regular users can borrow and return books.'
        messages.warning(request, msg)
        return redirect('book_list')
    
    if request.method == 'POST':
        borrowed_book = get_object_or_404(BorrowedBook, id=borrowed_id, user=request.user)
        book_title = borrowed_book.book.title
        borrowed_book.returned = True
        borrowed_book.save()
        
        # Update book availability in book list
        book = borrowed_book.book
        active_borrows = book.borrowedbook_set.filter(returned=False).count()
        if active_borrows < book.quantity:
            book.save()  # Trigger update of book status
        
        # Calculate remaining borrowed books
        remaining_books = BorrowedBook.objects.filter(user=request.user, returned=False).count()
        msg = f'📖 Book Returned: "{book_title}" has been successfully returned to the library. You now have {remaining_books} book(s) in your collection.'
        messages.success(request, msg)
        
    return redirect('borrowed_books')


@login_required
def borrow_book(request, book_id):
    # Prevent admins from borrowing books
    if request.user.is_superuser:
        messages.warning(request, '👨‍💼 Admin Notice: Library administrators cannot borrow books. Please use a regular user account for borrowing.')
        return redirect('book_list')
    
    book = get_object_or_404(Book, id=book_id)
    
    # Check if the user has reached their borrowing limit
    current_borrowed_count = BorrowedBook.objects.filter(user=request.user, returned=False).count()
    if current_borrowed_count >= request.user.max_books:
        messages.warning(request, f'📖 Borrowing Limit Reached: You have borrowed {current_borrowed_count} out of {request.user.max_books} allowed books. Please return some books before borrowing more.')
        return redirect('book_list')
    
    # Check if the book has available copies
    active_borrows = book.borrowedbook_set.filter(returned=False).count()
    if active_borrows >= book.quantity:
        messages.info(request, f'📚 Currently Unavailable: "{book.title}" is currently checked out by {active_borrows} reader(s). Please check back later or browse other available books.')
        return redirect('book_list')

    # Check if the book is already borrowed by the user
    if BorrowedBook.objects.filter(user=request.user, book=book, returned=False).exists():
        messages.info(request, f'📖 Already in Your Collection: You have already borrowed "{book.title}". Check your borrowed books to manage your current reads.')
        return redirect('borrowed_books')

    # Create a BorrowedBook entry for the user
    BorrowedBook.objects.create(user=request.user, book=book)
    
    # Update borrowed count
    new_borrowed_count = BorrowedBook.objects.filter(user=request.user, returned=False).count()
    messages.success(request, f'🎉 Successfully Borrowed: "{book.title}" has been added to your collection! You now have {new_borrowed_count} out of {request.user.max_books} books borrowed.')

    return redirect('borrowed_books')
