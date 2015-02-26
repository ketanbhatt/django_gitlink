from django.contrib import admin
from gitlink.models import UserProfile, Payload
from django.contrib.auth.models import User

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user', 'github_user_name', 'get_first_name', 'user_github_id', 'selected_repo', 'access' )

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = "Name"

class PayloadAdmin(admin.ModelAdmin):
    model = Payload
    list_display = ('message', 'for_user', 'url')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payload, PayloadAdmin)
