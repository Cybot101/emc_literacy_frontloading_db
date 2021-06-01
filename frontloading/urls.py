from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='frontloading-index'),
    path('documents', views.documents, name='documents'),
    path('document/new', views.document_new, name='document-new'),
    path('document/preview/<int:document_id>.pdf', views.document_pdf, name='document-pdf'),
    path('document/preview/<int:document_id>', views.document_prieview, name='document-preview'),
    path('document/<int:document_id>', views.document, name='document-detail'),

    path('domain', views.domains, name='domains'),
    path('domain/new', views.domain_new, name='domain-new'),
    path('domain/<int:domain_id>', views.domain, name='domain-detail'),
    # path('subject', views.subject, name='subject'),
    # path('topic', views.topic, name='topic'),

    path('topic', views.topics, name='topics'),
    path('topic/new', views.topic_new, name='topic-new'),
    path('topic/<int:topic_id>', views.topic, name='topic-detail'),

    path('words', views.words, name='words'),
    path('word/<int:word_id>', views.word, name='word-detail'),
    path('word/new', views.word_new, name='word-new'),
    path('word/backup.json', views.words_backup, name='words-backup'),

    # path('picture', views.picture_upload, name='picture-upload'),
    # path('picture/<int:picture_id>', views.picture_get, name='picture-get'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)