from django.shortcuts import render, redirect, get_object_or_404
from base.models import Exercise
from django.contrib.auth.decorators import login_required
from .filter import ExerciseFilter
from .forms import ExerciseCreateForm
from django.contrib import messages

@login_required
def exercise_filter(request):
    f = ExerciseFilter(request.GET, queryset=Exercise.objects.all())
    return render(request, 'exercises/exercise_filter.html', {'filter': f})

@login_required
def exercise_create(request):
    if not request.user.is_authenticated:
        return render(request, 'base/index.html')
    else:
        form = ExerciseCreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            # exercise.image = request.FILES['image']
            exercise.image = request.FILES['image'] if 'image' in request.FILES else 'default_exercise.jpg'
            exercise.save()
            messages.success(request, f'The exercise has been created')
            return redirect('exercise-filter')
        context = {
            "form": form,
        }
        return render(request, 'exercises/exercise_form.html', context)

def exercise_detail(request, pk):
    template_data = {}
    exercise = get_object_or_404(Exercise, pk=pk)
    template_data['exercise'] = exercise

    return render(request, 'exercises/exercise_detail.html', template_data)