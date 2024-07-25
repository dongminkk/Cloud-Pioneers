from django.urls import path
from .views import GetVideos, GetVideosAddress

urlpatterns = [
    path('videos/<int:video_id>/', GetVideos.as_view(), name='get_videos'),
    path('videos/<int:video_id>/addr/', GetVideosAddress.as_view(), name='get_video_address'),
]