from django.contrib import admin
from kerbie.models import post, comment, userProfile,addImage

class postAdmin(admin.ModelAdmin):
    fields = ['user_wall', 'messageId', 'username', 'date', 'postBody']

class commentAdmin(admin.ModelAdmin):
    fields = ['messageId', 'commentId', 'username', 'date', 'commentBody']
    
class userProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'userId', 'picture', 'location', 'joined', 'age']
    
class addImageAdmin(admin.ModelAdmin):
    fields= ['userId', 'title', 'image', 'date']

admin.site.register(post, postAdmin)
admin.site.register(comment, commentAdmin)
admin.site.register(userProfile)
admin.site.register(addImage, addImageAdmin)
