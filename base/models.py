from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from workouts.models import WorkoutPlan
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

class Workout(models.Model):

    class TrainingType(models.TextChoices):
        HIIT = 'HI', _('HIIT')
        STRENGTH = 'ST'
        YOGA = 'YO'
        CARDIO = 'CA'
        PILATES = 'PA'

    class BodyFocus(models.TextChoices):
        UPPER_BODY = 'UP'
        LOWER_BODY = 'LW'
        CORE = 'CR'
        TOTAL_BODY = 'TL'

    PUBLIC_PRIVATE = (
        (True, 'Every user can view this workout'), 
        (False, 'Only I can view this workout')
    )

    title = models.CharField(max_length=100)
    workout_day = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training_type = models.CharField(max_length=100, choices = TrainingType.choices)
    body_focus = models.CharField(max_length=100, choices = BodyFocus.choices)
    favorites = models.ManyToManyField(User, related_name='favorite', blank=True)
    public = models.BooleanField(default=True, choices=PUBLIC_PRIVATE)

    workout_plan = models.ForeignKey(WorkoutPlan, blank=True, on_delete=models.SET_NULL, null=True)
    plan_week = models.PositiveIntegerField(blank=True, null=True)
    plan_day = models.PositiveIntegerField(blank=True, null=True)
    plan_user = models.ManyToManyField(User, related_name="workouts", blank=True)

    def __str__(self):
        return f"{self.title} ({self.user}, ID_{self.id})"

    def get_absolute_url(self):
        return reverse('workout_detail', kwargs={'pk': self.pk})

    def is_simple_workout(self):
        return self.training_type in {self.TrainingType.PILATES, self.TrainingType.YOGA}

    class Meta:
        ordering = ["-workout_day", ]

class Exercise(models.Model):

    class Focus(models.TextChoices):
        ARMS = 'AR'
        LEGS = 'LG'
        CORE = 'CR'
        BACK = 'BK'
        CHEST = 'CH'
        SHOULDERS = 'SH'
        FULL_BODY = 'FB'
        CARDIO = 'CA'
        YOGA_POSE = 'YP'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_exercise.jpg', upload_to='exercise_pics', blank=True)
    description = models.TextField(blank=True)
    focus = models.CharField(max_length = 2, choices=Focus.choices)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('exercise_detail', kwargs={'pk': self.pk})

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    class Meta:
        ordering = ["name", ]

class MainExerciseSet(models.Model):
    """
    Base model for types of exercise sets (normal, simple)
    """
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField(default=100_000)

    def __str__(self):
        return f"{self.exercise.name}"

    def get_absolute_url(self):
        return reverse('workout_detail', kwargs={'pk': self.pk})

    class Meta():
        ordering = ['order',]

class SimpleExerciseSet(MainExerciseSet):
    """
    Model for simple exercise sets (e.g. Yoga, Pilates)
    """
    def __str__(self):
        return f"{self.workout.title}: {self.exercise.name}"

    class Meta():
        ordering = ['order',]
        
class ExerciseSet(MainExerciseSet):
    """
    Model for normal exercise sets (e.g. Strength, HIIT)
    """
    REP = 'RE'
    SEC = 'SE'
    MIN = 'MN'
    KM = 'KM'
    MILE = 'ML'

    KG = 'KG'
    BODYWEIGHT = 'BW'
    LBS = 'LB'

    REP_OR_SEC = [
        (REP, 'rep(s)'),
        (SEC, 'sec(s)'),
        (MIN, 'minute(s)'),
        (KM, 'km(s)'),
        (MILE, 'mile(s)'),
    ]
    KG_OR_BW = [
        (KG, 'kg'),
        (LBS, 'lbs'),
        (BODYWEIGHT, 'body weight'),
    ]

    DEFAULT_SETS = 4

    set_num = models.PositiveIntegerField(default=DEFAULT_SETS, verbose_name="Number of sets")
    rep_num = models.PositiveIntegerField(verbose_name="Repetitions")
    rep_type = models.CharField(max_length = 2, choices = REP_OR_SEC, default=REP, verbose_name="Unit")
    weight_num = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Weight", default=0, validators=[MinValueValidator(0)])
    weight_type = models.CharField(max_length = 2, choices = KG_OR_BW, default=BODYWEIGHT, verbose_name="Unit")
    rest_time = models.PositiveIntegerField(verbose_name="Rest Time", default=0)

    def __str__(self):
        return f"{self.workout.title} - {self.exercise.name}: {self.set_num} set(s) of {self.rep_num} {self.get_rep_type_display()} {self.weight_num} {self.get_weight_type_display()}"

    def get_absolute_url(self):
        return reverse('workout_detail', kwargs={'pk': self.pk})

    class Meta():
        ordering = ['order',]