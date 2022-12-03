from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List

# def home_page(request):
#     if request.method == 'POST':
#         Item.objects.create(text=request.POST['text'])
#         # return redirect('/')
#         return redirect('/lists/the-only-list-in-the-world/')
#     items = Item.objects.all()
#     return render(request, 'home.html', {'items': items})


# def home_page(request):
#     # if request.method == 'POST':
#     #     Item.objects.create(text=request.POST['text'])
#     #     return redirect('/lists/the-only-list-in-the-world/')
#     return render(request, 'home.html')
def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['text'])
    #     return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['text'], list=list_)
    return redirect(f'/lists/{list_.id}/')


def my_lists(request, email):
    return render(request, 'my_lists.html')
