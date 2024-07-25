import json
import mysql.connector
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class PostReview(View):
    def post(self, request, *args, **kwargs):
        try:
            # JSON 요청 데이터 파싱
            data = json.loads(request.body.decode('utf-8'))
            video_id = data.get('video_id')
            rating = data.get('rating')
            comments = data.get('comments')
            nickname = data.get('nickname')  # 사용자명을 추출

            # 외부 MariaDB에 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor()

            # 사용자명을 통해 사용자 ID를 조회
            cursor.execute('SELECT users_id FROM users WHERE nickname = %s;', (nickname,))
            user_row = cursor.fetchone()

            if not user_row:
                cursor.close()
                conn.close()
                return JsonResponse({'error': 'User not found'}, status=404)

            user_id = user_row[0]

            # 리뷰를 삽입하는 SQL 쿼리
            query = """
                INSERT INTO review (rating, comments, users_id, video_id)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (rating, comments, user_id, video_id))
            conn.commit()

            # 리뷰가 추가된 후, 추가된 리뷰 정보를 반환
            # 커서와 연결 종료
            cursor.close()
            conn.close()

            # 성공 메시지 반환
            response_data = [{
                'video_id': video_id,
                'rating': rating,
                'comments': comments,
                'nickname': nickname
            }]

            return JsonResponse(response_data, safe=False, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class GetAllReview(View):
    def get(self, request, *args, **kwargs):
        try:
            # 외부 MariaDB에 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor(dictionary=True)

            # 리뷰 정보를 선택하는 SQL 쿼리 실행
            cursor.execute('SELECT * FROM review;')
            rows = cursor.fetchall()  # 모든 결과를 가져옵니다.

            # 결과를 JSON 객체로 변환
            response_data = rows

            # 커서 및 연결 종료
            cursor.close()
            conn.close()

            # JSON 응답 반환
            return JsonResponse(response_data, safe=False, status=200, json_dumps_params={'ensure_ascii': False})
        
        except Exception as e:
            # 예외가 발생한 경우
            return JsonResponse({'error': str(e)}, status=500)

        

class GetReview(View):
    def get(self, request, video_id, *args, **kwargs):
        try:
            # 외부 MariaDB에 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor(dictionary=True)

            # 리뷰와 사용자 정보를 조회하는 SQL 쿼리
            query = """
                SELECT r.review_id, r.rating, r.comments, u.nickname 
                FROM review r
                JOIN users u ON r.users_id = u.users_id
                WHERE r.video_id = %s;
            """
            cursor.execute(query, (video_id,))
            reviews = cursor.fetchall()

            # 커서와 연결 종료
            cursor.close()
            conn.close()

            # 결과를 배열 형태로 변환
            response_data = [{'review_id': review['review_id'], 'rating': review['rating'], 'comments': review['comments'], 'nickname': review['nickname']} for review in reviews]

            # JSON 응답 반환
            return JsonResponse(response_data, safe=False, status=200, json_dumps_params={'ensure_ascii': False})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteReview(View):
    def delete(self, request, video_id, review_id, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            nickname = data.get('nickname')

            if not nickname:
                return JsonResponse({'error': 'nickname parameter is required'}, status=400)

            # MariaDB 연결 설정
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor()

            # 사용자명을 사용하여 사용자 ID를 조회
            cursor.execute("SELECT users_id FROM users WHERE nickname = %s;", (nickname,))
            user = cursor.fetchone()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            user_id = user[0]

            # 리뷰 삭제 쿼리
            query = "DELETE FROM review WHERE review_id = %s AND video_id = %s AND users_id = %s;"
            cursor.execute(query, (review_id, video_id, user_id))
            conn.commit()

            # 커서와 연결 종료
            cursor.close()
            conn.close()

            # 성공 메시지 반환
            response_data = [{
                'message': 'Review deleted successfully'
            }]
            return JsonResponse(response_data, safe=False, status=204, json_dumps_params={'ensure_ascii': False})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PutReview(View):
    def put(self, request, video_id, review_id, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            nickname = data.get('nickname') 
            new_rating = data.get('new_rating')
            new_comment = data.get('new_comment')

            if not nickname or not new_rating or not new_comment:
                return JsonResponse({'error': 'nickname, new_rating, and new_comment parameters are required'}, status=400)

            # MariaDB 연결 설정
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor()

            # 닉네임을 사용하여 사용자 ID를 조회
            cursor.execute("SELECT users_id FROM users WHERE nickname = %s;", (nickname,))
            user = cursor.fetchone()
            if not user:
                cursor.close()
                conn.close()
                return JsonResponse({'error': 'User not found'}, status=404)

            user_id = user[0]

            # 리뷰 수정 쿼리
            query = """
                UPDATE review 
                SET rating = %s, comments = %s 
                WHERE review_id = %s AND video_id = %s AND users_id = %s;
            """
            cursor.execute(query, (new_rating, new_comment, review_id, video_id, user_id))
            conn.commit()

            # 리뷰 수정 후 닉네임을 포함하여 리뷰 정보를 가져오는 쿼리
            query = """
                SELECT u.nickname 
                FROM review r
                JOIN users u ON r.users_id = u.users_id
                WHERE r.review_id = %s AND r.video_id = %s;
            """
            cursor.execute(query, (review_id, video_id))
            result = cursor.fetchone()
            updated_nickname = result[0] if result else nickname

            # 커서와 연결 종료
            cursor.close()
            conn.close()

            # 성공 메시지와 변경된 리뷰 정보 반환
            response_data = [{
                'message': 'Review updated successfully',
                'review': {
                    'video_id': video_id,
                    'review_id': review_id,
                    'new_rating': new_rating,
                    'new_comment': new_comment,
                    'nickname': nickname  
                }
            }]
            return JsonResponse(response_data, safe=False, status=200, json_dumps_params={'ensure_ascii': False})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
