from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.urls import URLResolver as urlresolvers, reverse

from carts import cart

from .forms import ProductAddToCartForm
from .models import Category, Product


def index(request, template_name="catalog/index.html"):
    page_title = "Musical Instruments and Sheet Music for Musicians"
    return render(
        request,
        template_name,
        locals(),
    )


def show_category(request, category_slug, template_name="catalog/category.html"):
    c = get_object_or_404(Category, slug=category_slug)
    products = c.products.all()
    page_title = c.name
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    return render(
        request,
        template_name,
        locals(),
    )


def show_product(request, product_slug, template_name="catalog/product.html"):
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description

    # add new things in chapter 4 under here
    # need to evaluate the HTTP method
    if request.method == "POST":
        # add to cart...create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if posted data is valid
        if form.is_valid():
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = reverse("show_cart", )
            # url = urlresolvers.reverse("show_cart")
            return HttpResponseRedirect(url)
    else:
        # it's a GET, create the unbound form. Note request as a kwarg
        form = ProductAddToCartForm(request=request, label_suffix=":")
    # assign the hidden input the product slug
    form.fields["product_slug"].widget.attrs["value"] = product_slug
    # set the test cookie on our first GET request
    request.session.set_test_cookie()

    return render(
        request,
        template_name,
        locals(),
    )
