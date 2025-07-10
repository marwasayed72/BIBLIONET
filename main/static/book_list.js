document.addEventListener("DOMContentLoaded", function() {
    const bookContainer = document.getElementById("bookContainer");

    // get books from localStorage
    const books = JSON.parse(localStorage.getItem('books')) || [];

    books.forEach(book => {
        const bookElement = document.createElement("div");
        bookElement.className = "book";
        bookElement.innerHTML = `
            <a href="book_details.html" data-book-id="${book.id}">
                <img src="${book.image}" alt="${book.title}" onerror="this.src='default-book.jpg'">
                <h3>${book.title}</h3>
            </a>
            <p><strong>Author:</strong> ${book.author}</p>
            <p><strong>Genre:</strong> ${book.category}</p>
            <p class="description">${book.description.substring(0, 100)}${book.description.length > 100 ? '...' : ''}</p>
        `;
        bookContainer.appendChild(bookElement);
    });

    document.querySelectorAll('.book a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const bookId = this.getAttribute('data-book-id');
            localStorage.setItem('selectedBookId', bookId);
            window.location.href = 'book_details.html';
        });
    });

    const searchForm = document.querySelector(".search-container");
    if (searchForm) {
        searchForm.addEventListener("submit", function(e) {
            e.preventDefault();
            const searchTerm = this.search.value.toLowerCase();
            const books = document.querySelectorAll(".book");

            books.forEach(book => {
                const title = book.querySelector("h3").textContent.toLowerCase();
                const author = book.querySelector("p:nth-of-type(1)").textContent.toLowerCase();
                const category = book.querySelector("p:nth-of-type(2)").textContent.toLowerCase();

                if (title.includes(searchTerm) || author.includes(searchTerm) || category.includes(searchTerm)) {
                    book.style.display = "block";
                } else {
                    book.style.display = "none";
                }
            });
        });
    }
});