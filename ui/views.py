from datetime import timezone
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login
import requests
from django.contrib.sessions.models import Session
import pyttsx3  
from .models import UserProfile, Summary, UploadedFile, UploadedPDF
from transformers import pipeline
import nltk
import fitz



def home(request):
    return render(request,'home.html')


def registration(request):
    if request.method=='POST':
        username = request.POST.get('userName').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        

        user = UserProfile.objects.create(userName=username, email=email, password=password)

        user.save()

        return HttpResponse("<h1>Registered</h1>")

    return render(request, 'registration.html')




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')
        

        # Authenticate user
        user = UserProfile.objects.filter(userName=username, password=password).first()
        print(user.id)
        request.session['user_id'] = user.id

        

        if user:
            
            # login(request, user)
            return render(request, 'summarease.html')  # Redirect to the home page or any desired URL after successful login
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')


def summarease(request):
   
    pass


summarizer = pipeline('summarization',model='facebook/bart-large-cnn')

def summarize_pdf(request,file_path):
    # pdf_reader = PyPDF2.PdfReader(file_path)
    # text = ""
    # for page_num in range(len(pdf_reader.pages)):
    #     page = pdf_reader.pages[page_num]
    #     text += page.extractText()
    text = ""

    pdf_document = fitz.open(file_path)


    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text += page.get_text()


    pdf_document.close()
    sentences = nltk.sent_tokenize(text)
    print(sentences)
    # summarizer = pipeline("summarization")
    # summary = summarizer(sentences, max_length=100, min_length=50, do_sample=False)[0]

    # return summary['summary_text']
    document = " ".join(sentences)
    request.session['document'] = document 
    text = summarizer(document, max_length=130,min_length=60,do_sample=False)[0]['summary_text']

    return text


def pdf1(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('file-input')

        temp_path =os.path.join(settings.MEDIA_ROOT, pdf_file.name)

        with open(temp_path, 'wb') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        
        summary_text = summarize_pdf(request,temp_path)

        # os.remove(temp_path)
        
        # return JsonResponse({'result': summary_text})

        user_id = request.session.get('user_id', '')

        summary = Summary(user=user_id, input_text=request.session.get('document'), generated_summary=summary_text)
        summary.save()
        return render(request,'pdf1.html',{"result": summary_text,"input":pdf_file})
    else:
        return render(request, 'pdf1.html')

def grammar(request):
    pass

def profile(request):
    pass

def home(request):
    pass

def output(request):
    if request.method=='POST':
        api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        api_token = "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"
        headers = {"Authorization": f"Bearer {api_token}"}

        data = request.POST.get("data")
        max_length = int(request.POST.get("maxL"))
        min_length = max_length // 4

        def query(payload):
            print(payload)
            response = requests.post(api_url, headers=headers, json=payload)
            return response.json()
        
        text= ""

        try:
            output = query({
                    "inputs": data,
                    "parameters": {"min_length": min_length, "max_length": max_length},
                })[0]
            text = output["summary_text"]

        except Exception as e:
            print(e)
            return HttpResponse("Kuch Likh behenchod")
        user_id = request.session.get('user_id', '')

        summary = Summary(user=user_id, input_text=data, generated_summary=text)
        summary.save()

        request.session['text_for_speech'] = text
        request.session['summarized_text'] = text
        return render(request, 'summarease.html', {"result": output["summary_text"],"input" : data})
    return HttpResponse("Enter something")
    
    



def texttospeech(request):
    rate = 150
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    text = request.session.get('text_for_speech', '')
    engine.say(text)
    engine.runAndWait()
    return render(request, 'summarease.html', {"result": text})  

def translate_summary(request):
    pass

def grammar_checker(request):
    pass

def pdf_summary_view(request):
    pass

def history(request):
    history = Summary.objects.filter(user=request.session.get('user_id'))
    print(history)
    return HttpResponse(history[0].input_text)
def forgotpassword():
    pass

def logout(request):
    print(Session.objects.all())
    Session.objects.all().delete()
    return render(request,'home.html')
