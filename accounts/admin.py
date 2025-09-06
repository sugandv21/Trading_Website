from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import SiteAsset
from .models import HomeSection, HomeSection2, HomeSection3, HomeSection4
from .models import CommunitySection, WhyChooseItem, AboutContent, BannerSection, BlogHero
from .models import BlogTab, BlogPost
from django.contrib import admin
from .models import PartnerSection, PartnerLead, PartnerBenefitsSection, PartnerBenefit
from .models import FAQ
from .models import DocSection
from .models import PressKit
from .models import InvestorPage
from .models import HeroSection, Market
from .models import ReadyToken
from .models import NewsletterSubscriber

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order', 'created')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    ordering = ('order',)


admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)


@admin.register(SiteAsset)
class SiteAssetAdmin(admin.ModelAdmin):
    list_display = ("key", "image")
    search_fields = ("key",)
    


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "updated_at")
    search_fields = ("title", "subtitle")


@admin.register(HomeSection2)
class HomeSection2Admin(admin.ModelAdmin):
    list_display = ("id", "short_para1", "short_para2", "short_para3", "image")

    def short_para1(self, obj):
        return obj.paragraph1[:50] + "..." if obj.paragraph1 else ""
    short_para1.short_description = "Paragraph 1"

    def short_para2(self, obj):
        return obj.paragraph2[:50] + "..." if obj.paragraph2 else ""
    short_para2.short_description = "Paragraph 2"

    def short_para3(self, obj):
        return obj.paragraph3[:50] + "..." if obj.paragraph3 else ""
    short_para3.short_description = "Paragraph 3"


@admin.register(HomeSection3)
class HomeSection3Admin(admin.ModelAdmin):
    list_display = ("step_number", "title", "short_description", "highlight")
    list_editable = ("highlight",)

    def short_description(self, obj):
        return obj.description[:60] + "..." if obj.description else ""
    short_description.short_description = "Description"

@admin.register(HomeSection4)
class HomeSection4Admin(admin.ModelAdmin):
    list_display = ("heading",)

@admin.register(BannerSection)
class BannerSectionAdmin(admin.ModelAdmin):
    list_display = ("title",)




@admin.register(CommunitySection)
class CommunitySectionAdmin(admin.ModelAdmin):
    list_display = ("heading",)


class WhyChooseInline(admin.TabularInline):
    model = WhyChooseItem
    extra = 1


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ('banner_title', 'who_title')
    inlines = [WhyChooseInline]
    
    

@admin.register(BlogHero)
class BlogHeroAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")

@admin.register(BlogTab)
class BlogTabAdmin(admin.ModelAdmin):
    list_display = ("tab_key",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date")
    list_filter = ("category",)
    search_fields = ("title", "short_desc")
   
@admin.register(PartnerLead)
class PartnerLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "is_verified", "created_at")
    search_fields = ("name", "email", "phone", "city")
    list_filter = ("is_verified", "created_at")

@admin.register(PartnerSection)
class PartnerSectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "phone", "email")
    search_fields = ("heading", "phone", "email")

class PartnerBenefitInline(admin.TabularInline):
    model = PartnerBenefit
    extra = 0
    fields = ("order", "title", "description", "icon")
    ordering = ("order",)

@admin.register(PartnerBenefitsSection)
class PartnerBenefitsSectionAdmin(admin.ModelAdmin):
    list_display = ("heading_line1", "is_active")
    inlines = [PartnerBenefitInline]

    # Optional: allow only one section instance
    def has_add_permission(self, request):
        if PartnerBenefitsSection.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(DocSection)
class DocSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("title", "content")


@admin.register(PressKit)
class PressKitAdmin(admin.ModelAdmin):
    list_display = ("title", "contact_email", "contact_phone", "updated")
    readonly_fields = ("updated",)


@admin.register(InvestorPage)
class InvestorPageAdmin(admin.ModelAdmin):
    list_display = ("title", "contact_email", "contact_phone", "updated")
    readonly_fields = ("updated",)
    
@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "short_desc")
    

@admin.register(ReadyToken)
class ReadyTokenAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'confirmed')
    search_fields = ('email',)