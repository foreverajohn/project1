from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404                 # Imported 'HttpResponseRedirect' and 'Http404'
from django.urls import reverse
from random import randint                                                          # Imported 'randint' from 'random' module.
import markdown2                                                                    # Imported 'markdown2'.

from . import util

def index(request, entry=''):                                                       # Give an empty entry as a default to accept
    return render(request, "encyclopedia/index.html", {                             # post request later.
        "entries": util.list_entries()                                              # Return 'index.html' with list of entries
    })                                                                              # as context variable making links functional.

def search(request):                                                                # Extract 'q' from search form in 'index.html'
    search = request.POST.get('q').lower()
    if util.get_entry(search):                                                      # If exact match for entry exists in list,
        return render(request, "encyclopedia/entry.html", {                         # return such entry.
            "entry": search,
            "text": markdown2.markdown(util.get_entry(search))
        })
    elif any(search.casefold() in entry.casefold() for entry                        # If exact match not found, look for substrings
        in util.list_entries()):                                                    # using list comprehension and .casefold()
        results = [entry for entry in util.list_entries() if                        # method to insure search is not case sensitive.
            search in entry.casefold()]
        return render(request, "encyclopedia/search.html", {
         "results": results
        })
    else:                                                                           # If result not in list of entries, return to
        return render(request, "encyclopedia/new.html", {                           # 'new' page with alert message.
            "message": f"Oops! It seems an entry for '{search}' does not exist"
            "... yet! Feel free to create it down below.",
        })

def entry(request, entry):
    if util.get_entry(entry) is not None:
        text = markdown2.markdown(util.get_entry(entry))                            # Render each entry page with corresponding
        return render(request, "encyclopedia/entry.html", {                         # content.
            "entry": entry,
            "text": text
        })
    else:
        return render(request, "encyclopedia/new.html", {                           # If not created, give the option to do so.
            "message": f"Oops! It seems an entry for '{entry}' does not exist"
            "... yet! Feel free to create it down below.",
        })

def new(request):
    if request.method == "POST":
        title = request.POST.get('title').title()
        entries = [k.lower() for k in util.list_entries()]
        if title.lower() in entries:                                                # If entry is already in list of entries user
            return render(request, "encyclopedia/new.html", {                       # is asked to create another one.
                "message": f"Oops! It seems an entry for '{title}' already"
                " exist. Please submit a different one.",
            })
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/new.html")

def random(request):
    random_entry = util.list_entries()[randint(0,len(util.list_entries())-1)]       # Extract a random entry in list of entries
    return render(request, "encyclopedia/entry.html", {                             # using randint function.
        "entry": random_entry,
        "text": markdown2.markdown(util.get_entry(random_entry))
    })

def edit(request, entry):
    if request.method == "POST":
        title = entry
        new_content = request.POST.get('edited-content')                            # For editing entry, previous content is
        util.save_entry(title, new_content)                                         # replaced by 'new_content'.
        return HttpResponseRedirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "text": util.get_entry(entry)
    })
