from django.urls import path
from addcorpus.views import *

urlpatterns = [
    path('', CorpusView.as_view()),
    path('image/<str:corpus>', CorpusImageView.as_view()),
    path('documentation/<str:corpus>/', CorpusDocumentationPageViewset.as_view({'get': 'list'})),
    path('citation/<str:corpus>', CorpusCitationView.as_view()),
    path('document/<str:corpus>/<str:filename>', CorpusDocumentView.as_view()),
]
