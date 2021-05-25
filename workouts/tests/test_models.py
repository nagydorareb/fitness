from django.test import TestCase, Client
from django.contrib.auth.models import User
from base.models import Workout
from workouts.models import WorkoutPlan
from django.urls import reverse

class WorkoutModelTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='Jelszo123', email='test@example.com')
        self.admin.save()
        self.workout1 = Workout.objects.create(title='Test Workout 1',
                                                training_type=Workout.TrainingType.STRENGTH,
                                                body_focus=Workout.BodyFocus.LOWER_BODY,
                                                public=True,
                                                user=self.admin, )
        self.workout1.save()

        self.workout2 = Workout.objects.create(title='Test Workout 2',
                                                training_type=Workout.TrainingType.YOGA,
                                                body_focus=Workout.BodyFocus.CORE,
                                                public=True,
                                                user=self.admin, )
        self.workout2.save()

        self.workout3 = Workout.objects.create(title='Test Workout 3',
                                                training_type=Workout.TrainingType.HIIT,
                                                body_focus=Workout.BodyFocus.TOTAL_BODY,
                                                public=True,
                                                user=self.admin, )
        self.workout3.save()

    def test_created_properly(self):
        self.assertEqual(WorkoutPlan.objects.count(), 0)
        self.workout_plan1 = WorkoutPlan.objects.create(title='Test Workout Plan 1',
                                                        difficulty=WorkoutPlan.BEGINNER,
                                                        plan_length=WorkoutPlan.TWO_WEEKS,
                                                        days_per_week=WorkoutPlan.THREE_DAYS,
                                                        time_per_workout=WorkoutPlan.SIXTY_MIN,
                                                        equipment=WorkoutPlan.DUMBBELL,
                                                        main_goal=WorkoutPlan.LOSE_FAT, )
        self.workout3.save()
        self.assertEqual(WorkoutPlan.objects.count(), 1)

        self.assertEqual(self.workout_plan1.title, 'Test Workout Plan 1')

        self.plan_workout1 = Workout.objects.get(title='Test Workout 1')
        self.plan_workout1.workout_plan = self.workout_plan1
        self.plan_week = 1
        self.plan_day = 1
        self.plan_workout1.save()

        self.assertEqual(self.plan_workout1.workout_plan.id, self.workout_plan1.id)