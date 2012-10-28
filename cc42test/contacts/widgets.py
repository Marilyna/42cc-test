from django.forms.widgets import DateInput


class CalendarWidget(DateInput):
    class Media:
        css = {'all': ('datepicker.css',)}
        js = ('bootstrap-datepicker.js',)

    def __init__(self, attrs=None, format=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'datepicker'
        attrs['data-date-format'] = 'yyyy-mm-dd'
        return super(CalendarWidget, self).__init__(attrs, format)
