from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm

from .utils import get_mongodb
from .models import Author, Quote
from datetime import datetime

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            db = get_mongodb()
            authors_collection = db['authors']

            author_data = {
                'fullname': form.cleaned_data['fullname'],
                'born_date': form.cleaned_data['born_date'],
                'born_location': form.cleaned_data['born_location'],
                'description': form.cleaned_data['description']
            }

            authors_collection.insert_one(author_data)

            return redirect('quotes:root')
    else:
        form = AuthorForm()

    return render(request, 'quotes/add_author.html', {'form': form})


@login_required
def add_quote(request):
    db = get_mongodb()

    authors_choices = [(author.id, author.fullname) for author in Author.objects.all()]

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        form.fields['author'].queryset = Author.objects.all()

        if form.is_valid():
            quote_data = form.cleaned_data
            author_id = quote_data['author'].id if quote_data['author'] else None

            new_quote = {
                "quote": quote_data['quote'],
                "author": quote_data['author'].id if quote_data['author'] else None,
                "created_at": datetime.utcnow()
            }
            db.quotes.insert_one(new_quote)

            return redirect('quotes:root')
    else:
        form = QuoteForm()
        form.fields['author'].queryset = Author.objects.all()

    return render(request, 'quotes/add_quote.html', {'form': form})

