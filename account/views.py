from django.shortcuts import render,redirect,get_object_or_404
from .form import *
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import unauthenticated_user
from .models import Account
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from article import models as articleModels
from PIL import Image
import datetime, copy

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage




# Create your views here.
@unauthenticated_user
def registration(request):
    form = AccountForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['last_name'] + '_' + form.cleaned_data['first_name'] 
            user.is_active = False
            user.save()
            Account.objects.create(
                user = user,
            )
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/register_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request,"Your account was successfully created.")
            return redirect("home:login")
        else:
            messages.error(request,"One of the fields is incorrect or invalid.")


    context = {'form':form}
    return render (request,'accounts/register.html',context)

@unauthenticated_user
def activateAccount(request, uidb64, token):
  
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request,"Your account has been activated successfully. You can login now.")
    else:
        messages.error(request,"Activation link is invalid!")

    return redirect("home:registrationDone")

@unauthenticated_user
def registrationDone(request):
    return render(request,"accounts/registration_after_account_activation.html")

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        user = authenticate(request,username = email,password = password)
        if user is not None and not user.is_active :
            messages.warning(request,"You must activate your account before login, please check your mail box or your spam folder.")
        elif user is not None:
            login(request,user)
            return redirect("home:index")
        else:
            messages.error(request,"Wrong username or password.")
    return render (request,'accounts/login.html')


def logoutPage(request):
    logout(request)
    return redirect("home:login")

@login_required(login_url="home:login")
def accountBasicInformation(request):
    user = request.user
    socialMedia = request.user.account
    
    userInfoForm = UserInfoForm(request.POST or None, instance=user)
    socialMediaInfoForm = SocialMediaInfoForm(request.POST or None,request.FILES or None, instance=socialMedia)

    if request.method == "POST":
        if userInfoForm.is_valid() and socialMediaInfoForm.is_valid():
            messages.success(request,"All fields were updated successfully.")
            user = userInfoForm.save(commit=False)
            user.username = userInfoForm.cleaned_data['last_name'] +" "+ userInfoForm.cleaned_data['first_name']
            smif = socialMediaInfoForm.save(commit=True)

            if (smif.profile_pic) and (smif.profile_pic.width != smif.profile_pic.height):
                smif.profile_pic.open()

                image = Image.open(smif.profile_pic)

                w, h = image.size
                x = math.trunc(max((w - h) / 2, 0))
                y = math.trunc(max((h - w) / 2, 0))

                image = image.crop((x, y, x+min(w,h), y+min(w,h)))

                image.save(smif.profile_pic.path)
                smif.save()
                smif.profile_pic.close()
        else:
            messages.error(request,"One of the fields is incorrect or invalid.")
                
    context = {'userForm' : userInfoForm,
               'moreInfoForm' : socialMediaInfoForm}
    return render(request,"accounts/basic_information.html",context = context)

@login_required(login_url="home:login")
def changePassword(request):
    form = PasswordChangeForm(user = request.user,data = request.POST or None)
    if request.method == "POST":
        if form.is_valid() :
            messages.success(request,"Your password was updated successfully.")
            form.save()
            update_session_auth_hash(request,form.user)
        else:
            messages.error(request,"One of the fields is incorrect or invalid.")

            
    
    context = {'form':form}
    return render(request,"accounts/change_password.html",context = context)

@login_required(login_url="home:login")
def deleteAccount(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request,"Your account has been deleted successfully.")
        return redirect("home:login")
   
    return render(request,"accounts/delete_account.html")

@login_required(login_url="home:login")
def account(request,id,last_name,first_name):
    context = {}
    context['profile'] = get_object_or_404(Account, id=id)
    context['follower'] = context['profile'].account_set.all()
    context['follow'] = context['profile'].follow.all()
    context['owner'] = (context['profile'] == request.user.account)
    context['following'] = False

    if not context['owner']:
        context['following'] = (context['profile'] in request.user.account.follow.all())

    if (request.method == 'POST'):
        if context['owner']:
            if ('delart' in request.POST) and (request.POST['delart'] != ''):
                try:
                    article = articleModels.Article.objects.get(pk=request.POST['delart'])
                except:
                    pass
                else:
                    if article.postmaster == context['profile']:
                        article.delete()
            elif ('delfw' in request.POST) and (request.POST['delfw'] != ''):
                fws = request.POST['delfw'].strip()[:-2].split(';;')
                for fwid in fws:
                    try:
                        fw = Account.objects.get(id=fwid)
                    except:
                        pass
                    else:
                        if fw in request.user.account.follow.all():
                            request.user.account.follow.remove(fw)
        else:
            if context['following']:
                request.user.account.follow.remove(context['profile'])
            else:
                request.user.account.follow.add(context['profile'])

        return redirect('/' + str(context['profile'].id) + '+' + context['profile'].user.last_name + '+' + context['profile'].user.first_name)

    context['rows'] = context['profile'].article_set.all().order_by('-date_creation', '-id')
    return render(request, "accounts/account.html", context=context)


@login_required(login_url="home:login")
def notifications(request):
            
    context = {}
    profile = request.user.account

    if (request.method == 'POST') and ('delnot' in request.POST):
        notifs_id = request.POST['delnot'].strip()[:-2].split(';;')
        
        for notif_id in notifs_id:
            try:
                notif = articleModels.Notification.objects.get(pk=notif_id)
            except Exception:
                pass
            else:
                if notif.destination == profile:
                    notif.delete();

        return redirect('account:notifications')

    notifs = profile.dest_set.all().order_by('-sending_date', '-id')
    context['notifications'] = []

    for notif in notifs:
        context['notifications'].append(copy.deepcopy(notif))
        notif.seen = True
        notif.save()

    profile.new_notifications = False
    profile.save()

    return render(request, "accounts/notifications.html", context=context)
