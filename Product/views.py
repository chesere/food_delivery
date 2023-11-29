from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView
from .models import Product, Order
from .forms import OrderForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(order_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = '/order/confirmed/'

    def get_context_data(self, object_list=None, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['product'] = get_object_or_404(Product, slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        product = Product.objects.get(slug__iexact=slug)
        form.instance.product = product
        form.instance.cost = int(form.instance.count) * int(product.price)
        return super(OrderCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order


def order_confirm(self):
    return render(self, 'Product/thanks.html')


def products_search(request):
    search = request.GET["search"]
    data = Product.objects.filter(Q(name__icontains=search))
    if search.isnumeric():
        price = float(search)
        data = Product.objects.filter(price=price)

    paginator = Paginator(data, 15)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)

    return render(request, 'Product/product_detail.html', {"Product": data})
