from django import forms

from ticket import models


class CreateQueryForm(forms.ModelForm):
    class Meta:
        model = models.Query
        fields = (
            'subject',
            'message',
            'user_related',
            'query_related',
        )
        # widgets = {
        #     'user_related': forms.Select
        # }
