from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Professor, Module, ModuleInstance, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('id', 'name')

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('code', 'name')

class ModuleInstanceSerializer(serializers.ModelSerializer):
    moduleCode = serializers.CharField(source='module.code')
    moduleName = serializers.CharField(source='module.name')
    professors = ProfessorSerializer(many=True, read_only=True)
    
    class Meta:
        model = ModuleInstance
        fields = ('moduleCode',
                  'moduleName',
                  'year',
                  'semester',
                  'professors')
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id',
                  'user',
                  'moduleInstance',
                  'professor',
                  'rating',
                  'dateCreated')
        readOnlyFields = ('user', 'dateCreated')

    def create(self, dataValidation):
        dataValidation['user'] = self.context['request'].user
        return super().create(dataValidation)
    
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, dataValidation):
        user = User.objects.create_user(
            username=dataValidation['username'],
            email=dataValidation['email'],
            password=dataValidation['password']
        )
        return user
    
class ProfessorRatingSerializer(serializers.ModelSerializer):
    averageRating = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ('id', 'name', 'averageRating')

    def getAverageRating(self, object):
        return object.getAverageRating()
    
class ProfessorModuleRatingSerializer(serializers.ModelSerializer):
    moduleRating = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ('id', 'name', 'moduleRating')

    def getModuleRating(self, object):
        moduleCode = self.context.get('moduleCode')
        if moduleCode:
            return object.getModuleAverageRating(moduleCode)
        return 0
    

    
