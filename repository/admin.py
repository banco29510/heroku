from django.contrib import admin

from repository.models import *

class RepositoryAdmin(admin.ModelAdmin):
    pass

class CommitAdmin(admin.ModelAdmin):
    pass

class FileAdmin(admin.ModelAdmin):
    pass

class TemporaryFileAdmin(admin.ModelAdmin):
    pass



admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(TemporaryFile, TemporaryFileAdmin)
