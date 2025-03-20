from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from rest_framework.response import Response
from django.db.models import Avg, Case, When, Value, IntegerField
from rest_framework import permissions
from rest_framework import filters
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserProfileSerializer, AttractionReviewListSerializer, AttractionReviewStaticSerializers,
    AttractionReviewCreateSerializer, ReplyToAttractionReviewSerializer, AttractionReviewSerializer,
    AttractionsListSerializer, AttractionsDetailSerializer, HomeSerializer, PopularPlacesListSerializer,
    PopularPlacesStaticSerializer, ReplyToPopularPlacesSerializer, ToTrySerializer, RegionSerializer,
    PopularReviewListSerializer, PopularReviewCreateSerializer, PopularPlacesDetailSerializer,
    HotelsListSerializer, HotelReviewListSerializer, HotelDetailSerializer, ReplyToHotelReviewSerializer,
    HotelsReviewCreateSerializer, HotelsReviewSerializer, HotelReviewStaticSerializers, KitchenListSerializer,
    KitchenReviewListSerializer, KitchenDetailSerializers, ReplyToKitchenReviewSerializer,
    KitchenReviewCreateSerializer, KitchenReviewStaticSerializers, EventSerializers, TicketsSerializers,
    CultureSerializers, CultureKitchenMainListSerializers, GamesSerializers, NationalClothesSerializers,
    HandCraftsSerializers, CurrencySerializers, NationalInstrumentsSerializers, CultureKitchenSerializers,
    PopularReviewSerializer, AirLineTicketsSerializers, FavoriteSerializer, FavoriteListSerializer,
    KitchenReviewSerializer
)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_profile = UserProfile.objects.get(email=request.user.email)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(email=self.request.user.email)


class HomeListAPIView(generics.ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer


class AttractionsListAPIView(generics.ListAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionsListSerializer


class AttractionsDetailAPIView(generics.RetrieveAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionsDetailSerializer


class AttractionReviewListAPIView(generics.ListAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
    filterset_class = AttractionReviewFilter


class AttractionReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = AttractionReview.objects.all()
    serializer_class = AttractionReviewListSerializer


class AttractionReviewStaticListApiView(generics.ListAPIView):
    queryset = Attractions.objects.all()
    serializer_class = AttractionReviewStaticSerializers


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


class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class PopularPlacesListAPI(generics.ListAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesListSerializer


class PopularPlacesDetailAPI(generics.RetrieveAPIView):
    queryset = PopularPlaces.objects.all()
    serializer_class = PopularPlacesDetailSerializer


class PopularReviewListAPIView(generics.ListAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
    filterset_class = PopularReviewFilter


class PopularReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = PopularReview.objects.all()
    serializer_class = PopularReviewListSerializer


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


class ToTryViewSet(viewsets.ModelViewSet):
    queryset = ToTry.objects.all()
    serializer_class = ToTrySerializer


class HotelsListAPIView(generics.ListAPIView):
    serializer_class = HotelsListSerializer

    def get_queryset(self):
        queryset = Hotels.objects.annotate(
            average_rating=Avg('hotel_reviews__rating'),
            is_popular=Case(
                When(average_rating__gte=4, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('-is_popular', '-average_rating')
        return queryset


class HotelsDetailAPIView(generics.RetrieveAPIView):
    queryset = Hotels.objects.all()
    serializer_class = HotelDetailSerializer


class HotelsReviewListAPIView(generics.ListAPIView):
    queryset = HotelsReview.objects.all()
    serializer_class = HotelReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
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


class KitchenListView(generics.ListAPIView):
    serializer_class = KitchenListSerializer

    def get_queryset(self):
        queryset = Kitchen.objects.annotate(
            average_rating=Avg('kitchen_reviews__rating'),
            is_popular=Case(
                When(average_rating__gte=4, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('-is_popular', '-average_rating')
        return queryset


class KitchenDetailView(generics.RetrieveAPIView):
    queryset = Kitchen.objects.all()
    serializer_class = KitchenDetailSerializers


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


class KitchenReviewListAPIView(generics.ListAPIView):
    queryset = KitchenReview.objects.all()
    serializer_class = KitchenReviewListSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['comment']
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


class AirLineTicketsAPIView(generics.ListAPIView):
    queryset = AirLineTickets.objects.all()
    serializer_class = AirLineTicketsSerializers


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteCreateView(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        attractions_id = self.request.data.get('attractions')
        popular_place_id = self.request.data.get('popular_place')
        kitchen_id = self.request.data.get('kitchen')
        hotels_id = self.request.data.get('hotels')

        attractions = Attractions.objects.get(pk=attractions_id) if attractions_id else None
        popular_place = PopularPlaces.objects.get(pk=popular_place_id) if popular_place_id else None
        kitchen = Kitchen.objects.get(pk=kitchen_id) if kitchen_id else None
        hotels = Hotels.objects.get(pk=hotels_id) if hotels_id else None

        serializer.save(
            user=self.request.user,
            attractions=attractions,
            popular_place=popular_place,
            kitchen=kitchen,
            hotels=hotels
        )


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        favorite_id = self.kwargs.get('favorite_id')
        return Favorite.objects.get(id=favorite_id, user=self.request.user)