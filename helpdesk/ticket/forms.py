from django import forms

from ticket import models


class CreateQueryForm(forms.ModelForm):
    class Meta:
        model = models.Query
        fields = (
            'subject',
            'message',
            'category_related',
        )


class EditQueryCategoryForm(forms.ModelForm):
    class Meta:
        model = models.Query
        fields = (
            'status',
            'user_related',
            'category_related',
            'is_active',
        )
        widgets = {
            'is_active': forms.CheckboxInput,
        }

    widgets = {
        'status': forms.Select,
        'user_related': forms.Select,
        'query_related': forms.Select,
    }


class CreateReplayForm(forms.ModelForm):
    """
    create replay with (operator_related and query_related) AJAX
    """

    class Meta:
        model = models.Replay
        fields = ('replay_message',
                  )

    widgets = {
        'replay_message': forms.TextInput,

    }