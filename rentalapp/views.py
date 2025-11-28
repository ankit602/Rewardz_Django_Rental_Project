# Create your views here.
# import requests
# from datetime import datetime, timedelta
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from .models import Book, Rental
# from .forms import StartRentalForm
# from django.db.models import Count, Sum

import requests
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg 
from .models import Book, Rental
from .forms import StartRentalForm


# ----------------------------------------------------------
#  UNIVERSAL BOOK FETCH FUNCTION (Correct Pages)
# ----------------------------------------------------------
def fetch_book_data(title):
    url = f"https://openlibrary.org/search.json?title={title}"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    data = res.json()
    if not data.get("docs"):
        return None

    book = data["docs"][0]

    # Try all possible page keys OpenLibrary may return
    possible_keys = [
        "number_of_pages",
        "number_of_pages_median",
        "number_of_pages_estimate",
        "physical_pages"
    ]

    pages = None
    for key in possible_keys:
        if key in book:
            pages = book[key]
            break

    # Additional fallback using edition_count (approximate)
    if pages is None and book.get("edition_count"):
        pages = book["edition_count"] * 50

    # Final fallback if still None OR page is not integer
    if not isinstance(pages, int):
        pages = 150   # best final fallback

    return {
        "title": book.get("title", title),
        "pages": pages
    }


# ----------------------------------------------------------
# Start rental
# ----------------------------------------------------------
def start_rental(request):
    if request.method == "POST":
        form = StartRentalForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            title = form.cleaned_data["title"]

            # Create user
            user, _ = User.objects.get_or_create(username=username)

            # Fetch from OpenLibrary
            data = fetch_book_data(title)

            if not data:
                return render(request, "start_rental.html", {
                    "form": form,
                    "error": "Book not found on OpenLibrary"
                })

            # Create book entry
            book, _ = Book.objects.get_or_create(
                title=data["title"],
                defaults={"pages": data["pages"]}
            )

            # End date = 1 month
            end_date = datetime.today().date() + timedelta(days=30)

            Rental.objects.create(
                user=user,
                book=book,
                end_date=end_date
            )

            return redirect("/dashboard/")
    else:
        form = StartRentalForm()

    return render(request, "start_rental.html", {"form": form})


# ----------------------------------------------------------
# Extend rental
# ----------------------------------------------------------
def extend_rental(request, rental_id):
    rental = Rental.objects.get(id=rental_id)

    if request.method == "POST":
        months = int(request.POST.get("months", 1))

        # Free period end date
        free_end = rental.start_date + timedelta(days=30)

        # Calculate new end date
        new_end_date = rental.end_date + timedelta(days=30 * months)

        # Charge only for months that go beyond free period
        if new_end_date > free_end:
            fee_per_month = rental.book.pages / 100

            # count how many months go beyond free period
            paid_months = (new_end_date - free_end).days // 30

            rental.total_fee += paid_months * fee_per_month

        # update end date
        rental.end_date = new_end_date
        rental.save()

        return redirect("/dashboard/")

    return render(request, "extend_rental.html", {"rental": rental})



# ----------------------------------------------------------
# Dashboard
# ----------------------------------------------------------
def dashboard(request):
    rentals = Rental.objects.all()

    for r in rentals:
        r.recommendations = fetch_recommendations(r.book.title)

    return render(request, 'dashboard.html', {'rentals': rentals})



def fetch_recommendations(title):
    url = f"https://openlibrary.org/search.json?title={title}"
    res = requests.get(url).json()

    if not res["docs"]:
        return []

    book = res["docs"][0]
    subjects = book.get("subject", [])

    # take first 3 subjects
    if not subjects:
        return []

    first_subject = subjects[0]

    url2 = f"https://openlibrary.org/subjects/{first_subject.lower().replace(' ','_')}.json?limit=5"
    res2 = requests.get(url2).json()

    recommendations = [b["title"] for b in res2.get("works", [])]

    return recommendations




def reports(request):
    report = (
        Rental.objects.values("book__title")
        .annotate(
            total_rented=Count("id"),
            avg_pages=Avg("book__pages"),
            total_revenue=Sum("total_fee")
        )
    )

    return render(request, "reports.html", {"report": report})

