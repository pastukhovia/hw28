from django.urls import path
from .views import CatListView, CatDetailView, CatCreateView, CatUpdateView, CatDeleteView

urlpatterns = [
    path('', CatListView.as_view()),
    path('<int:pk>/', CatDetailView.as_view()),
    path('create/', CatCreateView.as_view()),
    path('<int:pk>/update/', CatUpdateView.as_view()),
    path('<int:pk>/delete/', CatDeleteView.as_view()),
]
