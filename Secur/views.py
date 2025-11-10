from django.shortcuts import render, redirect, get_object_or_404
from .forms import Createaccount1, LoginForm
from django.contrib import messages
from django.contrib.auth import login
from .models import signup, Addproperty, Listproperties
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# Create your views here.

def homepage(request):
    return render (request, "securehome.html")

def aboutus(request):
    return render(request, "aboutus.html")

def propertiesPage(request):
    return render(request, "propertiespage.html")

def servicesPage(request):
    return render(request, "services.html")

def dashboard(request):
    TotalProp = Addproperty.objects.filter(user=request.user).count()
    unlisted_props = Addproperty.objects.filter(user=request.user)
    context = {
        "user" : request.user,
        "TotalProp" : TotalProp,
        "unlisted_props" : unlisted_props
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

        print("Before the creation")    
        Addproperty.objects.create(
            user = request.user,
            propertyName = propertyName,
            image = image,
            description = description,
            bedrooms = bedrooms,
            bathrooms = bathrooms,
            houseType = houseType,
        )
        print("After the creation")

        return redirect("dashboardProp")
    else : 
        print("GET request received")
        house_types = Addproperty.HOUSE_TYPE_CHOICES
        return render(request, "addproperties.html", {"house_types" : house_types, "user" : request.user})

    
def Propdash(request):
    return render(request, "dashboardSections/propdash.html")

def listproperties(request, id):
    print("Listing property with id:", id)
    prop = get_object_or_404(Addproperty, id=id, user=request.user)
    print("Found property:", prop)
    print("Request method:", request.method)

    if request.method == "POST":

        print("Getting form data")
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

        print("Creating Listproperties entry")

        listed_props = Listproperties.objects.create(
            user= request.user,
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
            image1 = image1,
            image2 = image2,
            image3 = image3,
        )


        print("success")
        messages.success(request, "Property Listed Successfully")
        print("Redirecting to property details")
        print(f"Property: {prop.propertyName}")
        print(f"User assigned: {prop.user}")  # What does this show?
        print(f"User ID: {prop.user.id if prop.user else 'None'}")
        return redirect("propdetails", id=listed_props.id)
    else:
        context= {
            "prop": prop,
            # "listed_props": listed_props
        }        
        print("error")
        messages.error(request, "Failed to List this property try again")
        return render(request, "listproperties.html", context) 
    

def propdetails(request, id):
    propDetails = get_object_or_404(Listproperties, id=id)
    return render (request, "Propertydetails.html", {"propdets": propDetails})

