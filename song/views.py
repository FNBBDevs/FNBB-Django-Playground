from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
import json
from .models import Song
from .tables import SongTable
from django.core.paginator import Paginator
from django_tables2 import RequestConfig

TRACK = "master_metadata_track_name"
ARTIST = "master_metadata_album_artist_name"
ALBUM = "master_metadata_album_album_name"
TIME = "ms_played"
DATE = "ts"

def home(request):
    return render(request, "song/home.html")

def about(request):
    return render(request, 'song/about.html')

def upload_file(request):
    global PRE_SEARCH_FILE
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                payload = json.loads(request.FILES['file'].read().decode('UTF-8'))

                for song in payload:
                    song_title = song[TRACK]
                    song_artist = song[ARTIST]
                    song_album = song[ALBUM]
                    song_time = song[TIME]
                    song_date = song[DATE]

                    if not song_title:
                        song_title = "No Track"
                    if not song_artist:
                        song_artist = "No Artist"
                    if not song_album:
                        song_album = "No Album"
                    if not song_time:
                        song_time = 0
                    if not song_date:
                        song_date = ""

                    s = Song(
                        date = song_date,
                        track = song_title,
                        artist = song_artist,
                        album = song_album,
                        time = song_time
                    )

                    s.save()

                return render(request, 'song/home.html')
            except Exception as exception:
                messages.warning(request, "A problem was encountered. Could not process file.")
                messages.warning(request, f"Additional information: {exception}")
                return redirect('song-home')
        else:
            messages.warning(request, "The form was not valid!")
            return redirect('song-home')
    else:
        form = UploadFileForm()

        context = {
            'title': 'Upload File',
            'form': form
        }

        return render(request, 'song/file_upload.html', context=context)

def view_tables(request):
    table = SongTable(Song.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    RequestConfig(request).configure(table)
    return render(request, "song/table.html", context={"table":table})
    # songs = Song.objects.all()
    # paginator = Paginator(songs, 15)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # return render(request, 'song/table.html', context={'page_obj': page_obj})