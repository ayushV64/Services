from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import studentViewSet, book_detail, userView

router = DefaultRouter()
router.register('students', studentViewSet, basename='student')

urlpatterns = [
    # path('student/', views.student_list, name='student'),
    # path('student/create/', views.postStudent, name='student_create'), 
    path('student-details/', views.student_details_list, name='student-details-list'),
    path('books/', book_detail.as_view(), name='book-list'),
    path('books/<int:pk>/', book_detail.as_view(), name='book-detail'),                                                                         
    path('create-user/', userView.as_view(), name='user-create'),                                                                        
    path('create-user/<int:id>/', userView.as_view(), name='user-detail'),                                                                        
    # path('student-details/<int:pk>/', views.student_detail, name='student-detail'),
]

urlpatterns += router.urls