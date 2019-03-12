from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Regions, Category, Firms, Security_object
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from .forms import RayonForm, FirmForm,  AddObjectForm, SearchObjectForm, UserProfileForm


def index(request):
    return render(request, 'homePage.html')


@login_required
def firm_detail(request, pk):
    firma = Firms.objects.get(id=pk)
    return render(request, 'firm_detail.html', {'firm': firma})


@login_required
def firm_edit(request, ident):
    a = Firms.objects.get(id=ident)
    f = FirmForm(request.POST, instance=a)
    f.save()
    return render(request, 'view_f.html', {'firms': f})


@login_required
def category_view(request):
    categorys = Category.objects.all()
    return render(request, 'view_cat.html', {'categorys': categorys})


def region_edit(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            form = RayonForm(request.POST, request.FILES)
            if form.is_valid():
                rayonu = form.save(commit=False)
                rayonu.save()
                return redirect('/')
        else:
            rayons = Regions.objects.all()
            form = RayonForm()
            return render(request, 'view_rayon.html', {'form': form, 'regions': rayons})


def firm_add(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            form = FirmForm(request.POST, request.FILES)
            if form.is_valid():
                firmy = form.save(commit=False)
                firmy.save()
                return redirect('/')
        else:
            firms = Firms.objects.all()
            formFirm = FirmForm()
            return render(request, 'view_f.html', {'form': formFirm, 'firms': firms})


def rayon_view(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        rayons = Regions.objects.all()
        return render(request, 'view_rayon.html', {'rayons': rayons})


def add_object(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            forma = AddObjectForm(request.POST, request.FILES)
            if forma.is_valid():
                object1 = forma.save(commit=False)
                object1.save()
                return redirect('/')
        else:
            formObject = AddObjectForm()
            return render(request, 'add_object.html', {'form': formObject})


def search_object(request):
    if request.user.is_anonymous or not request.user.is_authenticated:
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            forma = SearchObjectForm(request.POST, request.FILES)
            if forma.is_valid():
                # Получить чистые данные
                search_name = forma.cleaned_data['object_name'].lower().strip()
                search_address = forma.cleaned_data['object_address'].lower().strip()
                search_category = forma.cleaned_data['object_category']
                search_firm = forma.cleaned_data['object_firm']
                search_rayon = forma.cleaned_data['object_rayon']
                # Слепить запрос
                #schto = None
                # Вывести
                object_search = ''
                this_page = Paginator(object_search, 10)
                num_page = request.GET.get('page')
                try:
                    page_content = this_page.page(num_page)
                except PageNotAnInteger:
                    page_content = this_page.page(1)
                except EmptyPage:
                    page_content = this_page.page(this_page.page(this_page.num_pages))
                return render(request, 'view_obj.html', {'objects': page_content})

        else:
            searchForm = SearchObjectForm()
            return render(request, 'search.html', {'form': searchForm})


@login_required
def view_profile(request):
    if request.method == "POST":
        forma = UserProfileForm(request.POST, request.FILES)
        if forma.is_valid():
            user= forma.save(commit=False)
            user.save()
            return redirect('/')
    else:
        userForm = UserProfileForm()
        return render(request, 'registration/profile.html', {'form': userForm})


@login_required
def object_view_all(request):
    object_all = Security_object.objects.all().order_by('name', 'firm', 'rayon')
    this_page = Paginator(object_all, 10)
    num_page = request.GET.get('page')
    try:
        page_content = this_page.page(num_page)
    except PageNotAnInteger:
        page_content = this_page.page(1)
    except EmptyPage:
        page_content = this_page.page(this_page.page(this_page.num_pages))
    return render(request, 'view_obj.html', {'objects': page_content})


@login_required
def object_detail(request, pk):
    object_v = Security_object.objects.get(id=pk)
    return render(request, 'obj_detail.html', {'objects': object_v})
