from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import *
from .utils import _chunck_it_out, _query_in_group

PRE_SEARCH_FILE = None
PAGINATION_DATA = None
CURRENT_QUERY   = None
 
# Create your views here.
def home(request):
    return render(request, 'kwh/home.html')

def about(request):
    return render(request, 'kwh/about.html')

def upload_file(request):
    global PRE_SEARCH_FILE, PAGINATION_DATA
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                context = {
                    'title': 'View File',
                    'file': _chunck_it_out(request.FILES['file'], chunk_size=10),
                    'keyword': ''
                }

                PRE_SEARCH_FILE = context['file']

                PAGINATION_DATA = context['file']

                paginator = Paginator(PAGINATION_DATA, 10)

                page_number = 1

                page_obj = paginator.get_page(page_number)

                context['page_obj'] = page_obj

                return render(request, 'kwh/view_file.html', context=context)

            except Exception as exception:
                messages.warning(request, "A problem was encountered. Could not process file.")
                messages.warning(request, f"Additional information: {exception}")
                return redirect('kwh-home')
        else:
            messages.warning(request, "The form was not valid!")
            return redirect('kwh-home')
    else:
        form = UploadFileForm()

        context = {
            'title': 'Upload File',
            'form': form
        }

        return render(request, 'kwh/file_upload.html', context=context)
    
def view_file(request):
    global PRE_SEARCH_FILE, PAGINATION_DATA, CURRENT_QUERY
    context = {
        'title': 'View File',
        'file': PRE_SEARCH_FILE,
        'keyword': ''
    }
    if request.method == "POST": # query
        keyword = request.POST.get('keyword')
        if keyword:
            context['keyword'] = keyword.lower()
            context['query']   = keyword
            CURRENT_QUERY      = keyword

            PAGINATION_DATA = [group for group in PRE_SEARCH_FILE if _query_in_group(CURRENT_QUERY, group['group'])]

            paginator = Paginator(PAGINATION_DATA, 10)

            page_number = 1

            page_obj = paginator.get_page(page_number)

            context['page_obj'] = page_obj

    else: # pagination
        
        if CURRENT_QUERY:
            context['keyword'] = CURRENT_QUERY.lower()
            context['query']   = CURRENT_QUERY

        page_number = request.GET.get('page')

        paginator = Paginator(PAGINATION_DATA, 10)

        page_obj = paginator.get_page(page_number)
    
        context['page_obj'] = page_obj

    return render(request, 'kwh/view_file.html', context=context)