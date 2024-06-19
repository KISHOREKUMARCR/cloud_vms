import json,datetime,os ,yagmail
from json import dumps
import psycopg2
from django.core import serializers
from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from accounts.forms import UserAccountForm, UserAccountUpdateForm,CaptchaForms
from vfms.models import *
from accounts.models import UserAccount, Roles ,UserSocialAccount
from django.urls import reverse
from accounts.custom_auth import custom_login, custom_authenticate, custom_logout,show_data
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
# from validate_email import validate_email
from django.contrib import messages
from accounts.decorators import login_required
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.files.storage import FileSystemStorage
from .tokens import default_token_generator
#from .pipeline import get_avatar
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image 
from django.contrib.auth import logout

#global values 
social_image_url = ""
social_details = {}
current_login_user_id = 0
#global values endswith

#login func

# Create your views here.


'''
def edit_profile_account(request, id=None):
    global current_login_user_id
    id = current_login_user_id
    
    if UserAccount.objects.filter(id=id).exists():
        user = UserAccount.objects.get(id=id)
        #roles = Roles.objects.get(id = user.user_roles.id)
    else:
        user = request.user
        user = UserSocialAccount.objects.get(user_name = user)
    args = {'user': user}
    
    return render(request, 'templates/accounts/user_profile_edit_account.html', args)


def view_profile(request, id=None):
    print("\n UUUUUserRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRrrrrrrrrrrrrr : ",user['custom_user'])
    global current_login_user_id
    id = current_login_user_id
    roles = ""
    #if id:
    user = show_data(request)
    print("\n UUUUUserRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRrrrrrrrrrrrrr : ",user['custom_user'])
    print("\n RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRrrrrrrrrrrrrr : ",request.user)
    #print("\n RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRrrrrrrrrrrrrr : ",request.session['user'])
    print("\n RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRrrrrrrrrrrrrr : ",request.user.is_authenticated)
    if UserAccount.objects.filter(id=id).exists():
        user = UserAccount.objects.get(id=id)
        #roles = Roles.objects.get(id = user.user_roles.id)
    else:
        user = request.user
        user = UserSocialAccount.objects.get(user_name = user)
    args = {'user': user}
    
    print("\n\n UUUUUUUUUUUUUUUUUUSSSSSSSSSSSSSSSSSSSSSEEEEEEEEEEEEEEEE : ",user)
    return render(request, 'templates/accounts/user_profile_view.html', args)
  
''' 

def cal_timeline(a,b):
    val = " "
    d1 = a.strftime("%m/%d/%Y %H:%M:%S") 
    d2 = b.strftime("%m/%d/%Y %H:%M:%S")
    
    d11 = datetime.datetime.strptime(d1, "%m/%d/%Y %H:%M:%S")
    d21 = datetime.datetime.strptime(d2, "%m/%d/%Y %H:%M:%S")
    
    diff = (d11-d21).days
    if diff == 0:
        val = "Today"
       
    if diff > 0:
        val = str(diff)+" Day ago"
    
    if diff >= 31:
        diff = diff / 31
        val = str(round(diff))+" Month ago"
    
    if diff >= 365:
        diff = diff / 365
        val = str(round(diff))+" Year ago"
     
    return val
    #print("\n\n",a,b," ",(d11-d21).seconds)#," ",date_time)
def profile_value(person):
    
    total = 40
    user_mobile = 10
    user_company_name = 8
    user_business_type = 7
    user_image = 5
    user_description = 5
    user_country = 5
    user_state = 5
    user_city = 5
    
    userval = UserAccount.objects.get(user_name = person)
    print("\n\n\n userval : ",userval.user_mobile)
    
    if(userval.user_mobile is not None):
        total += 10
    if(userval.user_company_name is not None):
        total += 8
    if(userval.user_business_type is not None):
        total += 7
    if(userval.user_image != ""):
        total += 5
    if(userval.user_description is not None):
        total += 5
    if(userval.user_country is not None):
        total += 5
    if(userval.user_state is not None):
        total += 5
    if(userval.user_city is not None):
        total += 5
    
    return total
   

@login_required
def profile_view_final(request):
    user = show_data(request)
    if user['custom_user'] == "unknown":
        print("\n\n USER - unknown")
        user = request.user
        user = UserAccount.objects.get(user_name = user)
    else:
        print("\n\n else part of profile view")
        user = user['custom_user']
    #user = str(user).split("_")
    #user = user[0]
    print("\n\n USER PROFILE USER PROFILE USER PROFILE ): ",user)
    profile_val = profile_value(user.user_name)  
    login_val = cal_timeline(user.last_login,user.pre_last_login)
    print("\n\n profile_val : ",profile_val)
    #project and location details
    '''
    if(Projects.objects.filter(user_id = user).exists()):
        project = Projects.objects.filter(user_id = user)
        last_project = project.last()
        project_count = project.count()
        print("\n\n last_project _id : ",last_project.id)
        location = Location.objects.filter(project_id__in = project)
        print("\n\n last_Location : ",location)
        last_location = Location.objects.get(project_id = last_project.id).location_name
        print("\n\n last_location _id : ",last_location)
        location_count = location.count()
        camera = CameraStreams.objects.filter(location_id__in = location)
        camera_count = camera.count()
        
        context = {'user': user,"profile_val":profile_val,"last_project":last_project,"last_location":last_location,"project_count": project_count, 'location_count':location_count, 'camera_count':camera_count}
    else: 
    '''
    userid = request.session.get('user_id')  
    if userid:
        

        total_company = Company.objects.filter(userid=userid).count()
        total_projects = Project.objects.filter(userid=userid).count()
        total_locations = NewCloudURI.objects.filter(userid=userid).count()
        total_locations = NewCloudURI.objects.filter(userid=userid).values('location_name').distinct().count()
        total_cloud_url = NewCloudURI.objects.filter(userid=userid).count()
        
    else:
        total_company = 0
        total_projects = 0
        total_locations = 0
        total_cloud_url = 0
    
    context={'total_company':total_company,'total_projects':total_projects,'total_locations':total_locations,'total_cloud_url':total_cloud_url,
            'user': user,"profile_val":profile_val,"login_val":login_val}
    print(' PROFILE VIEW USER context")', context)
    return render(request, 'templates/accounts/user_profile_view.html', context)



    
@login_required
def profile_edit_account_delete(request):
    user = show_data(request)
    if user['custom_user'] == "unknown":
        user = request.user
        user = UserAccount.objects.get(user_name = user)
    else:
        user = user['custom_user']
    
    args = {'user': user}    
    
    if request.method == "POST":
        checking = request.POST.get('accountActivation')
        print("CCCCCCCCCCCCHHHHHHHHHHHHHHHHHH : ",checking)
        if checking == '1':
            #user.user_status = 0
            
            user.user_status = False
            user.save()
            print("UUUUUUUUUUUUUUUUUUSSSSSSSSSSSSSSSSSSSSSEEEEEEEEEEEEEEEE : ",user)
            custom_logout(request)
        
        return redirect('loginprocess')
        
    return render(request, 'templates/accounts/profile_edit_account_delete.html', args)
    
@login_required    
def profile_edit_security(request):
    user = show_data(request)
    if user['custom_user'] == "unknown":
        user = request.user
        user = UserAccount.objects.get(user_name = user)
    else:
        user = user['custom_user']
    args = {'user': user}    
    
    if request.method == "POST":
        pwd = request.POST.get('newPassword')
        new_password = urlsafe_base64_encode(force_bytes(pwd))
        user.user_password = new_password
        user.save()
        
        return redirect('profile_view_final')
    return render(request, 'templates/accounts/profile_edit_security.html', args)
    
@login_required 
def profile_edit_final(request):
    file_url = ""
    img_save_path = ""
    user = show_data(request)
    #print("\n\n UUUUUUUUUUUUUUUUUUUUUUUUUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSEEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRR : ",user)
    if user['custom_user'] == "unknown":
        #user = request.user
        user = UserAccount.objects.get(user_name = user)
        aa = 1
    else:
        user = user['custom_user']

        is_g_auth = UserAccount.objects.filter(user_name = user,user_social_provider="google-oauth2").exists()
        print("\n\n UUUUUUUUUUUUUUUUUUUUUUUUUSS is_g_auth : ",is_g_auth)
        if is_g_auth:
            aa = 1
        else:
            aa = 0
    args = {'user': user}  
    #img_save_path = upload(request)
    
    
    if request.method == "POST":# or request.FILES['upload_img']:
        
        edit_img = request.POST.get('upload_img')
        print("EEEEEEEEEEEEEEEEEEEEEEE : ",edit_img,aa)#user['custom_user'])#,request.FILES['upload_img'])
        if edit_img != "" and aa == 0:
            upload = request.FILES['upload_img']
            user_folder = 'static/profile/' #+ str(request.session['user_id'])
            if not os.path.exists(user_folder):
                os.mkdir(user_folder)

            img_save_path = str(user_folder)+str(request.session['user_id'])+'_'+str(upload)
            
            with open(img_save_path, 'wb+') as f:
                for chunk in upload.chunks():
                    f.write(chunk)
            user.user_image = img_save_path
        
        name = request.POST.get('name')
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        compname = request.POST.get('compname')
        phno = request.POST.get('mobile')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        description = request.POST.get('description')

        
        user.name = name
        user.user_name = user_name
        user.user_email = email
        user.user_company_name = compname
        user.user_mobile = phno
        user.user_country = country
        user.user_state = state
        user.user_city = city
        user.user_description = description
        user.user_profile_update = datetime.datetime.now(tz=timezone.utc)
        
        user.save()
        
        
        return redirect('profile_view_final')
        
        #return render(request, 'templates/accounts/profile_edit.html', {'user': user,'file_url': file_url,'img_save_path':img_save_path})
   
    return render(request, 'templates/accounts/profile_edit.html', {'user': user,'img_save_path':img_save_path})
    
def upload(request):
    if request.method == 'POST' and request.FILES['upload_img']:
        upload = request.FILES['upload_img']
        print("uploaduploaduploadupload : ", upload.name)
        #img_extension = os.path.splitext(upload.name)[1]

        user_folder = 'static/profile/' #+ str(request.session['user_id'])
        if not os.path.exists(user_folder):
            os.mkdir(user_folder)

        img_save_path = str(user_folder)+str(request.session['user_id'])+'_'+str(upload)
        with open(img_save_path, 'wb+') as f:
            for chunk in upload.chunks():
                f.write(chunk)
        print("img_save_pathimg_save_pathimg_save_path : ",img_save_path)
        
        #img 
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file = fss.save(img_save_path, upload)
        file_url = fss.url(file)
        
        #return render(request, 'templates/accounts/upload.html', {'file_url': file_url,'img_save_path':img_save_path})
        return img_save_path
    #return render(request, 'templates/accounts/upload.html')   

def terms_conditions(request):
    return render(request, 'templates/accounts/terms_and_conditions.html')
    
def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    print("\n\n\n  in Views  SSSSSSSSSSSSSSScccccccccccccccccccccc : ",social)
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}
            
def social_user_details(backend, details, response, *args, **kwargs):
    global social_details
    details = {}
    social_details = dict()
    print("\n \n social_details : ",backend.get_user_details(response),details)
    social_details = backend.get_user_details(response)
    #social_details = details
    
    print(social_details)
     
    
    
def get_avatar(backend, strategy, details, response,user=None, *args, **kwargs):
    global social_image_url
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        try:
            url = response['picture']
        except:
            url = response['image'].get('url')
        ext = url.split('.')[-1]
    if url:
        print("\n\n\n\n urrrrrrrrrrrrrrrrrrrrllllllllllll : ",url)
        
        social_image_url = str(url)
        
        #return url
        #user.avatar = url
        #user.save()

'''
def social_login_google(request):
    global social_image_url,current_login_user_id
    bb = request.user
    #aa = request.user.social_auth.get(provider='google-oauth2')
    #aa = social_auth.objects.filter(user=request.user)
    print("\n\n\n\n\n aaaaaaaaaaaaaaaaaaaaaa: ",bb)#.social_auth.get(provider='google-oauth2'))
    #print("\n\n\n\n\n aaaaaaaaaaaaaaaaaaaaaa: ",aa.extra_data)#.social_auth.get(provider='google-oauth2'))
    print("\n: user_name : ",bb.username)#.social_auth.get(provider='google-oauth2'))
    print("\n: Email : ",bb.email)#.social_auth.get(provider='google-oauth2'))
    #print("\n: social_provider : ",aa.provider)#.social_auth.get(provider='google-oauth2'))
    #print("\n: social_provider : ",aa.provider)#.social_auth.get(provider='google-oauth2'))
    #print("\n: image_url : ",aa.image_url)#.social_auth.get(provider='google-oauth2'))
    image_url = social_image_url
    #models.CharField(max_length=60)
    print("\n\n\n\n\nsocial_image_url : ",image_url   )
    last_login = datetime.datetime.now(tz=timezone.utc)
    date_joined = datetime.datetime.now(tz=timezone.utc)
    
    is_new = UserSocialAccount.objects.filter(user_email=bb.email).exists()
    #print("\n\n is_new : ",is_new)
    if is_new:
        usprofile = UserSocialAccount.objects.get(user_email=bb.email)
        is_status = UserSocialAccount.objects.get(user_email=bb.email).user_status
        print("isssssssssssssss_status : ",is_status)
        usprofile.last_login = datetime.datetime.now(tz=timezone.utc)
        
        usprofile.save()
        
        #return render(request,'tva/landing_page.html')
    else:
        usprofile = UserSocialAccount.objects.create(name=bb.username,user_name = bb.username,user_email=bb.email,user_image_url=image_url,user_social_provider='google-oauth2',date_joined=date_joined,last_login=last_login,user_roles_id=3)
        usprofile.save()
    current_login_user_id = usprofile.id
    return render(request,'tva/landing_page.html') 


def login_account_google(request):
    global social_image_url
    bb = request.user
    user = show_data(request)
    print("UUUUUUUUUUUUUUUUUUSSSSSSSSSSSSSSSSSSSSSEEEEEEEEEEEEEEEE : ",bb,user)
    
    #try:
    is_new = UserAccount.objects.filter(user_email=bb.email,user_social_provider="google-oauth2").exists()
    
    last_login = datetime.datetime.now(tz=timezone.utc)
    date_joined = datetime.datetime.now(tz=timezone.utc)
    
    if not is_new:
        usprofile = UserAccount.objects.create(name=bb.username,user_name = bb.username,user_email=bb.email,user_image_url=social_image_url,user_social_provider='google-oauth2',date_joined=date_joined,last_login=last_login,user_roles_id=3)
        usprofile.save()
        custom_login(request, usprofile)
    else:
        usprofile = UserAccount.objects.get(user_email=bb.email,user_social_provider="google-oauth2")
        usprofile.last_login = datetime.datetime.now(tz=timezone.utc)
        usprofile.save()
        custom_login(request, usprofile)
    #except:
    #    return render(request, 'templates/accounts/pagenotfound.html')
        
    return render(request, 'detections/dashboard2.html')
'''  
def load_timer(request):
    return render(request, 'templates/accounts/g_auth_timer.html')
    
def login_account_google(request):
    global social_image_url,social_details
    user = show_data(request)
    try:
        if user['custom_user'] == "unknown":
            user = social_details['username']
            last_login = datetime.datetime.now(tz=timezone.utc)
            date_joined = datetime.datetime.now(tz=timezone.utc)
            is_new = UserAccount.objects.filter(user_email=social_details['email'],user_social_provider="google-oauth2").exists()
            #user = UserAccount.objects.get(user_name = user)
            #aa = 1
            
   
    
            if str(is_new) == "False":
                usprofile = UserAccount.objects.create(name=social_details['username'],user_name = social_details['username'],user_email=social_details['email'],user_image_url=social_image_url,user_social_provider='google-oauth2',date_joined=date_joined,pre_last_login = last_login,last_login=last_login,user_roles_id=3)
                usprofile.save()
                request.user = social_details['username']
                custom_login(request, usprofile)
                social_details={}
            else:
                usprofile = UserAccount.objects.get(user_email=social_details['email'],user_social_provider="google-oauth2")
                usprofile.pre_last_login = usprofile.last_login
                print("\n\n usprofile.pre_last_login : ",usprofile.pre_last_login)
                usprofile.last_login = datetime.datetime.now(tz=timezone.utc)
                usprofile.save()
                request.user = social_details['username']
                custom_login(request, usprofile)
                social_details={}
    except:
        return redirect('load_timer')
     
    return render(request, 'detections/dashboard2.html')
    
def camera_list_update(request):
    return render(request, 'templates/accounts/camera_list_update.html')
    
def sending_mail(to_addr,content,subject):
     # a token for gmail
    user = 'mpkarthik312@gmail.com'
    app_password = 'pvslhkslmepjzbuc' # a token for gmail
    # to = str(to_addr)
    # to = ', '.join(to_addr)
    to = to_addr
    subject = subject
    content = content
    print("email addresses : ",to)
    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
        print('Sent email successfully')



def sending_mail_with_attachments(to_addr, content, subject, attachments=None):
    # a token for gmail
    user = 'mpkarthik312@gmail.com'
    app_password = 'pvslhkslmepjzbuc'  # a token for gmail

    # Convert to_addr to a list if it's not already
    to = to_addr if isinstance(to_addr, list) else [to_addr]

    # Attachments should be a list of file paths
    attachments = attachments or []

    # Create yagmail SMTP instance
    with yagmail.SMTP(user, app_password) as yag:
        # Send email with attachments
        yag.send(to, subject, content, attachments=attachments)

        print('Sent email successfully')


        
def forget_username(request):
    if request.method == "POST":
        email = request.POST.get('email')
        authenting = UserAccount.objects.filter(user_email = email,user_social_provider = 'manual').exists()
        user = UserAccount.objects.get(user_email = email,user_social_provider = 'manual')#,user_social_provider != 'google-oauth2')
        print("uuuuuuuuuuuuuuuuuuuuuuuuuu : ",user)
        
        uname = UserAccount.objects.get(user_email = email,user_social_provider = 'manual').user_name
        if authenting:
            subject = "Username Recovery Requested"
            email_template_name = "accounts/auth_uname_recovery_email_content.txt"
            c = {
            "email":email,
            'domain':'127.0.0.1:8000',
            'site_name': 'Website',
            "uname": uname,
            "user": user,
            'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            subject = 'Password Recovery'
            try:
                #send_mail(subject, email, 'cosaimp@gmail.com' , [user.user_email], fail_silently=False)
                sending_mail(user.user_email,email,subject)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("forget_username_msg")
    return render(request,'templates/accounts/forget_username.html')

def index(request):
    return render(request, 'templates/accounts/index.html')
    
def auth_password_confirm(request,uidb64,token):
    #print("Decoding : ",force_text(urlsafe_base64_decode(uidb64)))
    uprofile = UserAccount.objects.get(id = force_str(urlsafe_base64_decode(uidb64)))
    if default_token_generator.check_token(uprofile,token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if str(new_password) != str(confirm_password):              
                messages.error(request,"Please confirm the given password is correct")
                return render(request, 'templates/accounts/reset_password.html')
            else:
                
                #uprofile.user_confirm_password = confirm_password
                uprofile.user_password = urlsafe_base64_encode(force_bytes(new_password))
                uprofile.save()
                return redirect('loginprocess')
    
        return render(request, 'templates/accounts/reset_password.html')
    return HttpResponse('Invalid')
    
def auth_forget_password_msg(request):
    return render(request, 'templates/accounts/verify_email.html')
    
def forget_username_msg(request):
    return render(request, 'templates/accounts/verify_email_uname.html')


def login(request):
    return render(request, 'accounts1/auth_login_boxed.html')

def auth_superadmin(request):
    return render(request, 'accounts1/auth_superadmin.html')
    
def auth_admin(request):
    return render(request, 'accounts1/auth_admin.html')
    
def auth_user(request):
    return render(request, 'accounts1/auth_user.html')


'''
def registration(request):
    registered=False
    capform = CaptchaForms()
    if request.method == 'POST':
    
        cform = UserAccountForm(request.POST)
        capform = CaptchaForms(request.POST)
        if cform.is_valid() and capform.is_valid():
            username = cform.cleaned_data.get('user_name')
            password = cform.cleaned_data.get('user_password')
            con_password = request.POST.get('confirm_password')
                       
            emailid = cform.cleaned_data.get('user_email')
            #user = UserAccount.objects.get(user_name=username)
            authenting = UserAccount.objects.filter(user_name=username).exists()
            authenting_email = UserAccount.objects.filter(user_email=emailid).exists()
            
            is_valid = validate_email(emailid,verify=False)
            #print
            if authenting or authenting_email:              
                messages.error(request,"username or email Already exists")
                return redirect('registration')
                
            if not is_valid:              
                messages.error(request,"emailid not exists")
                return redirect('registration')

            if str(password) != str(con_password):              
                messages.error(request,"Please confirm the given password is correct")
                return redirect('registration')    
            else:
                
                cform.save()
                uprofile = UserAccount.objects.get(user_name = username)
                password = urlsafe_base64_encode(force_bytes(password))
                uprofile.user_password = password
                uprofile.last_login = datetime.datetime.now(tz=timezone.utc)
                uprofile.date_joined = datetime.datetime.now(tz=timezone.utc)
                uprofile.save()
                registered=True
                return redirect('loginprocess')
            return redirect('loginprocess')
    else:
        cform = UserAccountForm()
        
    return render(request, 'templates/accounts/registerpage.html',{'cform':cform,'capform':capform})
    #return render(request, 'templates/accounts/register-cover.html',{'cform':cform,'capform':capform})
'''

def registration(request):
    print("INSIDE registration")
    if request.method == 'POST': 
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        comp_name = request.POST.get('companyname')
        busi_type = request.POST.get('busitype')
        print("\n\n\n\n busitype : ",busi_type)
        password = urlsafe_base64_encode(force_bytes(pwd))
        last_login = datetime.datetime.now(tz=timezone.utc)
        date_joined = datetime.datetime.now(tz=timezone.utc)
        print(name,email,mobile,uname,pwd,password,comp_name,busi_type)
        uprofile = UserAccount.objects.create(name=name,user_name = uname,user_email=email,user_mobile=mobile,user_password=password,date_joined=date_joined,last_login=last_login,user_roles_id=1,user_company_name=comp_name,user_business_type=busi_type,user_social_provider='manual')
        print(uprofile)
        
        # uprofile.save()
        # print ("comp_name :",comp_name)
        # CompanyName=(comp_name,)
        try:
            # add_client_company(comp_name)
            messages.error(request,"User Registration Successfully")
            return render(request,'templates/accounts/registerpage.html')
        except Exception as e:
            messages.error(request,"Error! User Registration")

            print("error while registration : ",e)
            return render(request,'templates/accounts/registerpage.html')
            # return redirect('registration')
        uprofile.save()
        # return redirect('loginprocess')
       
        #registered=True
    return render(request,'templates/accounts/registerpage.html')

def db_connection():
    print("Inside DB connection call :" )
    conn = psycopg2.connect(
            host='127.0.0.1',
            database='vfms_db',
            user='postgres',
            password='123456'
        )
    return(conn)
    
def add_client_company(CompanyName):
    
    conn = db_connection()
    cursor = conn.cursor()
    createdate= datetime.datetime.now(tz=timezone.utc)
    updatedate= datetime.datetime.now(tz=timezone.utc)
    ##check whether company already exists or not
    selectqry="Select count(*) from vfms_company where name = '" + str(CompanyName.upper())   +"'"  
    cursor.execute(selectqry)
    result = cursor.fetchone()[0]
    # result = cursor.fetchone()[0]
    # postgres_cursor.execute(f"SELECT count(*) FROM vfms_objectdetection where video_id_id = {pk};")
    print ('fetch_query  result:',result)
    if (result == 0 or result == None): 
        # if new company then create company in DB

        qry='Insert into vfms_company("name","date_created","date_updated") values (%s,%s,%s)'
        data=(CompanyName,createdate,updatedate)
        print("Inside Add client company :",qry,data)
        try:
            cursor.execute(qry,data)
            conn.commit()
            cursor.close()
            conn.close()
            print("Added client company :", CompanyName.upper())
        except Exception as e:
            cursor.close()
            conn.close()
            print("Error adding client company :", CompanyName.upper())
            print("Error details:", e)
    else:
        print("company already exists")
        cursor.close()
        conn.close()
   #return render(request, 'templates/accounts/registerpage.html')
def loginprocess_func(uname,pwd,request):
    print("INSIDE loginprocess_func")
    global current_login_user_id
    user = custom_authenticate(uname, pwd)
    if user is not None:
        custom_login(request, user)
        role_id = Roles.objects.get(role_name = user.user_roles).id
        print("role_id",role_id)
        

        uprofile = UserAccount.objects.get(user_name = uname)
        uprofile.pre_last_login = uprofile.last_login
        uprofile.last_login = datetime.datetime.now(tz=timezone.utc)
        uprofile.save()
        messages.success(request, 'Login successful!')
        return 'AdminMenu'

        # if role_id == 3:
            
        #     #return redirect('role_auth')

        #     # current_login_user_id = uprofile.id
        #     # print("\n\n cuuuuuuuuuuuuuuuu : ",current_login_user_id)
        #     # return render(request,'templates/user_home.html')
        #     #return render(request, 'templates/dms/AddCustVideo.html')
        #     #return 'ListVideos'
        #     return 'AdminMenu'
            
        # elif role_id == 4:
            
        #     return 'ApproverMenu'
        #     #return redirect('auth_admin')
        # elif role_id == 1:
        #     return 'AdminMenu'
        #     #return redirect('vms_page')
        # else:
        #     return 'loginprocess'
        #     #return redirect('loginprocess')
    else:
        messages.error(request,"Invalid Username and Password")
        return 'loginprocess'
        #return redirect('loginprocess')


def admin_update_user_setting(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        delete_cloud_data = request.POST.get('delete_cloud_data') == 'on'

        # Update user_delete_access field in UserAccount model
        try:
            user = UserAccount.objects.get(pk=user_id)
            user.user_delete_access = delete_cloud_data
            user.save()
            return HttpResponse("User settings updated successfully")
        except UserAccount.DoesNotExist:
            return HttpResponse("User not found", status=404)

    return HttpResponse(status=405)  # Method Not Allowed


def fetch_user_delete_access(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = UserAccount.objects.get(id=user_id)
            user_delete_access = user.user_delete_access
            return JsonResponse({'user_delete_access': user_delete_access})
        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({}, status=400)


def admin_user_settings(request):
    user_accounts = UserAccount.objects.all()
    context = { 'user_accounts': user_accounts }
    return render(request, 'templates/dms/admin_user_setting.html',context)


def admin_user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        
        user = custom_authenticate(uname, pwd)
        
        if user is not None:
            custom_login(request, user)
            
            uprofile = UserAccount.objects.get(user_name=uname)
            uprofile.pre_last_login = uprofile.last_login
            uprofile.last_login = datetime.datetime.now(tz=timezone.utc)
            uprofile.save()
            
            messages.success(request, 'Login successful!')
            return JsonResponse({'redirect_url': '/vfms/Admin_Home/'})  # Adjust redirect URL as per your app
            
        else:
            messages.error(request, "Invalid Username and Password")
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    # If not a POST request or login failed, return to login page
    return JsonResponse({'error': 'Method not allowed'}, status=405)



def loginprocess(request):
    print("INSIDE loginprocess")
    if request.method == 'POST':
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        print("Request data are  ",request.POST)

        if uname == "cosaiadmin" and pwd == "cosaiadmin":
            role_id = Roles.objects.get(role_name = uname).id
            print("your role id is ",role_id)
            if role_id == 2:       
                messages.success(request, 'Admin Login successful!')     
                return redirect('admin')

        pwd = urlsafe_base64_encode(force_bytes(pwd))        
        a= loginprocess_func(uname,pwd,request)        
        return redirect(a)
              
    return render(request,'templates/accounts/login_page.html')
        
def auth_forget_password(request):
    print("INSIDE auth_forget_password")
    if request.method == "POST":
        email = request.POST.get('email')
        authenting = UserAccount.objects.filter(user_email = email,user_social_provider = 'manual').exists()
        user = UserAccount.objects.get(user_email = email,user_social_provider = 'manual')
        
        user_id = UserAccount.objects.get(user_email = email,user_social_provider = 'manual').id
        if authenting:
            subject = "Password Reset Requested"
            email_template_name = "accounts/auth_pass_recovery_email_content.txt"
            c = {
            "email":email,
            'domain':'127.0.0.1:8000',
            'site_name': 'Website',
            "uid": urlsafe_base64_encode(force_bytes(user_id)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                #send_mail(subject, email, 'cosaimp@gmail.com' , [user.user_email], fail_silently=False)
                sending_mail(user.user_email,email)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("auth_forget_password_msg")
    return render(request,'templates/accounts/forget_password.html')
    
@login_required
def logout_request(request):
    print("Inside Logout")
    custom_logout(request)
    #messages.info(request, "You have successfully logged out.") 
    return redirect('loginprocess')
      
def super_admin_view(request):
    print("INSIDE auth_forget_password")
    return render(request, 'accounts1/super_admin.html')

@login_required
def role_based_auth(request):
    multi_auth = UserAccount.objects.all()
    roles = Roles.objects.all()
    context = {'multi_auth':multi_auth, 'roles':roles}
    return render(request, 'accounts1/role_auth.html', context)

def update_auth_form(request, pk):
    multi_auth = UserAccount.objects.get(id = pk)
    form = UserAccountUpdateForm(instance = multi_auth)
    if request.method == "POST":
        form = UserAccountUpdateForm(request.POST, instance = multi_auth)
        if form.is_valid():
            form.save()
            return redirect('role_auth')
    context = {'form': form}
    return render(request, 'accounts1/update_auth_form.html', context)

   
def validate_username(request):
    print("Inside Validate username")
    is_is_status=""
    username = request.GET.get('username', None)
    if UserAccount.objects.filter(user_name=username).exists():
        print("user exists")
        is_is_status = UserAccount.objects.get(user_name=username).user_status
    email = request.GET.get('email', None)
    password = request.GET.get('password', None)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA : ",is_is_status,email,username,password,urlsafe_base64_encode(force_bytes(password)),UserAccount.objects.filter(user_email = email,user_social_provider='manual').exists(),UserAccount.objects.filter(user_name=username,user_password=urlsafe_base64_encode(force_bytes(password))).exists())
    
    
    
    data = {
        'is_username': UserAccount.objects.filter(user_name=username).exists(),
        'is_email': UserAccount.objects.filter(user_email=email).exists(),
        'is_manualemail' : UserAccount.objects.filter(user_email = email,user_social_provider='manual').exists(),
        'is_password': UserAccount.objects.filter(user_password=urlsafe_base64_encode(force_bytes(password))).exists(),
        'is_user' : UserAccount.objects.filter(user_name=username,user_password=urlsafe_base64_encode(force_bytes(password))).exists(),
        'is_status' : UserAccount.objects.filter(user_name=username,user_status=True).exists()
        
    }
    print(data)
    return JsonResponse(data)
'''   
def validate_password(request):
    username = request.GET.get('username', None)
    #email = request.GET.get('email', None)
    password = request.POST.get('password', None)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA : ",username,password,urlsafe_base64_encode(force_bytes(password)),UserAccount.objects.filter(user_name=username,user_password=urlsafe_base64_encode(force_bytes(password))).exists())
    
    
    data = {
        'is_username': UserAccount.objects.filter(user_name=username).exists(),
        #'is_email': UserAccount.objects.filter(user_email=email).exists(),
        'is_password': UserAccount.objects.filter(user_password=urlsafe_base64_encode(force_bytes(password))).exists(),
        'is_user' : UserAccount.objects.filter(user_name=username,user_password=urlsafe_base64_encode(force_bytes(password))).exists()
        
    }
    return JsonResponse(data)
'''
class DeleteUser(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        UserAccount.objects.get(id = id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

class UpdateRoles(View):

    def post(self, request):
        user_id = request.POST.get('user_id', None)
        role_id = request.POST.get('role_id', None)
        print(user_id, role_id)
        role_obj = Roles.objects.get(id = role_id)
        multi_auth = UserAccount.objects.get(id = user_id)
        multi_auth.user_roles = role_obj
        multi_auth.save()    
        data = {
            'id':multi_auth.id,
            'role':role_obj.role,
            'updated':True
        }
        return JsonResponse(data)




def role_data_table_view(request):
    return render(request, 'templates/accounts/roles_datatable.html')

class RolesDataTable(View):

    def get(self, request):
        roles1 = Roles.objects.values()
        roles1 = {"data": list(roles1)}
        return JsonResponse(roles1)

class DeleteRoleDataTable(View):
    """Delete roles"""
    def post(self, request):
        id1 = request.POST.get('id', None)
        try:
            Roles.objects.get(id = id1).delete()
            data = {'deleted': True}
        except ObjectDoesNotExist:
            data = {'deleted': False}
        
        return JsonResponse(data)

class AddRoleDataTable(View):

    def post(self, request):
        role_name1 = request.POST.get('role_name', None)
        role_description1 = request.POST.get('role_description', None)
        print(role_name1, role_description1)
        obj = Roles.objects.create(role_name = role_name1, role_description = role_description1, role_status = True)
        data = {'id':obj.id, 'role_name':obj.role_name, 'role_description':obj.role_description, 'role_status': obj.role_status}
        return JsonResponse(data)

class GetRoleData(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        obj = Roles.objects.get(pk = id1)
        data = {'id':obj.id, 'role_name':obj.role_name, 'role_description':obj.role_description, 'role_status':obj.role_status}
        print(data)
        return JsonResponse(data)



class UpdateRoleData(View):

    def post(self, request):
        id1 = request.POST.get('id', None)
        role_name1 = request.POST.get('role_name', None)
        role_description1 = request.POST.get('role_description', None)
        try:
            obj = Roles.objects.get(id = id1)
            obj.role_name = role_name1
            obj.role_description = role_description1
            obj.save()
            data = {'success': True, 'id':obj.id, 'role_name':obj.role_name, 'role_description':obj.role_description, 'role_status':obj.role_status}
        except Roles.DoesNotExist:
            data = {'success': False}
        return JsonResponse(data)

def user_table_view(request):
    user_account_form = UserAccountForm()
    context = {'user_account_form': user_account_form}
    return render(request, 'templates/accounts/useraccount_datatable.html', context)

class UserDataTable(View):

    def get(self, request):
        print("INSIDE UserDataTable")
        user_account = UserAccount.objects.values()
        user_account = {"data": list(user_account)}
        return JsonResponse(user_account)

# class CreateKvsData(View):

#     def get(self, request):
#         camera_name = request.GET.get('camera_name', None)
#         video_mode = request.GET.get('video_mode', None)
#         stream_name = request.GET.get('stream_name', None)
#         # start_time = request.GET.get('start_time', None)
#         # end_time = request.GET.get('end_time', None)
#         access_key = request.GET.get('access_key', None)
#         secret_key = request.GET.get('secret_key', None)
#         region = request.GET.get('region', None)
#         expire = request.GET.get('expire', None)
        
#         obj = KvsStream.objects.create(
#             camera_name = camera_name,
#             video_mode = video_mode,
#             stream_name = stream_name,
#             # start_time = start_time,
#             # end_time = end_time,
#             access_key = access_key,
#             secret_key = secret_key,
#             region = region,
#             expire = expire,
#         )
        
#         kvs_data = {
#             'id': obj.id,
#             'camera_name': obj.camera_name,
#             'video_mode': obj.video_mode,
#             'stream_name': obj.stream_name,
#             # 'start_time': obj.start_time,
#             # 'end_time': obj.end_time,
#             'access_key': obj.access_key,
#             'secret_key': obj.secret_key,
#             'region': obj.region,
#             'expire': obj.expire,
#         }

#         data = {'user':kvs_data}
#         return JsonResponse(data)

# class UpdateKvsData(View):

#     def get(self, request):
#         id1 = request.GET.get('id', None)
#         camera_name1 = request.GET.get('camera_name', None)
#         video_mode1 = request.GET.get('video_mode', None)
#         stream_name1 = request.GET.get('stream_name', None)
#         # start_time = request.GET.get('start_time', None)
#         # end_time = request.GET.get('end_time', None)
#         access_key1 = request.GET.get('access_key', None)
#         secret_key1 = request.GET.get('secret_key', None)
#         region1 = request.GET.get('region', None)
#         expire1 = request.GET.get('expire', None)

#         obj = KvsStream.objects.get(id = id1)
#         obj.camera_name = camera_name1
#         obj.video_mode = video_mode1
#         obj.stream_name = stream_name1
#         # start_time = start_time,
#         # end_time = end_time,
#         obj.access_key = access_key1
#         obj.secret_key = secret_key1
#         obj.region = region1
#         obj.expire = expire1
#         obj.save()
        
#         user = {
#             'id': obj.id,
#             'camera_name': obj.camera_name,
#             'video_mode': obj.video_mode,
#             'stream_name': obj.stream_name,
#             # 'start_time': obj.start_time,
#             # 'end_time': obj.end_time,
#             'access_key': obj.access_key,
#             'secret_key': obj.secret_key,
#             'region': obj.region,
#             'expire': obj.expire,
#         }
#         data = {'user':user}
#         return JsonResponse(data)

# class DeleteKvsData(View):

#     def get(self, request):
#         id1 = request.GET.get('id', None)
#         KvsStream.objects.get(id = id1).delete()
#         data = {
#             'deleted': True
#         }
#         return JsonResponse(data)
