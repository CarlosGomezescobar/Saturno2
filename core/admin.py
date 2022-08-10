from django.contrib import admin
from core.models import *


class ClienteAdmin(admin.ModelAdmin):

    list_display = ('id', 'first_name', 'last_name', 'email',
                    'phone_number', 'profile_pic', 'country', 'city', 'direction')
    list_filter = ("id", "first_name", "last_name", "country")
    search_fields = ("id", "first_name", "last_name")


# class CustomUserAdmin(admin.ModelAdmin):

# 	list_display=('user_type_choices', 'iuser_type')
# 	list_filter=("user_type_choices", "user_type")
# 	search_fields=("user_type")


# class AdminUserAdmin(admin.ModelAdmin):

# 	list_display=('profile_pic', 'auth_user_id', 'created_at')
# 	list_filter=( "auth_user_id")
# 	search_fields=( "auth_user_id")


# class StaffUserAdmin(admin.ModelAdmin):

#     list_display = ("auth_user_id", "profile_pic", "created_at")
#     list_filter = "auth_user_id"
#     search_fields = "auth_user_id"


# class MerchantUserAdmin(admin.ModelAdmin):

# 	list_display=('auth_user_id', 'profile_pic', 'company_name', 'gst_details', 'address', 'is_added_by_admin', 'created_at', 'objects')
# 	list_filter=("auth_user_id", "company_name", "objects")
# 	search_fields=("auth_user_id", "company_name")


# class CustomerUserAdmin(admin.ModelAdmin):

# 	list_display=('auth_user_id', 'profile_pic', 'created_at')
# 	list_filter=("auth_user_id")
# 	search_fields=("auth_user_id")


# # class CategoriesAdmin(admin.ModelAdmin):

# # 	list_display=('id', 'title', 'url_slug', 'thumbnail', 'description', 'created_at', 'is_active')
# # 	list_filter=("id", "title", "description")
# # 	search_fields=("id", "title", "description")


# # class SubCategoriesAdmin(admin.ModelAdmin):
# # 	list_display=('id ', 'title', 'url_slug', 'thumbnail', 'description', 'created_at', 'is_active')
# # 	list_filter=("id ", "title", "description")
# # 	search_fields=("id ", "title", "description")


# class ProductsAdmin(admin.ModelAdmin):

# 	list_display=('id', 'url_slug', 'subcategories_id', 'product_name', 'brand', 'product_max_price', 'product_discount_price','product_description', 'product_long_description', 'created_at', 'added_by_merchant', 'in_stock_total', 'is_active')
# 	list_filter=("id", "product_name")
# 	search_fields=("id", "product_name")

# class ProductMediadmin(admin.ModelAdmin):

# 	list_display=('id', 'product_id', 'media_type_choice', 'media_type', 'media_content', 'created_at', 'is_active')
# 	list_filter=("id", "product_id", "created_at")
# 	search_fields=("id", "product_id")


# class ProductTransactionAdmin(admin.ModelAdmin):

# 	list_display=('id', 'transaction_type_choices', 'product_id', 'transaction_product_count', 'transaction_type', 'transaction_description', 'created_at')
# 	list_filter=("id", "transaction_type_choices", "product_id", "created_at")
# 	search_fields=("id")


# class ProductDetailsAdmin(admin.ModelAdmin):

# 	list_display=('id', 'product_id', 'title', 'title_details', 'created_at', 'is_active')
# 	list_filter=("id", "product_id", "title")
# 	search_fields=("id", "title")


# class ProductTagsAdmin(admin.ModelAdmin):

# 	list_display=('id', 'product_id', 'title', 'title_details', 'created_at', 'is_active')
# 	list_filter=("id", "product_id", "title")
# 	search_fields=("id", "title")


# class ProductQuestionsAdmin(admin.ModelAdmin):

# 	list_display=('id', 'product_id', 'user_id', 'question', 'answer', 'created_at', 'is_active')
# 	list_filter=("id", "product_id", "uder_id")
# 	search_fields=("id", "product_id", "uder_id")

# class ProductReviewsAdmin(admin.ModelAdmin):

# 	list_display=('id', 'product_id', 'user_id', 'review_image', 'rating','review' 'created_at', 'is_active')
# 	list_filter=("id", "product_id", "uder_id")
# 	search_fields=("id", "product_id", "uder_id")

# class ProductReviewVotingAdmin(admin.ModelAdmin):

# 	list_display=('id', 'product_review_id', 'user_id_voting','created_at', 'is_active')
# 	list_filter=("id", "pruser_id_voting")
# 	search_fields=("id", "user_id_voting")


# class ProductVarientAdmin(admin.ModelAdmin):

# 	list_display=('id', 'title','created_at')
# 	list_filter=("id", "title")
# 	search_fields=("id", "title")

# class ProductVarientItemsAdmin(admin.ModelAdmin):

# 	list_display=('id', 'product_varient_id', 'product_id', 'title' 'created_at')
# 	list_filter=("id", "product_varient_id")
# 	search_fields=("id", "title")

# class CustomerOrdersAdmin(admin.ModelAdmin):

# 	list_display=('id', 'product_id', 'purchase_price', 'coupon_code', 'discount_amt', 'product_status', 'created_at')
# 	list_filter=("id", "product_id")
# 	search_fields=("id", "product_id")


# class OrderDeliveryStatusAdmin(admin.ModelAdmin):

# 	list_display=('id', 'order_id', 'product_id', 'status', 'status_message', 'created_at', 'updated_at')
# 	list_filter=("id", "order_id")
# 	search_fields=("id", "order_id")

admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(CustomUser)
admin.site.register(AdminUser)
admin.site.register(StaffUser)
admin.site.register(MerchantUser)
admin.site.register(CustomerUser)
admin.site.register(Products)
admin.site.register(ProductMedia)
admin.site.register(ProductTransaction)
admin.site.register(ProductDetails)
admin.site.register(ProductAbout)
admin.site.register(ProductTags)
admin.site.register(ProductQuestions)
admin.site.register(ProductReviews)
admin.site.register(ProductReviewVoting)
admin.site.register(ProductVarient)
admin.site.register(ProductVarientItems)
admin.site.register(CustomerOrders)
admin.site.register(OrderDeliveryStatus)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteStatus)
