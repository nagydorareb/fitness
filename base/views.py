from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workout, ExerciseSet, Exercise
from django.contrib.auth.models import User
from django.views.generic import ( 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.http import (
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SetForm, WorkoutForm, SetUpdateForm
from django.urls import reverse
from django.contrib import messages

import calendar
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse

from .helpers import WorkoutCalendar

from django.views.generic.edit import FormView
import datetime
from .filter import WorkoutDateFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def index(request):
    return render(request, 'base/index.html')

@login_required
def home(request):
    template_data = {}
    user = request.user
    date_filter = WorkoutDateFilter(request.GET, queryset=Workout.objects.filter(Q(user=request.user) | Q(plan_user=request.user)))
    template_data['date_filter'] = date_filter
    template_data['user'] = user

    workout_list = date_filter.qs
    paginator = Paginator(workout_list, 6)
    page = request.GET.get('page', 1)
    
    try:
        workouts = paginator.page(page)
    except PageNotAnInteger:
        workouts = paginator.page(1)
    except EmptyPage:
        workouts = paginator.page(paginator.num_pages)
        
    template_data['paginator'] = paginator
    template_data['workouts'] = workouts
    
    return render(request, 'base/home.html', template_data)

@login_required
def view(request, pk):
    template_data = {}
    workout = get_object_or_404(Workout, pk=pk)
    exercise = ExerciseSet.objects.filter(workout_id=pk)
    template_data['workout'] = workout
    template_data['exercises'] = exercise
    
    return render(request, 'base/detail.html', template_data)

@login_required
def workout_calendar(request, year=None, month=None):
    template_data = {}

    year = int(year) if year else datetime.date.today().year
    month = int(month) if month else datetime.date.today().month
    prev_month = int(month - 1)
    next_month = int(month + 1)

    # workouts = Workout.objects.filter(user=request.user, workout_day__year=year, workout_day__month=month, plan_user=request.user)

    workouts = Workout.objects.filter(Q(user=request.user, workout_day__year=year, workout_day__month=month) | Q(workout_day__year=year, workout_day__month=month, plan_user=request.user))
    
    cal = WorkoutCalendar(workouts).formatmonth(year, month)

    template_data['current_year'] = year
    template_data['current_month'] = month
    template_data['prev_month'] = prev_month
    template_data['next_month'] = next_month
    template_data['cal'] = cal
    template_data['workouts'] = workouts

    return render(request, 'base/workout_calendar.html', template_data) 

class WorkoutAddView(LoginRequiredMixin, CreateView):
    model = Workout
    form_class = WorkoutForm

    def form_valid(self, form):
        form.save()
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
    model = Workout
    fields = ['title']
    success_url = '/workout'

    def test_func(self):
        workout = self.get_object()
        if self.request.user == workout.user:
            return True
        return False

@login_required
def add_exercise(request, workout_pk, exercise_pk=None):
    template_data = {}

    workout = get_object_or_404(Workout, pk=workout_pk)
    """ if workout.get_owner_object().user != request.user:
        return HttpResponseForbidden() """

    # If exercise is added from Exercise Bank
    if exercise_pk == None:
        template_data['empty'] = False
        if request.is_ajax():
            term = request.GET.get('term')
            exercises = Exercise.objects.all().filter(name__icontains=term)
            response_content = list(exercises.values())
            return JsonResponse(response_content, safe=False)

        if request.method == 'POST':
            set_form  = SetForm(request.POST)
            if set_form.is_valid():
                workout_set = set_form.save(commit=False)
                workout_set.workout_id = workout_pk
                workout_set.save()

                messages.success(request, f'The exercise has been added to the workout')
                return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))
        else:
            set_form  = SetForm(instance=workout)
    else:
        template_data['empty'] = True
        exercise = get_object_or_404(Exercise, pk=exercise_pk)
        if request.method == 'POST':
            set_form  = SetForm(request.POST)
            if set_form.is_valid():
                workout_set = set_form.save(commit=False)
                workout_set.workout_id = workout_pk
                print(workout_set.exercise_id)
                workout_set.save()

                messages.success(request, f'The exercise has been added to the workout')
                return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))
        else:
            set_form  = SetForm(initial={'exercise': exercise }, instance=workout)

    template_data['workout'] = workout
    template_data['set_form'] = set_form

    return render(request, 'base/addexercise.html', template_data)

@login_required
def exercise_set_view(request, workout_pk, pk):
    template_data = {}
    exercise_set = get_object_or_404(ExerciseSet, pk=pk)
    template_data['exercise_set'] = exercise_set

    return render(request, 'base/exercise_set_detail.html', template_data)

@login_required
def exercise_set_update(request, workout_pk, pk):
    workout = get_object_or_404(Workout, pk=workout_pk)
    exercise_set = get_object_or_404(ExerciseSet, pk=pk)

    if request.is_ajax():
        term = request.GET.get('term')
        exercises = Exercise.objects.all().filter(name__icontains=term)
        response_content = list(exercises.values())
        return JsonResponse(response_content, safe=False)

    if request.method == 'POST':
        u_form = SetUpdateForm(request.POST, instance=exercise_set)
        if u_form.is_valid():
            u_form.save()
            return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))
    else:
        u_form = SetUpdateForm(instance=exercise_set)

    context = {
        'u_form' : u_form,
        'workout' : workout,
        'exercise_set': exercise_set
    }

    return render(request, 'base/exercise_edit.html', context)

@login_required
def exercise_set_delete(request, workout_pk, pk):
    workout = get_object_or_404(Workout, pk=workout_pk)
    exercise_set = get_object_or_404(ExerciseSet, pk=pk)
  
    if request.method =="POST":
        exercise_set.delete()
        return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))

    context = {
        'exercise_set' : exercise_set,
        'workout' : workout
    }
  
    return render(request, "base/exercise_set_confirm_delete.html", context)