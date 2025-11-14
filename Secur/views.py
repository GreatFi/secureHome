from django.shortcuts import render, redirect, get_object_or_404
from .forms import Createaccount1, LoginForm
from django.contrib import messages
from django.contrib.auth import login
from .models import signup, Addproperty, Listproperties
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
import json
# Create your views here.

def homepage(request):
    prop_rendering = Listproperties.objects.filter()[:3]
    return render (request, "securehome.html", {"prop_rendering" : prop_rendering})

def aboutus(request):
    return render(request, "aboutus.html")

def propertiesPage(request):
    prop_rendering = Listproperties.objects.filter()[:3]
    rent_prop = Listproperties.objects.filter(prop_choices= 'rent')[:3]
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
    
    for prop in all_props:
        try:
            listing = prop.listing
            print(f"Property {prop.id} ({prop.propertyName}) HAS listing: {listing.id}")
        except Listproperties.DoesNotExist:
            print(f"Property {prop.id} ({prop.propertyName}) has NO listing")
    
    unlisted_props = Addproperty.objects.filter(
        user=request.user,
        # listing__isnull=True
    )
    listed_properties = Listproperties.objects.filter(user=request.user)
    
    TotalProp = unlisted_props.count()
    Total_listed = listed_properties.count()
    
    context = {
        "user": request.user,
        "TotalProp": TotalProp,
        "properties": unlisted_props,
        "Total_listed": Total_listed,
        "listed_properties": listed_properties,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "dashboardSections/dash.html", context) 
    else:
        return render(request, "dashboard.html", context)
    
def dashboardProp(request):
    user_properties = Addproperty.objects.filter(user=request.user)
    listed_properties = Listproperties.objects.filter(user=request.user)
    context = {
        "user" : request.user,
        "properties" : user_properties,
        "listed_properties" : listed_properties
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "dashboardSections/Properties.html", context)
    else: 
        context['section'] = 'properties'
        return render(request, "dashboard.html", context)    
        
def createaccount(request):
    if request.method == "POST":
        form = Createaccount1(request.POST)

        if form.is_valid():
            user = form.save()
            username = user.username
            messages.success(request, f"You have signed up successfully {username}")
            return redirect("login")
        
        else:
            messages.error(request, "Signup unsuccessful")
    else:
        form = Createaccount1()

    return render(request, "createaccount1.html", {"form" : form})

def Login(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = form.get_user()

            if user is not None:
                login(request, user)
                messages.success(request, "Welcome Back")
                return redirect("homepage")
        else:
            messages.error(request, "Login was Unsuccessful")
    else:
        form = LoginForm()                               
    return render (request, "login.html" , {"form": form})


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

        print("Before the creation")    
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
        print("After the creation")

        return redirect("dashboardProp")
    else : 
        print("GET request received")
        
        context = {
            "house_types": Addproperty.HOUSE_TYPE_CHOICES,
            "lga_choices": Addproperty.LGA_CHOICES,
            "towns_by_lga": json.dumps(dict(Addproperty.TOWN_BY_LGA)),  
            "user": request.user,
        }  
        return render(request, "addproperties.html", context)
        
def Propdash(request):
    return render(request, "dashboardSections/propdash.html")

def listproperties(request, id):
    print("Listing property with id:", id)
    prop = get_object_or_404(Addproperty, id=id, user=request.user)
    print("Found property:", prop)
    print("Request method:", request.method)

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
        )

        messages.success(request, "Property Listed Successfully")
        return redirect("propdetails", id=listed_props.id)
    else:
        context= {
            "prop": prop,
            "lga_choices": Addproperty.LGA_CHOICES,
            "towns_by_lga": json.dumps(dict(Addproperty.TOWN_BY_LGA)),  
        }        
        # messages.error(request, "Failed to List this property try again")
        return render(request, "listproperties.html", context) 
    

def propdetails(request, id):
    propDetails = get_object_or_404(Listproperties, id=id)
    return render (request, "Propertydetails.html", {"propdets": propDetails})

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

