from django.db import models
from PIL import Image
from django.utils import timezone

class WorkoutPlan(models.Model):
    BEGINNER = 'BE'
    INTERMEDIATE = 'IN'
    ADVANCED = 'AD'
    DIFFICULTY = [
        (BEGINNER, 'Beginner'), 
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]

    TWO_WEEKS = '2W'
    FOUR_WEEKS = '4W'
    EIGHT_WEEKS = '8W'
    PLANLENGTH = [
        (TWO_WEEKS, '2'), 
        (FOUR_WEEKS, '4'),
        (EIGHT_WEEKS, '8'),
    ]

    THREE_DAYS = '3D'
    FOUR_DAYS = '4D'
    FIVE_DAYS = '5D'
    DAYSPERWEEK = [
        (THREE_DAYS, '3 Days'), 
        (FOUR_DAYS, '4 Days'),
        (FIVE_DAYS, '5 Days'),
    ]

    THIRTY_MIN = '30'
    FOURTYFIVE_MIN = '45'
    SIXTY_MIN = '60'
    TIMEPERWORKOUT = [
        (THREE_DAYS, '30 Min'), 
        (FOUR_DAYS, '45 Min'),
        (FIVE_DAYS, '60 Min'),
    ]

    NO_EQ = 'NE'
    DUMBBELL = 'DB'
    GYM = 'GM'
    EQUIPMENT = [
        (NO_EQ, 'No equipment'), 
        (DUMBBELL, 'Dumbbell'),
        (GYM, 'Gym'),
    ]

    LOSE_FAT = 'NE'
    BUILD_MUSCLE = 'DB'
    GET_FIT = 'GM'
    MAINGOAL = [
        (LOSE_FAT, 'Lose Fat'), 
        (BUILD_MUSCLE, 'Build Muscle'),
        (GET_FIT, 'Get Fit'),
    ]
    title = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=100, choices = DIFFICULTY)
    plan_length = models.CharField(max_length=100, choices = PLANLENGTH)
    days_per_week = models.CharField(max_length=100, choices = DAYSPERWEEK)
    time_per_workout = models.CharField(max_length=100, choices = TIMEPERWORKOUT)
    equipment = models.CharField(max_length=100, choices = EQUIPMENT)
    main_goal = models.CharField(max_length=100, choices = MAINGOAL)
    image = models.ImageField(default='default_exercise.jpg', upload_to='program_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    class Meta:
        ordering = ["-date_posted", ]