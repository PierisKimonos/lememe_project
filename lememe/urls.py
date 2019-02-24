from django.conf.urls import url
from lememe import views

app_name = "lememe"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    # url(r'^add_category/$', views.add_category, name='add_category'),
    # url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^post/(?P<post_id>[0-9]+)$', views.post, name='post'),
    # url(r'^restricted/', views.restricted, name='restricted'),
]