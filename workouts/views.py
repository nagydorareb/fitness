from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from base.models import Workout
from .models import WorkoutPlan
from .filter import WorkoutFilter
from .forms import StartingDateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.contrib import messages
from datetime import date, timedelta

def workouts_filter(request):
    """
    View for looking up workouts by training type (e.g. HIIT, Strength...) and/or body focus (e.g. Upper, Lower body...)
    """
    template_data = {}
    f = WorkoutFilter(request.GET, queryset=Workout.objects.filter(public=True))
    
    workout_list = f.qs
    paginator = Paginator(workout_list, 7)
    page = request.GET.get('page', 1)
    
    try:
        workouts = paginator.page(page)
    except PageNotAnInteger:
        workouts = paginator.page(1)
    except EmptyPage:
        workouts = paginator.page(paginator.num_pages)

    template_data['paginator'] = paginator
    template_data['workouts'] = workouts
    template_data['filter'] = f

    return render(request, 'workouts/workout_filter.html', template_data)

class WorkoutPlanListView(ListView):
    """
    List view of workout programs
    """
    model = WorkoutPlan
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def workoutplan_detail(request, pk):
    """
    Detail view of workout program

    Users can follow the program by setting a starting date
    The workouts get added to the calendar
    """
    template_data = {}
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    workouts = Workout.objects.filter(workout_plan__id=pk).order_by('plan_week', 'plan_day')

    for workout in workouts:
        if workout.plan_user.filter(username=request.user.username).exists():
            template_data['following'] = True
        else:
            template_data['following'] = False

    if request.method == 'POST':
        form = StartingDateForm(request.POST)
        if form.is_valid():
            starting_date = form.cleaned_data.get('workout_day')
            for workout in workouts:
                if workout.plan_week == 1:
                    if workout.plan_day == 1:
                        workout.plan_user.add(request.user)
                        workout.workout_day = starting_date
                        workout.save()
                    else:
                        workout.plan_user.add(request.user)
                        new_date = starting_date + timedelta(days = workout.plan_day - 1)
                        workout.workout_day = new_date
                        workout.save()
                else:
                    new_day = 7 * (workout.plan_week - 1) + (workout.plan_day - 1)
                    new_date = starting_date + timedelta(days = new_day)
                    workout.plan_user.add(request.user)
                    workout.workout_day = new_date
                    workout.save()
            messages.success(request, f'This workout plan has been added to your calendar')
            return HttpResponseRedirect(reverse('workout-program-detail', kwargs={'pk': pk}))
    else:
        form = StartingDateForm()

    form = StartingDateForm()
    template_data['form'] = form
    template_data['workouts'] = workouts
    template_data['plan'] = plan

    return render(request, 'workouts/workoutplan_detail.html', template_data)

def unfollow_workoutplan(request, pk):
    """
    Unfollow workout program by removing user from the plan users
    """
    workouts_to_update = Workout.objects.filter(workout_plan__id=pk)

    for workout in workouts_to_update:
        workout.plan_user.remove(request.user)
        workout.save()

    messages.success(request, f'You have unsubscribed from this workout plan')
    return HttpResponseRedirect(reverse('workout-program-detail', kwargs={'pk': pk}))

def follow_workoutplan(request, pk):
    """
    Show form in modal to set starting date for workout program
    """
    return render(request, 'workouts/starting_date_form.html')