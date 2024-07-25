from django.urls import path
from .views import GetAllVideos, GetVideos, GetVideosAddress

urlpatterns = [
    path('', GetAllVideos.as_view(), name='get_all_videos'),
    path('videos/<int:video_id>/', GetVideos.as_view(), name='get_videos'),
    path('videos/<int:video_id>/addr/', GetVideosAddress.as_view(), name='get_video_address'),
]