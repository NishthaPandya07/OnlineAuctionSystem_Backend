from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Listing


class ListingModelTests(TestCase):
    def test_listing_string_returns_title(self):
        user = User.objects.create_user(username='seller', password='pass12345')
        listing = Listing.objects.create(
            seller=user,
            title='Vintage Clock',
            description='A small table clock.',
            starting_price='25.00',
        )

        self.assertEqual(str(listing), 'Vintage Clock')


class ListingViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller', password='pass12345')

    def test_list_view_shows_listings(self):
        Listing.objects.create(
            seller=self.user,
            title='Vintage Clock',
            description='A small table clock.',
            starting_price='25.00',
        )

        response = self.client.get(reverse('listings:list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vintage Clock')

    def test_logged_in_user_can_create_listing(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('listings:create'),
            {
                'title': 'Desk Lamp',
                'description': 'Adjustable lamp.',
                'starting_price': '15.50',
            },
        )

        self.assertRedirects(response, reverse('listings:list'))
        listing = Listing.objects.get(title='Desk Lamp')
        self.assertEqual(listing.seller, self.user)
