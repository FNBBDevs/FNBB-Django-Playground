from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *

PRE_SEARCH_FILE = None
 
# Create your views here.
def home(request):
    return render(request, 'kwh/home.html')

def about(request):
    return render(request, 'kwh/about.html')

def upload_file(request):
    global PRE_SEARCH_FILE
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                context = {
                    'title': 'View File',
                    'file': [line.rstrip() for line in request.FILES['file'].read().decode('UTF-8').split('\n')],
                    'keyword': ''
                }
                PRE_SEARCH_FILE = context['file']

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
    global PRE_SEARCH_FILE
    context = {
        'title': 'View File',
        'file': PRE_SEARCH_FILE,
        'keyword': ''
    }
    PRE_SEARCH_FILE = PRE_SEARCH_FILE
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        print(f'VIEW FILE: GOT KEYWORD: {keyword}')
        if keyword:
            keyword = keyword.lower()

            context['keyword'] = keyword

    return render(request, 'kwh/view_file.html', context=context)