from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUser(AbstractUser):
    user_type_choices = ((1, "Admin"), (2, "Staff"),
                         (3, "Merchant"), (4, "Customer"))
    user_type = models.CharField(
        max_length=255, choices=user_type_choices, default=1)


class AdminUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.auth_user_id.username}- {self.auth_user_id.user_type}'


class StaffUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.auth_user_id.username}'


class MerchantUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    company_name = models.CharField(max_length=255)
    gst_details = models.CharField(max_length=255)
    address = models.TextField()
    is_added_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.auth_user_id.username}'


class CustomerUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.auth_user_id.username}'


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("category_list")

    def __str__(self):
        return self.title


class SubCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(
        Categories, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    url_slug = models.CharField(max_length=255)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("sub_category_list")

    def __str__(self):
        return f'{self.title}- {self.category_id.title}'


class OrdenesRate(models.IntegerChoices):
    RATING_1 = 1, _("Anulada")
    RATING_2 = 2, _("Coordinado Con Marcas")
    RATING_3 = 3, _("Cliente No Responde")
    RATING_4 = 4, _("Proceso de Activacion")


class Range(models.IntegerChoices):
    RATING_1 = 1, _("Cliente Con Deuda")
    RATING_2 = 2, _("Cliente Desiste")
    RATING_3 = 3, _("Cliente Sin Oferta")
    RATING_4 = 4, _("Cliente Vigente")


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    url_slug = models.CharField(max_length=255)
    subcategories_id = models.ForeignKey(
        SubCategories, on_delete=models.CASCADE, blank=True, null=True)
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_max_price = models.CharField(max_length=255)
    product_discount_price = models.CharField(max_length=255)
    product_description = models.TextField()
    product_long_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    added_by_merchant = models.ForeignKey(
        MerchantUser, on_delete=models.CASCADE, blank=True, null=True)
    in_stock_total = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product_name}- {self.subcategories_id.title}'


class ProductMedia(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True)
    media_type_choice = ((1, "Image"), (2, "Video"))
    media_type = models.CharField(max_length=255)
    media_content = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class ProductTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type_choices = ((1, "BUY"), (2, "SELL"))
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True)
    transaction_product_count = models.IntegerField(default=1)
    transaction_type = models.CharField(
        choices=transaction_type_choices, max_length=255)
    transaction_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductDetails(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    title_details = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class ProductAbout(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class ProductTags(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class ProductQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, blank=True, null=True)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class ProductReviews(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, blank=True, null=True)
    review_image = models.FileField()
    rating = models.CharField(default="5", max_length=255)
    review = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class ProductReviewVoting(models.Model):
    id = models.AutoField(primary_key=True)
    product_review_id = models.ForeignKey(
        ProductReviews, on_delete=models.CASCADE, blank=True, null=True)
    user_id_voting = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class ProductVarient(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductVarientItems(models.Model):
    id = models.AutoField(primary_key=True)
    product_varient_id = models.ForeignKey(
        ProductVarient, on_delete=models.CASCADE, blank=True, null=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Cliente(models.Model):

    id = models.CharField(primary_key=True, verbose_name=_(
        "RUT"), max_length=50, unique=True)
    first_name = models.CharField(verbose_name=_(
        "Nombre del Cliente"), max_length=50)
    last_name = models.CharField(verbose_name=_(
        "Apellido del Cliente"), max_length=50)
    email = models.EmailField(verbose_name=_(
        "Email del Cliente"), max_length=50)
    phone_number = models.CharField(
        verbose_name=_("Numero del Cliente"), max_length=50)

    # PhoneNumberField(verbose_name=_("Phone_Number_cliente"), max_length=30, default="+56000000000")
    profile_pic = models.FileField(default="")
    country = models.CharField(verbose_name=_(
        "Pais del Cliente"), max_length=50, default="Chile")
    # CountryField(verbose_name=_("Country_cliente"), default="CL", blank=False, null=False)
    city = models.CharField(verbose_name=_("Ciudad del Cliente"),
                            max_length=180, default="Santiago de Chile", blank=False, null=False)
    direction = models.CharField(verbose_name=_(
        "Direccion de Cliente"), max_length=100, default="", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,  null=True,)

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")

    def __str__(self):
        return f'{self.id}- {self.first_name}-  {self.last_name}'

    @property
    def get_full_name(self):
        return f"{self.first_name}- {self.last_name}"


class ClienteStatus(models.Model):
    cliente_id = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(
        verbose_name=_("Rating del Cliente"),
        choices=Range.choices,
        default="En Proceso",
    )


class CustomerOrders(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=255)
    ejecutivo = models.CharField(max_length=255)
    rut_cliente = models.CharField(max_length=255)
    nombre_cliente = models.CharField(max_length=255)
    apellido_cliente = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    telefono = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_id}- {self.ejecutivo}- {self.rut_cliente}- {self.nombre_cliente}- {self.apellido_cliente}- {self.created_at}- {self.status}'


class OrderDeliveryStatus(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(CustomerOrders, on_delete=models.CASCADE)
    status = models.IntegerField(
        verbose_name=_("Rating del Servicio"),
        choices=OrdenesRate.choices,
    )
    status_message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class ClienteVehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=255)
    modelo = models.CharField(max_length=255)
    año = models.CharField(max_length=255)
    patente = models.CharField(max_length=255)
    uso = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)


# class EjecutivoOrders(models.Model):
#     id = models.AutoField(primary_key=True)
#     customer_id = models.OneToOneField(
#         CustomerUser, on_delete=models.CASCADE)
#     product_id = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
#     cliente_id = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
#     created_at = models.DateTimeField(auto_now_add=True)


# class ejecutivoDeliveryStatus(models.Model):
#     id = models.AutoField(primary_key=True)
#     order_id = models.ForeignKey(EjecutivoOrders, on_delete=models.CASCADE)
#     status = models.IntegerField(
#         verbose_name=_("Rate del Servicio"),
#         choices=OrdenesRate.choices,
#     )
#     status_message = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
# @receiver(post_save, sender=CustomerOrders)
# def create_customerorder(sender, instance, created, **kwargs):
#     CustomerOrders.objects.create(id=instance)


# @receiver(post_save, sender=CustomerOrders)
# def save_customerorder(sender, instance, **kwargs):
#     instance.order.save()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type == 2:
            StaffUser.objects.create(auth_user_id=instance)
        if instance.user_type == 3:
            MerchantUser.objects.create(
                auth_user_id=instance, company_name="", gst_details="", address="")
        if instance.user_type == 4:
            CustomerUser.objects.create(auth_user_id=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminuser.save()
    if instance.user_type == 2:
        instance.staffuser.save()
    if instance.user_type == 3:
        instance.merchantuser.save()
    if instance.user_type == 4:
        instance.customeruser.save()


@receiver(post_save, sender=Cliente)
def create_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(id=instance)


# @receiver(post_save, sender=Cliente)
# def save_cliente(sender, instance, **kwargs):
#     instance.cliente.save()
