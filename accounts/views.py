from django.shortcuts import render,redirect
from .forms import SignupForm,ActivateForm
from django.core.mail import send_mail
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
def sigup(request):
    
        '''
            - create new user with code
            - send email
            - stop active user
            - return redirect activate html
        '''
        if request.method =='POST':
              form=SignupForm(request.POST)
              if form.is_valid():
                    username=form.cleaned_data['username']
                    email=form.cleaned_data['email']
                    user=form.save(commit=False)
                    user.is_active=False
                    form.save() 
                    # sendemail  # triger profile with code
                    profile=Profile.objects.get(user__username=username)
                    send_mail(
                "Activate code",
                f"welcome mr {username} \n use this {profile.code}",
                "r_mido@yahoo.com",
                [email],
                fail_silently=False,
            )
                    return redirect(f'/accounts/{username}/activate')

        else:
              form=SignupForm()
        return render(request,'accounts/signup.html',{'form':form})

def activate_code(request,username):
    profile=Profile.objects.get(user__username=username)
    if request.method == 'POST':
          form=ActivateForm(request.POST)
          if form.is_valid():
                code=form.cleaned_data['code']
                if code == profile.code:
                      profile.code=''

                      user=User.objects.get(username=username)
                      user.is_active=True

                      profile.save()
                      user.save()

                      return redirect('/accounts/login')
    else:
          form=ActivateForm()
    return render(request,'accounts/activate.html',{'form':form})
