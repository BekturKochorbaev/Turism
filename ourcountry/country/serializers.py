from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


# FOR CHARLES DEO

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'user_picture', 'from_user', 'cover_photo', "birth_date"]


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'user_picture', 'from_user']


# FOR Attraction

class AttractionsReviewImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = AttractionsReviewImage
        fields = ['id', 'image']


class ReplyToAttractionReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = ReplyToAttractionReview
        fields = ['id', 'user', 'comment']


class AttractionReviewListSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    attractions = serializers.SlugRelatedField(
        queryset=Attractions.objects.all(),
        slug_field='attraction_name'
    )
    attraction_review_image = AttractionsReviewImageSerializers(read_only=True, many=True)
    count_like = serializers.SerializerMethodField()
    reply_attraction_reviews = ReplyToAttractionReviewListSerializer(read_only=True, many=True)


    class Meta:
        model = AttractionReview
        fields = ['id', 'client', 'attractions', 'comment', 'attraction_review_image',
                  'count_like', 'reply_attraction_reviews']


    def count_like(self, obj):
        return obj.count_like()


class PostAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttraction
        fields = '__all__'


#NEW-----------


class AttractionReviewStaticSerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    excellent = serializers.SerializerMethodField()
    good = serializers.SerializerMethodField()
    not_bad = serializers.SerializerMethodField()
    bad = serializers.SerializerMethodField()
    terribly= serializers.SerializerMethodField()

    class Meta:
        model = Attractions
        fields = ['id', 'attraction_name', 'avg_rating', "rating_count", 'excellent', 'good', 'not_bad', 'bad',
                  'terribly']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()

    def get_excellent(self, obj):
        return obj.get_excellent()

    def get_good(self, obj):
        return obj.get_good()

    def get_not_bad(self, obj):
        return obj.get_not_bad()

    def get_bad(self, obj):
        return obj.get_bad()

    def get_terribly(self, obj):
        return obj.get_terribly()


class AttractionReviewCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = AttractionReview
        fields = ['id', 'client', 'attractions', 'comment', 'rating', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        attraction_review = AttractionReview.objects.create(**validated_data)

        for image in images:
            AttractionsReviewImage.objects.create(attractions=attraction_review, image=image)

        return attraction_review

#NEW-----------


class ReplyToAttractionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToAttractionReview
        fields = ['review', 'comment', 'user']


class AttractionReviewSerializer(serializers.ModelSerializer):
    attraction_review_image = AttractionsReviewImageSerializers(many=True, read_only=True)

    class Meta:
        model = AttractionReview
        fields = ['id', 'client', 'attractions', 'comment', 'rating', 'created_date',
                  'attraction_review_image', ]


class AttractionsImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = AttractionsImage
        fields = ['id', 'image']


class AttractionsListSerializer(serializers.ModelSerializer):
    region_category = serializers.SlugRelatedField(
        queryset=Region_Categoty.objects.all(),#Liliya
        slug_field='region_category'
    )
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()


    class Meta:
        model = Attractions
        fields = ['id', 'attraction_name', 'region_category', 'main_image', 'description', 'popular_places',
                  'avg_rating', 'rating_count']


    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()


class AttractionsDetailSerializer(serializers.ModelSerializer):
    rating_count = serializers.SerializerMethodField()
    image = AttractionsImageSerializers(read_only=True, many=True)
    rank = serializers.SerializerMethodField()
    attractions_review = AttractionReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = Attractions
        fields = ['id', 'attraction_name', "main_image", 'image', 'description', 'type_attraction',
                  'rating_count', 'rank', 'attractions_review']


    def get_rating_count(self, obj):
        return obj.get_rating_count()

    def get_rank(self, obj):
        return obj.get_place()


class HomeSerializer(serializers.ModelSerializer):
    attractions_home = AttractionsListSerializer(read_only=True, many=True)

    class Meta:
        model = Home
        fields = ['id', 'home_name', 'home_image', 'home_description', 'attractions_home']


# FOR REGIONS


class PopularPlacesListSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(
        slug_field='region_name',
        queryset=Region.objects.all()
    )
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    class Meta:
        model = PopularPlaces
        fields = ['id', 'popular_name', 'popular_image', 'region', 'avg_rating', 'rating_count', 'latitude', 'longitude']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()

#NEW---------------------


class PopularPlacesStaticSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    excellent = serializers.SerializerMethodField()
    good = serializers.SerializerMethodField()
    not_bad = serializers.SerializerMethodField()
    bad = serializers.SerializerMethodField()
    terribly= serializers.SerializerMethodField()
    class Meta:
        model = PopularPlaces
        fields = ['id', 'popular_name', 'avg_rating', 'rating_count', 'excellent', 'good', 'not_bad', 'bad',
                  'terribly']


    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()

    def get_excellent(self, obj):
        return obj.get_excellent()

    def get_good(self, obj):
        return obj.get_good()

    def get_not_bad(self, obj):
        return obj.get_not_bad()

    def get_bad(self, obj):
        return obj.get_bad()

    def get_terribly(self, obj):
        return obj.get_terribly()


class ReplyToPopularPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToPopularReview
        fields = ['review', 'comment', 'user']


#NEW---------------------

class ToTrySerializer(serializers.ModelSerializer):

    class Meta:
        model = ToTry
        fields = ['id', 'to_name', 'first_description',  'second_description', 'image']




class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image']


class RegionSerializer(serializers.ModelSerializer):
    popular_places = PopularPlacesListSerializer(read_only=True, many=True)
    What_to_try = ToTrySerializer(read_only=True, many=True)
    region_category = serializers.SlugRelatedField(
        slug_field='region_category',
        queryset=Region_Categoty.objects.all()

    )

    class Meta:
        model = Region
        fields = ['id', 'region_name', 'region_image', 'region_description', 'What_to_try', 'popular_places', 'region_category']


class ReplyToPopularPlacesListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = ReplyToAttractionReview
        fields = ['id', 'user', 'comment']


class PopularReviewListSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    review_image = ReviewImageSerializer(read_only=True, many=True)
    count_like = serializers.SerializerMethodField()
    reply_popular_places = ReplyToPopularPlacesListSerializer(read_only=True, many=True)

    class Meta:
        model = PopularReview
        fields = ['id', 'client', 'created_date', 'comment', 'review_image', 'count_like', 'reply_popular_places']

    def count_like(self, obj):
        return obj.count_like()


class PostPopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPopular
        fields = '__all__'

#NEW-----------


class PopularReviewCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = PopularReview
        fields = ['client', 'popular', 'comment', 'rating', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        popular_review = PopularReview.objects.create(**validated_data)

        for image in images:
            ReviewImage.objects.create(review=popular_review, image=image)

        return popular_review

#NEW-----------


class PopularPlacesDetailSerializer(serializers.ModelSerializer):
    popular_reviews = PopularReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = PopularPlaces
        fields = ['id', 'popular_name', 'popular_image', 'description', 'popular_reviews', 'latitude', 'longitude']

# FOR Hotels


class AmenitiesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = ['id', 'amenity', 'icon']


class SafetyAndHygieneSerializers(serializers.ModelSerializer):
    class Meta:
        model = SafetyAndHygiene
        fields = ['id', 'name']


class HotelImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelsImage
        fields = ['id', 'image']


class HotelsListSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    region = serializers.SlugRelatedField(
        slug_field='region_category',
        queryset=Region_Categoty.objects.all()  #Liliya
    )

    class Meta:
        model = Hotels
        fields = ['id', 'name', 'main_image', 'avg_rating', 'rating_count', 'region', 'popular_places','latitude', 'longitude']


    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()


class ReplyToHotelReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = ReplyToHotelReview
        fields = ['id', 'user', 'comment']


class HotelReviewListSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    hotel_review_image = HotelImageSerializers(read_only=True, many=True)
    count_like =serializers.SerializerMethodField()
    reply_hotel_reviews = ReplyToHotelReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = HotelsReview
        fields = ['id', 'client', 'hotel', 'comment', 'hotel_review_image', 'count_like', 'reply_hotel_reviews']

    def count_like(self, obj):
        return obj.count_like()


class HotelDetailSerializer(serializers.ModelSerializer):
    hotel_image = HotelImageSerializers(read_only=True, many=True)
    hotel_reviews = HotelReviewListSerializer(read_only=True, many=True)
    amenities = AmenitiesSerializers(read_only=True, many=True)
    safety_and_hygiene = SafetyAndHygieneSerializers(read_only=True, many=True)

    class Meta:
        model = Hotels
        fields = ['id', 'name', 'hotel_image', 'address', 'description', 'bedroom', 'bathroom', 'cars', 'bikes',
                  'pets', 'amenities', 'safety_and_hygiene', 'price_short_period', 'price_medium_period', 'price_long_period', 'hotel_reviews']


class ReplyToHotelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToHotelReview
        fields = ['review', 'comment', 'user']


class PostHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHotel
        fields = '__all__'                 


class HotelsReviewImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = HotelsReviewImage
        fields = ['id', 'image']


#NEW-----------

class HotelsReviewCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = HotelsReview
        fields = ['client', 'comment', 'hotel', 'rating', "images"]

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        hotel_review_create = HotelsReview.objects.create(**validated_data)

        for image in images:
            HotelsReviewImage.objects.create(hotel_review=hotel_review_create, image=image)

        return hotel_review_create

#NEW-----------


class HotelsReviewSerializer(serializers.ModelSerializer):
    client_hotel = UserProfileSimpleSerializer(read_only=True)
    hotel = serializers.SlugRelatedField(
        queryset=Hotels.objects.all(),
        slug_field='name'
    )
    hotel_review_image = HotelsReviewImageSerializers(read_only=True, many=True)

    class Meta:
        model = HotelsReview
        fields = '__all__'


class HotelReviewStaticSerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    excellent = serializers.SerializerMethodField()
    good = serializers.SerializerMethodField()
    not_bad = serializers.SerializerMethodField()
    bad = serializers.SerializerMethodField()
    terribly= serializers.SerializerMethodField()

    class Meta:
        model = Hotels
        fields = ['id', 'avg_rating', 'rating_count', 'excellent', 'good', 'not_bad', 'bad',
                  'terribly', 'name']

    def get_avg_rating(self, obj):
            return obj.get_avg_rating()

    def get_rating_count(self, obj):
            return obj.get_rating_count()

    def get_excellent(self, obj):
            return obj.get_excellent()

    def get_good(self, obj):
            return obj.get_good()

    def get_not_bad(self, obj):
            return obj.get_not_bad()

    def get_bad(self, obj):
            return obj.get_bad()

    def get_terribly(self, obj):
            return obj.get_terribly()


# FOR KITCHEN

class KitchenImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = KitchenImage
        fields = ['id', 'image']


class KitchenLocationSerializers(serializers.ModelSerializer):
    kitchen = serializers.SlugRelatedField(
        slug_field='kitchen_name',
        queryset=Kitchen.objects.all()
    )

    class Meta:
        model = KitchenLocation
        fields = ['id', 'address', 'Website', "email", 'phone_number', 'kitchen', 'latitude', 'longitude']


class KitchenListSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    kitchen_region = serializers.SlugRelatedField(
        queryset=Region_Categoty.objects.all(),  #Liliya
        slug_field='region_category'
    )

    class Meta:
        model = Kitchen
        fields = ['id', 'kitchen_name', 'price', 'popular_places', 'kitchen_region', 'type_of_cafe', 'average_rating', 'rating_count', 'main_image']


    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()


class KitchenReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenReviewImage
        fields = ['id', 'image']


class ReplyToKitchenReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = ReplyToKitchenReview
        fields = ['id', 'user', 'comment']


class KitchenReviewListSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    kitchen_region = serializers.SlugRelatedField(
        queryset=Kitchen.objects.all(),
        slug_field='kitchen_name'
    )
    kitchen_review_image = KitchenReviewImageSerializer(read_only=True, many=True)
    count_like = serializers.SerializerMethodField()
    reply_kitchen_reviews = ReplyToKitchenReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = KitchenReview
        fields = ['id', 'client', 'kitchen_region', 'comment',
                  'created_at', 'kitchen_review_image', 'count_like', 'reply_kitchen_reviews']

    def count_like(self, obj):
        return obj.count_like()


class KitchenDetailSerializers(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    kitchen_image = KitchenImageSerializers(read_only=True, many=True)
    nutrition_rating = serializers.SerializerMethodField()
    service_rating = serializers.SerializerMethodField()
    price_rating = serializers.SerializerMethodField()
    atmosphere_rating = serializers.SerializerMethodField()
    kitchen = KitchenLocationSerializers(read_only=True, many=True)
    kitchen_reviews = KitchenReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = Kitchen
        fields = ['id', 'kitchen_name', 'main_image', 'kitchen_image', 'price', 'specialized_menu', 'meal_time', 'description',
                  'average_rating', 'rating_count', 'nutrition_rating', 'service_rating', 'price_rating',
                  'atmosphere_rating', 'kitchen', 'kitchen_reviews']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()

    def get_nutrition_rating(self, obj):
        return obj.get_nutrition_rating()

    def get_service_rating(self, obj):
        return obj.get_service_rating()

    def get_price_rating(self, obj):
        return obj.get_price_rating()

    def get_atmosphere_rating(self, obj):
        return obj.get_atmosphere_rating()


class ReplyToKitchenReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToKitchenReview
        fields = ['review', 'comment', 'user']


class PostKitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostKitchen
        fields = '__all__'


#NEW-----------

class KitchenReviewCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = KitchenReview
        fields = ['client', 'kitchen_region', 'comment', 'rating',
                  'nutrition_rating', 'service_rating', 'price_rating', 'atmosphere_rating', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        kitchen_review_create = KitchenReview.objects.create(**validated_data)

        for image in images:
            KitchenReviewImage.objects.create(review=kitchen_review_create, image=image)

        return kitchen_review_create


class KitchenReviewStaticSerializers(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    excellent = serializers.SerializerMethodField()
    good = serializers.SerializerMethodField()
    not_bad = serializers.SerializerMethodField()
    bad = serializers.SerializerMethodField()
    terribly= serializers.SerializerMethodField()


    class Meta:
        model = Kitchen
        fields = ['id', 'kitchen_name', 'average_rating', 'rating_count', 'excellent', 'good', 'not_bad', 'bad',
                  'terribly']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()

    def get_excellent(self, obj):
            return obj.get_excellent()

    def get_good(self, obj):
            return obj.get_good()

    def get_not_bad(self, obj):
            return obj.get_not_bad()

    def get_bad(self, obj):
            return obj.get_bad()

    def get_terribly(self, obj):
            return obj.get_terribly()

#NEW-----------


class EventCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = EventCategories
        fields = ['id', 'category']


class EventSerializers(serializers.ModelSerializer):
    category = EventCategorySerializers(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'image', 'category', 'date', 'time', 'address', 'price']


class TicketsSerializers(serializers.ModelSerializer):
    concert = serializers.SlugRelatedField(
        queryset=EventCategories.objects.all(),
        slug_field='category'
    )
    class Meta:
        model = Ticket
        fields = ['id', 'concert', 'title', 'image', 'date', 'time', 'address', 'price']


class CultureSerializers(serializers.ModelSerializer):
    class Meta:
        model = Culture
        fields = ['id', 'culture_name', 'culture_description', 'culture_image']


class CultureKitchenMainListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CultureKitchenMain
        fields = ['id', 'culture', 'title', 'description', 'image_1', 'image_2', 'image_3', 'image_4']


class CultureSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = CultureCategory
        fields = ['id', 'culture_name']


class GamesSerializers(serializers.ModelSerializer):
    culture = CultureSimpleSerializers(read_only=True)

    class Meta:
        model = Games
        fields = ['id', "culture", 'games_name', 'games_description', 'games_image']


class NationalClothesSerializers(serializers.ModelSerializer):
    class Meta:
        model = NationalClothes
        fields = ['id', "culture", 'clothes_name', 'clothes_description', 'clothes_image']


class HandCraftsSerializers(serializers.ModelSerializer):
    culture = CultureSimpleSerializers(read_only=True)

    class Meta:
        model = HandCrafts
        fields = ["id", 'culture', 'hand_name', 'hand_description', 'hand_image']


#FOR CURRENCY

class Currency_DescriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Currency_Description
        fields = ['description']


class Currency_ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Currency_Image
        fields = ['front_image', 'back_image']


class CurrencySerializers(serializers.ModelSerializer):
    culture = CultureSimpleSerializers(read_only=True)
    currency_description = Currency_DescriptionSerializers(read_only=True, many=True)
    currency_image = Currency_ImageSerializers(read_only=True, many=True)


    class Meta:
        model = Currency
        fields = ['id',  "culture", 'currency_name', 'currency_description', 'currency_image']


class NationalInstrumentsSerializers(serializers.ModelSerializer):
    culture = CultureSimpleSerializers(read_only=True)

    class Meta:
        model = NationalInstruments
        fields = ['id',  "culture", 'national_name', 'national_description', 'national_image']


class CultureKitchenImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = CultureKitchenImage
        fields = ['id', 'image']


class CultureKitchenSerializers(serializers.ModelSerializer):
    culture = CultureSimpleSerializers(read_only=True)
    culture_kitchen_image = CultureKitchenImageSerializers(read_only=True, many=True)

    class Meta:
        model = CultureKitchen
        fields = ['id',  "culture", 'kitchen_name', 'kitchen_description', 'culture_kitchen_image']


#NEW-----------

class GalleryReviewCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = GalleryReview
        fields = ['id', 'client', 'comment', 'gallery', 'rating', 'images']


    def create(self, validated_data):
        images = validated_data.pop('images', [])
        gallery_review_create = GalleryReview.objects.create(**validated_data)

        for image in images:
            GalleryReviewImage.objects.create(gallery=gallery_review_create, image=image)

        return gallery_review_create


class ReplyToGalleryReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyToGalleryReview
        fields = ['review', 'comment', 'user']


class PostGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostGallery
        fields = '__all__'


#NEW-----------

class GalleryReviewImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = GalleryReviewImage
        fields = ['id', 'image']


class GallerySerializers(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ['id', 'gallery_name', 'gallery_image', 'address', 'avg_rating', 'rating_count',]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_rating_count(self, obj):
        return obj.get_rating_count()




# FOR USER_HISTORY_REVIEW

class AttractionReviewSerializer(serializers.ModelSerializer):
    client_home = UserProfileSimpleSerializer(read_only=True)
    attractions = serializers.SlugRelatedField(
        queryset=Attractions.objects.all(),
        slug_field='attraction_name'
    )
    attraction_review_image = AttractionsReviewImageSerializers(read_only=True, many=True)

    class Meta:
        model = AttractionReview
        fields = '__all__'


class PopularReviewSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    popular = serializers.SlugRelatedField(
        queryset=PopularPlaces.objects.all(),
        slug_field='popular_name'
    )
    review_image = ReviewImageSerializer(read_only=True, many=True)

    class Meta:
        model = PopularReview
        fields = '__all__'




class KitchenReviewSerializer(serializers.ModelSerializer):
    client_kitchen = UserProfileSimpleSerializer(read_only=True)
    kitchen_region = serializers.SlugRelatedField(
        queryset=Kitchen.objects.all(),
        slug_field='kitchen_name'
    )
    kitchen_review_image = KitchenReviewImageSerializer(read_only=True, many=True)

    class Meta:
        model = KitchenReview
        fields = '__all__'


class ReplyToGalleryReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = ReplyToGalleryReview
        fields = ['id', 'user', 'comment']


class GalleryReviewSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    gallery = serializers.SlugRelatedField(
        queryset=Gallery.objects.all(),
        slug_field='gallery_name'
    )
    gallery_review_image = GalleryReviewImageSerializers(read_only=True, many=True)
    count_like = serializers.SerializerMethodField()
    reply_gallery_reviews = ReplyToGalleryReviewListSerializer(read_only=True, many=True)

    class Meta:
        model = GalleryReview
        fields = ['id', 'client', 'comment', 'gallery', 'rating', 'count_like', 'gallery_review_image',
                  'created_date', 'reply_gallery_reviews']

    def count_like(self, obj):
        return obj.count_like()


class FavoriteItemSerializers(serializers.ModelSerializer):
    attractions = AttractionsListSerializer(read_only=True)
    popular_region = PopularPlacesListSerializer(read_only=True)
    gallery = GallerySerializers(read_only=True)
    hotels = HotelsListSerializer(read_only=True)

    class Meta:
        model = FavoriteItem
        fields = ['id', 'attractions', 'popular_region', 'gallery', 'hotels']


class FavoriteSerializers(serializers.ModelSerializer):
    items = FavoriteItemSerializers(read_only=True, many=True)

    class Meta:
        model = FavoriteItem
        fields = ['user', 'items']


