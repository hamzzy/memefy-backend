# from django.contrib import admin
#
# # Register your models here.
# from django.contrib.auth.admin import UserAdmin
#
# from authentication.models import CustomUser
# from meme.models import Meme
#
#
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('id','email','name','password')
#     list_filter = ('email', 'is_staff', 'is_active',)
#     # fieldsets = (
#     #     (None, {'fields': ('email', 'password')}),
#     #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     # )
#     # add_fieldsets = (
#     #     (None, {
#     #         'classes': ('wide',),
#     #         'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#     #     ),
#     # )
#     filter_horizontal = ()
#     search_fields = ('email',)
#     ordering = ('email',)
#
#
# admin.site.register(CustomUser, CustomUserAdmin)
