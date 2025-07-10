document.addEventListener("DOMContentLoaded", function() {
    // Function to show styled messages
    window.showMessage = function(message, type) {
        const messagesContainer = document.querySelector('.messages');
        if (!messagesContainer) {
            const newContainer = document.createElement('div');
            newContainer.className = 'messages';
            document.querySelector('header').after(newContainer);
        }
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="close-btn" onclick="this.parentElement.style.display='none';">&times;</button>
        `;
        
        document.querySelector('.messages').appendChild(alert);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    };

    // Get the book ID from localStorage
    const bookId = localStorage.getItem('selectedBookId');
    const books = JSON.parse(localStorage.getItem('books')) || [];
    const book = books.find(b => b.id === bookId);

    // Get DOM elements
    const bookImage = document.getElementById('bookImage');
    const bookTitle = document.getElementById('bookTitle');
    const bookAuthor = document.getElementById('bookAuthor');
    const bookGenre = document.getElementById('bookGenre');
    const bookDescription = document.getElementById('bookDescription');
    const borrowBtn = document.querySelector('.borrow-btn');
    const backBtn = document.querySelector('.back-btn');
    const adminControls = document.getElementById('adminControls');
    const editBtn = document.querySelector('.edit-btn');
    const deleteBtn = document.querySelector('.delete-btn');

    // Check if user is admin (you need to implement your own logic)
    const isAdmin = localStorage.getItem('isAdmin') === 'true';

    if (book) {
        // Display book details
        bookImage.src = book.image || 'default-book.jpg';
        bookImage.onerror = function() {
            this.src = 'default-book.jpg';
        };
        bookTitle.textContent = book.title;
        bookAuthor.textContent = book.author;
        bookGenre.textContent = book.category;
        bookDescription.textContent = book.description;

        // Show admin controls if user is admin
        adminControls.style.display = isAdmin ? 'block' : 'none';

        // Borrow button event
        borrowBtn.addEventListener('click', function() {
            let borrowedBooks = JSON.parse(localStorage.getItem('borrowedBooks')) || [];

            // Check if book is already borrowed
            if (borrowedBooks.some(b => b.id === book.id)) {
                showMessage('You have already borrowed this book!', 'info');
                return;
            }

            borrowedBooks.push(book);
            localStorage.setItem('borrowedBooks', JSON.stringify(borrowedBooks));
            showMessage(`"${book.title}" has been added to your borrowed books.`, 'success');
        });

        // Back button event
        backBtn.addEventListener('click', function() {
            window.location.href = 'BookList.html';
        });

        // Edit button event (for admin)
        editBtn.addEventListener('click', function() {
            localStorage.setItem('editBookId', book.id);
            window.location.href = 'admin_dashboard.html';
        });

        // Delete button event (for admin)
        deleteBtn.addEventListener('click', function() {
            if (confirm(`Are you sure you want to delete "${book.title}"?`)) {
                const updatedBooks = books.filter(b => b.id !== book.id);
                localStorage.setItem('books', JSON.stringify(updatedBooks));

                // Also remove from borrowed books if exists
                let borrowedBooks = JSON.parse(localStorage.getItem('borrowedBooks')) || [];
                borrowedBooks = borrowedBooks.filter(b => b.id !== book.id);
                localStorage.setItem('borrowedBooks', JSON.stringify(borrowedBooks));

                showMessage('Book deleted successfully!', 'success');
                window.location.href = 'BookList.html';
            }
        });
    } else {
        // If book not found, redirect to book list
        showMessage('Book not found!', 'error');
        window.location.href = 'BookList.html';
    }
});