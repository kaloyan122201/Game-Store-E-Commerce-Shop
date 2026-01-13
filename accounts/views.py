from django.contrib.auth.models import User
from django.shortcuts import redirect,render  #render -> shows HTML patterns ; redirect -> redirects the user to different url
from django.contrib import messages           #messages -> system for showing messages about success, errors
from django.contrib.auth import login,authenticate,logout  #Entering the system , Checks if pass and username are correct, Exiting the system
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm   #Authenticate -> form for registration ; User -> form for login


# Create your views here.

def register_view(request) :
    """ Using premade registration form from Django """
    if request.method == 'POST':        #checks if the user is sending the form
        form = UserCreationForm(request.POST)  # Creates the form with the POST data
        if form.is_valid():                    # Checks if the data is valid (password = password ; username = username)
            user = form.save()                 # Saves the user into DB and returns User object
            login(request, user)               # Automatically adds user into the system after registration
            messages.success(request, 'Account created successfully!') # Prints message
            return redirect('home')
    else:                                      # If the request is Get(user is just opening the web page)
        form = UserCreationForm()              # Creates empty form for registration

    return render(request, 'register.html', {'form': form})  # shows html pattern and gives the form

def login_view(request):
    #Handle POST request (user submitted login form)
    if request.method == 'POST':
        username = request.POST.get('username')#takes the username from the POST data
        password = request.POST.get('password')#takes the password from the POST data
        #Debug: Log login attempt (helpful for troubleshooting)
        print(f'DEBUG login attempt: username= "{username}", password= "[HIDDEN]"')

        user = authenticate(request, username=username, password=password) # checks if they match. If yes -> Object; Else -> None
        print(f'DEBUG authenticate result: {user}')

        #If authentication succeeded
        if user is not None:
            login(request, user) # Log the user in (create session)
            print(f'DEBUG: User {user.username} logged in successfully!')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home') # returns the user to the main page after successful login

        else:  #if authentication failed (pass or username don't match)
            #refreshes the page with error message showing you that you need to try again
            try:
                # Check if username exists in database
                existing_user = User.objects.get(username=username)
                print(f'DEBUG: User exists but wrong password. Password hash: {existing_user.password[:50]}...')
                error_msg = 'Wrong password'
            except User.DoesNotExist:
                # Username doesn't exist
                print(f'DEBUG: User {username} does not exist')
                error_msg = 'Username does not exist!'

            #Re-render login page with error message
            #User stays on login page to correct their input
            return render(request, 'login.html', {'error':error_msg})

    # Handle GET request (user just opened login page)
    # Show empty login form
    return render(request, 'login.html')


def logout_view(request):
    logout(request)  # logs out the user(session is deleted)
    messages.info(request, 'You have been logged out successfully!')
    return redirect('home')