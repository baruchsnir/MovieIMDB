from django import forms
from .models import Movie, Review

class ReviewForm(forms.ModelForm):
    CHOICES = (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6,6),
            (7,7),
            (8,8),
            (9,9),
            (10,10)
        )

    rating = forms.ChoiceField(
        choices=CHOICES,
        required=True,
        label='Rate this movie',
        help_text='Choose a rate 1 = Worst and 5 = Best'
    )
    class Meta:
        model = Review
        fields = ['rating', 'comment']
