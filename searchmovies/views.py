from django.shortcuts import render
from django.views import View

from searchmovies.utils import search_movie


# Create your views here.
class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        results = search_movie(query) if query else []

        return render(request, 'searchmovies/search_result.html',
                      {'results': results, 'query': query})
