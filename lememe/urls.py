from django.conf.urls import url
from lememe import views

app_name = "lememe"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^search/$', views.search, name='search'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    # url(r'^add_category/$', views.add_category, name='add_category'),
    # url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^post/(?P<post_id>[\w]+)/add_preference/$', views.ajax_add_preference, name='add_preference'),
    url(r'^post/(?P<post_id>[\w]+)/add_comment/$', views.ajax_create_comment, name='add_comment'),
    url(r'^post/(?P<post_id>[\w]+)$', views.show_post, name='show_post'),
    url(r'^user/settings/$', views.show_settings, name='show_settings'),
    url(r'^user/(?P<username>[\w\-]+)/$', views.show_profile, name='show_profile'),
    url(r'^feeling_lucky/$', views.feeling_lucky, name='feeling_lucky'),
    # url(r'^restricted/', views.restricted, name='restricted'),
]