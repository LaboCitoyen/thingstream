from django.contrib import admin
from timeseries.models import TimeSeries

#Api Key stuff:
from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#Add API key to admin
admin.site.register(ApiKey)
admin.site.register(ApiAccess)
class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)

#Register models
admin.site.register(TimeSeries)


