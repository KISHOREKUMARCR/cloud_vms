
# import http reponse library to return responses to the request we receive
from django .http import HttpResponse
from .models import *
from django.shortcuts import render
from accounts.models import UserAccount, Roles ,UserSocialAccount

def page(request):
       
       return render(request,'templates/main_base.html')
        #return render(request,'F:\\Django\\Projects\\DMS\\templates\\dms\\index.html')

#redirectng to success url
def successpage(request):
         
    return render(request,'templates/dms/success.html')

#redirectng to workinprogress url
def WorkInProgress(request):
         
    return render(request,'templates/dms/WorkInProgress.html')

#redirectng to error url
def ErrorMessage(request):
         
    return render(request,'templates/dms/Error.html')

    #redirectng to Admin Menu url
# def AdminMenu(request):
#     print("AdminMenu called")   
#     userid = request.session.get('user_id')  
#     if userid:
        

#         total_company = Company.objects.filter(userid=userid).count()
#         total_projects = Project.objects.filter(userid=userid).count()
#         # total_locations = CloudURI.objects.filter(userid=userid).count()
#         # total_locations = CloudURI.objects.filter(userid=userid).values('location_name').distinct().count()

#         # total_cloud_url = CloudURI.objects.filter(userid=userid).count()

#         total_locations = NewCloudURI.objects.filter(userid=userid).count()
#         total_locations = NewCloudURI.objects.filter(userid=userid).values('location_name').distinct().count()

#         total_cloud_url = NewCloudURI.objects.filter(userid=userid).count()
        
#     else:
#         total_company = 0
#         total_projects = 0
#         total_locations = 0
#         total_cloud_url = 0
    
#     context={'total_company':total_company,'total_projects':total_projects,'total_locations':total_locations,'total_cloud_url':total_cloud_url}
#     return render(request, "templates/dms/dashboards-analytics.html",context)

def AdminMenu(request):
    user_id = request.session.get('user_id')   
    data = NewCloudURI.objects.filter(userid=user_id).order_by('-id')[:10]
    company_list = Company.objects.filter(userid=user_id)   
    user_account = UserAccount.objects.get(id=user_id)
    print("*******************",user_account)
    return render(request, 'templates/dms/view_cloud_uri.html' ,{'data' : data,'company_list':company_list,'user_account':user_account})



#redirectng to Approver Menu url
def ApproverMenu(request):
         
    return render(request,'templates/main_base.html')

#redirectng to User Menu url
def UserMenu(request):
         
    return render(request,'templates/main_base.html')


def admin(request):
    user_accounts = UserAccount.objects.all()
    context = {
    'user_accounts': user_accounts 
    }

    return render(request, 'templates/dms/admin_view_page.html', context)



#redirectng to success url
def downloadreport(request):
         
    return render(request,'templates/dms/ReportDownload.html')