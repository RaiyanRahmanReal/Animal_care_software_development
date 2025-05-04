from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import PaymentForm
from .forms import AdoptionForm
from .forms import DaycareRequestForm
from django.shortcuts import render
from .forms import PetForm  
from .models import Petadd  
from django.core.exceptions import ValidationError
from .models import DaycareRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Petadd
from .forms import PaymentForm  

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import DaycareRequest



@login_required(login_url='login')
def homepage(request):
  
    pets = Petadd.objects.filter(is_approved=True, sold=False)
    # form = PetForm()
    
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    return render(request, 'home.html', {'pets': pets})


def signuppage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
 # Check if username already exists
        if User.objects.filter(username=uname).exists():
            return render(request, 'signup.html', {'error': 'Username already exists!'})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists!'})
        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login') 

    return render(request, 'signup.html')


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request, user)  
            return redirect('home')  
        else:
            return HttpResponse("Username or Password is incorrect!!!") 

    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return redirect('login')






@login_required
def add_adoption_pet(request):
    if request.method == 'POST':
        form = AdoptionForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.is_for_adoption = True
            pet.price = 0
            pet.save()
            return redirect('home')
    else:
        form = AdoptionForm()
    return render(request, 'add_adoption.html', {'form': form})


@login_required
def apply_adoption(request, pet_id):
    pet = get_object_or_404(Petadd, id=pet_id)
    
    if pet.owner == request.user:
        messages.error(request, "You cannot adopt your own pet.")
        return redirect('home')

    if request.method == 'POST':
        pet.sold = True
        pet.adopter = request.user  # ✅ Set adopter here
        pet.save()
        messages.success(request, "You applied for adoption! We will contact you soon.")
        return redirect('home')

    return render(request, 'adoption.html', {'pet': pet})


def adoption(request):
    adoption_pets = Petadd.objects.filter(is_approved=True, sold=False, is_for_adoption=True).exclude(owner=request.user)
    
    
    if request.method == "POST":
        pet_id = request.POST.get('pet_id')  
        pet = get_object_or_404(Petadd, id=pet_id)
        
        if not pet.sold:  
            pet.sold = True  
            pet.adopter = request.user 
            pet.save()  # Save the changes
            
            
            return redirect('user_profile')  
    
    return render(request, 'adoption.html', {'pets': adoption_pets})



def daycare_view(request):
    if request.method == 'POST':
        form = DaycareRequestForm(request.POST, request.FILES)
        if form.is_valid():
            
            daycare = form.save(commit=False)
            daycare.user = request.user  
            daycare.save() 

            
            messages.success(request, 'Your daycare request has been submitted successfully.')
            return redirect('daycare') 
        else:
            
            messages.error(request, 'There was an error in your submission. Please check the form.')

    else:
        form = DaycareRequestForm() 

    
    return render(request, 'daycare.html', {'form': form})


 
@login_required
def approved_daycare_requests(request):
    
    approved_requests = DaycareRequest.objects.filter(approved=True, accepted_by__isnull=True).exclude(user=request.user)
    return render(request, 'approved_daycare_requests.html', {'approved_requests': approved_requests})

@login_required
def accept_daycare_request(request, id):
    daycare_request = get_object_or_404(DaycareRequest, id=id)
    
    
    if daycare_request.accepted_by is None:
        daycare_request.accepted_by = request.user
        daycare_request.save()
    
    return render(request, 'daycare_request_accepted.html', {'request': daycare_request})





@login_required
def user_profile(request):
    user = request.user
    pets_listed = Petadd.objects.filter(owner=user)
    accepted_requests = DaycareRequest.objects.filter(accepted_by=user)
    daycare_requests = DaycareRequest.objects.filter(user=user)
    

    # Pets bought by user
    pets_bought = Petadd.objects.filter(buyer=user, sold=True)

    # Pets adopted by user
    pets_adopted = Petadd.objects.filter(adopter=user, is_for_adoption=True, sold=True)

    return render(request, 'user_profile.html', {
        'user': user,
        'pets_listed': pets_listed,
        'daycare_requests': daycare_requests,
        'accepted_requests': accepted_requests,
        'pets_bought': pets_bought,
        'pets_adopted': pets_adopted
    })
