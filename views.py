# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render
# from django.views import generic

from . import models


def index(request):
    sources = {
        'github': [f.feed for f in models.GithubFeed.objects.all()]
    }
    context = {
        'sources': sources
    }
    return render(request, 'aggregape/index.html', context)
