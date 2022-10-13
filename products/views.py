# from .utils import searchProducts
from .models import Product
from .forms import ProductForm
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
import os


def product_list(request):
    search_query = request.GET.get('search_query')
    if search_query:
        vector = SearchVector('category__name', 'title', 'description', 'price')
        query = SearchQuery(search_query)
        products = Product.objects.annotate(search=vector, rank=SearchRank(
            vector, query)).filter(search=query).order_by('-rank')
    else:
        products = Product.objects.filter(available=True)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {'products': products, 'page_obj': page_obj}

    if request.htmx:
        return render(request, 'products/partial/list.html', context)
    return render(request, 'products/book_list.html', context)


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug, available=True)

    context = {
        'product': product,
    }
    return render(request, 'products/book_detail.html', context)


@login_required(login_url='account:login')
def create_product(request):
    profile = request.user.profile
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = profile
            product.save()
            messages.success(request, 'Your Book Successfully Created')
            return redirect('books:product_list')

    context = {'form': form}
    return render(request, 'products/product_form.html', context)


@login_required(login_url='account:login')
def update_product(request, pk, slug):
    profile = request.user.profile
    product = profile.product_set.get(id=pk, slug=slug)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        # see if there image change
        if 'book_image' in request.FILES:
            if os.path.isfile(product.book_image.path):
                os.remove(product.book_image.path)

        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, 'Your Book Successfully Updated')
            return redirect('books:product_list')

    context = {'form': form}
    return render(request, 'products/product_form.html', context)


@login_required(login_url='account:login')
def delete_product(request, pk, slug):
    # product = get_object_or_404(Product, pk=pk, slug=slug, available=True)
    profile = request.user.profile
    product = profile.product_set.get(id=pk, slug=slug)

    if request.method == 'POST':
        if os.path.exists(product.book_image.path):
            os.remove(product.book_image.path)
        product.delete()
        messages.success(request, 'Your Book Successfully Deleted')
        return redirect('books:product_list')

    context = {'object': product}
    return render(request, 'delete_template.html', context)
