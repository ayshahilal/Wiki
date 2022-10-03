from django.shortcuts import render
from . import util
from django import forms
import markdown
import random

class NewContentForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput())
    content = forms.CharField(label="Content",widget=forms.Textarea(attrs={'style': 'height: 60vh;'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_markdown(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)


def entry_page(request, title):

    page = convert_markdown(title)
    
    if page is None:
        return render(request,"encyclopedia/error.html", {
            'error': "Page has not found"
        })
        
    else:
        return render(request,"encyclopedia/entry.html",{
        'title': title, 
        'content': page
    })
        
def search(request):
    if request.method == "POST":
        value = request.POST['q']
        content = convert_markdown(value)
        if content is None:
            # show the possible results
            entries = util.list_entries()
            valid_entries = []
            for entry in entries:
                if value.lower() in entry.lower():
                    valid_entries.append(entry)
            
            if len(valid_entries) == 0:
                return render(request,"encyclopedia/error.html", 
                {"error": "Page has not found"
                })
            else:
                return render(request,"encyclopedia/search.html",{
                    "entries":valid_entries,
                    "search":value
                })
        else:
            return render(request,"encyclopedia/entry.html",{
            'title': value, 
            'content': content
        })

def new_page(request):
    if request.method== "GET":
        return render(request,"encyclopedia/new.html",{
            "form": NewContentForm()
        })
    else:
        form = NewContentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            check_title = util.get_entry(title)
            if check_title is not None:
                return render(request, "encyclopedia/error.html",{
                    "error": "The title already exist"
                })
            else: 
                util.save_entry(title,content)
                return render(request, "encyclopedia/entry.html",{
                    "title": title,
                    "content": convert_markdown(title)
                })
                # create new page 
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        converted_content = convert_markdown(title)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":converted_content
        })

def random_page(request):
    all_entries = util.list_entries()
    random_title = random.choice(all_entries)
    content = convert_markdown(random_title)
    return render(request,"encyclopedia/entry.html", {
        "title":random_title,
        "content":content
    }) 