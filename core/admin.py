from django.contrib import admin
from core.models import Author, Book


@admin.register(Author)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_per_page = 25
    list_display_links = ('name', )


@admin.register(Book)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn')
    list_per_page = 25
    list_display_links = ('id', 'title')
