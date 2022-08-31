from django.http import HttpResponse
from django.shortcuts import render,redirect
from django import forms
from . import util
import markdown as md


class NewPageForm(forms.Form):
    title = forms.CharField(widget = forms.TextInput(attrs={'class':'add','name':'title'}))
    body = forms.CharField(widget = forms.Textarea(attrs={'class':'add','name':'body','rows':15, 'cols':5}))



def search_results(request):
    if request.method == "POST":
        query = request.POST.get('q',None)
        results  = []
        if query:
            try:
             entries = util.list_entries() 
            except:
                print("No entries in the database")
            if query =="*":
                results = entries
            else:
                results = filter(lambda entry: query in entry,entries)
        context = {'results': list(results)}
    return render(request,'encyclopedia/search_page.html', context) 

def newpage(request):
    title, body = None,None
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']

    if body and title:
        util.save_entry(title,body)
    context = {'form' : NewPageForm()}
    return render(request,'encyclopedia/newpage.html',context)

def edit(request,title):
    context = {'title':title}
    print(title)
    if request.method == "GET":
        title = title 
        body = util.get_entry(title)
        form = NewPageForm({'title':title, 'body':body})
        context['form'] = form
        return render(request,'encyclopedia/edit.html', context)

    form = NewPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        body = form.cleaned_data['body']
        if title and body:
            util.save_entry(title,body)
            return redirect("display_entry", title)

def index(request):
    context = {
            'entries' : util.list_entries(),
            }
    return render(request, "encyclopedia/index.html", context)


def display_title(request,title):
    """ display a title by name """
    try:
        entry = md.markdown(util.get_entry(title))
    except:
        entry = ['Something went wrong']
    context = {
             'entry': entry,
             'title':title
             }
    return render(request,'encyclopedia/entry.html',context)

