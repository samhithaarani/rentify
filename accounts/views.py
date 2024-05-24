from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .forms import PropertyForm
from .models import Property
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # Providing feedback to the user
            print("Form errors:", form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'seller':
                return redirect('seller_dashboard')
            elif user.user_type == 'buyer':
                return redirect('buyer_dashboard')
        else:
            messages.error(request, "Invalid email or password")
            
    return render(request, 'accounts/login.html')


@login_required
def seller_dashboard(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            return redirect('seller_dashboard')
    else:
        form = PropertyForm()

    properties = Property.objects.filter(user=request.user)
    return render(request, 'accounts/seller_dashboard.html', {
        'form': form,
        'properties': properties,
    })

@login_required
def view_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    return render(request, 'accounts/view_property.html', {
        'property': property,
    })

@login_required
def update_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'accounts/update_property.html', {
        'form': form,
        'property': property,
    })

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, user=request.user)
    if request.method == 'POST':
        property.delete()
        return redirect('seller_dashboard')
    return render(request, 'accounts/delete_property.html', {
        'property': property,
    })





def buyer_dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'Guest'
    
    # Get all properties initially
    properties = Property.objects.all()

    # Handle search query
    query = request.GET.get('q')
    if query:
        # Filter properties by city if query is present
        properties = properties.filter(city__icontains=query)

    # Handle filters
    if request.GET.get('bedrooms'):
        bedrooms = int(request.GET.get('bedrooms'))
        properties = properties.filter(bedrooms=bedrooms)
    if request.GET.get('bathrooms'):
        bathrooms = int(request.GET.get('bathrooms'))
        properties = properties.filter(bathrooms=bathrooms)
    if request.GET.get('balcony'):
        properties = properties.filter(balcony=True)
    if request.GET.get('pool'):
        properties = properties.filter(swimming_pool=True)
    if request.GET.get('play_area'):
        properties = properties.filter(playing_area=True)

    return render(request, 'accounts/buyer_dashboard.html', {'properties': properties, 'username': username})


def logout_view(request):
    logout(request)
    return redirect('login')
