from django.db import models


class SiteAsset(models.Model):
    key = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to="site_assets/")

    def __str__(self):
        return self.key


class HomeSection(models.Model):
    title = models.CharField(
        max_length=200,
        default="Build Confidence With Every Single Trade."
    )
    title1 = models.CharField(
        max_length=200,
        default="Invest for Your Future"
    )
    subtitle = models.CharField(
        max_length=200,
        default="Keep Your Money Safe !!!!"
    )
    
    description = models.CharField(
        max_length=250,
        default="Your Trading Journey Started Here…."
    )
    realtime_users_count = models.CharField(
        max_length=50,
        default="500+"
    )
    realtime_users_label = models.CharField(
        max_length=100,
        default="Realtime Users"
    )

    bg_banner = models.ImageField(upload_to="home/", blank=True, null=True)
    banner_user = models.ImageField(upload_to="home/", blank=True, null=True)
    vertical_bar = models.ImageField(upload_to="home/", blank=True, null=True)
    arrow = models.ImageField(upload_to="home/", blank=True, null=True)

    user1 = models.ImageField(upload_to="home/users/", blank=True, null=True)
    user2 = models.ImageField(upload_to="home/users/", blank=True, null=True)
    user3 = models.ImageField(upload_to="home/users/", blank=True, null=True)
    user4 = models.ImageField(upload_to="home/users/", blank=True, null=True)
    user5 = models.ImageField(upload_to="home/users/", blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Hero_Section"
        verbose_name_plural = "Home Hero_Section"

    def __str__(self):
        return f"Home Section (updated {self.updated_at:%Y-%m-%d %H:%M})"


class HomeSection2(models.Model):
    paragraph1 = models.TextField(
        blank=True, null=True, help_text="First paragraph (normal text)"
    )
    paragraph2 = models.TextField(
        blank=True, null=True, help_text="Second paragraph (highlighted in green)"
    )
    paragraph3 = models.TextField(
        blank=True, null=True, help_text="Third paragraph (footer text)"
    )
    image = models.ImageField(upload_to="homepage/", blank=True, null=True)
    image20years = models.ImageField(upload_to="homepage/", blank=True, null=True)

    class Meta:
        verbose_name = "Home Experience_Section"
        verbose_name_plural = "Home Experience_Section"

    def __str__(self):
        return "Home Section 2 Content"


class HomeSection3(models.Model):
    step_number = models.CharField(max_length=5, help_text="Step number like 01, 02, 03")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    highlight = models.BooleanField(
        default=False,
        help_text="Mark this step as highlighted (green middle box)"
    )

    class Meta:
        verbose_name = "Home Features_Section"
        verbose_name_plural = "Home Features_Section"
        ordering = ["step_number"]

    def __str__(self):
        return f"Step {self.step_number} - {self.title}"

class HomeSection4(models.Model):
    heading = models.CharField(max_length=200, default="How it Works?")

    apply_title = models.CharField(max_length=100, default="Apply")
    apply_desc = models.TextField(default="Join thousands of traders who trust our platform every day.")
    apply_img = models.ImageField(upload_to="section4/", blank=True, null=True)

    assess_title = models.CharField(max_length=100, default="Assessment")
    assess_desc = models.TextField(default="Take our short assessment to discover your trading style, risk tolerance, and the tools that fit you best.")
    assess_img = models.ImageField(upload_to="section4/", blank=True, null=True)

    fund_title = models.CharField(max_length=100, default="Get Funded")
    fund_desc = models.TextField(default="Trade with our capital and keep up to 90% of the profits.")
    fund_img = models.ImageField(upload_to="section4/", blank=True, null=True)

    trade_title = models.CharField(max_length=100, default="Trade & Grow")
    trade_desc = models.TextField(default="Whether you're just starting or scaling up, our tools, support, and funding help you grow with confidence.")
    trade_img = models.ImageField(upload_to="section4/", blank=True, null=True)
    
    class Meta:
        verbose_name = "Home How_It_Works_Section"
        verbose_name_plural = "Home How_It_Works_Section"

    def __str__(self):
        return self.heading
    
class BannerSection(models.Model):
    title = models.CharField(max_length=200, default="Welcome to Our Platform")
    banner_img = models.ImageField(upload_to="banner/", blank=True, null=True)
    
    class Meta:
        verbose_name = "Home Dashboard_Section"
        verbose_name_plural = "Home Dashbord_Section"
        
    def __str__(self):
        return self.title

class CommunitySection(models.Model):
    heading = models.CharField(max_length=200, default="Build a Strong Community")
    description = models.TextField(default="Join a global network of passionate traders...")
    
    image1 = models.ImageField(upload_to="community/", blank=True, null=True)
    image2 = models.ImageField(upload_to="community/", blank=True, null=True)
    image3 = models.ImageField(upload_to="community/", blank=True, null=True)
    image4 = models.ImageField(upload_to="community/", blank=True, null=True)
    image5 = models.ImageField(upload_to="community/", blank=True, null=True)
    
    class Meta:
        verbose_name = "Home community_Section"
        verbose_name_plural = "Home community_Section"

    def __str__(self):
        return self.heading


class AboutContent(models.Model):
    banner_image = models.ImageField(upload_to='about/banner/')
    banner_title = models.CharField(max_length=200, default="About TRACO")

    who_title = models.CharField(max_length=200, default="Who are We?")
    who_para1 = models.TextField(blank=True, null=True)
    who_para2 = models.TextField(blank=True, null=True)

    # Mission Section
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_text = models.TextField(blank=True, null=True)
    mission_image = models.ImageField(upload_to='about/mission/', blank=True, null=True)

    # Vision Section
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_text = models.TextField(blank=True, null=True)
    vision_image = models.ImageField(upload_to='about/vision/', blank=True, null=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"
        
    def _str_(self):
        return self.banner_title


class WhyChooseItem(models.Model):
    about = models.ForeignKey(AboutContent, related_name="why_items", on_delete=models.CASCADE)
    icon = models.ImageField(upload_to="about/why_icons/")
    title = models.CharField(max_length=200)
    def _str_(self):
        return self.title

class BlogHero(models.Model):
    title = models.CharField(max_length=200, default="Don’t Just Gain info")
    subtitle = models.CharField(max_length=200, default="Build Knowledge")
    description = models.TextField(
        default="Whether you’re a new investor or a market expert, we’ve got something for everyone at the TRACO blog"
    )
    image = models.ImageField(upload_to="blog/", blank=True, null=True)  
    sparkle = models.ImageField(upload_to="blog/", blank=True, null=True)  
    
    class Meta:
        verbose_name = "Blog Hero_Section"
        verbose_name_plural = "Blog Hero_Section"

    def __str__(self):
        return self.title

class BlogTab(models.Model):
    TAB_CHOICES = [
        ("stocks", "Stocks"),
        ("mutual", "Mutual Funds"),
        ("finance", "Personal Finance"),
        ("futures", "Futures & Options"),
    ]
    tab_key = models.CharField(max_length=20, choices=TAB_CHOICES, unique=True)

    class Meta:
        verbose_name = "Blog tabs"
        verbose_name_plural = "Blog tabs"
    def __str__(self):
        return self.get_tab_key_display()


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ("stocks", "Stocks"),
        ("mutual", "Mutual Funds"),
        ("finance", "Personal Finance"),
        ("futures", "Futures & Options"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    short_desc = models.TextField()
    read_time = models.CharField(max_length=50, default="5 Mins Read")
    date = models.DateField()
    image = models.ImageField(upload_to="blog_posts/", blank=True, null=True)

    class Meta:
        verbose_name = "Blog Posts"
        verbose_name_plural = "Blog Posts"
    def __str__(self):
        return self.title

class PartnerLead(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=80, blank=True)
    pincode = models.CharField(max_length=12, blank=True)
    otp = models.CharField(max_length=6, blank=True)        
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Partner Lead"
        verbose_name_plural = "Partner Leads"

    def __str__(self):
        return f"{self.name} ({self.email})"


class PartnerSection(models.Model):
    heading = models.CharField(
        max_length=200,
        default="Welcome to the First Step of Becoming a TRACO Partner"
    )
    sub_text = models.TextField(
        blank=True,
        null=True,
        default="Contact us Alternatively, You can Contact Our Business Partner Team"
    )
    phone = models.CharField(
        max_length=30,
        default="022 982231",
        help_text="Display phone number shown on the partner page"
    )
    email = models.EmailField(
        default="businesspartner@tranco.in",
        help_text="Display email shown on the partner page"
    )
    image = models.ImageField(
        upload_to="partner/",
        blank=True,
        null=True,
        help_text="Hero/side image for the partner page"
    )

    class Meta:
        verbose_name = "Partner Page Content"
        verbose_name_plural = "Partner Page Content"

    def __str__(self):
        return self.heading


class PartnerBenefitsSection(models.Model):
    # Big heading lines above the cards
    heading_line1 = models.CharField(
        max_length=200,
        default="People become partners to earn passive income and grow with a trusted brand."
    )
    heading_line2 = models.CharField(
        max_length=200,
        default="They get access to high commissions, marketing support, and long-term business potential."
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Partner – Benefits (Section 2)"
        verbose_name_plural = "Partner – Benefits (Section 2)"

    def __str__(self):
        return "Partner – Benefits Section"

class PartnerBenefit(models.Model):
    section = models.ForeignKey(
        PartnerBenefitsSection,
        related_name="items",
        on_delete=models.CASCADE
    )
    # Small card content
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.ImageField(upload_to="partner/benefit_icons/", blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]
        verbose_name = "Partner Benefit Item"
        verbose_name_plural = "Partner Benefit Items"

    def __str__(self):
        return f"{self.order}. {self.title}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(help_text="You can use plain text or HTML here.")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide from public FAQ page")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', '-created')

    def __str__(self):
        return self.question

class DocSection(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Plain text or HTML")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "title")

    def __str__(self):
        return self.title
    

class PressKit(models.Model):
    title = models.CharField(max_length=200, default="Press Kit")
    subtitle = models.CharField(max_length=300, blank=True)
    overview = models.TextField(blank=True)
    media_text = models.TextField(blank=True, help_text="Short description about downloads")
    brand_guide = models.FileField(upload_to="press/", blank=True, null=True,
                                   help_text="Upload PDF brand guide (PDF recommended)")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Press Kit"
        verbose_name_plural = "Press Kit"

    def __str__(self):
        return "Press Kit (editable content)"
    
class InvestorPage(models.Model):
    title = models.CharField(max_length=200, default="Investor Relations")
    subtitle = models.CharField(max_length=300, blank=True)
    mission = models.TextField(blank=True)
    highlights = models.TextField(
        blank=True,
        help_text="Enter key highlights, one per line."
    )
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Investor Page"
        verbose_name_plural = "Investor Page"

    def __str__(self):
        return "Investor Relations Content"
    
    

class HeroSection(models.Model):
    title = models.CharField(max_length=200, default="Explore Markets")
    subtitle = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name = "Market Explore HeroSection"
        verbose_name_plural = "Market Explore HeroSection"
    def __str__(self):
        return self.title


class Market(models.Model):
    title = models.CharField(max_length=150)
    short_desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="market_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  
    
    class Meta:
        verbose_name = "Market Explore Section"
        verbose_name_plural = "Market Explore Section"

    def __str__(self):
        return self.title
    

class ReadyToken(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="readytoken_images/", blank=True, null=True)

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False) 

    def __str__(self):
        return self.email



    
