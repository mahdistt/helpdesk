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


class EditQueryCategoryForm(forms.ModelForm):
    class Meta:
        model = models.Query
        fields = (
            'status',
            'user_related',
            'query_related',
            'is_active',
        )

    widgets = {
        'status': forms.Select,
        'user_related': forms.Select,
        'query_related': forms.Select,
    }
