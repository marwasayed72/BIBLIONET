from django.contrib.auth.models import AbstractUser
from django.db import models
# models.py
from django.db import models

# models.py
class Book(models.Model):
    CATEGORY_CHOICES = [
   
    ('novel', 'Novel'),
    ('classic', 'Classic Literature'),
    ('drama', 'Drama'),
    ('short_stories', 'Short Stories'),
    ('satire', 'Satire'),
    ('horror', 'Horror'),
    ('thriller', 'Thriller'),
    ('adventure', 'Adventure'),

    ('science', 'Science'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry'),
    ('biology', 'Biology'),
    ('mathematics', 'Mathematics'),
    ('astronomy', 'Astronomy'),
    ('geography', 'Geography'),
    ('environment', 'Environmental Studies'),

    ('self_help', 'Self Help'),
    ('productivity', 'Productivity'),
    ('psychology', 'Psychology'),
    ('motivation', 'Motivation'),
    ('leadership', 'Leadership'),
    ('time_management', 'Time Management'),

    ('history', 'History'),
    ('world_history', 'World History'),
    ('ancient_civilizations', 'Ancient Civilizations'),
    ('war_history', 'Military & War History'),

    ('politics', 'Politics'),
    ('sociology', 'Sociology'),
    ('anthropology', 'Anthropology'),
    ('gender_studies', 'Gender Studies'),
    ('human_rights', 'Human Rights'),

    ('religion', 'Religion & Spirituality'),
    ('islamic', 'Islamic Studies'),
    ('christian', 'Christian Studies'),
    ('comparative_religion', 'Comparative Religion'),
    ('ethics', 'Ethics'),
    ('logic', 'Logic'),

    ('children', 'Children'),
    ('young_adult', 'Young Adult'),
    ('fairy_tales', 'Fairy Tales'),
    ('activity_books', 'Activity Books'),
    ('educational_kids', 'Educational for Kids'),

    ('biography', 'Biography'),
    ('memoir', 'Memoirs'),

    ('business', 'Business'),
    ('marketing', 'Marketing'),
    ('finance', 'Finance'),
    ('entrepreneurship', 'Entrepreneurship'),
    ('economics', 'Economics'),
    ('investment', 'Investment'),

    ('art', 'Art'),
    ('cinema', 'Film & Cinema'),
    ('music', 'Music'),
    ('design', 'Graphic Design'),
    ('photography', 'Photography'),
    ('fashion', 'Fashion'),

    ('language_learning', 'Language Learning'),
    ('english_lit', 'English Literature'),
    ('arabic_lit', 'Arabic Literature'),
    ('translation', 'Translation Studies'),

    ('travel', 'Travel Guides'),
    ('cookbook', 'Cooking & Recipes'),
    ('gardening', 'Gardening'),
    ('home_improvement', 'Home Improvement'),
    ('technology', 'Technology'),
    ('legal', 'Law & Legal Studies'),

    ('others', 'Others'),
]


    

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    image = models.URLField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    max_books = models.IntegerField(default=5, help_text='Maximum number of books the user can borrow at once')
    
    # Override email field to make it unique
    email = models.EmailField(unique=True)



class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username}"