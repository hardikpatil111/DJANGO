from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm,UserAdminChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User=get_user_model()
# Register your models here.
class UserAdmin(BaseUserAdmin):
    add_form = UserAdminCreationForm
    add_fieldsets = (
        ("User Details", {
            'classes':('wide',),
            'fields' :('full_name','mobile','email')}
            ),
            ("Password Details",
            {
                'classes':('wide'),
                'fields':('password1','password2')
            })
    )
    form= UserAdminChangeForm
    fieldsets= (
        ("Personal Info", {
            'classes':('wide',),
            'fields' :('full_name','mobile','email','password')}
            ),
            ("Permissions",
            {
                'classes':('wide'),
                'fields':('admin','staff','active')
            })
    )

    #modification in view page of admin site
    list_filter = ('active','admin','staff')
    filter_horizontal = ()
    ordering = ('full_name',)
    list_display = ('full_name','email')
    search_fields= ('full_name','email','mobile')

admin.site.register(User,UserAdmin)
admin.site.unregister(Group)