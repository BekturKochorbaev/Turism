from rest_framework.templatetags.rest_framework import data

from .serializers import *
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from country.serializers import *
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Сериализация данных пользователя
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Генерация токенов
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            # Подготовка ответа
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({"detail": f"Введенные данные неверны, {e}"}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Сервер не работает, {e}"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Сохранение токенов в cookies
        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=True,  # Для продакшн-среды: используйте secure=True
            samesite='Strict',
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,  # Для продакшн-среды
            samesite='Strict',
        )
        return response
  


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        # Проверяем, что все необходимые поля присутствуют
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'detail': f'Поле {field} обязательно'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            # Генерация токенов
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            response_data = {
                'access': str(access),
                'refresh': str(refresh),
            }

        except serializers.ValidationError:
            return Response({'detail': "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": f"Сервер не работает, {e}"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response_data, status=status.HTTP_200_OK)
        
	    # Установка cookies
        response.set_cookie(
                key='access_token',
                value=str(access),
                httponly=True,
                secure=False,
                samesite='Strict',
            )
        response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Strict',
            )
        return response



class LogoutView(generics.GenericAPIView):
    serializer_class = EmptySerializer  # Пустой сериализатор

    def post(self, request, *args, **kwargs):
        try:
            # Получаем access токен из запроса
            access_token = request.COOKIES.get('access_token')
            if not access_token:
                return Response({'error': 'Access токен отсутствует'}, status=status.HTTP_400_BAD_REQUEST)

	            # Аннулируем токен (черный список)
            try:
                token = AccessToken(access_token)
                token.blacklist()  # Это сработает только если включен Blacklist
            except (TokenError, AttributeError):
                pass  # Если Blacklist не включен, просто игнорируем

            # Подготовка ответа
            response = Response({'message': 'Вы успешно вышли'}, status=status.HTTP_205_RESET_CONTENT)

            # Удаляем токены из cookies
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')

            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# FOR USER_HISTORY_REVIEW


from itertools import chain
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError


class UserCommentsHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # Предполагается, что у пользователя есть профиль UserProfile
        try:
            attraction = AttractionReview.objects.filter(client=user)
            popular_review = PopularReview.objects.filter(client=user)
            hotel_review = HotelsReview.objects.filter(client=user)
            kitchen_review = KitchenReview.objects.filter(client=user)
            gallery_review = GalleryReview.objects.filter(client=user)

            serialized_attraction_review = AttractionReviewSimpleSerializer(attraction, many=True).data
            serialized_popular_review = PopularReviewSimpleSerializer(popular_review, many=True).data
            serialized_hotel_review = HotelsReviewSimpleSerializer(hotel_review, many=True).data
            serialized_kitchen_review = KitchenReviewSimpleSerializer(kitchen_review, many=True).data

            combined_reviews = list(chain(serialized_attraction_review, serialized_popular_review,
                                          serialized_hotel_review, serialized_kitchen_review))
            return Response(combined_reviews)

        except IntegrityError as e:
            return Response(
            {"error": "There was an issue retrieving user comments.", "details": str(e)},
                  status=500
            )


# RESET PSSSWORD

from django_rest_passwordreset.views import ResetPasswordRequestToken
from .serializers import VerifyResetCodeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def verify_reset_code(request):
    serializer = VerifyResetCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def custom_password_reset(request):
    """
    Переопределенный эндпоинт для сброса пароля.
    """
    # Передаем стандартный HttpRequest через request._request
    response = ResetPasswordRequestToken.as_view()(request._request)

    if response.status_code == 200:
        return Response({'status': "Код отправлен"}, status=status.HTTP_200_OK)
    return response

