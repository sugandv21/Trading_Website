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


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        user = User.objects.create_user(
            username=email, email=email, password=password, first_name=name
        )
        user.save()
        messages.success(request, "Registration successful! Please log in.")
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