from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField


class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('У пользователя должен быть указан email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    username = None  # Убираем поле username
    email = models.EmailField(unique=True)  # Уникальный email для аутентификации
    phone_number = PhoneNumberField(region=None, null=True, blank=True)
    user_picture = models.ImageField(upload_to='user_pictures/', null=True, blank=True)
    from_user = models.CharField(max_length=62)
    cover_photo = models.ImageField(upload_to='cover_photo/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'  # Устанавливаем email в качестве идентификатора
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Поля, обязательные при создании суперпользователя

    objects = UserProfileManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# FOR HOME


class Region_Categoty(models.Model):
    CHOICES = (
        ('Chui', 'Chui'),
        ('Talas', 'Talas'),
        ('Batken', 'Batken'),
        ('Osh', 'Osh'),
        ('Naryn', 'Naryn'),
        ('Issyk-Kul', 'Issyk-Kul'),
        ('Jalal-Abad', 'Jalal-Abad'),
    )
    region_category = models.CharField(max_length=20, choices=CHOICES)

    def __str__(self):
        return self.region_category


class Region(models.Model):
    region_name = models.CharField(max_length=55)
    region_image = models.ImageField(upload_to='region_images')
    region_description = models.TextField()
    region_category = models.ForeignKey(Region_Categoty, on_delete=models.CASCADE, related_name='region')
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта') 

    def __str__(self):
        return self.region_name


class Home(models.Model):
    home_name = models.CharField(max_length=55)
    home_image = models.ImageField(upload_to='home_images', null=True, blank=True)
    home_description = models.TextField()

    def __str__(self):
        return self.home_name


class PopularPlaces(models.Model):
    popular_name = models.CharField(max_length=250)
    popular_image = models.ImageField(upload_to='popular_images')
    description = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='popular_places')
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта') 
    address = models.CharField(max_length=250, null=True, blank=True)
    def __str__(self):
        return f'{self.popular_name}'

    def get_avg_rating(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def get_excellent(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0

    def get_avg_rating(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.popular_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def get_attraction_len(self):
        len = self.popular_places.all()
        if len.exists():
            return len.count()
        return 0


class Attractions(models.Model):
    attraction_name = models.CharField(max_length=155)
    description = models.TextField()
    region_category = models.ForeignKey(Region_Categoty, on_delete=models.CASCADE, null=True, blank=True)#Liliya
    popular_places = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE, related_name='popular_places', null=True, blank=True)#Liliya
    main_image = models.ImageField(upload_to='main_image/', null=True, blank=True)
    type_attraction = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.attraction_name

    # NEW-----------

    def get_excellent(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0

    def get_avg_rating(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.attractions_review.all()
        if ratings.exists():
            return ratings.count()
        return 0


    @staticmethod
    def get_attractions_by_excellent():
        attractions = Attractions.objects.all()
        sorted_attractions = sorted(attractions, key=lambda attraction: attraction.get_excellent(), reverse=True)
        for index, attraction in enumerate(sorted_attractions):
            attraction.rank = index + 1

        return sorted_attractions

    def get_place(self):
        sorted_attractions = Attractions.get_attractions_by_excellent()
        for index, attraction in enumerate(sorted_attractions):
            if attraction == self:
                return index + 1
        return None


class AttractionsImage(models.Model):
    attractions = models.ForeignKey(Attractions, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='attartions_image/', null=True, blank=True)


class AttractionReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='home_reviews')
    attractions = models.ForeignKey(Attractions, on_delete=models.CASCADE, related_name='attractions_review')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True, verbose_name='Рейтинг')
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.client}'

    def count_like(self):
        like = self.post.all()
        if like.exists():
            return like.count()
        return 0


class ReplyToAttractionReview(models.Model):
    review = models.ForeignKey(AttractionReview, on_delete=models.CASCADE, related_name='reply_attraction_reviews')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client')
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class PostAttraction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_attractions')
    post = models.ForeignKey(AttractionReview, on_delete=models.CASCADE, related_name='post')
    like = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} - {self.post}'


class AttractionsReviewImage(models.Model):
    attractions = models.ForeignKey(AttractionReview, on_delete=models.CASCADE, related_name='attraction_review_image')
    image = models.ImageField(upload_to='attraction_review_image/', null=True, blank=True)


# FOR REGIONS


class PopularReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    popular_place = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE,  related_name='popular_reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True, verbose_name='Рейтинг')
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.client}-{self.popular_place}'


    def count_like(self):
        like = self.post_popular.all()
        if like.exists():
            return like.count()
        return 0


class ReplyToPopularReview(models.Model):
    review = models.ForeignKey(PopularReview, on_delete=models.CASCADE, related_name='reply_popular_places')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class PostPopular(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_popular')
    post = models.ForeignKey(PopularReview, on_delete=models.CASCADE, related_name='post_popular')
    like = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} - {self.post}'


class ReviewImage(models.Model):
    review = models.ForeignKey(PopularReview, on_delete=models.CASCADE, related_name='review_image')
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)


class ToTry(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='What_to_try')
    to_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='to_try_image/', null=True, blank=True)
    first_description = models.TextField()
    second_description = models.TextField()
    image = models.ImageField(upload_to='to_try_image/', null=True, blank=True)

    def __str__(self):
        return self.to_name


# FOR Hotels


class Hotels(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    main_image = models.ImageField(upload_to='main_image/', null=True, blank=True)
    region = models.ForeignKey(Region_Categoty, on_delete=models.CASCADE, related_name='hotels_region', null=True, blank=True)#Liliya
    popular_places = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    bedroom = models.PositiveIntegerField(default=1)
    bathroom = models.PositiveIntegerField(default=1)
    cars = models.PositiveIntegerField(default=1)
    bikes = models.PositiveIntegerField(default=1)
    pets = models.PositiveIntegerField()
    price_short_period = models.PositiveIntegerField()
    price_medium_period = models.PositiveIntegerField()
    price_long_period = models.PositiveIntegerField()
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта')

    def __str__(self):
        return self.name

    def get_excellent(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0

    def get_avg_rating(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.hotel_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0


class Amenities(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name="amenities")
    amenity = models.CharField(max_length=55)
    icon = models.FileField(upload_to='icons/')


class SafetyAndHygiene(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='safety_and_hygiene')
    name = models.CharField(max_length=55)


class HotelsImage(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='hotel_image')
    image = models.ImageField(upload_to='hotel_images/', null=True, blank=True)


class HotelsReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_hotel')
    comment = models.TextField()
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE, related_name='hotel_reviews')  # inline
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def count_like(self):
        like = self.post_hotel.all()
        if like.exists():
            return like.count()
        return 0


    def __str__(self):
        return f'{self.client}'


class ReplyToHotelReview(models.Model):
    review = models.ForeignKey(HotelsReview, on_delete=models.CASCADE, related_name='reply_hotel_reviews')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class PostHotel(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_hotel')
    post = models.ForeignKey(HotelsReview, on_delete=models.CASCADE, related_name='post_hotel')
    like = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} - {self.post}'


class HotelsReviewImage(models.Model):
    hotel_review = models.ForeignKey(HotelsReview, on_delete=models.CASCADE, related_name='hotel_review_image')
    image = models.ImageField(upload_to='hotel_review_image/', null=True, blank=True)

# for kitchen


class Kitchen(models.Model):
    kitchen_name = models.CharField(max_length=155)
    description = models.TextField()
    main_image = models.ImageField(upload_to='main_image/', null=True, blank=True)
    kitchen_region = models.ForeignKey(Region_Categoty, on_delete=models.CASCADE, null=True, blank=True)#Liliya
    popular_places = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE, null=True, blank=True)
    price = models.PositiveIntegerField()
    specialized_menu = models.TextField()
    MEAL_TIME = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Brunch', 'Brunch'),
        ('Open Late', 'Open Late'),
        ('Drinks', 'Drinks'),
    )
    meal_time = MultiSelectField(choices=MEAL_TIME)
    TYPE = (
        ('Russian', 'Russian'),
        ('Asian', 'Asian'),
        ('Canadian', 'Canadian'),
        ('Chinese', 'Chinese'),
        ('European', 'European'),
        ('Japan', 'Japan'),
        ('Korean', 'Korean'),
    )
    type_of_cafe = MultiSelectField(choices=TYPE)

    def __str__(self):
        return self.kitchen_name

    def get_average_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.price_rating for rating in ratings if rating.price_rating is not None]
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_rating_count(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0

    def get_nutrition_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.nutrition_rating for rating in ratings if rating.nutrition_rating is not None]

        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return

    def get_service_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.service_rating for rating in ratings if rating.service_rating is not None]

        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_price_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.price_rating for rating in ratings if rating.price_rating is not None]

        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_atmosphere_rating(self):
        ratings = self.kitchen_reviews.all()
        valid_ratings = [rating.atmosphere_rating for rating in ratings if rating.atmosphere_rating is not None]

        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 1)
        return 0

    def get_excellent(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 5:
                    total += 1
            return total
        return 0

    def get_good(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 4:
                    total += 1
            return total
        return 0

    def get_not_bad(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 3:
                    total += 1
            return total
        return 0

    def get_bad(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 2:
                    total += 1
            return total
        return 0

    def get_terribly(self):
        ratings = self.kitchen_reviews.all()
        if ratings.exists():
            total = 0
            for i in ratings:
                if i.rating == 1:
                    total += 1
            return total
        return 0


class KitchenLocation(models.Model):
    address = models.TextField()
    Website = models.URLField(null=True, blank=True)
    email = models.CharField(max_length=60)
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen')
    longitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Долгота')
    latitude = models.CharField(max_length=100, null=True, blank=True, verbose_name='Широта') #inline


class KitchenImage(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_image')
    image = models.ImageField(upload_to='kitchen_images/', null=True, blank=True)


class KitchenReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField()
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, related_name='kitchen_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    nutrition_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    service_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    price_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    atmosphere_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.client}'

    def count_like(self):
        like = self.post_kitchen.all()
        if like.exists():
            return like.count()
        return 0


class ReplyToKitchenReview(models.Model):
    review = models.ForeignKey(KitchenReview, on_delete=models.CASCADE, related_name='reply_kitchen_reviews')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)


class PostKitchen(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_kitchen')
    post = models.ForeignKey(KitchenReview, on_delete=models.CASCADE, related_name='post_kitchen')
    like = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} - {self.post}'


class KitchenReviewImage(models.Model):
    review = models.ForeignKey(KitchenReview, on_delete=models.CASCADE, related_name='kitchen_review_image')
    image = models.ImageField(upload_to='kitchen_review_image/', null=True, blank=True)


# FOR event
#  7 categories


class EventCategories(models.Model):
    CATEGORIES = (
        ('Concert', 'Concert'),
        ('Cinema', 'Cinema'),
        ('Leisure', 'Leisure'),
        ('Exhibitions', 'Exhibitions'),
        ('Theater', 'Theater'),
        ('Master classes', 'Master classes'),
        ('Tourism', 'Tourism'),
    )
    category = models.CharField(max_length=20, choices=CATEGORIES, null=True, blank=True)

    def __str__(self):
        return self.category


class Event(models.Model):
    category = models.ForeignKey(EventCategories, on_delete=models.CASCADE, related_name='event_category')
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    popular_places = models.ForeignKey(PopularPlaces, on_delete=models.CharField, null=True, blank=True)
    title = models.CharField(max_length=52)
    date = models.DateField()
    time = models.TimeField()
    address = models.CharField(max_length=150)
    price = models.PositiveIntegerField()
    ticket = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Ticket(models.Model):
    concert = models.ForeignKey(EventCategories, on_delete=models.CASCADE, related_name='concert')
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    title = models.CharField(max_length=52)
    date = models.DateField()
    time = models.TimeField()
    address = models.CharField(max_length=150)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.title


# FOR GALLERY


class Gallery(models.Model):
    gallery_name = models.CharField(max_length=55)
    gallery_image = models.ImageField(upload_to='gellery_images')
    address = models.CharField(max_length=62)

    def __str__(self):
        return self.gallery_name

    def get_avg_rating(self):
        ratings = self.gallery_reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0

    def get_rating_count(self):
        ratings = self.gallery_reviews.all()
        if ratings.exists():
            return ratings.count()
        return 0


class GalleryReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField()
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='gallery_reviews') #inline
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}'

    def count_like(self):
        like = self.post_gallery.all()
        if like.exists():
            return like.count()
        return 0


class ReplyToGalleryReview(models.Model):
    review = models.ForeignKey(GalleryReview, on_delete=models.CASCADE, related_name='reply_gallery_reviews')
    comment = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class PostGallery(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_gallery')
    post = models.ForeignKey(GalleryReview, on_delete=models.CASCADE, related_name='post_gallery')
    like = models.BooleanField(default=False, null=True, blank=True)
    created_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} - {self.post}'


class GalleryReviewImage(models.Model):
    gallery = models.ForeignKey(GalleryReview, on_delete=models.CASCADE, related_name='gallery_review_image')
    image = models.ImageField(upload_to='gallery_review_image/', null=True, blank=True)

# FOR CULTURE


class CultureCategory(models.Model):
    CATEGORIES = (
        ("Games", "Games"),
        ("National clothes", "National clothes"),
        ("Hand crafts", "Hand crafts"),
        ("Currency", "Currency"),
        ("National instruments", "National instruments"),
        ("Kitchen", "Kitchen"),
    )
    culture_name = models.CharField(max_length=35, choices=CATEGORIES)

    def __str__(self):
        return self.culture_name


class Culture(models.Model):
    culture_name = models.CharField(max_length=35)
    culture_description = models.TextField()
    culture_image = models.ImageField(upload_to='culture-images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.culture_name


class Games(models.Model):
    games_name = models.CharField(max_length=300)
    games_description = models.TextField()
    games_image = models.ImageField(upload_to='games_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.games_name


class NationalClothes(models.Model):
    clothes_name = models.CharField(max_length=300)
    clothes_description = models.TextField()
    clothes_image = models.ImageField(upload_to='clothes_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.clothes_name


class HandCrafts(models.Model):
    hand_name = models.CharField(max_length=300)
    hand_description = models.TextField()
    hand_image = models.ImageField(upload_to='hand_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.hand_name


class Currency(models.Model):
    currency_name = models.CharField(max_length=300)
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.currency_name


class Currency_Description(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_description', null=True, blank=True)
    description = models.TextField()


class Currency_Image(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_image', null=True, blank=True)
    front_image = models.ImageField(upload_to='front_image_currency', null=True, blank=True)
    back_image = models.ImageField(upload_to='back_image_currency', null=True, blank=True)


class NationalInstruments(models.Model):
    national_name = models.CharField(max_length=300)
    national_description = models.TextField()
    national_image = models.ImageField(upload_to='national_images')
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.national_name


class CultureKitchen(models.Model):
    kitchen_name = models.CharField(max_length=300)
    kitchen_description = models.TextField()
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.kitchen_name


class CultureKitchenImage(models.Model):
    culture_kitchen = models.ForeignKey(CultureKitchen, on_delete=models.CASCADE, related_name='culture_kitchen_image')
    image = models.ImageField(upload_to='culture_kitchen_image/', null=True, blank=True)


class CultureKitchenMain(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    culture = models.ForeignKey(CultureCategory, on_delete=models.CASCADE)
    image_1 = models.ImageField(upload_to='culture_kitchen_image', null=True, blank=True)
    image_2 = models.ImageField(upload_to='culture_kitchen_image', null=True, blank=True)
    image_3 = models.ImageField(upload_to='culture_kitchen_image', null=True, blank=True)
    image_4 = models.ImageField(upload_to='culture_kitchen_image', null=True, blank=True)


class AirLineTickets(models.Model):
    logo = models.FileField(upload_to='airline_logos/', null=True, blank=True)
    name = models.CharField(max_length=250)
    description = models.TextField()
    website = models.URLField()

    def __str__(self):
        return str(self.name)


class AirLineDirections(models.Model):
    ticket = models.ForeignKey(AirLineTickets, on_delete=models.CASCADE, related_name='airline_tickets')
    directions = models.CharField(max_length=250)


# FOR FAVORITE


class Favorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    attractions = models.ForeignKey(Attractions, on_delete=models.CASCADE, null=True, blank=True)
    popular_place = models.ForeignKey(PopularPlaces, on_delete=models.CASCADE, null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, null=True, blank=True)
    hotels = models.ForeignKey(Hotels, on_delete=models.CASCADE, null=True, blank=True)
    like = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    # Полностью удаляем ограничение unique_together и заменяем на отдельную логику в save()
    def save(self, *args, **kwargs):
        # Проверка на существование похожей записи перед сохранением
        if self.attractions:
            existing = Favorite.objects.filter(
                user=self.user,
                attractions=self.attractions,
                popular_place__isnull=True,
                kitchen__isnull=True,
                hotels__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                # Запись уже существует, обновляем лайк
                existing.like = self.like
                existing.save()
                return existing

        elif self.popular_place:
            existing = Favorite.objects.filter(
                user=self.user,
                popular_place=self.popular_place,
                attractions__isnull=True,
                kitchen__isnull=True,
                hotels__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                existing.like = self.like
                existing.save()
                return existing

        elif self.kitchen:
            existing = Favorite.objects.filter(
                user=self.user,
                kitchen=self.kitchen,
                attractions__isnull=True,
                popular_place__isnull=True,
                hotels__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                existing.like = self.like
                existing.save()
                return existing

        elif self.hotels:
            existing = Favorite.objects.filter(
                user=self.user,
                hotels=self.hotels,
                attractions__isnull=True,
                popular_place__isnull=True,
                kitchen__isnull=True
            ).first()
            if existing and (not self.pk or self.pk != existing.pk):
                existing.like = self.like
                existing.save()
                return existing

        # Если мы дошли сюда, значит запись уникальная, сохраняем её
        return super().save(*args, **kwargs)
