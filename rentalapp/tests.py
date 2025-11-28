# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import Book, Rental


class RentalTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="ankit")
        self.book = Book.objects.create(title="Test Book", pages=200)

    def test_start_rental(self):
        """Rental should be created with +30 days free."""
        start = date.today()
        end = start + timedelta(days=30)

        rental = Rental.objects.create(
            user=self.user,
            book=self.book,
            end_date=end,
        )

        self.assertEqual(rental.user.username, "ankit")
        self.assertEqual(rental.book.title, "Test Book")
        self.assertEqual(rental.end_date, end)
        self.assertEqual(rental.total_fee, 0)

    def test_extend_rental_after_free_month(self):
        """Fee should apply once rental is older than 30 days."""
        start = date.today() - timedelta(days=40)
        end = start + timedelta(days=30)

        rental = Rental.objects.create(
            user=self.user,
            book=self.book,
            start_date=start,
            end_date=end,
            total_fee=0
        )

        # simulate extend by 1 month
        fee_per_month = rental.book.pages / 100
        rental.total_fee += fee_per_month
        rental.save()

        self.assertEqual(rental.total_fee, 2.0)  # 200 pages / 100
