from django.shortcuts import render, redirect, get_object_or_404
from .forms import Createaccount1, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import *
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q, Exists, OuterRef
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
# from .tasks import *
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from .utils import *
# Create your views here.

def homepage(request):
    if request.user.is_authenticated:
        prop_rendering = Listproperties.objects.annotate(
            is_saved = Exists(
                SavedProperty.objects.filter(
                user = request.user,
                listing = OuterRef('id')
                )
            )             
        ).filter(status = 'approved')[:3]
        rent_prop = Listproperties.objects.annotate(
            is_saved = Exists(
                SavedProperty.objects.filter(
                    user = request.user,
                    listing = OuterRef('id'),
                    
                    )
                ) 
        ).filter(prop_choices = 'rent', status = 'approved')[:3] 
    else:
        prop_rendering = Listproperties.objects.select_related('user').filter(status = 'approved')[:3]
        rent_prop = Listproperties.objects.filter(prop_choices='rent', status = 'approved')[:3]    

    return render(request, "securehome.html", {
            "prop_rendering" : prop_rendering, 
            "rent_prop" : rent_prop
            })




def aboutus(request):
    return render(request, "aboutus.html")

def propertiesPage(request):
    if request.user.is_authenticated:
        prop_rendering = Listproperties.objects.annotate(
            is_saved = Exists(
                SavedProperty.objects.filter(
                user = request.user,
                listing = OuterRef('id')
                )
            )
        ).filter(status = 'approved')[:3]
        rent_prop = Listproperties.objects.annotate(
            is_saved = Exists(
                SavedProperty.objects.filter(
                    user = request.user,
                    listing = OuterRef('id'),
                    
                )
            )
        ).filter(prop_choices = 'rent', status = 'approved')[:3] 
    else:
        prop_rendering = Listproperties.objects.select_related('user').filter(status = "approved")[:3]
        rent_prop = Listproperties.objects.filter(prop_choices = 'rent', status = "approved")[:3]
    return render(request, "propertiespage.html", {
        "prop_rendering" : prop_rendering, 
        "rent_prop" : rent_prop,
        "towns_by_lga": json.dumps(dict(Listproperties.TOWN_BY_LGA)),
        "lga_choices": Listproperties.LGA_CHOICES,  
        })


def servicesPage(request):
    return render(request, "services.html")

def dashboard(request):
    all_props = Addproperty.objects.filter(user=request.user)
    pending_props = Listproperties.objects.filter(user=request.user, status="pending")
    unread_notifs = Notification.objects.filter(user=request.user, is_read=False)
    for prop in all_props:
        try:
            listing = prop.listing
        except Listproperties.DoesNotExist:
            prop.listing = None
    unlisted_props = Addproperty.objects.filter(
        user=request.user,
    )
    listed_properties = Listproperties.objects.filter(user=request.user)
    
    TotalProp = unlisted_props.count()
    Total_listed = listed_properties.count()
    pending=pending_props.count()
    unread_count = unread_notifs.count()
    context = {
        "user": request.user,
        "TotalProp": TotalProp,
        "properties": unlisted_props,
        "Total_listed": Total_listed,
        "listed_properties": listed_properties,
        "pending": pending,
        "unread": unread_count,
        "section": "dashboard", 
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "dashboardSections/dash.html", context) 
    else:
        return render(request, "dashboard.html", context)
    
def dashboardProp(request):
    active_tab = request.GET.get("tab", "pending")
    user_properties = Addproperty.objects.filter(user=request.user)
    listed_properties = Listproperties.objects.filter(user=request.user, status = active_tab)
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    unread_notifications_count = unread_notifications.count()
    context = {
        "user" : request.user,
        "properties" : user_properties,
        "listed_properties" : listed_properties,
        "active_tab":active_tab,
        "unread" : unread_notifications_count
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "dashboardSections/Properties.html", context)
    else: 
        context['section'] = 'properties'
        return render(request, "dashboard.html", context)    

# signup view 
def createaccount(request):
    if request.method == "POST":
        form = Createaccount1(request.POST)

        if form.is_valid():
            user = form.save()
            username = user.username
            messages.success(request, f"You have signed up successfully {username}")
            request.session['verifying_user_id'] = user.id
            request.session['last_code_sent'] = timezone.now().isoformat()

            # commented out for email api issues will be updated later

            # send_account_created_email.delay(
            #     user.email,
            #     request.user.username
            # )
            # otp_verification(user, user.email)
            return redirect("login")
        
        else:
            messages.error(request, "Signup unsuccessful")
    else:
        form = Createaccount1()

    return render(request, "createaccount1.html", {"form" : form})


def verify_email(request):

    if request.user.is_authenticated and request.user.is_verified:
        return redirect('homepage')
    user_id = request.session.get("verifying_user_id")

    if not user_id:
       return redirect('login')
    user = CustomUser.objects.get(id=user_id)
    if request.method == "POST":

        submitted_code = request.POST.get("otp_input")

        fifteen_minutes =timezone.now() - timedelta(minutes=15)
        otp = OTPVerification.objects.filter(
            user_verification=user,
            otp_code = submitted_code,
            is_used=False,
            created_at__gte = fifteen_minutes
        )
        if otp.exists():
            otp_obj = otp.first()
            otp_obj.is_used = True
            otp_obj.save()


            login(request, user)
            del request.session['verifying_user_id']
            messages.success(request, "Email verified successfully!")
            user.is_verified = True
            user.save()

            return redirect('homepage')
        else:
            messages.error(request, "failed to verify email")
        
    context = {
        "user":user
    }
    return render(request, "otp.html", context)
    

def resend_otp(request):
    user_id = request.session.get("verifying_user_id")

    if not user_id :
        return redirect('login')
    
    user = CustomUser.objects.get(id=user_id)
    last_sent_str = request.session.get('last_code_sent')

    if last_sent_str:
        last_sent = parse_datetime(last_sent_str)
        time_passed = timezone.now()-last_sent

        if time_passed.total_seconds() < 60:
            messages.error(request, "Please wait before requesting a new code")
            return redirect('verify')
        else:
            # otp_verification(user, user.email)
            request.session['last_code_sent'] = timezone.now().isoformat()
            messages.success(request, "Code has been sent successfully")
            return redirect('verify')
        

# Login view
def Login(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            if user is not None:
                login(request, user)
                messages.success(request, "Welcome Back")
                # send_loggedin_email.delay(
                #     request.user.email,
                #     request.user.username
                # )
                return redirect("homepage")
        else:
            messages.error(request, "Login was Unsuccessful")
    else:
        form = LoginForm()                               
    return render (request, "login.html" , {"form": form})


# View for uploading properties
def addproperty(request):
    if request.method == "POST":

        propertyName = request.POST.get("propertyName")
        image = request.FILES.get("image")
        description = request.POST.get("description")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        houseType = request.POST.get("houseType")
        lga = request.POST.get("lga")
        Town = request.POST.get("Town")

        Addproperty.objects.create(
            user = request.user,
            propertyName = propertyName,
            image = image,
            description = description,
            bedrooms = bedrooms,
            bathrooms = bathrooms,
            houseType = houseType,
            Town = Town,
            lga = lga,
        )
        # send_property_upload_email.delay(
        #     request.user.email,
        #     propertyName
        # )
        return redirect("dashboardProp")
    else : 
        
        context = {
            "house_types": Addproperty.HOUSE_TYPE_CHOICES,
            "lga_choices": Addproperty.LGA_CHOICES,
            "towns_by_lga": json.dumps(dict(Addproperty.TOWN_BY_LGA)),  
            "user": request.user,
        }  
        return render(request, "addproperties.html", context)

# view for editing uploaded properties

def edit_uploaded_properties(request, id):

    edit_uploads = get_object_or_404(Addproperty, id=id, user=request.user)

    if request.method == "POST":

        edit_uploads.propertyName = request.POST.get("propertyName", edit_uploads.propertyName)
        edit_uploads.image = request.FILES.get("image", edit_uploads.image)
        edit_uploads.description = request.POST.get("description", edit_uploads.description)
        edit_uploads.bedrooms = request.POST.get("bedrooms", edit_uploads.bedrooms)    
        edit_uploads.bathrooms = request.POST.get("bathrooms", edit_uploads.bathrooms)    
        edit_uploads.houseType = request.POST.get("houseType", edit_uploads.houseType)    
        edit_uploads.Town = request.POST.get("Town", edit_uploads.Town)    
        edit_uploads.lga = request.POST.get("lga", edit_uploads.lga)    
        edit_uploads.duration = request.POST.get("duration", edit_uploads.duration)

        edit_uploads.save()
        return redirect("dashboard")
    else:
        context = {
            "prop": edit_uploads,
            "house_types": Addproperty.HOUSE_TYPE_CHOICES,
            "lga_choices": Addproperty.LGA_CHOICES,
            "towns_by_lga": json.dumps(dict(Addproperty.TOWN_BY_LGA)),  
        }
        return render (request, "editproperties.html", context)



# View for listing of properties
def listproperties(request, id):
    prop = get_object_or_404(Addproperty, id=id, user=request.user)

    if request.method == "POST":

        propertyName = request.POST.get("propertyName")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")       
        houseType = request.POST.get("houseType")

        image1 = None
        image2 = None
        image3 = None

        if request.FILES.get("image"):
            image1 = request.FILES.get("image")
        if request.FILES.get("image2"):
            image2 = request.FILES.get("image2")
        if request.FILES.get("image3"):
            image3 = request.FILES.get("image3")
        price = request.POST.get("price")
        location = request.POST.get("location")
        is_negotiable = request.POST.get("is_negotiable") == "on"
        moreDescription = request.POST.get("moreDescription")
        contact_phone = request.POST.get("contact_phone")
        email = request.POST.get("email")
        prop_size = request.POST.get("prop_size")
        prop_choices = request.POST.get("prop_choices")
        lga = request.POST.get("lga")
        Town = request.POST.get("Town")
        duration = request.POST.get("duration")
        # status = request.POST.get("pending")
        # reasonText = None

        listed_props = Listproperties.objects.create(
            user= request.user,
            prop_links = prop,
            propertyName = propertyName,
            bedrooms = bedrooms,
            bathrooms = bathrooms,
            houseType = houseType,
            price = price,
            location = location,
            is_negotiable = is_negotiable,
            moreDescription = moreDescription,
            contact_phone = contact_phone,
            email = email,
            prop_size = prop_size,
            prop_choices = prop_choices,
            image1 = image1,
            image2 = image2,
            image3 = image3,
            Town = Town,
            lga = lga,
            duration=duration,
            status = "pending",
            reasonText = None
        )
        # send_property_listing_email.delay(
        # request.user.email,
        # propertyName
        # )
        # send_status_update_email.delay(
        #     request.user.email,
        #     propertyName, 
        #     listed_props.status
        # )

        messages.success(request, "Property Listed Successfully")
        return redirect("dashboardProp")
    else:
        context= {
            "prop": prop,
            "house_types": Listproperties.HOUSE_TYPE_CHOICES,
            "lga_choices": Addproperty.LGA_CHOICES,
            "towns_by_lga": json.dumps(dict(Addproperty.TOWN_BY_LGA)),  
            "list_type": Listproperties.PROP_CHOICES,
            "durations" : json.dumps(dict(Listproperties.RENT_DURATION)),
            "statuses" : Listproperties.STATUS
        }        
        # messages.error(request, "Failed to List this property try again")
        return render(request, "listproperties.html", context) 

    
# view for editing listed properties
def edit_listed_properties(request, id):

    listing = get_object_or_404(Listproperties, id=id, user=request.user)

    if request.method == "POST":
            
        listing.image1 = request.FILES.get("image1", listing.image1)
        listing.image2 = request.FILES.get("image2", listing.image2)
        listing.image3 = request.FILES.get("image3", listing.image3)

        listing.propertyName = request.POST.get("propertyName", listing.propertyName)
        listing.prop_links = request.POST.get("prop_links", listing.prop_links)
        listing.bedrooms = request.POST.get("bedrooms", listing.bedrooms)
        listing.bathrooms = request.POST.get("bathrooms", listing.bathrooms)
        listing.price = request.POST.get("price", listing.price)
        listing.location = request.POST.get("location", listing.location)
        listing.is_negotiable = request.POST.get("is_negotiable") == "on"
        listing.moreDescription = request.POST.get("moreDescription", listing.moreDescription)
        listing.contact_phone = request.POST.get("contact_phone", listing.contact_phone)
        listing.email = request.POST.get("email", listing.email)
        listing.prop_size = request.POST.get("prop_size", listing.prop_size)
        listing.houseType = request.POST.get("houseType", listing.houseType)
        listing.prop_choices = request.POST.get("prop_choices", listing.prop_choices)
        listing.lga = request.POST.get("lga", listing.lga)
        listing.Town = request.POST.get("Town", listing.Town)
        listing.duration = request.POST.get("duration", listing.duration)

        listing.save()

        return redirect("dashboard")
    else:
        context = {
            "prop" : listing,
            "lga_choices": Listproperties.LGA_CHOICES,
            "house_types": Listproperties.HOUSE_TYPE_CHOICES,
            "towns_by_lga": json.dumps(dict(Listproperties.TOWN_BY_LGA)),  
            "list_type": Listproperties.PROP_CHOICES,
            "durations" : json.dumps(dict(Listproperties.RENT_DURATION))
        }

    return render(request, "editlistedprops.html", context)


def propdetails(request, id):
    propDetails = get_object_or_404(Listproperties, id=id, status='approved')

    Property_View.objects.create(
        Propname = propDetails
    )
    return render (request, "Propertydetails.html", {"propdets": propDetails})


# Search functionality

def search_results(request):
    search_query = request.GET.get('q', '').strip()
    lga_filter = request.GET.get("lga")
    town_filter = request.GET.get('town')
    house_type_filter = request.GET.get('house_type')
    prop_choices_filter = request.GET.get('prop_choices')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_size = request.GET.get('min_size')
    max_size = request.GET.get('max_size')

    search_results = Listproperties.objects.all()
    
    if search_query:
        search_results = search_results.filter(
            Q(propertyName__icontains = search_query)|
            Q(moreDescription__icontains = search_query)
        )

    if lga_filter:
        search_results = search_results.filter(lga = lga_filter)

    if town_filter:
        search_results = search_results.filter(Town= town_filter)

    if house_type_filter:
        search_results = search_results.filter(houseType=house_type_filter)
    if prop_choices_filter:
        search_results = search_results.filter(prop_choices =prop_choices_filter)     
    if min_size:
        search_results = search_results.filter(prop_size__gte = min_size)
    if max_price:
        search_results = search_results.filter(price__lte = max_price)  
    if min_price:
        search_results = search_results.filter(price__gte = min_price)
    if max_size:
        search_results = search_results.filter(prop_size__lte = max_size)  

    context = {
        "search_results": search_results,
        "total_results": search_results.count(),
        "lga_choices": Listproperties.LGA_CHOICES,
        "towns_by_lga": json.dumps(dict(Listproperties.TOWN_BY_LGA)),
        # Pass back filter values so form stays filled
        "search_query": search_query,
        "lga_filter": lga_filter,
        "town_filter": town_filter,
        "house_type_filter": house_type_filter,
        "prop_choice_filter": prop_choices_filter,
        "min_price": min_price,
        "max_price": max_price,
    }

    return render(request, "searchresults.html", context)    

@require_POST
def deleteprops(request, id):
    delete_prop = get_object_or_404(Addproperty, id=id, user=request.user)
    delete_prop.delete()
    messages.success(request, "Property deleted successfully")
    return redirect("dashboard")

@require_POST
def delisting_props(request, id):
    delist_prop = get_object_or_404(Listproperties, id=id, user=request.user)
    delist_prop.delete()
    messages.success(request, "Property delisted successfully")
    return redirect("dashboard")

def admin_delete_property(request):
    prop = Listproperties.objects.get(id=user)
    user = prop.user 

    if request.method == "POST":
        reason = request.POST.get("reason_text")

        create_notification(
            user=user,
            notification_type='property_deleted',
            message=f"Your property {prop.propertyName} has been deleted. Reason:{reason}",

        )
        prop.delete()
        # make sure to update this redirect
        return redirect("homepage")
def confirm_delete_draft(request, id):
    draft = get_object_or_404(Addproperty, id=id, user=request.user)
    
    context = {
        "property": draft,
        "property_type": "draft"
    }
    return render(request, "confirm_delete_props.html", context)

def confirm_delist(request, id):
    listing = get_object_or_404(Listproperties, id=id, user=request.user)
    
    context = {
        "listed": listing,
        "property_type": "listing"
    }
    return render(request, "confirm_delete_props.html", context)

@login_required
def saveprops(request, id):
    save_prop = get_object_or_404(Listproperties, id=id)
    if request.method == "POST":

        saved_prop = SavedProperty.objects.filter(user=request.user, listing=save_prop).exists()
        if saved_prop:
            saved_prop= SavedProperty.objects.filter(
                user= request.user,
                listing = save_prop,
            ).delete()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success' : True,
                    'is_saved' : False
                })
            messages.success(request, "Property removed successfully")
            return redirect(request.META.get("HTTP_REFERER", "homepage"))
            
        else:
            SavedProperty.objects.create(
                user = request.user,
                listing = save_prop
            )
            if request.headers.get('X-Requested-With') == "XMLHttpRequest":
                return JsonResponse({
                    'success' : True,
                    'is_saved' : True
                })
            messages.success(request, "Property saved successfully")
            return redirect(request.META.get("HTTP_REFERER", "homepage"))

@login_required
def saved_props(request):
    if request.method == "POST":
        return redirect("saved_props")

    # Only get properties that ARE saved by this user
    prop_rendering = Listproperties.objects.filter(
        savedproperty__user=request.user  # This filters ONLY saved properties
    ).annotate(
        is_saved = Exists(
            SavedProperty.objects.filter( 
                user=request.user,
                listing=OuterRef('id')
            )
        )
    )
    
    return render(request, "saved_props.html", {
        "prop_rendering": prop_rendering
    })

def logout_view(request):

    # send_logout_email.delay(
    #     request.user.email,
    #     request.user.username
    # )
    logout(request)
    return redirect("login")


def webs (request):
    return render(request, "websoc.html")           

def notifications(request):
    all_notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    context={
        'all_notifs':all_notifs
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "dashboardSections/notifications.html", context) 
    else:
        context['section']= 'notifications' 
        return render(request, "dashboard.html", context)
        
def notifications_details(request, id):
    notif_details = get_object_or_404(Notification, id=id, user=request.user)

    notif_details.is_read = True
    notif_details.save()

    context={
        "notif_details":notif_details
    }
    if request.headers.get('X-Requested-With') == "XMLHttpRequest":
        return render(request, "dashboardSections/notifications_details.html", context)
    else:
        context['section']= 'notifications_details' 
        return render(request, "dashboard.html", context)
    
def saved_dashboard(request):
    all_saved = SavedProperty.objects.filter(user=request.user)

    context={
        "all_saved": all_saved
    }
    if request.headers.get('X-Requested-With') == "XMLHttpRequest":
        return render(request, "dashboardSections/saved.html", context)
    else:
        context['section'] = 'saved'
        return render(request, "dashboard.html", context)
