import debug_toolbar

from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from rest_framework.routers import SimpleRouter
from django.urls import include
from django.conf.urls import url


from store.views import BookViewSet, auth, UserBookRelationView



router = SimpleRouter()

router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += router.urls



