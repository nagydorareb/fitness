from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workout, ExerciseSet
from django.contrib.auth.models import User
from django.views.generic import ( 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import (
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SetForm, SetUpdateForm
from django.urls import reverse
from django.contrib import messages

def index(request):
    return render(request, 'base/index.html')

@login_required
def home(request):
    template_data = {}
    workouts = Workout.objects.filter(user=request.user)
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

class WorkoutAddView(LoginRequiredMixin, CreateView):
    model = Workout
    fields = ['title', 'training_type', 'body_focus']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    fields = ['title', 'training_type', 'body_focus']
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
def add_exercise(request, workout_pk):
    workout = get_object_or_404(Workout, pk=workout_pk)
    if workout.get_owner_object().user != request.user:
        return HttpResponseForbidden()

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

    context = {
        'workout' : workout,
        'set_form' : set_form
    }

    return render(request, 'base/addexercise.html', context)

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
    if request.method == 'POST':
        u_form = SetUpdateForm(request.POST, instance=exercise_set)
        if u_form.is_valid():
            u_form.save()
            return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.id}))
    else:
        u_form = SetUpdateForm(instance=exercise_set)

    context = {
        'u_form' : u_form,
        'workout' : workout
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