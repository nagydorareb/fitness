from datetime import date
from calendar import HTMLCalendar
from itertools import groupby
from .models import Workout

from django.utils.html import conditional_escape as esc

class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<br>']
                for workout in self.workouts[day]:
                    body.append('<a href="%s">' % workout.get_absolute_url())
                    if workout.training_type == "ST":
                        body.append('<i class="fas fa-dumbbell lilpadding"></i>')
                    if workout.training_type == "HI":
                        body.append('<i class="fas fa-heartbeat lilpadding"></i>')
                    if workout.training_type == "CA":
                        body.append('<i class="fas fa-running lilpadding"></i>')
                    if workout.training_type == "YO":
                        body.append('<i class="fas fa-spa lilpadding"></i>')
                    body.append(esc(workout.title))
                    body.append('<br>')
                body.append('')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.workout_day.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s align-top">%s</td>' % (cssclass, body)
