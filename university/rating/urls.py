from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'module-instances', views.ModuleInstanceViewset)
router.register(r'professor-ratings', views.ProfessorRatingViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('professor-module-rating/<str:professorID>/<str:moduleCode>/',
         views.professorModuleRating, name='professor-module-rating'),
    path('rate-professor/', views.rateProfessor, name='rate-professor'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', auth_views.obtain_auth_token, name='api-token-auth')
]