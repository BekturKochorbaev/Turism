from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


@admin.register(Region, Home, PopularPlaces, ToTry, Culture,
                Games, NationalClothes, HandCrafts, NationalInstruments,

                )
class AllAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class CultureKitchenImageInline(admin.TabularInline):
    model = CultureKitchenImage
    extra = 1


@admin.register(CultureKitchen)
class CultureKitchenAdmin(TranslationAdmin):
    inlines = [CultureKitchenImageInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class AttractionsImageInline(admin.TabularInline):
    model = AttractionsImage
    extra = 1


@admin.register(Attractions)
class AttractionsAdmin(TranslationAdmin):
    inlines = [AttractionsImageInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }



class AttractionsReviewImageInline(admin.TabularInline):
    model = AttractionsReviewImage
    extra = 1


class AttractionReviewAdmin(admin.ModelAdmin):
    inlines = [AttractionsReviewImageInline]


admin.site.register(AttractionReview, AttractionReviewAdmin)


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


class PopularReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImageInline]


admin.site.register(PopularReview, PopularReviewAdmin)


class GalleryReviewInline(admin.TabularInline):
    model = GalleryReview
    extra = 1


@admin.register(Gallery)
class GalleryAdmin(TranslationAdmin):
    inlines = [GalleryReviewInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class HotelsImageInlines(admin.TabularInline):
    model = HotelsImage
    extra = 1


class HotelsReviewImageInline(admin.TabularInline):
    model = HotelsReviewImage
    extra = 1


class HotelsReviewAdmin(admin.ModelAdmin):
    inlines = [HotelsReviewImageInline]


admin.site.register(HotelsReview, HotelsReviewAdmin)

@admin.register(Hotels)
class HotelsAdmin(TranslationAdmin):
    inlines = [HotelsImageInlines]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class KitchenReviewImageInline(admin.TabularInline):
    model = KitchenReviewImage
    extra = 1


class KitchenLocationInline(TranslationInlineModelAdmin, admin.TabularInline):
    model = KitchenLocation
    extra = 1


class KitchenImageInline(admin.TabularInline):
    model = KitchenImage
    extra = 1


class KitchenReviewAdmin(admin.ModelAdmin):
    inlines = [KitchenReviewImageInline]


admin.site.register(KitchenReview, KitchenReviewAdmin)


@admin.register(Kitchen)
class KitchenAdmin(TranslationAdmin):
    inlines = [KitchenImageInline, KitchenLocationInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class EventInlines(admin.TabularInline):
    model = Event
    extra = 1


class EventCategoriesAdmin(admin.ModelAdmin):
    inlines = [EventInlines]


admin.site.register(EventCategories, EventCategoriesAdmin)
admin.site.register(UserProfile)
admin.site.register(CultureCategory)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
admin.site.register(Region_Categoty)
admin.site.register(Ticket)

admin.site.register(PostKitchen)
admin.site.register(PostHotel)
admin.site.register(PostAttraction)
admin.site.register(PostGallery)
admin.site.register(PostPopular)


class Currency_DescriptionInlines(TranslationInlineModelAdmin, admin.TabularInline):
    model = Currency_Description
    extra = 1


class Currency_ImageInlines(admin.TabularInline):
    model = Currency_Image
    extra = 1



@admin.register(Currency)
class CultureKitchenAdmin(TranslationAdmin):
    inlines = [Currency_DescriptionInlines, Currency_ImageInlines]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
