from django import forms
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput
class NameForm(forms.Form):
    pass


class ParentForm(forms.Form):
    start_date_a = forms.DateTimeField(required=False,
        widget=DateTimePickerInput(options={
            "format": "YYYY-MM-DD HH:mm",  # moment date-time format
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,
            "locale": "en-gb",

        }), )
    end_date_a = forms.DateTimeField(required=False,
        widget=DateTimePickerInput(options={
            "format": "YYYY-MM-DD HH:mm",  # moment date-time format
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,
            "locale": "en-gb",

        }), )

    start_date_b = forms.DateTimeField(required=False,
        widget=DateTimePickerInput(options={
            "format": "YYYY-MM-DD HH:mm",  # moment date-time format
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,
            "locale": "en-gb",

        }), )
    end_date_b = forms.DateTimeField(required=False,
        widget=DateTimePickerInput(options={
            "format": "YYYY-MM-DD HH:mm",  # moment date-time format
            "showClose": True,
            "showClear": True,
            "showTodayButton": True,
            "locale": "en-gb",

        }), )



