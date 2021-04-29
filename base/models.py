from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from workouts.models import WorkoutPlan

class Workout(models.Model):
    HIIT = 'HI'
    STRENGTH = 'ST'
    YOGA = 'YO'
    CARDIO = 'CA'

    TRAINING = [
        (HIIT, 'HIIT'),
        (STRENGTH, 'Strength Training'),
        (YOGA, 'Yoga'),
        (CARDIO, 'Cardio'),
    ]

    UPPER = 'UP'
    LOWER = 'LW'
    CORE = 'CR'
    TOTAL = 'TL'

    BODYFOCUS = [
        (UPPER, 'Upper Body'), 
        (LOWER, 'Lower Body'),
        (CORE, 'Core'),
        (TOTAL, 'Total Body'),
    ]

    title = models.CharField(max_length=100)
    workout_day = models.DateField(default=date.today)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    training_type = models.CharField(max_length=100, choices = TRAINING)
    body_focus = models.CharField(max_length=100, choices = BODYFOCUS)

    workout_plan = models.ManyToManyField(WorkoutPlan, blank=True)
    plan_week = models.PositiveIntegerField(blank=True, null=True)
    plan_day = models.PositiveIntegerField(blank=True, null=True)
    plan_user = models.ManyToManyField(User, related_name="workouts", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('workout_detail', kwargs={'pk': self.pk})

    def get_owner_object(self):
        return self

    class Meta:
        ordering = ["-workout_day", ]

class Exercise(models.Model):
    ARMS = 'AR'
    LEGS = 'LG'
    CORE = 'CR'
    BACK = 'BK'
    CHEST = 'CH'
    SHOULDERS = 'SH'
    FULLBODY = 'FB'
    CARDIO = 'CA'
    YOGAPOSE = 'YP'

    FOCUS = [
        (ARMS, 'Arms'),
        (LEGS, 'Legs'),
        (CORE, 'Core'),
        (BACK, 'Back'),
        (CHEST, 'Chest'),
        (SHOULDERS, 'Shoulders'),
        (FULLBODY, 'Full Body'),
        (CARDIO, 'Cardio'),
        (YOGAPOSE, 'Yoga Pose'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default_exercise.jpg', upload_to='exercise_pics', blank=True)
    description = models.TextField(blank=True)
    focus = models.CharField(max_length = 2, choices = FOCUS)

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
        
class ExerciseSet(models.Model):
    REP = 'RE'
    SEC = 'SE'
    KG = 'KG'
    BODYWEIGHT = 'BW'

    REP_OR_SEC = [
        (REP, 'rep(s)'),
        (SEC, 'sec(s)'),
    ]
    KG_OR_BW = [
        (KG, 'kg'),
        (BODYWEIGHT, 'bodyweight'),
    ]

    DEFAULT_SETS = 4
    MAX_SETS = 10

    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    set_num = models.PositiveIntegerField(default=DEFAULT_SETS, verbose_name="Number of sets")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    rep_num = models.IntegerField(verbose_name="Repetitions")
    rep_type = models.CharField(max_length = 2, choices = REP_OR_SEC, default=REP, verbose_name="Unit") # repetitions or seconds
    weight_num = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Weight")
    weight_type = models.CharField(max_length = 2, choices = KG_OR_BW, default=KG, verbose_name="Unit")

    def __str__(self):
        return f"{self.exercise.name}: {self.set_num} set(s) of {self.rep_num} {self.get_rep_type_display()} {self.weight_num} {self.get_weight_type_display()}"

    def get_absolute_url(self):
        return reverse('exercise_set_detail', kwargs={'pk': self.pk})