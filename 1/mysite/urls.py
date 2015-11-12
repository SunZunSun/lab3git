from django.conf.urls import patterns, include, url
from addr_book.views import hello,book_add,author_add,book_query_auth
from addr_book.views import book_update,book_delete,query,create,see_book
from django.conf import settings
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^$', hello),
    (r'^/$',create),
    (r'^book_query_auth/$',book_query_auth),
    (r'^book_add/$',book_add),
    (r'^author_add/$',author_add),
    (r'^update/',book_update),
    (r'^delete/',book_delete),
    (r'^query/',query),
    (r'^see/',see_book),
    (r'^site_media/(?P<path>.*)','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    (r'^css/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_ROOT,}),
)