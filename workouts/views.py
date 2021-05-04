from django.shortcuts import render, redirect, get_object_or_404
from base.models import Workout, ExerciseSet
from .models import WorkoutPlan
from .filter import WorkoutFilter
from .forms import StartingDateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic import FormView
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from datetime import date, timedelta
# from bootstrap_modal_forms.generic import BSModalUpdateView
from django.http import JsonResponse
from django.template.loader import render_to_string

def workouts_filter(request):
    template_data = {}
    f = WorkoutFilter(request.GET, queryset=Workout.objects.all())
    template_data['filter'] = f
    
    workout_list = f.qs
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

    return render(request, 'workouts/workout_filter.html', template_data)

class WorkoutPlanListView(ListView):
    model = WorkoutPlan
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def workoutplan_detail(request, pk):
    template_data = {}
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    workouts = Workout.objects.filter(workout_plan__id=pk).order_by('plan_week', 'plan_day')

    for workout in workouts:
        if workout.plan_user.filter(username=request.user.username).exists():
            template_data['following'] = True
        else:
            template_data['following'] = False

    if request.method == 'POST':
        workouts_to_update = Workout.objects.filter(workout_plan__id=pk)
        form = StartingDateForm(request.POST)
        if form.is_valid():
            starting_date = form.cleaned_data.get('workout_day')

            # add to calendar with starting date set by user
            for workout in workouts_to_update:
                w = Workout.objects.get(pk=workout.id)
                if workout.plan_week == 1:
                    if workout.plan_day == 1:
                        workout.plan_user.add(request.user)
                        w.workout_day = starting_date
                        w.save()
                    else:
                        new_date = starting_date + timedelta(days = workout.plan_day - 1)
                        workout.plan_user.add(request.user)
                        w.workout_day = new_date
                        w.save()
                else:
                    new_day = 7 * (workout.plan_week - 1) + (workout.plan_day - 1)
                    new_date = starting_date + timedelta(days = new_day)
                    
                    workout.plan_user.add(request.user)
                    w.workout_day = new_date
                    w.save()
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
    workouts_to_update = Workout.objects.filter(workout_plan__id=pk)

    for workout in workouts_to_update:
        w = Workout.objects.get(pk=workout.id)
        w.plan_user.remove(request.user)
        w.save()

    messages.success(request, f'You have unsubscribed from this workout plan')
    return HttpResponseRedirect(reverse('workout-program-detail', kwargs={'pk': pk}))

def follow_workoutplan(request, pk):
    return render(request, 'workouts/starting_date_form.html')