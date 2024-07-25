from django.http import JsonResponse
import mysql.connector
from django.conf import settings
from django.views import View

class GetVideos(View):
    def get(self, request, video_id, *args, **kwargs):
        try:
            # 데이터베이스 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor(dictionary=True)  # 커서를 딕셔너리 형태로 사용합니다.

            # 특정 비디오 정보를 선택하는 SQL 쿼리
            query = 'SELECT * FROM video WHERE video_id = %s;'
            cursor.execute(query, (video_id,))
            row = cursor.fetchone()  # 단일 결과를 가져옵니다.

            # 커서 및 연결 종료
            cursor.close()
            conn.close()

            if row:
                # 결과가 있는 경우
                return JsonResponse({"video": row}, status=200)
            else:
                # 비디오 ID가 존재하지 않는 경우
                return JsonResponse({'error': 'Video not found'}, status=404)

        except Exception as e:
            # 예외가 발생한 경우
            return JsonResponse({'error': str(e)}, status=500)
        

class GetVideosAddress(View):
    def get(self, request, video_id, *args, **kwargs):
        try:
            # 데이터베이스 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor(dictionary=True)  # 커서를 딕셔너리 형태로 사용합니다.

            # 비디오 주소를 선택하는 SQL 쿼리
            query = 'SELECT video_addr FROM video WHERE video_id = %s;'
            cursor.execute(query, (video_id,))  # video_id를 쿼리에 바인딩합니다.
            row = cursor.fetchone()  # 단일 결과를 가져옵니다.

            # 커서 및 연결 종료
            cursor.close()
            conn.close()

            if row:
                # 결과가 있는 경우
                return JsonResponse({"video_addr": row['video_addr']}, status=200)
            else:
                # 비디오 ID가 존재하지 않는 경우
                return JsonResponse({'error': 'Video not found'}, status=404)

        except Exception as e:
            # 예외가 발생한 경우
            return JsonResponse({'error': str(e)}, status=500)
        

