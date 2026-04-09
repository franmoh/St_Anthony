from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from .models import DeceasedDetails



def index(request):

    info = request.GET.get('search_query')   
    
    if info:
        vector = SearchVector('first_name', 'last_name', 'dob_year', 'dod_year')
        query = SearchQuery(info)
        info = DeceasedDetails.objects.annotate(search=vector).filter(search=query)
        #info = DeceasedDetails.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')

    else:
        info = None
    context = {"info": info}

    return render(request, 'index/index.html', context)

def detail(request):
    return render(request, 'index/detail.html')

def plot(request):
    return render(request, 'index/plot.html')