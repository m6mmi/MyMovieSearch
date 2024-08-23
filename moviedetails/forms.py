from django import forms


from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 11)], attrs={'class': 'horizontal-radio'}),
            'comment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write a review...'}),
        }

