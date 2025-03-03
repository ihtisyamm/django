from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Professor, Module, ModuleInstance, Rating
from .serializers import (
    UserSerializer, ProfessorSerializer, ModuleSerializer,
    ModuleInstanceSerializer, RatingSerializer, RegistrationSerializer,
    ProfessorRatingSerializer, ProfessorModuleRatingSerializer
)

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

class ModuleInstanceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleInstance.objects.all().order_by('module__code',
                                                     'year',
                                                     'semester')
    serializer_class = ModuleInstanceSerializer

    def list(self, request):
        instances = self.get_queryset()
        serializer = self.get_serializer(instances, many=True)
        return Response(serializer.data)

class ProfessorRatingViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorRatingSerializer

@api_view(['GET'])
def professorModuleRating(request, professorID, moduleCode):
    professor = get_object_or_404(Professor, id=professorID)
    module = get_object_or_404(Module,code=moduleCode)

    serializer = ProfessorModuleRatingSerializer(professor,
                                                 context={'moduleCode': moduleCode})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rateProfessor(request):
    professorID = request.data.get('professorID')
    moduleCode = request.data.get('moduleCode')
    year = request.data.get('year')
    semester = request.data.get('semester')
    ratingValue = request.data.get('rating')

    if not all([professorID, moduleCode, year, semester, ratingValue]):
        return Response({"ERROR: Missing some fields"},
                        status=status.HTTP_400_BAD_REQUEST)
    
    try:
        professor = Professor.objects.get(id=professorID)
        moduel = Module.objects.get(code=moduleCode)
        moduleInstance = ModuleInstance.objects.get(module=moduel,
                                                    year=year,
                                                    semester=semester)
        
        if professor not in moduleInstance.professors.all():
            return Response({"ERROR: Wrong professor for this module"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        rating, create = Rating.objects.update_or_create(
            user=request.user,
            moduleInstance=moduleInstance,
            professor=professor,
            defaults={'rating':ratingValue})
        
        serializer = RatingSerializer(rating)
        if create:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
    except (Professor.DoesNotExist,
            Module.DoesNotExist,
            ModuleInstance.DoesNotExist) as e:
        return Response({f"ERROR: str{e}"},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({f"ERROR: str{e}"},
                        status=status.HTTP_400_BAD_REQUEST)
