from django.shortcuts import render
import tagger.new_entity_recognition as ner

# Create your views here.
def index(request):
    return render(request, 'entity/index.html')

def result(request):
    headline = ""
    if 'headline' in request.POST.keys():
      headline = request.POST['headline']

    #entities = ner.st.tag(headline.split())
    entities = ner.recognize_entities(headline)

    return render(request, 'entity/result.html', { 'entities': entities})