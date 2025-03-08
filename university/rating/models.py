from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Module(models.Model):
    code = models.CharField(max_length=10,
                            primary_key=True,
                            help_text="Module Code (eg COMP1)")
    name = models.CharField(max_length=100,
                            help_text="eg, Web services...")

class Professor(models.Model):
    id = models.CharField(max_length=10,
                          primary_key=True,
                          help_text="Professor ID (eg, JE1)")
    name = models.CharField(max_length=100,
                            help_text="Professor's full name, eg John Smith")

    def get_average_rating(self):
        ratings = Rating.objects.filter(professor=self)

        if not ratings.exists():
            return 0

        total = sum(r.rating for r in ratings)
        count = ratings.count()
        avg = total / count

        return round(avg)

    def get_module_average_rating(self, moduleCode):
        module = Module.objects.get(code=moduleCode)

        ratings = Rating.objects.filter(professor=self,
                                        moduleInstance__module=module)

        if not ratings.exists():
            return 0

        total = sum(r.rating for r in ratings)
        count = ratings.count()
        avg = total / count

        return round(avg)


class ModuleInstance(models.Model):
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name='instances')
    year = models.IntegerField(help_text="eg 2018 for 2018-2019")
    semester = models.IntegerField(help_text="Semester: 1 or 2",
                                   validators=[MinValueValidator(1),
                                               MaxValueValidator(2)])
    professors = models.ManyToManyField(Professor,
                                        related_name='moduleInstance',
                                        help_text="Professor(s) teaching this module")

    class Meta:
        unique_together = ('module', 'year', 'semester')

    def __str__(self):
        return f"{self.module.code} ({self.year}, Semester {self.semester})"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moduleInstance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5"
    )
    dateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'moduleInstance', 'professor')







