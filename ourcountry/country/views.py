import email

from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import *
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from rest_framework.response import Response
from django.db.models import Avg, Case, When, Value, IntegerField
from rest_framework import permissions
from rest_framework import filters
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated


# FOR CHARLES DEO

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if isinstance(request.user, AnonymousUser):
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Получаем профиль пользователя по email (или другому полю, связанному с пользователем)
            user_profile = UserProfile.objects.get(email=request.user.email)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Сериализуем данные с partial=True для частичного обновления
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Возвращаем ошибки валидации, если данные невалидны
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(email=self.request.user.email)

# FOR HOME


class HomeListAPIView(generics.ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class AttractionsListAPIView(generics.ListAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionsListSerializer


class AttractionsDetailAPIView(generics.RetrieveAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionsDetailSerializer


class PostAttractionCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='user'),
                'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='post'),
                'like': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='like'),
            },
            required=['user']
        ),
    )
    def patch(self, request, *args, **kwargs):
        serializer = PostAttractionSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttractionReviewListAPIView(generics.ListAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AttractionReviewFilter


class AttractionReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewListSerializer


class AttractionReviewStaticListApiView(generics.ListAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionReviewStaticSerializers

#NEW-----------


class AttractionReviewCreateAPIView(generics.CreateAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            attraction_review = serializer.save()
            response_serializer = AttractionReviewSerializer(attraction_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyToAttractionReviewView(generics.CreateAPIView):
    queryset = ReplyToAttractionReview.objects.all()
    serializer_class = ReplyToAttractionReviewSerializer

# FOR REGIONS


class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class PostPopularPlacesCreateApiView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='user'),
                'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='post'),
                'like': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='like'),
            },
            required=['user']
        ),
    )
    def patch(self, request, *args, **kwargs):
        serializer = PostPopularSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PopularPlacesListAPI(generics.ListAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesListSerializer


class PopularPlacesDetailAPI(generics.RetrieveAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesDetailSerializer


class PopularReviewListAPIView(generics.ListAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PopularReviewFilter


class PopularReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewListSerializer

#NEW-----------
class PopularPlacesStaticAPIView(generics.ListAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesStaticSerializer


class PopularReviewCreateAPIView(generics.CreateAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            popular_review = serializer.save()
            response_serializer = PopularReviewSerializer(popular_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyToPopularPlacesCreateView(generics.CreateAPIView):
    queryset = ReplyToPopularReview.objects.all()
    serializer_class = ReplyToPopularPlacesSerializer

#NEW-----------


class ToTryViewSet(viewsets.ModelViewSet):
    queryset = ToTry.objects.all()
    serializer_class = ToTrySerializer


class PostHotelCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='user'),
                'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='post'),
                'like': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='like'),
            },
            required=['user']
        ),
    )
    def patch(self, request, *args, **kwargs):
        serializer = PostHotelSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelsListAPIView(generics.ListAPIView):
    serializer_class = HotelsListSerializer

    def get_queryset(self):
        queryset = Hotels.objects.annotate(
            average_rating=Avg('hotel_reviews__rating'),  # Вычисляем средний рейтинг
            is_popular=Case(
                When(average_rating__gte=4, then=Value(1)),  # Если рейтинг >= 4, помечаем как популярный
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('-is_popular', '-average_rating')  # Сортируем сначала по популярности, затем по рейтингу

        return queryset


class HotelsDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotels.objects.all()
    serializer_class = HotelDetailSerializer


class HotelsReviewListAPIView(generics.ListAPIView):
    queryset = HotelsReview.objects.all()
    serializer_class = HotelReviewListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = HotelsReviewFilter


class HotelsReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = HotelsReview.objects.all()
    serializer_class = HotelReviewListSerializer


class HotelReviewCreateAPiView(generics.CreateAPIView):
    queryset = HotelsReview.objects.all()
    serializer_class = HotelsReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hotel_review = serializer.save()
            response_serializer = HotelsReviewSerializer(hotel_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelsReviewStaticListAPIView(generics.ListAPIView):
    queryset = Hotels.objects.all()
    serializer_class = HotelReviewStaticSerializers


class ReplyToHotelReviewView(generics.CreateAPIView):
    queryset = ReplyToHotelReview.objects.all()
    serializer_class = ReplyToHotelReviewSerializer


# for kitchen

class KitchenListView(generics.ListAPIView):
    serializer_class = KitchenListSerializer

    def get_queryset(self):
        # Аннотируем отели средним рейтингом
        queryset = Kitchen.objects.annotate(
            average_rating=Avg('kitchen_reviews__rating'),  # Вычисляем средний рейтинг
            is_popular=Case(
                When(average_rating__gte=4, then=Value(1)),  # Если рейтинг >= 4, помечаем как популярный
                default=Value(0),  # В противном случае, помечаем как непопулярный
                output_field=IntegerField(),
            )
        ).order_by('-is_popular', '-average_rating')  # Сортируем сначала по популярности, затем по рейтингу

        return queryset


class KitchenDetailView(generics.RetrieveAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenDetailSerializers


class PostKitchenCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='user'),
                'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='post'),
                'like': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='like'),
            },
            required=['user']
        ),
    )
    def patch(self, request, *args, **kwargs):
        serializer = PostKitchenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#NEW-----------

class KitchenReviewCreateAPIView(generics.CreateAPIView):
    queryset = KitchenReview.objects.all()
    serializer_class = KitchenReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            kitchen_review = serializer.save()
            response_serializer = KitchenReviewSerializer(kitchen_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#NEW-----------


class KitchenReviewListAPIView(generics.ListAPIView):
    queryset = KitchenReview.objects.all()
    serializer_class = KitchenReviewListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = KitchenReviewFilter


class KitchenReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = KitchenReview.objects.all()
    serializer_class = KitchenReviewListSerializer


class KitchenReviewStaticAPIView(generics.ListAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenReviewStaticSerializers


class ReplyToKitchenReviewView(generics.CreateAPIView):
    queryset = ReplyToKitchenReview.objects.all()
    serializer_class = ReplyToKitchenReviewSerializer


class EventListAPiView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = EventFilter
    search_fields = ['title']


class TicketListAPIView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializers


class CultureListAPiView(generics.ListAPIView):
    queryset = Culture.objects.all()
    serializer_class = CultureSerializers


class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializers


class NationalClothesViewSet(viewsets.ModelViewSet):
    queryset = NationalClothes.objects.all()
    serializer_class = NationalClothesSerializers


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializers


class HandCraftsViewSet(viewsets.ModelViewSet):
    queryset = HandCrafts.objects.all()
    serializer_class = HandCraftsSerializers


class NationalInstrumentsViewSet(viewsets.ModelViewSet):
    queryset = NationalInstruments.objects.all()
    serializer_class = NationalInstrumentsSerializers


class CultureKitchenViewSet(viewsets.ModelViewSet):
    queryset = CultureKitchen.objects.all()
    serializer_class = CultureKitchenSerializers


class CultureKitchenMainListViewSet(viewsets.ModelViewSet):
    queryset = CultureKitchenMain.objects.all()
    serializer_class = CultureKitchenMainListSerializers


class GalleryListAPIView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializers


class ReplyToGalleryReviewView(generics.CreateAPIView):
    queryset = ReplyToGalleryReview.objects.all()
    serializer_class = ReplyToGalleryReviewSerializer


class PostGalleryCreateAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='user'),
                'post': openapi.Schema(type=openapi.TYPE_INTEGER, description='post'),
                'like': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='like'),
            },
            required=['user']
        ),
    )
    def patch(self, request, *args, **kwargs):
        serializer = PostGallerySerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GalleryReviewCreateAPIView(generics.CreateAPIView):
    queryset = GalleryReview.objects.all()
    serializer_class = GalleryReviewCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            gallery_review = serializer.save()
            response_serializer = GalleryReviewSerializer(gallery_review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryReviewListAPIView(generics.ListAPIView):
    queryset = GalleryReview.objects.all()
    serializer_class = GalleryReviewSerializer


class GalleryReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = GalleryReview.objects.all()
    serializer_class = GalleryReviewSerializer


class AirLineTicketsAPIView(generics.ListAPIView):
    queryset = AirLineTickets.objects.all()
    serializer_class = AirLineTicketsSerializers


# NEW-----------


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        favorite_id = self.kwargs.get('favorite_id')
        return Favorite.objects.get(id=favorite_id, user=self.request.user)

