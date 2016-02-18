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


class BrancheAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class DownloadUserAdmin(admin.ModelAdmin):
    pass

class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Commit, CommitAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(TemporaryFile, TemporaryFileAdmin)
admin.site.register(Branche, BrancheAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(DownloadUser, DownloadUserAdmin)
admin.site.register(Author, AuthorAdmin)