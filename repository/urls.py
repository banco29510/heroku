from django.conf.urls import *

from repository.views import *

urlpatterns = [

    url(r'^search$', 'repository.views.search', name="repository-search"),
    url(r'^newScore$', 'repository.views.newScore', name="repository-newScore"),
    url(r'^showRepositoryProduction/(?P<pk>\d+)$', 'repository.views.showRepositoryProduction', name="repository-showRepositoryProduction"),
    url(r'^showRepositoryDeveloppement/(?P<pk>\d+)$', 'repository.views.showRepositoryDeveloppement', name="repository-showRepositoryDeveloppement"),
    url(r'^addFile/(?P<pk>\d+)$', 'repository.views.addFile', name="repository-addFile"),
    url(r'^editRepository/(?P<pk>\d+)$', 'repository.views.editRepository', name="repository-editRepository"),
    url(r'^deleteRepository/(?P<pk>\d+)$', 'repository.views.deleteRepository', name="repository-deleteRepository"),
    url(r'^deleteFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'repository.views.deleteFile', name="repository-deleteFile"),
    url(r'^deleteCommit/(?P<pk>\d+)$', 'repository.views.deleteCommit', name="repository-deleteCommit"),
    url(r'^renameFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'repository.views.renameFile', name="repository-renameFile"),
    url(r'^mergeCommit', 'repository.views.mergeCommit', name="repository-mergeCommit"),
    url(r'^showFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'repository.views.showFile', name="repository-showFile"),
    url(r'^downloadViewsFile/(?P<pk>.+)/(?P<pk_commit>.+)$', 'repository.views.downloadViewsFile', name="repository-downloadViewsFile"),
    url(r'^downloadCommit/(?P<pk>.+)/$', 'repository.views.downloadCommit', name="repository-downloadCommit"),
    url(r'^createBranch/(?P<pk>.+)/$', 'repository.views.createBranch', name="repository-createBranch"),
    url(r'^updateDatabase/(?P<pk>.+)/$', 'repository.views.updateDatabase', name="repository-updateDatabase"),
    url(r'^deleteBranch/(?P<pk>.+)/$', 'repository.views.deleteBranch', name="repository-deleteBranch"),
    url(r'^editMarkdown/(?P<pk>.+)/$', 'repository.views.editMarkdown', name="repository-editMarkdown"),

    url(r'^warningDownloadFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'repository.views.warningDownloadFile', name="repository-warningDownloadFile"),
    url(r'^downloadFile/(?P<pk>.+)/$', 'repository.views.downloadFile', name="repository-downloadFile"),

    url(r'^warningDownloadRepository/(?P<pk>\d+)$', 'repository.views.warningDownloadRepository', name="repository-warningDownloadRepository"),
    #url(r'^downloadRepository$', 'downloadRepository', name="repository-downloadRepository"),

    url(r'^warningDownloadCommit/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'repository.views.warningDownloadCommit', name="repository-warningDownloadCommit"),
    url(r'^downloadCommit$', 'repository.views.downloadCommit', name="repository-downloadCommit"),

    url(r'^changeDeprecated/(?P<pk>\d+)/(?P<boolean>\d+)$', 'repository.views.changeDeprecated', name="repository-changeDeprecated"),
    url(r'^changeCommitVisibility/(?P<pk>\d+)/(?P<boolean>\d+)$', 'repository.views.changeCommitVisibility', name="repository-changeCommitVisibility"),
    url(r'^restartRepositoryByOldCommit/(?P<pk>\d+)/$', 'repository.views.restartRepositoryByOldCommit', name="repository-restartRepositoryByOldCommit"),

    url(r'^commits/(?P<pk>\d+)$', 'repository.views.listCommits', name="repository-listCommits"),
    url(r'^listContributeurs/(?P<pk>\d+)$', 'repository.views.listContributeurs', name="repository-listContributeurs"),
    url(r'^publishDemand/(?P<pk>\d+)$', 'repository.views.publishDemand', name="repository-publishDemand"),
    
    url(r'^listDownload$', 'repository.views.listDownload', name="repository-listDownload"),
    url(r'^tagCommit/(?P<pk>\d+)$', 'repository.views.tagCommit', name="repository-tagCommit"),


]
