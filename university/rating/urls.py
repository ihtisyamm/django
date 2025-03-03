from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'module-instances', views.ModuleInstanceViewset)
router.register(r'professor-ratings', views.ProfessorRatingViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('professor-module-rating/<str:professor_id>/<str:module_code>/', 
         views.professorModuleRating, name='professor-module-rating'),
    path('rate-professor/', views.rateProfessor, name='rate-professor'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]