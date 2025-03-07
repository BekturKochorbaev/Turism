import email

from django.shortcuts import render
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

class PostAttractionCreateAPIView(generics.CreateAPIView):
    serializer_class = PostAttractionSerializer


class AttractionReviewListAPIView(generics.ListAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AttractionReviewFilter


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


class ReplyToAttractionReviewListView(generics.ListAPIView):
    queryset = ReplyToAttractionReview.objects.all()
    serializer_class = ReplyToAttractionReviewListSerializer



#NEW-----------



# FOR REGIONS


class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer



class PostPopularPlacesCreateApiView(generics.CreateAPIView):
    serializer_class = PostPopularSerializer


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

#NEW-----------

class ToTryViewSet(viewsets.ModelViewSet):
    queryset = ToTry.objects.all()
    serializer_class = ToTrySerializer



class PostHotelCreateAPIView(generics.CreateAPIView):
    serializer_class = PostHotelSerializer



class HotelsListAPIView(generics.ListAPIView):
    serializer_class = HotelsListSerializer

    def get_queryset(self):
        # Аннотируем отели средним рейтингом
        queryset = Hotels.objects.annotate(
            average_rating=Avg('hotel_reviews__rating'),  # Вычисляем средний рейтинг
            is_popular=Case(
                When(average_rating__gte=4, then=Value(1)),  # Если рейтинг >= 4, помечаем как популярный
                default=Value(0),  # В противном случае, помечаем как непопулярный
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

class PostKitchenCreateAPIView(generics.CreateAPIView):
    serializer_class = PostKitchenSerializer



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


class KitchenReviewStaticAPIView(generics.ListAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenReviewStaticSerializers



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

class PostGalleryCreateAPIView(generics.CreateAPIView):
    serializer_class = PostGallerySerializer




# NEW-----------

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

# NEW-----------

class FavoriteItemViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializers

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Favorite.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteItemSerializers

    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
