import logging
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import SiteAsset   
from .models import HomeSection, HomeSection2, HomeSection3, HomeSection4,  BannerSection, CommunitySection
from .models import AboutContent
from .models import BlogHero, BlogTab, BlogPost
from .forms import PartnerLeadForm, VerifyOtpForm
import random
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import PartnerLead, PartnerSection, PartnerBenefitsSection
from .models import FAQ
from .models import DocSection
from .models import PressKit
from .models import InvestorPage
from .models import HeroSection, Market
from .models import ReadyToken
from django.core.files.storage import FileSystemStorage
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import NewsletterSubscriber
from django.db import IntegrityError


def docs_page(request):
    sections = DocSection.objects.filter(is_active=True).order_by("order")
    return render(request, "front_end/layout/docs.html", {"sections": sections})

def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('order', '-created')
    return render(request, 'front_end/layout/faq.html', {'faqs': faqs})


def home(request):
    home_section = HomeSection.objects.first()
    section2 = HomeSection2.objects.first()
    steps = HomeSection3.objects.all().order_by("step_number")
    section4 = HomeSection4.objects.first()  

    users = []
    if home_section:
        users = [home_section.user1, home_section.user2, home_section.user3,
                 home_section.user4, home_section.user5]
        users = [u for u in users if u]
        community = CommunitySection.objects.first()
    banner = BannerSection.objects.first()
    context = {
        "banner": banner,
        "community": community,
        "home": home_section,
        "users": users,
        "section2": section2,
        "steps": steps,
        "section4": section4,
    }
    return render(request, "front_end/layout/home.html", context)

def get_bull_image():
    return SiteAsset.objects.filter(key="bull").first()


def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    return redirect("register")


logger = logging.getLogger(__name__)

def register(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        mobile = request.POST.get("mobile", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        try:
            user = User.objects.create_user(
                username=email, email=email, password=password, first_name=name
            )
            user.save()
        except Exception as e:
            logger.exception("Error creating user for %s: %s", email, e)
            messages.error(request, "Could not create user. Try again later.")
            return redirect("register")

        # --- Send confirmation email ---
        subject = "Welcome to TRACO — Registration successful"
        message = (
            f"Hi {name or 'there'},\n\n"
            "Thanks for registering at TRACO. Your account has been created successfully.\n\n"
            "You can now log in using the email and password you provided.\n\n"
            "— TRACO Team"
        )
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", settings.SERVER_EMAIL)

        try:
            send_mail(subject, message, from_email, [email], fail_silently=False)
            messages.success(request, "Registration successful! A confirmation email has been sent. Please check your inbox.")
            logger.info("Registration email sent to %s", email)
        except BadHeaderError:
            logger.exception("BadHeaderError when sending registration email to %s", email)
            messages.success(request, "Registration successful! (Email not sent due to invalid headers.)")
        except Exception as e:
            # Log full exception for debugging (SMTP auth issues, connection refused, etc.)
            logger.exception("Failed to send registration email to %s: %s", email, e)
            # Optionally show a non-sensitive generic error to user
            messages.success(request, "Registration successful! We were unable to send a confirmation email — please check your account settings.")
            # (do NOT show raw exception to end user in production)

        return redirect("login")

    context = {"bull": get_bull_image()}
    return render(request, "front_end/layout/register.html", context)



def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("login")

    context = {"bull": get_bull_image()}
    return render(request, "front_end/layout/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


def about_view(request):
    content = AboutContent.objects.first()
    why_items = [
        {"title": "Research & Recommended Stock", "icon": "images/ar4.png"},
        {"title": "Join Our Community of 5 Million + Happy Inversters", "icon": "images/ar3.png"},
        {"title": "Invest in All-in-one Platform", "icon": "images/ar2.png"},
        {"title": "Get personalized service at 160+ branches in India", "icon": "images/ar1.png"},
    ]
    return render(request, 'front_end/layout/about.html', {'content': content, 'why_items': why_items})




def blog(request):
    hero = BlogHero.objects.first()
    tabs = BlogTab.objects.all().order_by("id")
    posts = BlogPost.objects.all().order_by("-date")

    return render(
        request,
        "front_end/layout/blog.html",
        {"hero": hero, "tabs": tabs, "posts": posts}
    )


def partner(request):
    section = PartnerSection.objects.first()  # <-- pulls your dynamic content
    lead_form = PartnerLeadForm()
    verify_form = VerifyOtpForm()
    benefits_section = PartnerBenefitsSection.objects.filter(is_active=True).first()
    benefits = benefits_section.items.all() if benefits_section else []

    # STEP 1: Save lead + send OTP
    if request.method == "POST" and request.POST.get("action") == "send_otp":
        lead_form = PartnerLeadForm(request.POST)
        if lead_form.is_valid():
            lead = lead_form.save(commit=False)
            lead.otp = f"{random.randint(0, 999999):06d}"
            lead.is_verified = False
            lead.save()

            request.session["partner_lead_id"] = lead.id

            subject = "Your TRACO Partner OTP"
            body = (
                f"Hello {lead.name},\n\n"
                f"Your OTP is: {lead.otp}\n"
                f"This code is valid for 10 minutes.\n\n"
                "If you did not request this, please ignore this email."
            )
            try:
                send_mail(
                    subject,
                    body,
                    getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    [lead.email],
                    fail_silently=False,
                )
                messages.success(request, "OTP sent to your email.")
            except BadHeaderError:
                messages.error(request, "Invalid header found while sending email.")
            except Exception as e:
                messages.error(request, f"Could not send OTP: {e}")

            return redirect("partner")
        else:
            messages.error(request, "Please fix the errors and try again.")

    # STEP 2: Verify OTP
    if request.method == "POST" and request.POST.get("action") == "verify_otp":
        verify_form = VerifyOtpForm(request.POST)
        lead_id = request.session.get("partner_lead_id")
        if not lead_id:
            messages.error(request, "Start again by submitting the form.")
            return redirect("partner")

        lead = get_object_or_404(PartnerLead, pk=lead_id)
        if verify_form.is_valid():
            if verify_form.cleaned_data["otp"] == lead.otp:
                lead.is_verified = True
                lead.save(update_fields=["is_verified"])
                messages.success(request, "OTP verified! We’ll contact you shortly.")
                request.session.pop("partner_lead_id", None)
                return redirect("partner")
            else:
                messages.error(request, "Incorrect OTP. Please try again.")

    show_verify = bool(request.session.get("partner_lead_id"))

    return render(
        request,
        "front_end/layout/partner.html",
        {
            "section": section,
            "lead_form": lead_form,
            "verify_form": verify_form,
            "show_verify": show_verify,
            "benefits_section": benefits_section,
            "benefits": benefits,
        },
    )
    
  

def press_kit(request):
    press, created = PressKit.objects.get_or_create(pk=1, defaults={
        "title": "Press Kit",
        "subtitle": "",
        "overview": "Welcome to our Press Kit. Edit this content from the Django admin.",
        "media_text": "Download our brand guide below.",
        "contact_email": "press@tradingproject.com",
        "contact_phone": "+91 98765 43210",
    })
    return render(request, "front_end/layout/press_kit.html", {"press": press})


def investor(request):
    investor_page, created = InvestorPage.objects.get_or_create(
        pk=1,
        defaults={
            "title": "Investor Relations",
            "subtitle": "Welcome to our Investor Relations page",
            "mission": "To provide smart, accessible, and transparent trading tools.",
            "highlights": " Innovative trading insights platform\n Growing global investor base\n Secure and reliable technology",
            "contact_email": "investors@tradingproject.com",
            "contact_phone": "+91 91234 56789",
        }
    )
    return render(request, "front_end/layout/investor.html", {"page": investor_page})


def market_explore(request):
    hero = HeroSection.objects.first()
    markets = Market.objects.all()
    return render(
        request,
        "front_end/layout/market_explore.html",
        {"hero": hero, "markets": markets}
    )
    

def readytoken_list(request):
    tokens = ReadyToken.objects.all()
    return render(request, "front_end/layout/readytoken_list.html", {"tokens": tokens})

def readytoken_detail(request, pk):
    token = get_object_or_404(ReadyToken, pk=pk)
    return render(request, "front_end/layout/readytoken_detail.html", {"token": token})

def main_options(request):
    return render(request, "front_end/layout/main_options.html")


def filechecking(request):
    uploaded_file = None
    error = None

    if request.method == "POST" and request.FILES.get("data_file"):
        uploaded_file = request.FILES["data_file"]
        filename = uploaded_file.name.lower()

        # Validation
        if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
            error = "Only CSV or Excel files are allowed."
            uploaded_file = None
        else:
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_url = fs.url(file_path)

            return render(
                request,
               "front_end/layout/filechecking.html",
                {"uploaded_file": uploaded_file, "uploaded_file_url": uploaded_file_url}
            )

    return render(
        request,
        "front_end/layout/filechecking.html",
        {"uploaded_file": None, "error": error}
    )


def subscribe(request):
    referer = request.META.get('HTTP_REFERER', '/')
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect(referer)

    email = request.POST.get('email', '').strip()
    if not email:
        messages.error(request, "Please enter an email address.")
        return redirect(referer)

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, "Please enter a valid email address.")
        return redirect(referer)

    # Compose email
    subject = "Thanks for subscribing to TRACO"
    message = (
        "Hi,\n\n"
        "Thanks for subscribing to the TRACO newsletter. We'll keep you updated.\n\n"
        "If you did not sign up, you can ignore this email.\n\n"
        "— TRACO Team"
    )
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", settings.SERVER_EMAIL)

    # Debug: print to console
    print("DEBUG subscribe: sending email to:", email, "from:", from_email)
    logger.info("subscribe attempt: %s", email)

    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
    except BadHeaderError:
        logger.exception("BadHeaderError when sending subscription email.")
        messages.error(request, "Invalid header found. Could not send email.")
        return redirect(referer)
    except Exception as e:
        logger.exception("Error sending subscription email: %s", e)
        # If using console backend you'll see the email in runserver console
        messages.error(request, f"Failed to send confirmation email: {e}")
        return redirect(referer)

    messages.success(request, "Thanks! A confirmation email has been sent to your address.")
    return redirect(referer)
