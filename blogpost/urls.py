from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from posts import views


from posts.views import homepage, post, about, search, postlist, allposts, like_post, add_comment, unlike_post, favourite_post
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name = 'homepage'),
    path('post/<slug>/', post, name = 'post'),
    path('about/', about,name = 'about' ),
    path('search/', search, name = 'search'),
    path('postlist/<slug>/', postlist, name = 'postlist'), 
    path('posts/', allposts, name = 'allposts'),
    path('like/<int:pk>/', like_post, name='like_post'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('comment/<int:pk>/', add_comment, name='add_comment'),
    path('unlike/<int:pk>/', unlike_post, name='unlike_post'),
    path('favourite/<int:pk>/', favourite_post, name='favourite_post'),
    path('post/<int:post_id>/', views.post_view, name='post_view'),
    path('post/<int:post_id>/report/', views.report_post, name='report_post'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
