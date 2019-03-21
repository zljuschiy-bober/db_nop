from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import regions, category, firms, security_object, dogovor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden
from .forms import RegionForm, FirmForm,  AddObjectForm, SearchObjectForm, UserProfileForm, AddDocumentForm


def index(request):
    return render(request, 'homePage.html')


@login_required
def firm_detail(request, pk):
    firma = get_object_or_404(firms, pk=pk)
    if request.method == "POST":
        form = FirmForm(request.POST, request.FILES, instance=firma)
        if form.is_valid():
            firm_f = form.save()
            firm_f.save()
            return render(request, 'firm_detail.html', {'result': 'success', 'firm': firm_f})
    else:
        firma = firms.objects.get(id=pk)
        form = FirmForm(instance=firma)
        return render(request, 'firm_detail.html', {'form': form, 'firm': firma})


@login_required
def firm_view(request):
    if request.method == "POST":
        form = FirmForm(request.POST, request.FILES)
        if form.is_valid():
            firm_f = form.save(commit=False)
            firm_f.save()
            return redirect('/', {'result': 'success', 'id': firm_f.id})
    Firms = firms.objects.all()
    formFirm = FirmForm()
    return render(request, 'view_f.html', {'form': formFirm, 'firms': Firms})


@login_required
def category_view(request):
    category_all = category.objects.all().order_by('name')
    this_page = Paginator(category_all, 10)
    num_page = request.GET.get('page')
    try:
        page_content = this_page.page(num_page)
    except PageNotAnInteger:
        page_content = this_page.page(1)
    except EmptyPage:
        page_content = this_page.page(this_page.page(this_page.num_pages))
    return render(request, 'view_cat.html', {'categorys': page_content})


@login_required
def region_edit(request):
    if request.method == "POST":
        form = RayonForm(request.POST, request.FILES)
        if form.is_valid():
            region = form.save(commit=False)
            region.save()
            return redirect('/', {'result': 'success', 'id': region.id})
    rayons = regions.objects.all().order_by('name')
    form = RegionForm()
    return render(request, 'view_region.html', {'form': form, 'regions': rayons})


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
                search_rayon = forma.cleaned_data['object_region']
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
            user.save()
            return redirect('/')
    else:
        userForm = UserProfileForm()
        return render(request, 'registration/profile.html', {'form': userForm})


@login_required
def object_view_all(request):
    if request.method == "POST":
        formObj = AddObjectForm(request.POST, request.FILES)
        if formObj.is_valid():
        # проверка на дату
            object_f = formObj.save(commit=False)
            object_f.save()
            return redirect('/', {'result': 'success', 'id': object_f.id})
    object_all = security_object.objects.all().order_by('name', 'firm', 'region')
    this_page = Paginator(object_all, 10)
    num_page = request.GET.get('page')
    objForm = AddObjectForm()
    try:
        page_content = this_page.page(num_page)
    except PageNotAnInteger:
        page_content = this_page.page(1)
    except EmptyPage:
        page_content = this_page.page(this_page.page(this_page.num_pages))
    return render(request, 'view_obj.html', {'objects': page_content, 'form': objForm})


@login_required
def object_detail(request, pk):
    object = get_object_or_404(security_object, pk=pk)
    if request.method == "POST":
        objectForm = AddObjectForm(request.POST, request.FILES, instance=object)
        button_del = request.POST.get('delete')
        if button_del:
            if button_del == 'del':
                object_id = request.POST.get('object')
                object = security_object.objects.get(id=object_id)
                #object.delete()
                #return render(request, '/', {'result': 'success'})
                return redirect('/', {'result': 'success_object_del', 'id': object_id})
        else:
            if objectForm.is_valid():
                object_f = objectForm.save()
                object_f.save()
                return render(request, 'obj_detail.html', {'result': 'success_object_save', 'object': object_f})
    else:
        object_f = security_object.objects.get(id=pk)
        form = AddObjectForm(instance=object_f)
        return render(request, 'obj_detail.html', {'form': form, 'object': object_f})


# DOCUMENTS
@login_required
def doc_view_all(request):
    if request.method == "POST":
        form = AddDocumentForm(request.POST, request.FILES)
        if form.is_valid():
        # Проверка на дату
           document = form.save(commit=False)
           document.save()
           return redirect('/', {'result': 'success_doc_save', 'id': document.id})
    doc_all = dogovor.objects.all().order_by('name', 'firm')
    this_page = Paginator(doc_all, 10)
    num_page = request.GET.get('page')
    docForm = AddDocumentForm()
    try:
        page_content = this_page.page(num_page)
    except PageNotAnInteger:
        page_content = this_page.page(1)
    except EmptyPage:
        page_content = this_page.page(this_page.page(this_page.num_pages))
    return render(request, 'view_doc.html', {'docs': page_content, 'form': docForm})


@login_required
def doc_detail(request, pk):
    doc_v = dogovor.objects.get(id=pk)
    return render(request, 'doc_detail.html', {'document': doc_v})


@login_required
def search_doc(request):
    if request.method == "POST":
       forma = SearchObjectForm(request.POST, request.FILES)
       searchForm = SearchDocumentForm()
       return render(request, 'search_doc.html', {'form': searchForm})
    return redirect('/')
