from django.urls import path
from .views import PostReview, GetReview, DeleteReview, PutReview, GetAllReview

urlpatterns = [

    # POST 요청으로 리뷰 생성
    path('videos/<int:video_id>/reviews/posts/', PostReview.as_view(), name='post_review'),

    # GET 요청으로 리뷰 조회
    path('videos/<int:video_id>/reviews/', GetReview.as_view(), name='get_review'),

    # GET 요청으로 모든 리뷰 조회
    path('videos/reviews/', GetAllReview.as_view(), name='get_all_review'),
    
    
    # DELETE 요청으로 리뷰 삭제
    path('videos/<int:video_id>/reviews/<int:review_id>/delete/', DeleteReview.as_view(), name='delete_review'),
    
    # PUT 요청으로 리뷰 수정
    path('videos/<int:video_id>/reviews/<int:review_id>/update/', PutReview.as_view(), name='update_review'),
      
]



