from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from gensite.accounts.views import register, my_home
from gensite.gendbs.views import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^gensite/', include('gensite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
	(r'^accounts/login/$', login),
	(r'^accounts/logout/$', logout),
	(r'^accounts/register/$', register),
	(r'^gendbs/post/$', exp_post),
	(r'^gendbs/post/(\d{1,2})/$', exp_post),
	(r'^gendbs/hyper_json/(\d+)/$', hyper_json),
	(r'^gendbs/hyper_json/$', hyper_json),
	(r'^gendbs/Vregion_json/(\d+)/$', Vregion_json),
	(r'^gendbs/Primer_json/(\d+)/$', Primer_json),
	(r'^gendbs/list/$', exp_list),
	(r'^gendbs/history/$', history),
	(r'^gendbs/data_json/(\d+)/$', data_json),
	(r'^gendbs/data_json2/(\d+)/$', data_json2),
	
	(r'$', my_home),

)
