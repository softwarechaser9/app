from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import pygame
from gtts import gTTS
from .forms import FileUploadForm
import random

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # save the uploaded file to a temporary location
            uploaded_file = request.FILES['file']
            with open('temp_file.txt', 'wb+') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

            # redirect to the next view to display the first line
            language = form.cleaned_data['language']
            return HttpResponseRedirect(reverse('display_line', args=[1, language]))
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})


def display_line(request, line_number, language):
    # read the specified line from the temporary file
    with open('temp_file.txt', 'r') as temp_file:
        lines = temp_file.readlines()
        try:
            line_to_skip = int(request.POST.get('lines_to_skip', 0))
            line_number += line_to_skip
            if line_number >= len(lines):
                return render(request, 'done.html')
            if request.POST.get('mode') == 'skip':
                # Select a random line between current line and 5 lines ahead
                max_line = min(line_number + 5, len(lines) - 1)
                line_number = random.randint(line_number, max_line)
            line = lines[line_number-1].strip()
        except IndexError:
            return render(request, 'done.html')

    # convert the line to speech using gTTS
    speech = gTTS(text=line, lang=language, slow=False)

    # save the speech as an mp3 file
    speech_file = f'speech_{line_number}.mp3'
    speech.save(speech_file)

    # load and play the speech using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(speech_file)
    pygame.mixer.music.play()

    # render the template with the line 
    context = {
        'line_number': line_number,
        'line': line,
        'speech_file': speech_file,
        'language': language,
        'mode': request.POST.get('mode', 'normal'),
    }
    return render(request, 'display_line.html', context)


def skip_line(request, line_number, lines_to_skip, language):
    # skip the specified number of lines
    line_number = int(line_number) + int(lines_to_skip)

    # redirect to the next view to display the next line
    return HttpResponseRedirect(reverse('display_line', kwargs={'line_number': line_number, 'language': language}))


