from django.urls import path
from core import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add-book', views.AddBookView.as_view(), name='add-book'),
    path('find-book', views.FindBookView.as_view(), name='find-book'),
    path('import-book', views.ImportBookView.as_view(), name='import-book'),

]
