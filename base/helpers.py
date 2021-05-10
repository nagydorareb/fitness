from datetime import date
from calendar import HTMLCalendar
from itertools import groupby
from django.utils.html import conditional_escape as esc
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from base.templatetags.extras import get_type_icon

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
                    if workout.workout_plan:
                        body.append('<span style="color: mediumslateblue;">')
                    body.append(get_type_icon(workout.training_type))
                    body.append(esc(workout.title))
                    body.append('<br>')
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

def setform_helper():
    """
    Custom crispy fields for normal exercise sets
    """
    helper = FormHelper()
    helper.layout = Layout(
        'exercise',
        'set_num',
        Row(
            Column('rep_num', css_class='form-group col-md-6 mb-0'),
            Column('rep_type', css_class='form-group col-md-6 mb-0'),
            css_class='form-row'
        ),
        Row(
            Column('weight_num', css_class='form-group col-md-6 mb-0'),
            Column('weight_type', css_class='form-group col-md-6 mb-0'),
            css_class='form-row'
        ),
        'rest_time',
        Submit('submit', 'Save')
    )
    return helper

def simplesetform_helper():
    """
    Custom crispy fields for simple exercise sets
    """
    helper = FormHelper()
    helper.layout = Layout(
        'exercise',
        Submit('submit', 'Save')
    )
    return helper