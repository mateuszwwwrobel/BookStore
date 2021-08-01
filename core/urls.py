from django.urls import path, include
from core import views
from rest_framework import routers
from rest_framework.schemas import get_schema_view


schema_view = get_schema_view(title='Test API')

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'author', views.AuthorViewSet)


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add-book', views.AddBookView.as_view(), name='add-book'),
    path('find-book', views.FindBookView.as_view(), name='find-book'),
    path('import-book', views.ImportBookView.as_view(), name='import-book'),

    path('api/', include(router.urls)),

]
