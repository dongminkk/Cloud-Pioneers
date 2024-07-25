from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views import View
import mysql.connector
from django.conf import settings
import json

class GetAllUsers(View):
    def get(self, request, *args, **kwargs):
        try:
            # 데이터베이스 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor(dictionary=True)  # 커서를 딕셔너리 형태로 사용합니다.

            # 사용자 정보를 선택하는 SQL 쿼리를 실행합니다.
            cursor.execute('SELECT * FROM users;')
            rows = cursor.fetchall()  # 모든 결과를 가져옵니다.

            # 결과를 하나의 JSON 객체로 변환
            response_data = rows

            # 커서 및 연결 종료
            cursor.close()
            conn.close()

            # JSON 응답 반환
            return JsonResponse(response_data, safe=False, status=200)
        
        except Exception as e:
            # 예외가 발생한 경우
            return JsonResponse({'error': str(e)}, status=500)

class GetUser(View):
    def get(self, request, users_id, *args, **kwargs):
        try:
            # 데이터베이스 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor(dictionary=True)
            
            # 특정 사용자 정보를 선택하는 SQL 쿼리
            query = 'SELECT * FROM users WHERE users_id = %s;'
            cursor.execute(query, (users_id,))
            row = cursor.fetchone()

            # 커서 및 연결 종료
            cursor.close()
            conn.close()

            if row:
                return JsonResponse([row], safe=False, status=200)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class PutUser(View):
    def put(self, request, users_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')

            # 데이터베이스 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor()

            # 사용자 정보를 업데이트하는 SQL 쿼리
            query = 'UPDATE users SET username = %s, email = %s WHERE users_id = %s;'
            cursor.execute(query, (username, email, users_id))
            conn.commit()

            # 커서 및 연결 종료
            cursor.close()
            conn.close()

            return JsonResponse({'message': 'User updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class DeleteUser(View):
    def delete(self, request, users_id, *args, **kwargs):
        try:
            # 데이터베이스 연결
            conn = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME']
            )
            cursor = conn.cursor()

            # 사용자 정보를 삭제하는 SQL 쿼리
            query = 'DELETE FROM users WHERE users_id = %s;'
            cursor.execute(query, (users_id,))
            conn.commit()

            # 커서 및 연결 종료
            cursor.close()
            conn.close()

            return JsonResponse({'message': 'User deleted successfully'}, status=204)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class Login(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('users_id')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                # 로그인 성공
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                # 로그인 실패
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
