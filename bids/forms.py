from django import forms

from .models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, listing=None, bidder=None, **kwargs):
        self.listing = listing
        self.bidder = bidder
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Bid amount must be greater than zero.')
        return amount

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        if amount is None or self.listing is None:
            return cleaned_data

        if not self.listing.is_active or self.listing.has_ended:
            raise forms.ValidationError('This listing is no longer accepting bids.')

        if self.bidder is not None and self.listing.seller_id == self.bidder.pk:
            raise forms.ValidationError('You cannot bid on your own listing.')

        minimum = Bid.current_price_for(self.listing)
        if amount <= minimum:
            raise forms.ValidationError(
                'Your bid must be higher than the current price of $%(minimum)s.',
                params={'minimum': minimum},
            )
        return cleaned_data

    def save(self, commit=True):
        bid = super().save(commit=False)
        bid.listing = self.listing
        bid.bidder = self.bidder
        if commit:
            bid.save()
        return bid
