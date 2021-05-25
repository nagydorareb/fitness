from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.http import require_POST
from .models import Workout, MainExerciseSet, ExerciseSet, SimpleExerciseSet, Exercise 
from .forms import (
    SetForm, 
    WorkoutForm, 
    SetUpdateForm, 
    OrderingForm, 
    SimpleSetForm, 
    SimpleSetUpdateForm
)
from django.views.generic import (
    CreateView, 
    UpdateView, 
    DeleteView,
)
from django.views import View
from django.http import (
    HttpResponse,
    HttpResponseForbidden, 
    HttpResponseRedirect, 
    JsonResponse,
)
from .helpers import WorkoutCalendar
import datetime
from .filter import WorkoutDateFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db import transaction

def home(request):
    """ 
    Shows index page
    
    Shows created/followed workouts if user is logged in
    """
    template_data = {}
    user = request.user
    if request.user.is_authenticated:
        date_filter = WorkoutDateFilter(request.GET, queryset=Workout.objects.filter(Q(user=request.user) | Q(plan_user=request.user)))

        workout_list = date_filter.qs
        paginator = Paginator(workout_list, 7)
        page = request.GET.get('page', 1)
        try:
            workouts = paginator.page(page)
        except PageNotAnInteger:
            workouts = paginator.page(1)
        except EmptyPage:
            workouts = paginator.page(paginator.num_pages)
            
        template_data['date_filter'] = date_filter
        template_data['user'] = user
        template_data['paginator'] = paginator
        template_data['workouts'] = workouts 

        return render(request, 'base/home.html', template_data)
    else:
        return render(request, 'base/index.html')

@login_required
def view(request, pk):
    """
    Detail view for workouts
    """
    template_data = {}
    workout = get_object_or_404(Workout, pk=pk)
    exercise = ExerciseSet.objects.filter(workout_id=pk)
    simple_exercise = SimpleExerciseSet.objects.filter(workout_id=pk)
    fav = bool
    user_follows_plan = bool

    if workout.favorites.filter(id=request.user.id).exists():
        fav = True

    if workout.plan_user.filter(id=request.user.id).exists():
        user_follows_plan = True

    template_data['workout'] = workout
    template_data['exercises'] = exercise
    template_data['simple_exercises'] = simple_exercise
    template_data['fav'] = fav
    template_data['user_follows_plan'] = user_follows_plan
    
    return render(request, 'base/detail.html', template_data)

@login_required
def fav_add(request, pk):
    """
    Add workout to favorites / remove from favorites
    """
    workout = get_object_or_404(Workout, pk=pk)
    if workout.favorites.filter(id=request.user.id).exists():
        workout.favorites.remove(request.user)
        messages.success(request, f'{workout.title} has been removed from favorites')
    else:
        workout.favorites.add(request.user)
        messages.success(request, f'{workout.title} has been added to favorites')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def workout_favorites(request):
    """
    View for the user's favorite workouts
    """
    workouts = Workout.objects.filter(favorites=request.user)
    return render(request, 'base/favorites.html', {'workouts': workouts})

@require_POST
def save_new_ordering(request, pk):
    """
    Order the exercises inside a workout
    """
    form = OrderingForm(request.POST)
    if form.is_valid():
        ordered_ids = form.cleaned_data["ordering"].split(',')

        with transaction.atomic():
            current_order = 1
            for id in ordered_ids:
                exerciseset = MainExerciseSet.objects.get(id__exact=id)
                exerciseset.order = current_order
                exerciseset.save()
                current_order += 1

    return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': pk}))

@login_required
def workout_calendar(request, year=None, month=None):
    """
    Monthly calendar view of workouts created or followed by user
    """
    template_data = {}

    year = int(year) if year else datetime.date.today().year
    month = int(month) if month else datetime.date.today().month
    prev_month = int(month - 1)
    next_month = int(month + 1)
    workouts = Workout.objects.filter(Q(user=request.user, workout_day__year=year, workout_day__month=month) | 
                                        Q(workout_day__year=year, workout_day__month=month, plan_user=request.user))
    cal = WorkoutCalendar(workouts).formatmonth(year, month)

    template_data['current_year'] = year
    template_data['current_month'] = month
    template_data['prev_month'] = prev_month
    template_data['next_month'] = next_month
    template_data['cal'] = cal
    template_data['workouts'] = workouts

    return render(request, 'base/workout_calendar.html', template_data) 

class WorkoutAddView(LoginRequiredMixin, CreateView):
    """ 
    View to create workout
    """
    model = Workout
    form_class = WorkoutForm

    def form_valid(self, form):
        """
        Set the user this workout belongs to
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update an existing workout
    """
    model = Workout
    form_class = WorkoutForm
    template_name = 'base/workout_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False

class WorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Deletes the given workout
    """
    model = Workout
    fields = ['title']
    success_url = '/'

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False

@login_required
def add_exercise(request, workout_pk, exercise_pk=None):
    """ 
    Adds exercise to given workout

    Exercises can be added from the Exercise Bank or with the help of Select2
    Different forms for normal sets (e.g. HIIT, Strength) and simple sets (e.g. Yoga, Pilates)
    """
    template_data = {}

    workout = get_object_or_404(Workout, pk=workout_pk)

    if exercise_pk == None:
        if request.is_ajax():
            term = request.GET.get('term')
            exercises = Exercise.objects.all().filter(name__icontains=term)
            response_content = list(exercises.values())
            return JsonResponse(response_content, safe=False)

        if request.method == 'POST':
            if workout.is_simple_workout():
                set_form = SimpleSetForm(request.POST)
            else:
                set_form  = SetForm(request.POST)

            if set_form.is_valid():
                workout_set = set_form.save(commit=False)
                workout_set.workout_id = workout_pk
                workout_set.save()

                messages.success(request, f'The exercise has been added to the workout')
                return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))
        else:
            if workout.is_simple_workout():
                set_form = SimpleSetForm()
            else:
                set_form  = SetForm()
    else:
        exercise = get_object_or_404(Exercise, pk=exercise_pk)
        if request.method == 'POST':
            if workout.is_simple_workout():
                set_form = SimpleSetForm(request.POST)
            else:
                set_form  = SetForm(request.POST)

            if set_form.is_valid():
                workout_set = set_form.save(commit=False)
                workout_set.workout_id = workout_pk
                workout_set.save()

                messages.success(request, f'The exercise has been added to the workout')
                return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))
        else:
            if workout.is_simple_workout():
                set_form = SimpleSetForm(initial={'exercise': exercise }, instance=workout)
            else:
                set_form  = SetForm(initial={'exercise': exercise }, instance=workout)

    template_data['workout'] = workout
    template_data['set_form'] = set_form

    return render(request, 'base/addexercise.html', template_data)

@login_required
def exercise_set_update(request, workout_pk, exercise_set_pk):
    """
    View to edit workout sets
    """
    workout = get_object_or_404(Workout, pk=workout_pk)
    if workout.is_simple_workout():
        exercise_set = get_object_or_404(SimpleExerciseSet, pk=exercise_set_pk)
    else:
        exercise_set = get_object_or_404(ExerciseSet, pk=exercise_set_pk)

    if request.is_ajax():
        term = request.GET.get('term')
        exercises = Exercise.objects.all().filter(name__icontains=term)
        response_content = list(exercises.values())
        return JsonResponse(response_content, safe=False)

    if request.method == 'POST':
        if workout.is_simple_workout():
            u_form = SimpleSetUpdateForm(request.POST, instance=exercise_set)
        else:
            u_form = SetUpdateForm(request.POST, instance=exercise_set)

        if u_form.is_valid():
            u_form.save()
            return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))
    else:
        if workout.is_simple_workout():
            u_form = SimpleSetUpdateForm(instance=exercise_set)
        else:
            u_form = SetUpdateForm(instance=exercise_set)

    template_data = {
        'u_form' : u_form,
        'workout' : workout,
        'exercise_set': exercise_set
    }

    return render(request, 'base/exercise_edit.html', template_data)

@login_required
def exercise_set_delete(request, workout_pk, exercise_set_pk):
    """
    View to delete workout sets
    """
    workout = get_object_or_404(Workout, pk=workout_pk)
    if workout.is_simple_workout():
        exercise_set = get_object_or_404(SimpleExerciseSet, pk=exercise_set_pk)
    else:
        exercise_set = get_object_or_404(ExerciseSet, pk=exercise_set_pk)
  
    if request.method =="POST":
        exercise_set.delete()
        return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))

    template_data = {
        'exercise_set' : exercise_set,
        'workout' : workout
    }
  
    return render(request, "base/exercise_set_confirm_delete.html", template_data)