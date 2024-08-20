from django.shortcuts import render
from django.views import View
from mainpage.utils import current_movie_list

class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        results = current_movie_list()
        return render(request, self.template_name,
                      {'results': results})

