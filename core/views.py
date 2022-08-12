from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
import xlwt
import datetime
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.db.models import Q
from core.models import *
from core.forms import *

# Create your views here


def home(request):
    return render(request,  "customer_template/home.html")


def demoPage(request):
    return HttpResponse("demo Page")


@login_required(login_url="/CustomerUser")
def customer_home(request):
    return render(request, "customer_template/customer_home.html")


def demoPageTemplate(request):
    return render(request, "demo.html")

# @login_required(login_url="/customer/")


def customerLogin(request):
    return render(request,  "customer_template/customer_signin.html")


def adminLogin(request):
    return render(request,  "admin_templates/signin.html")

# def staffLogin(request):
#     return render(request,  "staff_template/staff_signin.html")


# LOGEO PROCESS

def adminLoginProcess(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request=request, username=username, password=password)
    if user.is_active:

        if user is not None and StaffUser:
            login(request=request, user=user)
            return HttpResponseRedirect(reverse("admin_home"))

    else:
        messages.error(request, "Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("home"))


def adminLogoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return HttpResponseRedirect(reverse("home"))


def customerLoginProcess(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request=request, username=username, password=password)
    if user is not None and CustomerUser:
        login(request=request, user=user)
        return HttpResponseRedirect(reverse("customer_home"))

    else:
        messages.error(request, "Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("home"))


def customerLogoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return HttpResponseRedirect(reverse("home"))


# def staffLoginProcess(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")

#     user = authenticate(request=request, username=username, password=password)
#     if user is not None and StaffUser:
#         login(request=request, user=user)
#         return HttpResponseRedirect(reverse("staff_home"))

#     else:
#         messages.error(request, "Error in Login! Invalid Login Details!")
#         return HttpResponseRedirect(reverse("home"))


# def staffLogoutProcess(request):
#     logout(request)
#     messages.success(request, "Logout Successfully!")
#     return HttpResponseRedirect(reverse("home"))


# def add_order(request):
#     cliente = Cliente.objects.all()
#     customer_user = CustomerUser.objects.filter(
#         auth_user_id__is_active=True)
#     productos = Products.objects.all()
#     cliente_form = ClienteForm(request.POST or None)
#     customerOrden_form = CustomerOrdersForm(request.POST or None)
#     # cliente_form = self.request.GET.get('Cliente')
#     #producto_form= self.request.GET.get('Producto')
#     if cliente_form.is_valid() and customerOrden_form.is_valid():
#         cliente_form.save()
#         customerOrden_form.save()
#         messages.success(request, 'Agregado Sastifactoriamente ')
#         return redirect('/list_order')

#     context = {
#         'cliente': cliente,
#         'customer_user': customer_user,
#         'productos': productos,
#         'cliente_form': cliente_form,
#         'customerOrden_form':  customerOrden_form,
#     }

#     return render(request, "customer_template/add_order.html", context)


# def list_order(request):

#     customerOrden_form = CustomerOrdersForm(request.POST or None)
#     cliente_form = ClienteForm(request.POST or None)
#     queryset = CustomerOrders.objects.all()
#     context = {
#         "customerOrden_form": customerOrden_form,
#         "cliente_form": cliente_form,
#         "queryset": queryset,
#     }
#     return render(request, "customer_template/list_order.html", context)


# def delete_order(request,pk):
# 	queryset = Cliente.objects.get(pk=pk)
# 	if request.method == 'POST':
# 		queryset.delete()
# 		messages.success(request, 'Borrado Sastifactoriamente')
# 		return redirect('/list_order')
# 	return render (request, 'customer_template/delete_order.html')

class CustomerOrdenCreateView(SuccessMessageMixin, CreateView):
    template_name = "customer_template/add_order.html"
    model = CustomerOrders
    fields = ["product_id", "ejecutivo", "rut_cliente", "nombre_cliente",
              "apellido_cliente", "email", "telefono", "pais", "ciudad", "direccion", "descripcion"]
    product = Products.objects.all()

    def form_valid(self, form):
        order = form.save(commit=False)
        order.is_active = True
        order.save()

        messages.success(self.request, "Orden de Servicio Creado")
        return HttpResponseRedirect(reverse("customer_home"))

#


class CustomerOrdeCreateView(SuccessMessageMixin, CreateView):
    template_name = "customer_template/add_orde.html"
    model = CustomerOrders
    fields = ["status"]
    product = Products.objects.all()

    def form_valid(self, form):
        order = form.save(commit=False)
        order.is_active = True
        order.save()

        messages.success(self.request, "Orden de Servicio Creado")
        return HttpResponseRedirect(reverse("order_list"))

#


def OrderListView(request):
    header = 'Lista de Ordenes'
    form = CustomerOrdersForm(request.POST or None)
    paginate_by = 8
    queryset = CustomerOrders.objects.all()

    context = {
        "header": header,
        "form": form,
        "queryset": queryset,
        "paginate_by": paginate_by,


    }

    return render(request, "customer_template/order_list.html", context)


def update_order(request, pk):
    queryset = CustomerOrders.objects.get(pk=pk)
    form = CustomerOrderForm(instance=queryset)

    if request.method == 'POST':
        form = CustomerOrderForm(request.POST, instance=queryset)

        if form.is_valid():
            form.save()
            messages.success(request, 'Actualizacion Sastifactoriamente')
            return redirect('/order_list')
    context = {
        "form": form,
    }
    return render(request, "customer_template/add_orde.html", context)


def export_excel_order(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=CustomerOrders' + \
        str(datetime.datetime.now())+'.xlsx'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("CustomerOrders")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID', 'Nombre del Producto', 'Ejecutivo', 'RUT del Cliente', 'Nombre de Cliente',
               'Apellido del Cliente', 'Email', 'Telefono', 'Pais', 'Ciudad', 'Direccion', 'Descripcion', 'Creado', 'Status']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = CustomerOrders.objects.all().values_list('id', 'product_id', 'ejecutivo', 'rut_cliente', 'nombre_cliente',
                                                    'apellido_cliente', 'email', 'telefono', 'pais', 'ciudad', 'direccion', 'descripcion', 'created_at', 'status')
    # filter(
    #   owner=request.user).values_list('id','product_id', 'ejecutivo', 'rut_cliente', 'nombre_cliente', 'apellido_cliente', 'email', 'telefono', 'pais', 'ciudad', 'direccion', 'descripcion', 'created_at', 'status')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response
