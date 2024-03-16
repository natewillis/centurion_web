import os
from django.http import Http404
from django.shortcuts import render

DOC_DIR = '../docs/'


def generic_html_page_view(request, page_name):

    # check if requested page exists
    if os.path.exists(DOC_DIR + page_name):
        # if yes, then serve the page
        with open(DOC_DIR + page_name) as f:
            content = f.read()
        return render(request, 'common/base.html', {'generic_html': content})
    else:
        raise Http404