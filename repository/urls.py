from django.conf.urls import *

from repository.views import *

urlpatterns = patterns('repository.views',

    url(r'^search$', 'search', name="repository-search"),
    url(r'^newScore$', 'newScore', name="repository-newScore"),
    url(r'^showRepositoryProduction/(?P<pk>\d+)$', 'showRepositoryProduction', name="repository-showRepositoryProduction"),
    url(r'^showRepositoryDeveloppement/(?P<pk>\d+)$', 'showRepositoryDeveloppement', name="repository-showRepositoryDeveloppement"),
    url(r'^addFile/(?P<pk>\d+)$', 'addFile', name="repository-addFile"),
    url(r'^editRepository/(?P<pk>\d+)$', 'editRepository', name="repository-editRepository"),
    url(r'^deleteRepository/(?P<pk>\d+)$', 'deleteRepository', name="repository-deleteRepository"),
    url(r'^deleteFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'deleteFile', name="repository-deleteFile"),
    url(r'^deleteCommit/(?P<pk>\d+)$', 'deleteCommit', name="repository-deleteCommit"),
    url(r'^renameFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'renameFile', name="repository-renameFile"),
    url(r'^mergeCommit', 'mergeCommit', name="repository-mergeCommit"),
    url(r'^showFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'showFile', name="repository-showFile"),
    url(r'^downloadViewsFile/(?P<pk>.+)/(?P<pk_commit>.+)$', 'downloadViewsFile', name="repository-downloadViewsFile"),
    url(r'^downloadCommit/(?P<pk>.+)/$', 'downloadCommit', name="repository-downloadCommit"),
    url(r'^createBranch/(?P<pk>.+)/$', 'createBranch', name="repository-createBranch"),
    url(r'^deleteBranch/(?P<pk>.+)/$', 'deleteBranch', name="repository-deleteBranch"),

    url(r'^warningDownloadFile/(?P<pk>\d+)/(?P<pk_commit>\d+)$', 'warningDownloadFile', name="repository-warningDownloadFile"),
    url(r'^downloadFile$', 'downloadFile', name="repository-downloadFile"),

    url(r'^warningDownloadRepository/(?P<pk>\d+)$', 'warningDownloadRepository', name="repository-warningDownloadRepository"),
    #url(r'^downloadRepository$', 'downloadRepository', name="repository-downloadRepository"),

    url(r'^warningDownloadCommit/(?P<pk>\d+)$', 'warningDownloadCommit', name="repository-warningDownloadCommit"),
    url(r'^downloadCommit$', 'downloadCommit', name="repository-downloadCommit"),

    url(r'^changeDeprecated/(?P<pk>\d+)/(?P<boolean>\d+)$', 'changeDeprecated', name="repository-changeDeprecated"),
    url(r'^changeCommitVisibility/(?P<pk>\d+)/(?P<boolean>\d+)$', 'changeCommitVisibility', name="repository-changeCommitVisibility"),
    url(r'^restartRepositoryByOldCommit/(?P<pk>\d+)/$', 'restartRepositoryByOldCommit', name="repository-restartRepositoryByOldCommit"),

    url(r'^commits/(?P<pk>\d+)$', 'listCommits', name="repository-listCommits"),
    url(r'^listContributeurs/(?P<pk>\d+)$', 'listContributeurs', name="repository-listContributeurs"),
    url(r'^publishDemand$', 'publishDemand', name="repository-publishDemand"),
    
    url(r'^listDownload$', 'listDownload', name="repository-listDownload"),
    url(r'^tagCommit/(?P<pk>\d+)$', 'tagCommit', name="repository-tagCommit"),


)
