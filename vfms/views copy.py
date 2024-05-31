from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.views import View 
from django.views.generic.edit import UpdateView
from accounts.models import *
from django.conf import settings
from django.db.models import Q
from django.db import IntegrityError
import psycopg2
from psycopg2 import sql
from urllib.parse import quote
from django.utils import timezone


import json
import requests

# import paramiko
import datetime
from django.core.mail import send_mail
from accounts.views import *

from .filters import *
from accounts.decorators import login_required

##########
import os
import shutil
from django.conf import settings
from django.templatetags import static
####
# from .filters import*
from django.forms import inlineformset_factory
from django.http import JsonResponse,HttpResponse, Http404,HttpResponseRedirect

### gdrive
from google.oauth2.credentials import Credentials
from google.auth import impersonated_credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials

###
from googleapiclient.http import MediaFileUpload
from django.shortcuts import render
from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

###pydrive
import argparse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
## pemfile p12key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends.openssl import backend
# from cryptography.hazmat.backends.openssl import load_certificate
from google.auth.transport import requests
from google.auth import exceptions
from google.auth import jwt

### dashboard information
# def dashboarddata(request):
#   if request.method =="GET":
#     total_company=Company.objects.all().count()
#     total_projects=Project.objects.all().count()
#     total_locations=Location.objects.all().count()
#     total_videos=VideoFiles.objects.all().count()
#     context={'total_company':total_company,'total_projects':total_projects,'total_locations':total_locations,'total_videos':total_videos}
#     return render(request, "templates/dms/Dashboard.html", context)
#   else:
#     return redirect('Error_url')
def dashboarddata(request):
  if request.method =="GET":
    total_company=Company.objects.all().count()
    total_projects=Project.objects.all().count()
    total_locations=Location.objects.all().count()
    total_videos=VideoFiles.objects.all().count()
    context={'total_company':total_company,'total_projects':total_projects,'total_locations':total_locations,'total_videos':total_videos}
    return render(request, "templates/dms/dashboards-analytics.html", context)
  else:
    return redirect('Error_url')

### aduit log for all the actions performed
def auditdata(form_name,action_performed,acted_by):
    acted_by='Admin' ## temporary set as admin
    auditlog = AuditLog(form_name=form_name, action_performed=action_performed,acted_by=acted_by) # create new model instance
    auditlog.save() #save to db



### loading media files images
def WorkInProgress(request):
    path = settings.MEDIA_ROOT
    print(path)
    img_list = os.listdir(path + '/images')
    print(img_list)
    context = {'images' : img_list}
    return render(request, "templates/dms/WorkInProgress.html", context)

## to add new company information entered by user
def my_form(request):
    # user = get_current_user(request)
    # user_id = user.id
  if request.method == "POST":
    form = MyForm(request.POST)
    if form.is_valid():
      
      form.save()
      ###adding to the auditlog ###
      auditdata('Company','ADD','Admin')
      # auditlog = AuditLog(form_name='AddCompany', action_performed='ADD',acted_by='Admin') # create new model instance
      # auditlog.save() #save to db
      ###end##
      return redirect('success_url')
    else:
      return render(request, 'templates/dms/AddCompany.html', {'form': form})
  else:
      form = MyForm()
      return render(request, 'templates/dms/AddCompany.html', {'form': form})


# to update specific company information modified by user

class CompanyUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_company=Company.objects.get(id=pk_id)
    form=MyForm(instance=get_company)
    context={'form':form}
    return render(request,'templates/dms/CompanyUpdate.html',context)

  def get(self,request,pk_id):
    get_company=Company.objects.get(id=pk_id)
    form=MyForm(instance=get_company)
    context={'form':form}

    return render(request,'templates/dms/CompanyUpdate.html', context)

  def post(self,request,pk_id):
    update_company=Company.objects.get(id=pk_id)
    self.form=MyForm(request.POST,instance=update_company)
    if self.form.is_valid():
      self.form.save()
      ###adding to the auditlog ###
      auditdata('Company','Update','Admin')
      return redirect('success_url')
    else:
      return render(request, 'templates/dms/CompanyUpdate.html', {'form': self.form})


## listing company details

class ListCompany(View):
    def get(self,request,*args,**kwargs):
        form = MyForm()
        all_companies=Company.objects.all()
        context={'all_companies':all_companies,'form':form}
      
        return render (request,'templates/dms/ListCompany.html',context=context)

## new method ## Modify company ## list generation

def edit_form(request):
  
  if request.method == "POST":
    edit_company=request.POST.GET(id)
    print('edit_company',edit_company)
    try:
      update_company=Company.objects.get(id=edit_company)
      if update_company!=None:
        print("not None")
        form = MyForm(request.POST)
        if form.is_valid():
          form.save()
          ###adding to the auditlog ###
          auditdata('Company','Update','Admin')
          return redirect('success_url')
        else:
            form =  MyForm(request.POST)
            error = "Invalid data please check"
            return render(request, 'templates/dms/ModifyCompany.html', {'form': form,'error':error})
    except Exception  as e:
          return render(request, 'templates/dms/ModifyCompany.html', {'form': form,'error':e})
          # return redirect('Error_url')
       
  else:
    all_companies=Company.objects.all()
    context={'all_companies':all_companies}

    return render(request,'templates/dms/ModifyCompany.html', context)


###### Project relevant classes########


class ListProject(View):
    def get(self,request,*args,**kwargs):
        form = ProjForm()
        all_projects=Project.objects.all()
        context={'all_projects':all_projects,'form':form}
       
        return render (request,'templates/dms/ListProject.html',context=context)

## to add new project information entered by user
@login_required
def project_form(request):
  if request.method == "POST":
    company=request.POST.get("company")
    if (company):
      form = ProjForm(request.POST)
    
    # print('PROJECT FORM IS VALID OR NOT :' ,form.is_valid())
      if form.is_valid():
        form.save()
        ###adding to the auditlog ###
        auditdata('Project','Add','Admin')
        return redirect('success_url')
      else:
         error = "Invalid data. Please check"
         return render(request, 'templates/dms/AddProject.html', {'form': form,'error':error})
    else:
         error = "Company does not exists. Please check"
         return render(request, 'templates/dms/AddProject.html', {'form': form,'error':error})
  else:
      #  GET method
      form = ProjForm()
      return render(request, 'templates/dms/AddProject.html', {'form': form})

# to update station information 
@login_required
def editproj_form(request):
  if request.method == "POST":
    form = ProjForm(request.POST)
    if form.is_valid():
      form.save()
      ###adding to the auditlog ###
      auditdata('Project','update','Admin')
      return redirect('success_url')
    else:
        form = ProjForm()
        return render(request, 'templates/dms/ModifyProject.html', {'form': form})
  else:
    all_projects=Project.objects.all()
    context={'all_projects':all_projects}

    return render(request,'templates/dms/ModifyProject.html', context)


# to update specific project information edited by user

class ProjectUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_project=Project.objects.get(id=pk_id)
    form=ProjForm(instance=get_project)
    context={'form':form}
    return render(request,'templates/dms/ProjectUpdate.html',context)

  def get(self,request,pk_id):
    get_project=Project.objects.get(id=pk_id)
    form=ProjForm(instance=get_project)
    context={'form':form}

    return render(request,'templates/dms/ProjectUpdate.html', context)

  def post(self,request,pk_id):
    update_Project=Project.objects.get(id=pk_id)
    self.form=ProjForm(request.POST,instance=update_Project)
    if self.form.is_valid():
      self.form.save()
      ###adding to the auditlog ###
      auditdata('Project','update','Admin')
      return redirect('success_url')
    else:
      return self.render(request)




########## Station/Location class ##############
## station List

class ListStation(View):
    def get(self,request,*args,**kwargs):
        form = LocationForm()
        all_locations=Location.objects.all()
         
        context={'all_locations':all_locations,'form':form}
       
        return render (request,'templates/dms/ListStation.html',context=context)

## to add new station information entered by user
def station_form(request):
    if request.method == "POST":
      form = LocationForm(request.POST)
      if form.is_valid():
        form.save()
        ###adding to the auditlog ###
        auditdata('Station','Add','Admin')
      return redirect('success_url')
    else:
      form = LocationForm()
      return render(request, 'templates/dms/AddStation.html', {'form': form})

# to update station information - listing for user
def editstn_form(request):
  if request.method == "POST":
    form = LocationForm(request.POST)
    if form.is_valid():
      form.save()
      ###adding to the auditlog ###
      auditdata('station','update','Admin')
      return redirect('success_url')
    else:
        form = LocationForm()
        return render(request, 'templates/dms/ModifyStation.html', {'form': form})
  else:
    all_locations=Location.objects.all()
    context={'all_locations':all_locations}

    return render(request,'templates/dms/ModifyStation.html', context)

# to update specific station information edited by user

class StationUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_station=Location.objects.get(id=pk_id)
    form=LocationForm(instance=get_station)
    context={'form':form}
    return render(request,'templates/dms/StationUpdate.html',context)

  def get(self,request,pk_id):
    get_station=Location.objects.get(id=pk_id)
    form=LocationForm(instance=get_station)
    context={'form':form}

    return render(request,'templates/dms/StationUpdate.html', context)

  def post(self,request,pk_id):
    update_station=Location.objects.get(id=pk_id)
    self.form=LocationForm(request.POST,instance=update_station)
    if self.form.is_valid():
      self.form.save()
      auditdata('station','update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)


############## camera Model #############
## list camera models

class ListcModel(View):
  
    def get(self,request, *args,**kwargs):
        form = CModelForm()
        all_cModels=CameraModel.objects.all()
        context={'all_cModels':all_cModels,'form':form}
        
        return render(request,'templates/dms/ListCameraModel.html',context=context)

## to add new camera model information entered by user
@login_required
def Cmodel_form(request):
  if request.method == "POST":
    form = CModelForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('cameraModel','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      form = CModelForm()
      return render(request, 'templates/dms/AddCameraModel.html', {'form': form})

# to update Camera Model information modified by user
@login_required
def editcModel_form(request):
  if request.method == "POST":
    form = CModelForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('cameraModel','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = CModelForm()
        return render(request, 'templates/dms/ModifyCameraModel.html', {'form': form})
  else:
    all_cModels=CameraModel.objects.all()
    context={'all_cModels':all_cModels}

    return render(request,'templates/dms/ModifyCameraModel.html', context)

# to update specific camera model information edited by user

class CModelUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_cModel=CameraModel.objects.get(id=pk_id)
    form=CModelForm(instance=get_cModel)
    context={'form':form}
    return render(request,'templates/dms/CModelUpdate.html',context)

  def get(self,request,pk_id):
    get_cModel=CameraModel.objects.get(id=pk_id)
    form=CModelForm(instance=get_cModel)
    context={'form':form}

    return render(request,'templates/dms/CModelUpdate.html', context)

  def post(self,request,pk_id):
    update_cModel=CameraModel.objects.get(id=pk_id)
    self.form=CModelForm(request.POST,instance=update_cModel)
    if self.form.is_valid():
      self.form.save()
      auditdata('cameraModel','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)




### Camera Position ########

class ListcPosition(View):
    def get(self,request,*args,**kwargs):
        form = CPositionForm()
        all_cpositions=CameraPosition.objects.all()
        context={'all_cpositions':all_cpositions,'form':form}
      
        return render (request,'templates/dms/ListCameraPosition.html',context=context)



## to add new camera position  information entered by user
@login_required
def CPosition_form(request):
  if request.method == "POST":
    form = CPositionForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('cameraPosition','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      form = CPositionForm()
      return render(request, 'templates/dms/AddCameraPosition.html', {'form': form})


# to update station information modified by user
@login_required
def editcPosition_form(request):
  if request.method == "POST":
    form = CPositionForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('cameraPosition','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = CPositionForm()
        return render(request, 'templates/dms/ModifyCameraPosition.html', {'form': form})
  else:
    all_cpositions=CameraPosition.objects.all()
    context={'all_cpositions':all_cpositions}

    return render(request,'templates/dms/ModifyCameraPosition.html', context)

# to update specific camera Position information edited by user

class CPositionUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_cpos=CameraPosition.objects.get(id=pk_id)
    form=CPositionForm(instance=get_cpos)
    context={'form':form}
    return render(request,'templates/dms/CModelUpdate.html',context)

  def get(self,request,pk_id):
    get_cpos=CameraPosition.objects.get(id=pk_id)
    form=CPositionForm(instance=get_cpos)
    context={'form':form}

    return render(request,'templates/dms/CModelUpdate.html', context)

  def post(self,request,pk_id):
    update_cPos=CameraPosition.objects.get(id=pk_id)
    self.form=CPositionForm(request.POST,instance=update_cPos)
    if self.form.is_valid():
      self.form.save()
      auditdata('cameraPosition','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)


############3 USER PROFILE ##############

## to add new company information entered by user
@login_required
def add_user(request):
  if request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('User','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      form = UserForm()
      return render(request, 'templates/dms/AddUser.html', {'form': form})


# to update specific company information modified by user

class UserProfileUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_user=User.objects.get(id=pk_id)
    form=UserForm(instance=get_user)
    context={'form':form}
    return render(request,'templates/dms/ProfileUpdate.html',context)

  def get(self,request,pk_id):
    get_user=User.objects.get(id=pk_id)
    form=UserForm(instance=get_user)
    context={'form':form}

    return render(request,'templates/dms/ProfileUpdate.html', context)

  def post(self,request,pk_id):
    update_user=User.objects.get(id=pk_id)
    self.form=UserForm(request.POST,instance=update_user)
    if self.form.is_valid():
      self.form.save()
      auditdata('User','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)


## listing company details

class ListUser(View):
    def get(self,request,*args,**kwargs):
        form = UserForm()
        all_users=User.objects.all()
        context={'all_users':all_users,'form':form}
      
        return render (request,'templates/dms/ListUser.html',context=context)

## list userprofile information for editing
@login_required
def edit_user(request):
  if request.method == "POST":
    form = UserForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('User','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = UserForm()
        return render(request, 'templates/dms/ModifyUser.html', {'form': form})
  else:
    all_users=User.objects.all()
    context={'all_users':all_users}

    return render(request,'templates/dms/ModifyUser.html', context)


############ ROLEs ##############

## to add new role  information entered by user
@login_required
def add_role(request):
  if request.method == "POST":
    form = RoleForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('Role','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      form = RoleForm()
      return render(request, 'templates/dms/AddRole.html', {'form': form})


# to update specific  role modified by user

class RoleUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_role=Role.objects.get(id=pk_id)
    form=RoleForm(instance=get_role)
    context={'form':form}
    return render(request,'templates/dms/RoleUpdate.html',context)

  def get(self,request,pk_id):
    get_role=Role.objects.get(id=pk_id)
    form=RoleForm(instance=get_role)
    context={'form':form}

    return render(request,'templates/dms/RoleUpdate.html', context)

  def post(self,request,pk_id):
    update_role=Role.objects.get(id=pk_id)
    self.form=RoleForm(request.POST,instance=update_role)
    if self.form.is_valid():
      self.form.save()
      auditdata('Role','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)


## listing role details

class ListRole(View):
    def get(self,request,*args,**kwargs):
        form = RoleForm()
        all_roles=Role.objects.all()
        context={'all_roles':all_roles,'form':form}
      
        return render (request,'templates/dms/ListRole.html',context=context)

## list role information for editing
def edit_role(request):
  if request.method == "POST":
    form = RoleForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('Role','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = RoleForm()
        return render(request, 'templates/dms/ModifyRole.html', {'form': form})
  else:
    all_roles=Role.objects.all()
    context={'all_roles':all_roles}

    return render(request,'templates/dms/ModifyRole.html', context)

############ Video Files ##############

## to add new video File format  information entered by user
@login_required
def add_vff(request):
  if request.method == "POST":
    form = VideoFileForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('VideoFileFormat','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      form = VideoFileForm()
      return render(request, 'templates/dms/AddVFF.html', {'form': form})


# to update specific  video File format modified by user

class VFFUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_vff=VideoFF.objects.get(id=pk_id)
    form=VideoFileForm(instance=get_vff)
    context={'form':form}
    return render(request,'templates/dms/VFFUpdate.html',context)

  def get(self,request,pk_id):
    get_vff=VideoFF.objects.get(id=pk_id)
    form=VideoFileForm(instance=get_vff)
    context={'form':form}

    return render(request,'templates/dms/VFFUpdate.html', context)

  def post(self,request,pk_id):
    update_vff=VideoFF.objects.get(id=pk_id)
    self.form=VideoFileForm(request.POST,instance=update_vff)
    if self.form.is_valid():
      self.form.save()
      auditdata('VideoFileFormat','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)


## listing video File format details

class ListVFF(View):
    def get(self,request,*args,**kwargs):
        form = VideoFileForm()
        all_vff=VideoFF.objects.all()
        context={'all_vff':all_vff,'form':form}
      
        return render (request,'templates/dms/ListVFF.html',context=context)

## list video File format information for editing
@login_required
def edit_vff(request):
  if request.method == "POST":
    form = VideoFileForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('VideoFileFormat','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = VideoFileForm()
        return render(request, 'templates/dms/ModifyVFF.html', {'form': form})
  else:
    all_vff=VideoFF.objects.all()
    context={'all_vff':all_vff}

    return render(request,'templates/dms/ModifyVFF.html', context)

############ Light Intensity  ##############

## to add new Light Intensity category  information entered by user
@login_required
def add_li(request):
  if request.method == "POST":
    form = LIForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('LightIntensity','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      form = LIForm()
      return render(request, 'templates/dms/AddLI.html', {'form': form})


# to update specific  Light Intensity  modified by user

class LIUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_li=LItypes.objects.get(id=pk_id)
    form=LIForm(instance=get_li)
    context={'form':form}
    return render(request,'templates/dms/LIUpdate.html',context)

  def get(self,request,pk_id):
    get_li=LItypes.objects.get(id=pk_id)
    form=LIForm(instance=get_li)
    context={'form':form}

    return render(request,'templates/dms/LIUpdate.html', context)

  def post(self,request,pk_id):
    update_li=LItypes.objects.get(id=pk_id)
    self.form=LIForm(request.POST,instance=update_li)
    if self.form.is_valid():
      self.form.save()
      auditdata('LightIntensity','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)


## listing Light Intensity  details

class ListLI(View):
    def get(self,request,*args,**kwargs):
        form = LIForm()
        all_li=LItypes.objects.all()
        context={'all_li':all_li,'form':form}
      
        return render (request,'templates/dms/ListLI.html',context=context)

## list Light Intensity  information for editing
@login_required
def edit_li(request):
  if request.method == "POST":
    form = LIForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('LightIntensity','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = LIForm()
        return render(request, 'templates/dms/ModifyLI.html', {'form': form})
  else:
    all_li=LItypes.objects.all()
    context={'all_li':all_li}

    return render(request,'templates/dms/ModifyLI.html', context)
  

### Labelling

############ Label Informations  ##############

## to add new Light Intensity category  information entered by user
@login_required
def ttImportLabel(request):
  if request.method == "POST":
    form = LIForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('ImportLabel','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      form = LIForm()
      return render(request, 'templates/dms/AddLI.html', {'form': form})

import openpyxl
import psycopg2
from django.shortcuts import render
@login_required
def ImportLabel(request):
    if request.method == 'POST' and request.FILES['xlsx_file']:
        # Get the uploaded file
        xlsx_file = request.FILES['xlsx_file']

        # Load the XLSX file
        wb = openpyxl.load_workbook(xlsx_file)

        # Select the active sheet
        sheet = wb.active
        

        #   'NAME': database_name,
        # # 'NAME': 'tms_product5',
        # 'USER': 'postgres',
        # 'PASSWORD': 'cosaimp@2020',
        # 'HOST': '127.0.0.1',
        # 'PORT': '5432',

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='vfms_db',
            user='postgres',
            password='cosaimp@2020'
        )
        cursor = conn.cursor()

        # Iterate over rows in the sheet and insert into the database
        for row in sheet.iter_rows(values_only=True):
            # Assuming your XLSX file has three columns: col1, col2, col3
            # col1, col2, col3, col4, col5, col6, col7, col8 = row
            # print("col1 : ",col1, " Col2 : ", col2 ," col3: ", col3)
            # query='INSERT INTO vfms_LabelInformation ("LName", "AnnotationCnt", "ImageCnt", "LightCdn", "CameraHeight", "RoadType", "Reviewed", "DatasetLocation") VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            # record_to_insert=(col1, col2, col3, col4, col5, col6, col7, col8)
            col1, col2, col3, col4, col5, col6, col7, col8,col9,col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20=row
            print("col1 : ", col1)
            fetch_query=f"""SELECT id FROM vfms_Location where name = '{col1}'"""
            print(fetch_query)
            cursor.execute(fetch_query)
            LNameID = cursor.fetchone()[0]
            print("LNameID : ",LNameID)

            # area_name	auto_rickshaw	bus	car	others(earth mover)	lcv	mini bus	Two Wheeler	multi axle	Truck_3Axle	Truck_4Axle	Truck_6Axle	tracktor	tracktor_trailer	Truck_2Axle	van	Eicher	instance_count	image_count
            ins_query='INSERT INTO vfms_AddLabelInfo("LName_id", "Threewheelercnt", "Buscnt", "Carcnt","Otherscnt","Lcvcnt","MiniBuscnt","Twowheelercnt", "MultiAxlecnt","Axle3cnt","Axle4cnt","Axle6cnt","Tractorcnt","TTrailercnt","Truck2Acnt","Vancnt","Echiercnt","AnnotationCnt", "ImageCnt", "DatasetLocation") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            record_to_insert=(LNameID, col2, col3, col4, col5, col6, col7, col8,col9,col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20)


            print(ins_query , " ---- " ,record_to_insert)
            cursor.execute(ins_query,record_to_insert)
    #          postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
    # record_to_insert = (5, 'One Plus 6', 950)
    # cursor.execute(postgres_insert_query, record_to_insert

        # Commit the changes and close the database connection
        conn.commit()
        cursor.close()
        conn.close()

        return render(request, 'templates/dms/success.html')
    return render(request, 'templates/dms/upload_dataset.html')


## listing label  details

class ListLabel(View):
    def get(self,request,*args,**kwargs):
        form = AddLabelForm()
        all_labels=AddLabelInfo.objects.all()
        # print(all_labels)
        context={'all_labels':all_labels,'form':form}
        
      
        return render (request,'templates/dms/ListLabel.html',context=context)
    

    
## to add new location/station label information 
@login_required
def add_label(request):
  if request.method == "POST":
    form = AddLabelForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('Labelinformation','Add','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
  else:
      print("ADD LABEL INFO")
      form = AddLabelForm()
      return render(request, 'templates/dms/AddLabelInfo.html', {'form': form})
  
## list label  information for editing
@login_required
def edit_label(request):
  if request.method == "POST":
    form = AddLabelForm(request.POST)
    if form.is_valid():
      form.save()
      auditdata('AddLabelForm','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = AddLabelForm()
        return render(request, 'templates/dms/ModifyLabelInfo.html', {'form': form})
  else:
    all_label=AddLabelInfo.objects.all()
    context={'all_label':all_label}

    return render(request,'templates/dms/ModifyLabelInfo.html', context)
  
# to update specific  label information  modified by user

class LabelUpdate(UpdateView):
  
  def render(self,request,pk_id):
    get_label=AddLabelInfo.objects.get(id=pk_id)
    form=AddLabelForm(instance=get_label)
    context={'form':form}
    return render(request,'templates/dms/LabelUpdate.html',context)

  def get(self,request,pk_id):
    get_label=AddLabelInfo.objects.get(id=pk_id)
    form=AddLabelForm(instance=get_label)
    context={'form':form}

    return render(request,'templates/dms/LabelUpdate.html', context)

  def post(self,request,pk_id):
    update_label=AddLabelInfo.objects.get(id=pk_id)
    self.form=AddLabelForm(request.POST,instance=update_label)
    if self.form.is_valid():
      self.form.save()
      auditdata('AddLabelInfo','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
      return self.render(request)

### labelling





######## Video Files upload ##############3

class GetProjects(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        projects = Project.objects.filter(company_id = id1).values('id','name')
        
        data = {'data':list(projects)}
        print(data)
        return JsonResponse(data)

class GetLocations(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        locations = Location.objects.filter(project_id = id1).values('id','name')
        
        data = {'data':list(locations)}
        return JsonResponse(data)


############videos files @@@@@@@@@
############function to filter and pass only the valid  inputs #######
def set_if_not_none(mapping, key, value):
    print(key,'__',value)
    if value is not None and not value == "":
        mapping[key] = value
        print(mapping)

       
class ListVideos(View): ## ,pk_id
    def get(self,request,*args,**kwargs):
        
        print('request.GET', request.GET)
        form = VFiles()
        # all_Videos=VideoFiles.objects.all()
        sort_params = {}
             

       ####### Get the inputs from  filter #######
        PName=request.GET.get('ProjectName', None)
        SName=request.GET.get('StationName', None)
        LICat=request.GET.get('LICate',None)
        vidstatus=request.GET.get('videostatus',None)

      ####### call function to pass only the valid filter inputs #######
        set_if_not_none(sort_params, 'ProjectName', PName)
        set_if_not_none(sort_params, 'StationName', SName)
        set_if_not_none(sort_params, 'LICate', LICat)
        set_if_not_none(sort_params, 'videostatus', vidstatus)
        print(sort_params)
        #######pass the valid inputs filters to db model to fetch records ########
        all_Videos=VideoFiles.objects.filter(**sort_params)
            
        VideoFilter=VideoFileFilter(queryset=all_Videos)
                     
        context={'all_Videos':all_Videos,'form':form,'VideoFilter':VideoFilter}
       
        return render (request,'templates/dms/ListVideos.html',context=context)

## to add new project information entered by user
@login_required
def Videos_form(request):
  print("POSTING POSTING",request.POST)
 
  # path = settings.EXTERNAL_ROOT
  # print(path)
  # Thumbnail_list = os.listdir(path + '/ThumbNailImages')
  # print(Thumbnail_list)
  # video_list = os.listdir(path + '/UploadedVideos')
  # print(video_list)
  if request.method == "POST":
    print("POST METHOD")
    form = VFiles(request.POST,request.FILES)
    if form.is_valid():
     
      print(form)
      form.save()
      auditdata('VideoFiles','Add','Admin')  ###adding to the auditlog ###

      return redirect('success_url')
    else:
      print("INVALID INVALID FORM IS INVALID")
      print(form.errors)
  else:
      print("GET METHOD")
      # user=UserAccount.objects.filter(username=user_name).get(user_company_name)
      all_comp=Company.objects.all()
      all_cameraMod=CameraModel.objects.all()
      all_vff=VideoFF.objects.all()
      all_li=LItypes.objects.all()
      form = VFiles(initial={'RejectedReason': 'NA'})
    
      context={'all_comp':all_comp,'all_cameraMod':all_cameraMod, 'all_vff':all_vff,'all_li':all_li, 'form':form}
      
      return render(request, 'templates/dms/AddVideo.html',  context)


 
      
      

# to update videofile information 
@login_required
def editvideos_form(request):
  print("inside edit videos")
  
  if request.method == "POST":
    
    form = VFiles(request.POST)

    if form.is_valid():
      form.save()
      auditdata('VideoFiles','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = VFiles()
        return render(request, 'templates/dms/ModifyVideo.html', {'form': form})
  else:
    
    print("inside ELSE PART")

    # all_Videos=VideoFiles.objects.all() 
    all_Videos=VideoFiles.objects.exclude(videostatus = 'Approved' )
    context={'all_Videos':all_Videos}

    return render(request,'templates/dms/ModifyVideo.html', context)  

############################################



class VideosUpdate(UpdateView):
  def render(self,request,pk_id):
    # thumbpath = Path(settings.EXTERNAL_ROOT) 
    # thumbpath.mkdir(parents=True, exist_ok=True)
    # thumbpath_str = str(thumbpath)

    # fs=FileSystemStorage(location=thumbpath_str) 
    print("inside render function",pk_id)
    if (pk_id==0):
       get_video=VideoFiles.objects.all()
    else:
      get_video=VideoFiles.objects.get(id=pk_id)
    form=VFiles(instance=get_video)
    context={'form':form}
    return render(request,'templates/dms/VideosUpdate.html',context)

  
  def get(self,request,pk_id):
    print("inside get function VideosUpdate",pk_id)
    if (pk_id==0):
       get_video=VideoFiles.objects.all()
    else:
      get_video=VideoFiles.objects.get(id=pk_id)

    form=VFiles(instance=get_video)
    
    context={'form':form}
    return render(request,'templates/dms/VideosUpdate.html',context)

  def post(self,request,pk_id):
    update_video=VideoFiles.objects.get(id=pk_id)
    update_video.videostatus="Modified"
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    self.form=VFiles(request.POST,request.FILES,instance=update_video)
    print("request.FILES", request.FILES)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    if self.form.is_valid():


        ### save updated form details      
        self.form.save()
        auditdata('VideoFiles','Update','Admin')  ###adding to the auditlog ###
        return redirect('success_url')
    else:
      if (pk_id==0):
        update_video=VideoFiles.objects.all()
      else:
        update_video=VideoFiles.objects.get(id=pk_id)
      self.form=VFiles(request.POST,instance=update_video)
      print("not valid", self.form)
      return self.render(request,pk_id)
    
@login_required
def VideosApprovalRejection(request):
  print("inside VideosApprovalRejection ",request.method)
  print("inside VideosApprovalRejection ",request.FILES)
  if request.method=="POST":
      id1 = request.POST.get('id', None)
      print("RECORD ID",id1)
      vidstatus=request.POST.get("videostatus")
      print("VIDEO STATUS",vidstatus)
      if vidstatus == "Rejected":
        print("inside Rejected ")
        RejectedReason=request.POST.get("RejectedReason")
        updatevideodet1 = VideoFiles.objects.filter(id = id1).update(videostatus=vidstatus,RejectedReason=RejectedReason)
        auditdata('VideoFiles','Rejected','Admin')  ###adding to the auditlog ###
        print('updatevideodet',updatevideodet1)
      if vidstatus == "Approved":
        print("inside Approval ")
        updatevideodet2 = VideoFiles.objects.filter(id = id1).update(videostatus=vidstatus)
        auditdata('VideoFiles','Rejected','Admin')  ###adding to the auditlog ###
        print('updatevideodet',updatevideodet2)
      # updatevideodet.videostatus=request.POST.get("videostatus")
      
      
      # print('getting videostatus',request.POST.get('videostatus'))
      
      form = VFiles()
      all_Videos = VideoFiles.objects.all()
      context={'all_Videos':all_Videos,'form':form}
      data = {'context':context}
      return render(request,'templates/dms/ApproveRejectVideo.html',context)
      # return JsonResponse(data)
      # return redirect('success_url')
  else:
    print('GET GET GET')
    sort_params={}
    set_if_not_none(sort_params, 'videostatus', 'New')
    set_if_not_none(sort_params, 'videostatus', 'Modified')
    print(sort_params)
    all_Videos=VideoFiles.objects.filter(**sort_params)
    
    print(all_Videos.count())
    form = VFiles()
    context={'all_Videos':all_Videos,'form':form}   

    return render(request,'templates/dms/ApproveRejectVideo.html', context)  

###### dehradun file upload #####
@login_required
def dehradhun(request):
    if request.method == 'POST':  
        
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']
        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':
                # path = 'media/' + fileName
                path = settings.DRIVE_ROOT + fileName
                print('path',path)
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                FileFolder = File()
                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName
                FileFolder.save()
                if int(end):
                    res = {'data':'Saved Successfully','existingPath': fileName}
                else:
                    res = {'existingPath': fileName}
                return JsonResponse(res)

            else:
                # path = 'media/' + fileName
                path = settings.DRIVE_ROOT + fileName
                print('path',path)
                model_id = File.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            # res = JsonResponse({'data':'Uploaded Successfully','existingPath':model_id.existingPath})
                            res = {'data':'Uploaded Successfully','existingPath':model_id.existingPath}
                        else:
                            # res = JsonResponse({'existingPath':model_id.existingPath})   
                            res =  {'existingPath':model_id.existingPath}
                        # return res
                        return JsonResponse(res)
                    else:
                        # res = JsonResponse({'data':'EOF found. Invalid request'})
                        # return res
                        res = {'data':'EOF found. Invalid request'}
                        return JsonResponse(res)
                else:
                    # res = JsonResponse({'data':'No such file exists in the existingPath'})
                    # return res
                    res = {'data':'No such file exists in the existingPath'}
                    return JsonResponse(res)
    return render(request, 'templates/upload.html')

@login_required
def CustVideos_form(request):
  print("POSTING POSTING",request.POST)
  
  if request.method == "POST":
        
        print(request.FILES)
        file = request.FILES['file'].read()
        fileName= request.POST['filename']

        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']


        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = {'data':'Invalid Request'}
            return JsonResponse(res) 
        else:
            if existingPath == 'null':
                
                # path = 'media/' + fileName
                path = settings.DRIVE_ROOT + fileName
                print('path',path)
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                print("##########################",request.POST)
                CompanyName = request.POST["CompanyName"]
                print("##########################",CompanyName)
                ProjectName = request.POST["ProjectName"]
                StationName = request.POST["StationName"]
                CameraNo = request.POST["CameraNo"]
                CModel = request.POST["CModel"]
                CHeight = request.POST["CHeight"]
                CView = request.POST["CView"]
                VideoTakenDate=request.POST["videodate"]
                VideoStartTime=request.POST["starttime"]
                VideoEndTime=request.POST["endtime"]
                LICate = request.POST["LICate"]
                Remarks = request.POST["Remarks"]
                VideoFormat = request.POST["VideoFormat"]
                

                if CompanyName and ProjectName and StationName and CameraNo and CModel and CHeight and CView and VideoTakenDate and VideoStartTime and VideoEndTime and LICate and VideoFormat :


                    CompanyName = Company.objects.get(id = CompanyName)
                    ProjectName = Project.objects.get(id = ProjectName)
                  
                    StationName = Location.objects.get(id=StationName)
                    CModel = CameraModel.objects.get(id = CModel)
                    VideoFormat = VideoFF.objects.get(id = VideoFormat)
                    LICate = LItypes.objects.get(id = LICate)
                    print("calling Try n EXCEPTION")
                    try:
                        FileFolder = CustVideoFiles.objects.get_or_create(
                              existingPath = fileName,
                                eof = end,
                                name = fileName,
                                CompanyName = CompanyName,
                                ProjectName =ProjectName,
                                StationName = StationName,
                                CameraNo = CameraNo,
                                CModel = CModel,
                                CHeight = CHeight,
                                CView = CView,
                                VideoTakenDate=VideoTakenDate,
                                VideoStartTime=VideoStartTime,
                                VideoEndTime=VideoEndTime,
                                LICate =LICate,
                                Remarks = Remarks,
                                VideoFormat = VideoFormat
                          )
                        FileFolder.save()
                    except:
                      print("INSIDE EXCEPTION")
                      res = {'data':'File already Exists','existingPath': fileName}
                      return JsonResponse(res)


                    
                    if int(end):
                        print("File upload end reached",fileName)
                        res = {'data':'Uploaded Successfully','existingPath': fileName}
                    else:
                        print("File upload no end",fileName)
                        res = {'existingPath': fileName}
                    return JsonResponse(res)
                else: 
                   return JsonResponse({'data': "invalid data ..please check"})

            else:
                path =  settings.DRIVE_ROOT + existingPath
                print("ELSE part : path" ,path)
                
                model_id = CustVideoFiles.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            print("File upload completed",model_id.existingPath)
                            res = {'data':'Uploaded Successfully','existingPath':model_id.existingPath}
                        else:
                            print("File upload inprogress",model_id.existingPath)
                            res = {'existingPath':model_id.existingPath}    
                        return JsonResponse(res)
                    else:
                        res = {'data':'EOF found. Invalid request'}
                        return JsonResponse(res)
                else:
                    res ={'data':'No such file exists in the existingPath'}
                    return JsonResponse(res)
  return render(request, 'templates/dms/AddCustVideo.html')


class ListCustVideos(View): ## ,pk_id
    def get(self,request,*args,**kwargs):
        
        print('request.GET', request.GET)
        form = VFiles()
        # all_Videos=VideoFiles.objects.all()
        sort_params = {}
             

       ####### Get the inputs from  filter #######
        PName=request.GET.get('ProjectName', None)
        SName=request.GET.get('StationName', None)
        LICat=request.GET.get('LICate',None)
        vidstatus=request.GET.get('videostatus',None)

      ####### call function to pass only the valid filter inputs #######
        set_if_not_none(sort_params, 'ProjectName', PName)
        set_if_not_none(sort_params, 'StationName', SName)
        set_if_not_none(sort_params, 'LICate', LICat)
        set_if_not_none(sort_params, 'videostatus', vidstatus)
        print(sort_params)
        #######pass the valid inputs filters to db model to fetch records ########
        all_Videos=CustVideoFiles.objects.filter(**sort_params)
            
        VideoFilter=VideoFileFilter(queryset=all_Videos)
                     
        context={'all_Videos':all_Videos,'form':form,'VideoFilter':VideoFilter}
       
        return render (request,'templates/dms/ListCustVideo.html',context=context)
      

# to update customer videofile information 
@login_required
def editcustvideos_form(request):
  print("inside edit cust videos")
  
  if request.method == "POST":
    
    form = CustVideoFiles(request.POST)

    if form.is_valid():
      form.save()
      auditdata('CustVideoFiles','Update','Admin')  ###adding to the auditlog ###
      return redirect('success_url')
    else:
        form = CustVideoFiles()
        return render(request, 'templates/dms/ModifyCustVideo.html', {'form': form})
  else:
    
    print("inside ELSE PART")

    # all_Videos=VideoFiles.objects.all() 
    all_Videos=CustVideoFiles.objects.exclude(videostatus = 'Approved' )
    context={'all_Videos':all_Videos}

    return render(request,'templates/dms/ModifyCustVideo.html', context)  

############################################

##customer video updates

class VideosUpdateCust(UpdateView):
  def render(self,request,pk_id):
    # thumbpath = Path(settings.EXTERNAL_ROOT) 
    # thumbpath.mkdir(parents=True, exist_ok=True)
    # thumbpath_str = str(thumbpath)

    # fs=FileSystemStorage(location=thumbpath_str) 
    print("inside render function",pk_id)
    if (pk_id==0):
       get_video=CustVideoFiles.objects.all()
    else:
      get_video=CustVideoFiles.objects.get(id=pk_id)
    form=VCustFiles(instance=get_video)
    context={'form':form}
    return render(request,'templates/dms/VideosUpdateCust.html',context)

  
  def get(self,request,pk_id):
    print("inside get function VideosUpdateCust",pk_id)
    if (pk_id==0):
       get_video=CustVideoFiles.objects.all()
    else:
      get_video=CustVideoFiles.objects.get(id=pk_id)

    form=VCustFiles(instance=get_video)
    
    context={'form':form}
    return render(request,'templates/dms/VideosUpdateCust.html',context)

  def post(self,request,pk_id):
    update_video=CustVideoFiles.objects.get(id=pk_id)
    update_video.videostatus="Modified"
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    self.form=VCustFiles(request.POST,request.FILES,instance=update_video)
    print("request.POST", request.POST)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    if self.form.is_valid():


        ### save updated form details      
        self.form.save()
        auditdata('VideoFiles','Update','Admin')  ###adding to the auditlog ###
        return redirect('success_url')
    else:
      if (pk_id==0):
        update_video=CustVideoFiles.objects.all()
      else:
        update_video=CustVideoFiles.objects.get(id=pk_id)
      self.form=VCustFiles(request.POST,instance=update_video)
      print("not valid", self.form)
      return self.render(request,pk_id)
    
@login_required
def CustVideosApprovalRejection(request):
  print("inside CustVideosApprovalRejection ",request.method)
  print("inside CustVideosApprovalRejection ",request.FILES)

  if request.method=="POST":
      id1 = request.POST.get('id', None)
      print("RECORD ID",id1)
      vidstatus=request.POST.get("videostatus")
      print("VIDEO STATUS",vidstatus)
      if vidstatus == "Rejected":
        print("inside Rejected ")
        RejectedReason=request.POST.get("RejectedReason")
        updatevideodet1 = CustVideoFiles.objects.filter(id = id1).update(videostatus=vidstatus,RejectedReason=RejectedReason)
        auditdata('CustVideoFiles','Rejected','Admin')  ###adding to the auditlog ###
        print('updatevideodet',updatevideodet1)
      if vidstatus == "Approved":
        print("inside Approval ")
        updatevideodet2 = CustVideoFiles.objects.filter(id = id1).update(videostatus=vidstatus)
        auditdata('CustVideoFiles','Rejected','Admin')  ###adding to the auditlog ###
        print('updatevideodet',updatevideodet2)
      # updatevideodet.videostatus=request.POST.get("videostatus")
      
      
      # print('getting videostatus',request.POST.get('videostatus'))
      
      form = VCustFiles()
      all_Videos = CustVideoFiles.objects.all()
      context={'all_Videos':all_Videos,'form':form}
      data = {'context':context}
      return render(request,'templates/dms/ApproveRejectCustVideo.html',context)
      # return JsonResponse(data)
      # return redirect('success_url')
  else:
    print('GET GET GET')
    # sort_params={}
    # set_if_not_none(sort_params, 'videostatus', 'New')
    # set_if_not_none(sort_params, 'videostatus', 'Modified')
    # print(sort_params)filter(id__in=[1, 5, 34, 567, 229])
    all_Videos=CustVideoFiles.objects.filter( videostatus__in = ['New','Modified','Rejected'])
    print(all_Videos)
    form = VCustFiles()
    context={'all_Videos':all_Videos,'form':form}   

    return render(request,'templates/dms/ApproveRejectCustVideo.html', context)  
  

  ############# testing #########
@login_required
def CustVideos_form1(request):
  print("POSTING POSTING",request.POST)
  
  if request.method == "POST":
        
        print(request.FILES)
        file = request.FILES['file'].read()
        fileName= request.POST['filename']

        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']


        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = {'data':'Invalid Request'}
            return JsonResponse(res) 
        else:
            if existingPath == 'null':
                
                # path = 'media/' + fileName
                path = settings.DRIVE_ROOT + fileName
                print('path',path)
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                print("##########################",request.POST)
                CompanyName = request.POST["CompanyName"]
                print("##########################",CompanyName)
                ProjectName = request.POST["ProjectName"]
                StationName = request.POST["StationName"]
                CameraNo = request.POST["CameraNo"]
                CModel = request.POST["CModel"]
                CHeight = request.POST["CHeight"]
                CView = request.POST["CView"]
                VideoTakenDate=request.POST["videodate"]
                VideoStartTime=request.POST["starttime"]
                VideoEndTime=request.POST["endtime"]
                LICate = request.POST["LICate"]
                Remarks = request.POST["Remarks"]
                VideoFormat = request.POST["VideoFormat"]
                

                if CompanyName and ProjectName and StationName and CameraNo and CModel and CHeight and CView and VideoTakenDate and VideoStartTime and VideoEndTime and LICate and VideoFormat :


                    CompanyName = Company.objects.get(id = CompanyName)
                    ProjectName = Project.objects.get(id = ProjectName)
                  
                    StationName = Location.objects.get(id=StationName)
                    CModel = CameraModel.objects.get(id = CModel)
                    VideoFormat = VideoFF.objects.get(id = VideoFormat)
                    LICate = LItypes.objects.get(id = LICate)
                    print("calling Try n EXCEPTION")
                    try:
                        FileFolder = CustVideoFiles.objects.get_or_create(
                              existingPath = fileName,
                                eof = end,
                                name = fileName,
                                CompanyName = CompanyName,
                                ProjectName =ProjectName,
                                StationName = StationName,
                                CameraNo = CameraNo,
                                CModel = CModel,
                                CHeight = CHeight,
                                CView = CView,
                                VideoTakenDate=VideoTakenDate,
                                VideoStartTime=VideoStartTime,
                                VideoEndTime=VideoEndTime,
                                LICate =LICate,
                                Remarks = Remarks,
                                VideoFormat = VideoFormat
                          )
                        FileFolder.save()
                    except:
                      print("INSIDE EXCEPTION")
                      res = {'data':'File already Exists','existingPath': fileName}
                      return JsonResponse(res)


                    
                    if int(end):
                        print("File upload end reached",fileName)
                        res = {'data':'Uploaded Successfully','existingPath': fileName}
                    else:
                        print("File upload no end",fileName)
                        res = {'existingPath': fileName}
                    return JsonResponse(res)
                else: 
                   return JsonResponse({'data': "invalid data ..please check"})

            else:
                path =  settings.DRIVE_ROOT + existingPath
                print("ELSE part : path" ,path)

                model_id = CustVideoFiles.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            print("File upload completed",model_id.existingPath)
                            res = {'data':'Uploaded Successfully','existingPath':model_id.existingPath}
                        else:
                            print("File upload inprogress",model_id.existingPath)
                            res = {'existingPath':model_id.existingPath}    
                        return JsonResponse(res)
                    else:
                        res = {'data':'EOF found. Invalid request'}
                        return JsonResponse(res)
                else:
                    res ={'data':'No such file exists in the existingPath'}
                    return JsonResponse(res)
  return render(request, 'templates/dms/AddCustVideo1.html')


class AddCustVideoCustomized(UpdateView):
  def render(self,request,user_name):
    print("inside render function",user_name)
    form = VCustFiles()
    if (user_name):
      #  user_company=UserAccount.objects.filter('user_company_name').get(user_name=user_name)
       user_company=UserAccount.objects.filter(user_name=user_name).values_list("user_company_name", flat=True)
       print("user_company : ",user_company)
       get_user_company=Company.objects.filter( name__in = [user_company])
       context={'form':form,'user_company':get_user_company}
    else:
        get_user_company=Company.objects.all()
        context={'form':form,'user_company':get_user_company}
    
    context={'form':form}
    return render(request,'templates/dms/AddCustVideo.html',context)
  
  print("Inside AddCustVideoCustomized :")
  def get(self,request,user_name):
    print("inside get function AddCustVideoCustomized",user_name)
    form = VCustFiles()
    if (user_name):
      #  user_company=UserAccount.objects.filter('user_company_name').get(user_name=user_name)
       camera_model=CameraModel.objects.all()
       LICate=LItypes.objects.all()
       VideoFormat=VideoFF.objects.all()
       user_company=UserAccount.objects.filter(user_name=user_name).values_list("user_company_name", flat=True)
       print("user_company : ",user_company[0])
       usercomp=user_company[0]
       if (user_company[0] == "COSAI"):
          get_user_company=Company.objects.all()
          context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company,'camera_model':camera_model,"LICate":LICate,"VideoFormat" :VideoFormat}
       else:
          get_user_company=Company.objects.filter( name__in = [user_company])
          print("No.of company : ",len(get_user_company))
          user_compid=get_user_company[0]
          get_user_project=Project.objects.filter(company__in = [user_compid])
          print("No.of projects : ",len(get_user_project),"project name : ",get_user_project)
          project_count=len(get_user_project)
          if len(get_user_project)== 1:
            context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company, 'project_count':project_count,'get_user_project':get_user_project  ,'camera_model':camera_model,"LICate":LICate,"VideoFormat" :VideoFormat}
      #  print("company list :",get_user_company)
          context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company,'camera_model':camera_model,"LICate":LICate,"VideoFormat" :VideoFormat}
    
    return render(request,'templates/dms/AddCustVideo.html',context)

  def post(self,request,user_name):
    if request.method == "POST":
        
        print(request.FILES)
        file = request.FILES['file'].read()
        fileName= request.POST['filename']

        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']


        
        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = {'data':'Invalid Request'}
            return JsonResponse(res) 
        else:
            if existingPath == 'null':
                
                # path = 'media/' + fileName
                path = settings.DRIVE_ROOT + fileName
                print('path',path)
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                print("##########################",request.POST)
                CompanyName = request.POST["CompanyName"]
                print("##########################",CompanyName)
                ProjectName = request.POST["ProjectName"]
                StationName = request.POST["StationName"]
                CameraNo = request.POST["CameraNo"]
                CModel = request.POST["CModel"]
                CHeight = request.POST["CHeight"]
                CView = request.POST["CView"]
                VideoTakenDate=request.POST["videodate"]
                VideoStartTime=request.POST["starttime"]
                VideoEndTime=request.POST["endtime"]
                LICate = request.POST["LICate"]
                Remarks = request.POST["Remarks"]
                VideoFormat = request.POST["VideoFormat"]
                

                if CompanyName and ProjectName and StationName and CameraNo and CModel and CHeight and CView and VideoTakenDate and VideoStartTime and VideoEndTime and LICate and VideoFormat :


                    CompanyName = Company.objects.get(id = CompanyName)
                    ProjectName = Project.objects.get(id = ProjectName)
                  
                    StationName = Location.objects.get(id=StationName)
                    CModel = CameraModel.objects.get(id = CModel)
                    VideoFormat = VideoFF.objects.get(id = VideoFormat)
                    LICate = LItypes.objects.get(id = LICate)
                    print("calling Try n EXCEPTION")
                    try:
                        FileFolder = CustVideoFiles.objects.get_or_create(
                              existingPath = fileName,
                                eof = end,
                                name = fileName,
                                CompanyName = CompanyName,
                                ProjectName =ProjectName,
                                StationName = StationName,
                                CameraNo = CameraNo,
                                CModel = CModel,
                                CHeight = CHeight,
                                CView = CView,
                                VideoTakenDate=VideoTakenDate,
                                VideoStartTime=VideoStartTime,
                                VideoEndTime=VideoEndTime,
                                LICate =LICate,
                                Remarks = Remarks,
                                VideoFormat = VideoFormat
                          )
                        FileFolder.save()
                    except:
                      print("INSIDE EXCEPTION")
                      res = {'data':'File already Exists','existingPath': fileName}
                      return JsonResponse(res)


                    
                    if int(end):
                        print("File upload end reached",fileName)
                        res = {'data':'Uploaded Successfully','existingPath': fileName}
                    else:
                        print("File upload no end",fileName)
                        res = {'existingPath': fileName}
                    return JsonResponse(res)
                else: 
                   return JsonResponse({'data': "invalid data ..please check"})

            else:
                path =  settings.DRIVE_ROOT + existingPath
                print("ELSE part : path" ,path)
                
                model_id = CustVideoFiles.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.eof = int(end)
                            model_id.save()
                            print("File upload completed",model_id.existingPath)
                            res = {'data':'Uploaded Successfully','existingPath':model_id.existingPath}
                        else:
                            print("File upload inprogress",model_id.existingPath)
                            res = {'existingPath':model_id.existingPath}    
                        return JsonResponse(res)
                    else:
                        res = {'data':'EOF found. Invalid request'}
                        return JsonResponse(res)
                else:
                    res ={'data':'No such file exists in the existingPath'}
                    return JsonResponse(res)
    return render(request, 'templates/dms/AddCustVideo.html')
  
  ### to detect videos uploaded by user
  # class DetectVideos(View): ## ,pk_id

@login_required     
def detect(request):
    print("detection:", request.method)
    if request.method=='GET':
        print('request.GET', request.GET)
        sort_params={}
        form = VCustFiles()
        # all_Videos=CustVideoFiles.objects.all()
         ####### Get the inputs from  filter #######
        PName=request.GET.get('ProjectName', None)
        SName=request.GET.get('StationName', None)
        ####### call function to pass only the valid filter inputs #######
        set_if_not_none(sort_params, 'ProjectName', PName)
        set_if_not_none(sort_params, 'StationName', SName)
        #######pass the valid inputs filters to db model to fetch records ########
        all_Videos=CustVideoFiles.objects.filter(**sort_params)
            
        VideoDetect=VideoDetectFilter(queryset=all_Videos)
                     
        context={'all_Videos':all_Videos,'form':form,'VideoDetect':VideoDetect}
       
        return render (request,'templates/dms/DetectVideos.html',context=context)
    else:
       ##post method
       print("post method", request.FILES)

       ##api call to track.py with videofilename ,path and date time
##ss

class detectexternal(UpdateView):
  def render(self,request,user_name):
    print("inside render function",user_name)
    form = VCustExtFiles()

    if (user_name):
      #  user_company=UserAccount.objects.filter('user_company_name').get(user_name=user_name)
       user_company=UserAccount.objects.filter(user_name=user_name).values_list("user_company_name", flat=True)
       print("user_company : ",user_company)
       get_user_company=Company.objects.filter( name__in = [user_company])
       context={'form':form,'user_company':get_user_company}
    else:
        get_user_company=Company.objects.all()
        context={'form':form,'user_company':get_user_company}
    
    context={'form':form}
    return render(request,'templates/dms/AddVideoExternal.html',context)
  
  print("Inside detectexternal :")
  def get(self,request,user_name):
    print("inside get function  detectexternal ",user_name)
    form = VCustExtFiles()
    if (user_name):
      #  user_company=UserAccount.objects.filter('user_company_name').get(user_name=user_name)
       VideoFormat=VideoFF.objects.all()
       user_company=UserAccount.objects.filter(user_name=user_name).values_list("user_company_name", flat=True)
       print("user_company : ",user_company[0])
       usercomp=user_company[0]
       if (user_company[0] == "COSAI"):
          get_user_company=Company.objects.all()
          context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company,"VideoFormat" :VideoFormat}
       else:
          get_user_company=Company.objects.filter( name__in = [user_company])
          print("No.of company : ",len(get_user_company))
          # user_compid=get_user_company[0]
          # get_user_project=Project.objects.filter(company__in = [user_compid])
          # print("No.of projects : ",len(get_user_project),"project name : ",get_user_project)
          # project_count=len(get_user_project)
          # if len(get_user_project)== 1:
          #   context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company, 'project_count':project_count,'get_user_project':get_user_project  ,"VideoFormat" :VideoFormat}
      #  print("company list :",get_user_company)
          context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company,"VideoFormat" :VideoFormat}
    
    return render(request,'templates/dms/AddVideoExternal.html',context)

  def post(self,request,user_name):
   
    if request.method == "POST"  :
        print('external video : inside post method : ', request.POST.get('urlpath'))
        urlpath= request.POST.get('urlpath')
        CompanyName = request.POST["CompanyName"]
        ProjectName = request.POST["ProjectName"]
        StationName = request.POST["StationName"]
        VideoTakenDate=request.POST["videodate"]
        VideoStartTime=request.POST["starttime"]
        VideoEndTime=request.POST["endtime"]
        Remarks = request.POST["Remarks"]
        VideoFormat = request.POST["VideoFormat"]
        if (urlpath != "NA" or len(urlpath)>2):
            # print("url save")
            CompanyName = Company.objects.get(id = CompanyName)
            ProjectName = Project.objects.get(id = ProjectName)                      
            StationName = Location.objects.get(id=StationName)                        
            VideoFormat = VideoFF.objects.get(id = VideoFormat)

            # print("CompanyName:",CompanyName,"ProjectName :",ProjectName,"StationName : ",StationName,'VideoFormat :',VideoFormat)
            # print("VideoTakenDate:",VideoTakenDate,"VideoStartTime :",VideoStartTime,"VideoEndTime : ",VideoEndTime)

            if CompanyName and ProjectName and StationName and VideoFormat:
               
              try:
                FileFolder = CustExternalFiles.objects.create(
                                      existingPath = "NA",
                                      eof = True,
                                      name = "NA",
                                      CompanyName = CompanyName,
                                      ProjectName =ProjectName,
                                      StationName = StationName,                                    
                                      VideoTakenDate=VideoTakenDate,
                                      VideoStartTime=VideoStartTime,
                                      VideoEndTime=VideoEndTime,
                                      urlpath=urlpath,
                                      Remarks = Remarks,
                                      VideoFormat = VideoFormat
                                )
                FileFolder.save()
                res = {'data':'Uploaded Successfully'}
                return JsonResponse(res)
              except IntegrityError as e:
                    print("INSIDE EXCEPTION :",urlpath )
                    if e.__cause__:
                      print(f"PostgreSQL error message: {e.__cause__.pgcode} - {e.__cause__.pgerror}")
                    res = {'data':'creation failed'}
                    return JsonResponse(res)
            else:
               print("parent enteries check")
               return JsonResponse("Invalid Form Data. Please check")
            

        else:
            # print(request.FILES)
        
          file = request.FILES['file'].read()
          fileName= request.POST['filename']

          existingPath = request.POST['existingPath']
          end = request.POST['end']
          nextSlice = request.POST['nextSlice']

          if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
                res = {'data':'Invalid Request'}
                return JsonResponse(res) 
          else:
                if existingPath == 'null':
                    
                    # path = 'media/' + fileName
                    path = settings.DRIVE_ROOT + fileName
                    print('path',path)
                    with open(path, 'wb+') as destination: 
                        destination.write(file)
                    print("##########################",request.POST)
                    CompanyName = request.POST["CompanyName"]
                    print("##########################",CompanyName)
                    ProjectName = request.POST["ProjectName"]
                    StationName = request.POST["StationName"]
                    VideoTakenDate=request.POST["videodate"]
                    VideoStartTime=request.POST["starttime"]
                    VideoEndTime=request.POST["endtime"]
                    Remarks = request.POST["Remarks"]
                    VideoFormat = request.POST["VideoFormat"]
                    
                    if CompanyName and ProjectName and StationName and VideoTakenDate and VideoStartTime and VideoEndTime and  VideoFormat :


                        CompanyName = Company.objects.get(id = CompanyName)
                        ProjectName = Project.objects.get(id = ProjectName)                      
                        StationName = Location.objects.get(id=StationName)                        
                        VideoFormat = VideoFF.objects.get(id = VideoFormat)
                        
                        print("calling Try n EXCEPTION")
                        try:
                            FileFolder = CustExternalFiles.objects.get_or_create(
                                  existingPath = fileName,
                                    eof = end,
                                    name = fileName,
                                    CompanyName = CompanyName,
                                    ProjectName =ProjectName,
                                    StationName = StationName,
                                    
                                    VideoTakenDate=VideoTakenDate,
                                    VideoStartTime=VideoStartTime,
                                    VideoEndTime=VideoEndTime,
                                    urlpath='NA',
                                    Remarks = Remarks,
                                    VideoFormat = VideoFormat
                              )
                            FileFolder.save()
                        except:
                          print("INSIDE EXCEPTION")
                          res = {'data':'File already Exists','existingPath': fileName}
                          return JsonResponse(res)


                        
                        if int(end):
                            print("File upload end reached",fileName)
                            res = {'data':'Uploaded Successfully','existingPath': fileName}
                        else:
                            print("File upload no end",fileName)
                            res = {'existingPath': fileName}
                        return JsonResponse(res)
                    else: 
                      return JsonResponse({'data': "invalid data ..please check"})

                else:
                    path =  settings.DRIVE_ROOT + existingPath
                    print("ELSE part : path" ,path)
                    
                    model_id = CustExternalFiles.objects.get(existingPath=existingPath)
                    if model_id.name == fileName:
                        if not model_id.eof:
                            with open(path, 'ab+') as destination: 
                                destination.write(file)
                            if int(end):
                                model_id.eof = int(end)
                                model_id.save()
                                print("File upload completed",model_id.existingPath)
                                res = {'data':'Uploaded Successfully','existingPath':model_id.existingPath}
                            else:
                                print("File upload inprogress",model_id.existingPath)
                                res = {'existingPath':model_id.existingPath}    
                            return JsonResponse(res)
                        else:
                            res = {'data':'EOF found. Invalid request'}
                            return JsonResponse(res)
                    else:
                        res ={'data':'No such file exists in the existingPath'}
                        return JsonResponse(res)
    
    return render(request, 'templates/dms/AddVideoExternal.html')
@login_required
def saveextvideo(request):
   if request.method=='POST':
        print("saveextvideo - request.FILES : ",request.FILES)
        # if form.is_valid():
           
        
        # data = {'data':list(projects)}
        # print(data)
        # return JsonResponse(data)
        return render(request, 'templates/dms/AddVideoExternal.html')
   
   



@login_required
def ExternalVideoDetectionStatus(request):
  if request.method=="GET":
    print('GET GET GET')
    all_Videos=FileUploadExternal.objects.exclude(videostatus="Completed")  
    
    print(all_Videos.count())
    form = FileUploadForm()
    context={'all_Videos':all_Videos,'form':form}   

    return render(request,'templates/dms/ExternalVideoDetectStatus.html', context) 
  
  
 
class ExternalVideosUpdate(UpdateView):
  def render(self,request,pk_id):
   
    print("inside render function",pk_id)
    if (pk_id==0):
       form=FileUploadForm1()
       context={'form':form,'error':'Invalid Video ID'}
       return redirect('error_url')
    else:
      get_video=FileUploadExternal.objects.get(id=pk_id)
      form=FileUploadForm1(instance=get_video)
      context={'form':form}
      return render(request,'templates/dms/ExternalVideosUpdate.html',context)

  
  def get(self,request,pk_id):
    print("inside get function ExternalVideosUpdate",pk_id)
    if (pk_id==0):
       form=FileUploadForm1()
       context={'form':form,'error':'Invalid Video ID'}
       return render(request,'templates/dms/ExternalVideosUpdate.html',context)
    else:
        get_video=FileUploadExternal.objects.get(id=pk_id)
        form=FileUploadForm1(instance=get_video)    
        context={'form':form}
        return render(request,'templates/dms/ExternalVideosUpdate.html',context)

  def post(self,request,pk_id):
    print("HERE HERE post validity check",request.FILES)
    update_video=FileUploadExternal.objects.get(id=pk_id)
    update_video.videostatus=request.POST.get("videostatus")
    CompanyName=request.POST.get("CompName")
    ProjectName=request.POST.get("ProjName")
    FileName=update_video.files
    URLpath=update_video.urlpath
    CompanyName=CompanyName.upper().strip()
    print("update_video.videostatus :",update_video.videostatus,CompanyName,ProjectName,FileName)
    self.form=FileUploadForm1(request.POST,request.FILES,instance=update_video)
    
    print("@@@",self.form)
    if self.form.is_valid():
        if (update_video.videostatus=="Completed"):
            # if (URLpath):
            if len(URLpath.strip())>0:
              print("sending email alert invoked")
              recipient_list = ['meenakshidcosai@gmail.com','costm1993@gmail.com','coscmd@gmail.com']
              content= "Detection Completed for client " + CompanyName + " project " + ProjectName + " shared via URLPath "+ URLpath
              subject="Detection Completed on "  + str(time.strftime("%Y%m%d_%H%M%S")) + " for URLPath "+ URLpath
              sending_mail(recipient_list,content,subject) 
              print("self.form save")
              ### save updated form details      
              self.form.save()
              auditdata('ExtVideoFiles','Update','Admin')  ###adding to the auditlog ###        
              return redirect('success_url')
            else:
                print("status completed")
              ## fetch sqllite db data and insert into postgres db
                filename, _ =  os.path.splitext(str(FileName))
                # filename="L12_20231115_114420_1"
                print('calling sqllite',pk_id,filename)
                dbinsert = readsqllite(pk_id,CompanyName,filename)
                if (dbinsert): 
                  print("sending email alert invoked")
                  recipient_list = ['meenakshidcosai@gmail.com','costm1993@gmail.com','coscmd@gmail.com']
                  content= " Detection Completed for client " + CompanyName + " project " + ProjectName
                  subject="Detection Completed on "  + str(time.strftime("%Y%m%d_%H%M%S"))
                  sending_mail(recipient_list,content,subject) 
                  print("self.form save")
                  ### save updated form details      
                  self.form.save()
                  auditdata('ExtVideoFiles','Update','Admin')  ###adding to the auditlog ###
                  return redirect('success_url')
                else:
                  print(self.form.errors)
                  self.form=FileUploadForm1(request.POST,request.FILES,instance=update_video)
                  context={"error":self.form.errors,"form":self.form}
                  # return redirect('Error_url')
                  return render(request,'templates/dms/ExternalVideosUpdate.html',context)
        else:
            print("self.form save")
            ### save updated form details      
            self.form.save()
            auditdata('ExtVideoFiles','Update','Admin')  ###adding to the auditlog ###
            return redirect('success_url')
   
    else:
      
      print("not valid")
      print(self.form.errors)
      return redirect('Error_url')
   
class ExternalVideosReport(UpdateView):
  def render(self,request,pk_id):
    
    # thumbpath = Path(settings.EXTERNAL_ROOT) 
    # thumbpath.mkdir(parents=True, exist_ok=True)
    # thumbpath_str = str(thumbpath)

    # fs=FileSystemStorage(location=thumbpath_str) 
    print("inside render function",pk_id)
    if (pk_id==0):
       get_video=ObjectDetection.objects.all()
    else:
      get_video=ObjectDetection.objects.filter(video_id=pk_id)
    form=ObjectDetectionReport(instance=get_video)
    context={'form':form}
    return render(request,'templates/dms/ExternalVideoDetectReport.html',context)

  
  def get(self,request,pk_id):
    print("inside get function ExternalVideosReport",pk_id)
    if (pk_id==0):
       get_video=ObjectDetection.objects.all()
    else:
      get_video=ObjectDetection.objects.filter(video_id=pk_id)

    form=ObjectDetectionReport()    
    context={'form':form,'get_video':get_video}
    print("context : ",context)
    return render(request,'templates/dms/ExternalVideoDetectReport.html',context)


    
@login_required
def ExternalVideoDetectionList(request,user_name):
  print("inside ExternalVideoDetectionList ",request.method)
  print("inside ExternalVideoDetectionList ",request.FILES)
  if request.method=="POST":
      id1 = request.POST.get('id', None)
      print("RECORD ID",id1)
      vidstatus=request.POST.get("detectionstatus")
      print("VIDEO STATUS",vidstatus)
   
      
      form = FileUploadForm1()
      all_Videos = FileUploadExternal.objects.filter()
      context={'all_Videos':all_Videos,'form':form}
      # data = {'context':context}
      print("all_videos:", all_Videos)
      return render(request,'templates/dms/ExternalVideoDetectStatusList.html',context)
      # return JsonResponse(data)
      # return redirect('success_url')
  else:
    print('GET GET GET')
    if (user_name):
      #  user_company=UserAccount.objects.filter('user_company_name').get(user_name=user_name)
      user_company=UserAccount.objects.filter(user_name=user_name).values_list("user_company_name", flat=True)
       
       
      print("user_company : ",user_company)
      if (user_company[0] == 'COSAI'):
        print(" Admin")
        all_Videos=FileUploadExternal.objects.filter(videostatus="Completed")
      else:
          print(" client")
          get_user_company=Company.objects.filter( name__in = [user_company])
          print("No.of company : ",len(get_user_company))
          user_compid=get_user_company[0]
          # get_user_project=Project.objects.filter(company__in = [user_compid])
        
          all_Videos=FileUploadExternal.objects.filter(CompanyName__in = [user_compid])
    
    print("GET all_videos:", all_Videos)
    form = FileUploadForm1()
    context={'all_Videos':all_Videos,'form':form}   

    return render(request,'templates/dms/ExternalVideoDetectStatusList.html', context)  
  


### ADDED on 16th oct by Meenakshi 
### to read the sqllite file based on the video id provided 

def readsqllite(pk,CompanyName,filename):
     
    import sqlite3
    # Connect to PostgreSQL Database
    postgres_conn = psycopg2.connect(
            host='127.0.0.1',
            database='vfms_db',
            user='postgres',
            password='cosaimp@2020'
    )
    postgres_cursor = postgres_conn.cursor()
    
    video_id=pk
    select_qry="SELECT count(*) FROM vfms_objectdetection where video_id_id = " + str(video_id)
   
    postgres_cursor.execute(select_qry)
    result = postgres_cursor.fetchone()[0]
    # postgres_cursor.execute(f"SELECT count(*) FROM vfms_objectdetection where video_id_id = {pk};")
    print ('fetch_query  result:',result)
    if (result == 0 or result == None):
    # Connect to the SQLite database file
        
        dbfile_path= settings.DETECTIONDB_ROOT + CompanyName +'/'
        print("dbfile_path :",dbfile_path)
        # dbfile_path="D:/django_project/DMS-latest/sqllite/2/"
        db_file = dbfile_path+filename +'.db'  # Replace with the actual path to your .db file
        if os.path.exists(db_file):
            print(f'The file {db_file} exists.')
            connection = sqlite3.connect(db_file)
            ## check whether detection details exists for selected video_id
            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()
            table_name = 'object_detection'
            postgres_table='vfms_objectdetection'
            # Fetch the list of tables in the database
            # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            # tables = cursor.fetchall()

            # # Print the list of tables
            # print("Tables in the database:")
            # for table in tables:
            #     print(table[0])
            #     table_name = table[0]
            #### # Step 1:Add video id field as it is not there  as of now..
            video_id='video_id'
            # cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {video_id} INT")
            # Step 2: Update values in the new column
            update_value = pk  # Replace with the value you want to add
            cursor.execute(f"UPDATE {table_name} SET {video_id} = ? WHERE 1", (update_value,))
            # connection.commit()
            # # Step 3:Fetch and insert data into PostgreSQL
            cursor.execute(f"SELECT * FROM {table_name};")
            data = cursor.fetchall()
            # print ("data : ", data)
            #fetch data from table and insert into postgres table
            for row in data:
                    # print("row:", row)
                    insert_query = 'INSERT INTO vfms_objectdetection("id", "date_time", "vehicle_id", "vehicle_class_id", "vehicle_name", "direction", "Cross_line", "frame_number", "image_path", "video_id_id") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    # columns=("id", "date_time", "vehicle_id", "vehicle_class_id", "vehicle_name", "direction", "Cross_line", "frame_number", "image_path", "video_id_id")
                    record_to_insert = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
                    # ins_query='INSERT INTO vfms_AddLabelInfo("LName_id", "Threewheelercnt", "Buscnt", "Carcnt","Otherscnt","Lcvcnt","MiniBuscnt","Twowheelercnt", "MultiAxlecnt","Axle3cnt","Axle4cnt","Axle6cnt","Tractorcnt","TTrailercnt","Truck2Acnt","Vancnt","Echiercnt","AnnotationCnt", "ImageCnt", "DatasetLocation") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    # record_to_insert=(LNameID, col2, col3, col4, col5, col6, col7, col8,col9,col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20)
                    print("insert_query:", insert_query,record_to_insert)
                    postgres_cursor.execute(insert_query,record_to_insert)
                    postgres_conn.commit()
            print("insert completed")
        # Close the sql lite cursor and connection
            cursor.close()
            connection.close()

            postgres_cursor.execute(f"SELECT count(*) FROM vfms_objectdetection where video_id_id = {pk};")
            print ("Video_count :",postgres_cursor.fetchone()[0])
            postgres_cursor.close()
            postgres_conn.close()
            return True
    
        else:
            print(f'The file {db_file} does not exist.Try later')
            postgres_cursor.close()
            postgres_conn.close()
            return False
    else: #(fetch_query > 0):
          print("Detection data already exists")
          postgres_cursor.close()
          postgres_conn.close()
          return True
        

class ReportDownload(View):
   def get(self, request, pk_id):
        print('ReportDownload')
        # source_folder = "//10.0.0.2/Servershare/meenakshi/sqllite/"
        videofile=FileUploadExternal.objects.get(id=pk_id)
        source_folder = settings.CSVREPORT_ROOT
        compname=videofile.CompanyName
        filename=videofile.files
        file, _ = os.path.splitext(str(filename))
        report_folder = os.path.join(source_folder, str(compname))
        file_name = f"{file}.xlsx"
        
        # Specify the source file path
        source_path = os.path.join(report_folder, file_name)
        print("source_path :",source_path)
        try:
            # Check if the file exists
            if not os.path.exists(source_path):
                raise Http404(f"File '{file_name}' not found in the source folder.")

            # Open the file foNot Found:r reading
            with open(source_path, 'rb') as file:
                # Create a response with the file content
                response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'

                # Return the response
                return response
        except Http404 as e:
            print(f"Error: {e}")
            # Handle 404 error
            return HttpResponse(f"File not found: {e}", status=404)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle other errors
            return HttpResponse(f"An error occurred: {e}", status=500)
        
  

from django.shortcuts import render
@login_required
def download_file(request):
    source_folder = "D:/django_project/DMS-latest/sqllite/"
    report_Folder=source_folder+str(pk_id) +'/'
    file_name = str(pk_id) + ".xlsx"
    
    file_path = '/path/to/your/copied/file.txt'
    file_name = 'downloaded_file.txt'

    context = {
        'file_path': file_path,
        'file_name': file_name,
    }

    return render(request, 'templates/dms/ExternalVideoDetectStatusList.html', context)

@login_required
def redirect_to_folder(request, folder_path):
 # Encode the folder path for use in a URL
    encoded_folder_path = quote(folder_path)

    # Construct the relative URL without a protocol or domain
    relative_url = f'/{encoded_folder_path}'

    # Redirect the user to the specified folder
    return HttpResponseRedirect(relative_url)
@login_required
def redirect_to_folder1(request, folder_path):
    # Assuming 'folder_path' is the path of the folder you want to redirect to
    # You may need to sanitize and validate the path to prevent security issues

    # Assuming the folder_path is a valid path, you can construct the absolute URL
    # You may need to customize this based on your actual folder structure

    # Replace '192.168.1.2' with the actual IP address or hostname of the PC
    # base_url = '\\10.0.0.2'
    file='\\10.0.0.2'
    folder_path= folder_path + '/DetectionVideos/1/'
    # Construct the full URL by joining the base URL and the quoted folder path
    absolute_url = f'{file}://{quote(folder_path)}'
    # absolute_url = f'/DETECTIONVIDEO/{folder_path}/'

    # Redirect the user to the specified folder
    return HttpResponseRedirect(absolute_url)




# relative path
def get_relative_path(full_path):
    # Remove the base path and leading slashes
    relative_path = os.path.relpath(full_path, settings.DRIVE_ROOT)
    return relative_path.replace('\\', '/')
# multifile uploads.py
from django.shortcuts import render, redirect
from .forms import FileUploadForm


class upload_files(UpdateView):
  def render(self,request,user_name):
    print("inside render function",user_name)
    form = FileUploadForm()

    if (user_name):
      #  user_company=UserAccount.objects.filter('user_company_name').get(user_name=user_name)
       user_company=UserAccount.objects.filter(user_name=user_name).values_list("user_company_name", flat=True)
       print("user_company : ",user_company[0])
       if user_company[0]=='COSAI':
          get_user_company=Company.objects.all()
          
          context={'form':form,'user_company':get_user_company}
       else: 
          get_user_company=Company.objects.filter( name__in = [user_company])
          print("get_user_company : ",get_user_company)
          context={'form':form,'user_company':get_user_company}
    else:
        error='No Information about User Company found'
        context={'form':form,'error':error}
    
    context={'form':form}
    return render(request,'templates/dms/upload_files.html',context)
  
  def get(self,request,user_name):
    print("inside get function upload_files",user_name)
    if (user_name=="ww" or user_name == ""):
      print("user_name wrong : ",user_name)
      return render(request,'templates/dms/upload_files.html')
    else: 
       
        form = FileUploadForm()
        if (user_name):
          #  user_company=UserAccount.objects.filter('user_company_name').get(user_name=user_name)
          VideoFormat=VideoFF.objects.all()
          # Extracting file formats
          file_formats = [video.vtype for video in VideoFormat]

          # Combining file formats into a single string
          VideoFormat = ",".join(file_formats)

          # Print or use the result as needed
          print(VideoFormat)
          
          user_company=UserAccount.objects.filter(user_name=user_name).values_list("user_company_name", flat=True)
          print("usercomp : ",user_company)
          if user_company:
                usercomp=user_company[0]
                print("user_company:", user_company[0],"---",usercomp)
                if (user_company[0] == "COSAI"):
                    get_user_company=Company.objects.all()
                    context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company,"VideoFormat" :VideoFormat}
                else:
                    get_user_company=Company.objects.filter( name__in = [user_company])

                    print("No.of company : ",len(get_user_company)," company : ",get_user_company)         
                    context={'form':form,"usercomp":usercomp,  'get_user_company':get_user_company,"VideoFormat" :VideoFormat}
                    return render(request,'templates/dms/upload_files.html',context)
          else:
                print("user_company is empty")
                return redirect('Error_url')
        else:
                print("user is empty")
                return redirect('Error_url')
        return render(request,'templates/dms/upload_files.html',context)
 
  def post2(self,request,user_name):
    print("request.method:",request.method)
    print('files : ',request.FILES.getlist('fileupload'))
    exceptionvar=False
    if request.method == 'POST':
        # Handle other form data
        company_name = request.POST.get('Company')
        project_name = request.POST.get('Project')
        Location_name = request.POST.get('Location')
        GIS = request.POST.get('gisInput')
        print("GIS:",GIS)
        TrafficType = request.POST.get('TrafficType')
        Remarks = request.POST.get('Remarks')
        Ndays = request.POST.get('Ndays')
        StartDate = request.POST.get('StartDate')
        EndDate = request.POST.get('EndDate')
        urlpath=request.POST.get('urlpath')
        files = request.FILES.getlist('fileupload')
        
        # ... other fields
        try:
          print("company name",company_name)
          company=Company.objects.get(name__iexact=company_name.upper().strip())
          print("company object:",company)
          if company :
           try:
              print("project",project_name,company.id)
              project=Project.objects.get(company=company.id,name__iexact=project_name.upper().strip() )
           except Project.DoesNotExist:
              # exceptionvar=True
              print("project does not exist")
              NewProject=Project.objects.create(
                 company=company,
                 name=project_name,
                 date_created=datetime.datetime.now(tz=timezone.utc),
                 date_updated=datetime.datetime.now(tz=timezone.utc)
              )
              NewProject.save
              print("project created")
             
          else:
              exceptionvar=True
              xhr = {'error':'Error - project not created'}
              return JsonResponse(xhr)  
          project=Project.objects.get(company=company.id,name__iexact=project_name.upper().strip() )
          if project :
              try:
                print("project ID",project.id)
                location=Location.objects.get(project=project.id,name__iexact=Location_name.upper().strip())
                
                # location=Location.objects.filter(project__in = [project]).filter(name__in = [Location_name])
              except Location.DoesNotExist:
                print("location does not exist")
                # exceptionvar=True
                NewLocation=Location.objects.create(
                project=project,
                name=Location_name,
                date_created=datetime.datetime.now(tz=timezone.utc),
                date_updated=datetime.datetime.now(tz=timezone.utc)
              )
                NewLocation.save 
                print("location created")
          else:
              exceptionvar=True
              xhr = {'error':'Error - Location not created'}
              return JsonResponse(xhr)  
          location=Location.objects.get(project=project.id,name__iexact=Location_name.upper().strip())
          print("location id",location.id)
          if location :
                timestr=time.strftime("%Y%m%d_%H%M%S")
                files = request.FILES.getlist('fileupload')
                if (files):  
                    i=0
                    for file in files:
                          i += 1
                          print("filename : ",file)
                          # Customize the filename as needed
                          try:
                              

                              # Get the file extension from the original filename
                              _, file_extension = os.path.splitext(file.name)
                             
                              newfilename=f"{Location_name.upper().strip()}_{timestr}_{i}{file_extension}"
                              
                              print("newfilename:",newfilename)
                              # Get the upload path using the customized filename
                              print("companyname:",company_name)
                              upload_path = get_company_upload_path(company_name.upper().strip(), newfilename)
                              # upload_path=settings.DRIVE_ROOT+'/'+ company_name.upper().strip()
                              
                              os.makedirs(upload_path, exist_ok=True)
                              print("upload_path : ",upload_path)
                             

                              
                              
                              # video_id=new_file_instance.id

                              # print("file  created:",newfilename)
                              # Now move the file to the correct location
                              try:
                               
                                
                                with open(os.path.normpath(os.path.join(upload_path, newfilename)), 'wb') as destination:
                                  print("destination:",destination)
                                  for chunk in file.chunks():
                                      destination.write(chunk)
                              except Exception as e:
                                res = {'errror':'Data save error local ' }
                                return JsonResponse(res)
                                #  upload to gdrive()               
                              print("Gdrive called")
                              try:
                                vlink = gdrive_upl(upload_path,newfilename,None)
                              except Exception as e:
                                  res = {'data':f'google drive upload failed ,{e}'}
                                  return JsonResponse(res)
                              if (vlink != None) :
                              # vlink,dwnlink = upload_to_Gdrive(company_name,newfilename)
                                ## update  DB with gdrive link to view files / download
                                print ("vlink :",vlink )
                                # print("dwnlink :",dwnlink)
                                new_file_instance = FileUploadExternal(
                                CompanyName=company,
                                ProjectName=project,
                                StationName=location,
                                GIS=GIS,
                                TrafficType=TrafficType,
                                Remarks=Remarks,
                                Ndays=Ndays,
                                VideoStartDate=StartDate,
                                VideoEndDate=EndDate,                                
                                files= newfilename, 
                                gdrive_view=vlink,
                                gdrive_dwnld=vlink

                                                                                                    # files=os.path.join(upload_path,newfilename),  # Use the customized filename and path
                                  # ... other fields
                              )
                                new_file_instance.save() ## Save the instance
                                print("delete locally saved file from the storage path :",os.path.normpath(os.path.join(upload_path, newfilename)))
                                try:
                                  os.remove(os.path.normpath(os.path.join(upload_path, newfilename)))
                                except Exception as e:
                                  exceptionvar=True
                                  res = {'data':f'Local files not deleted ,{e}'}
                                  return JsonResponse(res)
                            # except Exception as e:
                            #   exceptionvar=True
                            #   print("error while uploading video file : ", e)
                            #   res = {'data':'error while uploading video file'+e}
                            #   return JsonResponse(res)
                          except Exception as e:
                            exceptionvar=True
                            print("error while converting to string : ", e)
                            xhr = {'error':'Error while converting to string'}
                            return JsonResponse(xhr)
                    
                    # email alert
                    print("exceptionvar :",exceptionvar)
                    if exceptionvar == False:
                        print("email alert invoked")
                        # to_addr='meenakshidcosai@gmail.com'
                        recipient_list = ['meenakshidcosai@gmail.com','costm1993@gmail.com','coscmd@gmail.com']
                        content= "New Video files " + str(i) +" got uploaded now by client  " + company_name
                        subject="New Video files uploaded on "  + timestr +" by client  " + company_name
                        # sending_mail(recipient_list,content,subject)
                        print("email sent")
                        
                        res = {'data':'Files uploaded successfully'}
                        return JsonResponse(res)
                    else:
                        xhr = {'error':'Exception Error'}
                        return JsonResponse(xhr)
                else:
                    if len(urlpath.strip())>0:
                                new_file_instance = FileUploadExternal(
                                              CompanyName=company,
                                              ProjectName=project,
                                              StationName=location,
                                              GIS=GIS,
                                              TrafficType=TrafficType,
                                              Remarks=Remarks,
                                              Ndays=Ndays,
                                              VideoStartDate=StartDate,
                                              VideoEndDate=EndDate,
                                              urlpath=urlpath,
                                              
                                              # files=os.path.join(upload_path,newfilename),  # Use the customized filename and path
                                              # ... other fields
                                          )

                                          # Save the instance
                                new_file_instance.save()
                                print("email alert invoked")
                        
                                recipient_list = ['meenakshidcosai@gmail.com','costm1993@gmail.com','coscmd@gmail.com']
                                content= "New Video files link " +  urlpath + " shared now by client  " + company_name
                                subject="New Video files link  shared on "  + timestr + " by client  " + company_name
                                sending_mail(recipient_list,content,subject)
                                print("email sent")
                                res = {'data':'Data saved successfully'}
                                return JsonResponse(res)
                    else:
                        print("error while saving urlpath: ", e)
                        xhr = {'error':'Error while saving urlpath ' + e}
                        return JsonResponse(xhr)
          else:
              xhr = {'data':'Error - location not found'}
              return JsonResponse(xhr)     
        except Exception as e:
          print("error while saving : ", e)
          xhr = {'error':'Error while uploading'}
          return JsonResponse(xhr)    
 ####################################       # 
  def post(self,request,user_name):
     print("calling move files")
     move_files()
    #  drivefiles=move_files()
     res = {'data':'Data saved successfully'}
     return JsonResponse(res)

  def post3(self,request,user_name):
    print("request.method:",request.method)
    print('files : ',request.FILES.getlist('fileupload'))
    exceptionvar=False
    if request.method == 'POST':
        # Handle other form data
        company_name = request.POST.get('Company')
        project_name = request.POST.get('Project')
        Location_name = request.POST.get('Location')
        GIS = request.POST.get('gisInput')
        print("GIS:",GIS)
        TrafficType = request.POST.get('TrafficType')
        Remarks = request.POST.get('Remarks')
        Ndays = request.POST.get('Ndays')
        StartDate = request.POST.get('StartDate')
        EndDate = request.POST.get('EndDate')
        urlpath=request.POST.get('urlpath')
        files = request.FILES.getlist('fileupload')
        
        # ... other fields
        try:
          print("company name",company_name)
          company=Company.objects.get(name__iexact=company_name.upper().strip())
          print("company object:",company)
          if company :
           try:
              print("project",project_name,company.id)
              project=Project.objects.get(company=company.id,name__iexact=project_name.upper().strip() )
           except Project.DoesNotExist:
              exceptionvar=True
              print("project does not exist")
              NewProject=Project.objects.create(
                 company=company,
                 name=project_name,
                 date_created=datetime.datetime.now(tz=timezone.utc),
                 date_updated=datetime.datetime.now(tz=timezone.utc)
              )
              NewProject.save
              print("project created")
          else:
              exceptionvar=True
              xhr = {'error':'Error - project not created'}
              return JsonResponse(xhr)  
          project=Project.objects.get(company=company.id,name__iexact=project_name.upper().strip() )
          if project :
              try:
                print("project ID",project.id)
                location=Location.objects.get(project=project.id,name__iexact=Location_name.upper().strip())
                
                # location=Location.objects.filter(project__in = [project]).filter(name__in = [Location_name])
              except Location.DoesNotExist:
                print("location does not exist")
                exceptionvar=True
                NewLocation=Location.objects.create(
                project=project,
                name=Location_name,
                date_created=datetime.datetime.now(tz=timezone.utc),
                date_updated=datetime.datetime.now(tz=timezone.utc)
              )
                NewLocation.save 
                print("location created")
          else:
              exceptionvar=True
              xhr = {'error':'Error - Location not created'}
              return JsonResponse(xhr)  
          location=Location.objects.get(project=project.id,name__iexact=Location_name.upper().strip())
          print("location id",location.id)
          if location :
                timestr=time.strftime("%Y%m%d_%H%M%S")
                files = request.FILES.getlist('fileupload')
                if (files):  
                    i=0
                    for file in files:
                          i += 1
                          print("filename : ",file)
                          # Customize the filename as needed
                          try:
                              

                              # Get the file extension from the original filename
                              _, file_extension = os.path.splitext(file.name)
                             
                              newfilename=f"{Location_name.upper().strip()}_{timestr}_{i}{file_extension}"
                              
                              print("newfilename:",newfilename)
                              # Get the upload path using the customized filename
                              print("companyname:",company_name)
                              upload_path = get_company_upload_path(company_name.upper().strip(), newfilename)
                              # upload_path=settings.DRIVE_ROOT+'/'+ company_name.upper().strip()
                              
                              os.makedirs(upload_path, exist_ok=True)
                              print("upload_path : ",upload_path)
                             

                              
                              
                              # video_id=new_file_instance.id

                              # print("file  created:",newfilename)
                              # Now move the file to the correct location
                              try:
                               
                                
                                with open(os.path.normpath(os.path.join(upload_path, newfilename)), 'wb') as destination:
                                  print("destination:",destination)
                                  for chunk in file.chunks():
                                      destination.write(chunk)
                                #  upload to gdrive()               
                                print("Gdrive called")
                               
                                # vlink,dwnlink = p12_drive(company_name,newfilename)
                                vlink,dwnlink = upload_to_Gdrive(company_name,newfilename)
                                # try:
                                #   copy_gdrive_file()
                                # except Exception as e:
                                #    print("error copy file",e)
                                #    exceptionvar=True
                                #    res = {'data':f'Local files not copied ,{e}'}
                                #    return JsonResponse(res)
                                ## update  DB with gdrive link to view files / download
                                print ("vlink :",vlink )
                                print("dwnlink :",dwnlink)
                                new_file_instance = FileUploadExternal(
                                CompanyName=company,
                                ProjectName=project,
                                StationName=location,
                                GIS=GIS,
                                TrafficType=TrafficType,
                                Remarks=Remarks,
                                Ndays=Ndays,
                                VideoStartDate=StartDate,
                                VideoEndDate=EndDate,                                
                                files= newfilename, 
                                gdrive_view=vlink,
                                gdrive_dwnld=dwnlink

                                                                                                    # files=os.path.join(upload_path,newfilename),  # Use the customized filename and path
                                  # ... other fields
                              )
                                new_file_instance.save() ## Save the instance
                                print("delete locally saved file from the storage path :",os.path.normpath(os.path.join(upload_path, newfilename)))
                                try:
                                  os.remove(os.path.normpath(os.path.join(upload_path, newfilename)))
                                except Exception as e:
                                  exceptionvar=True
                                  res = {'data':f'Local files not deleted ,{e}'}
                                  return JsonResponse(res)
                              except Exception as e:
                                exceptionvar=True
                                print("error while uploading video file : ", e)
                                res = {'data':'error while uploading video file'+e}
                                return JsonResponse(res)
                          except Exception as e:
                              exceptionvar=True
                              print("error while converting to string : ", e)
                              xhr = {'error':'Error while converting to string'}
                              return JsonResponse(xhr)
                    
                    # email alert
                    if exceptionvar == False:
                        print("email alert invoked")
                        # to_addr='meenakshidcosai@gmail.com'
                        recipient_list = ['meenakshidcosai@gmail.com','costm1993@gmail.com','coscmd@gmail.com']
                        content= "New Video files " + str(i) +" got uploaded now by client  " + company_name
                        subject="New Video files uploaded on "  + timestr +" by client  " + company_name
                        try:
                          sending_mail(recipient_list,content,subject)
                          print("email sent")
                        except Exception as e:
                          xhr = {'error':'sending email Error'}
                          return JsonResponse(xhr)
                        res = {'data':'Files uploaded successfully'}
                        return JsonResponse(res)
                    else:
                        xhr = {'error':'Exception Error'}
                        return JsonResponse(xhr)
                else:
                    if len(urlpath.strip())>0:
                                new_file_instance = FileUploadExternal(
                                              CompanyName=company,
                                              ProjectName=project,
                                              StationName=location,
                                              GIS=GIS,
                                              TrafficType=TrafficType,
                                              Remarks=Remarks,
                                              Ndays=Ndays,
                                              VideoStartDate=StartDate,
                                              VideoEndDate=EndDate,
                                              urlpath=urlpath,
                                              
                                              # files=os.path.join(upload_path,newfilename),  # Use the customized filename and path
                                              # ... other fields
                                          )

                                          # Save the instance
                                new_file_instance.save()
                                print("email alert invoked")
                        
                                recipient_list = ['meenakshidcosai@gmail.com','costm1993@gmail.com','coscmd@gmail.com']
                                content= "New Video files link " +  urlpath + " shared now by client  " + company_name
                                subject="New Video files link  shared on "  + timestr + " by client  " + company_name
                                sending_mail(recipient_list,content,subject)
                                print("email sent")
                                res = {'data':'Data saved successfully'}
                                return JsonResponse(res)
                    else:
                        print("error while saving urlpath: ", e)
                        xhr = {'error':'Error while saving urlpath ' + e}
                        return JsonResponse(xhr)
          else:
              xhr = {'data':'Error - location not found'}
              return JsonResponse(xhr)     
        except Exception as e:
          print("error while saving : ", e)
          xhr = {'error':'Error while uploading'}
          return JsonResponse(xhr)
        
    
  
def upload_to_Gdrive(company_name,filename):
    import os
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = '.\GdriveAccess\\vms-project-405809-ebc7c6ce645e.json'  # Replace with your service account file
    # SERVICE_ACCOUNT_FILE = '.\GdriveAccess\COSAI\\vms-project-405809-a6c450a9b2c9.json' ## info@cosai.in
    # SERVICE_ACCOUNT_FILE = '.\GdriveAccess\VMSCOSAI\cosai-vms-987eae029b67.json' ## vmscosai@gmail.com
    credentials = None
    if os.path.exists('token.json'):
        print("herererrrr 1 ")
        # credentials = Credentials.from_authorized_user_file('token.json')
        credentials = Credentials.from_authorized_user_file('token.json')
       # print("herererrrr 2 ",credentials)
    if not credentials or not credentials.valid:
        #print("herererrrr 3 ")
        if credentials and credentials.expired and credentials.refresh_token:
            print("herererrrr 4 ")
            credentials.refresh()
        else:
            print("herererrrr 5 ")
            credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    try:
        drive_service = build('drive', 'v3', credentials=credentials)
        print("herererrrr 8 ",drive_service)
        # folder_name = 'VMS_VIDEOS' 
        #  # folder_name = 'VMS-VIDEOS' ##Replace with your folder name in Google Drive
        folder_id =   '1AimceH2tbCqmGoybE-wmHrnFmA8uF6Km' #vmscosai
        # folder_id =   '1-gc5Tv09ponupCxQu2pOE73EKk8OxUVC' #info.cosai
        # folder_id = get_folder_id(drive_service, folder_name)
        print("herererrrr 9 ",folder_id)
        media = MediaFileUpload(
            os.path.join(settings.DRIVE_ROOT, company_name.upper().strip(), filename),
            resumable=True,
        )
        print("herererrrr 10 ",media)
        request = drive_service.files().create(
            media_body=media,
            body={
                'name': filename,
                'parents': [folder_id],
                
            },
        ) 
        print("herererrrr 11 ",request)
        response = request.execute()
        newfile=response["id"]
        file_id = response.get('id')
    except Exception as e:
           print("file create owner",e)
           return (e)
    try:
       # List files that are shared with the user
        results = drive_service.files().list(q="sharedWithMe=true").execute()
        print("results",results)
        files = results.get('files', [])
        
        if not files:
            print('No shared files found.')
        else:
            print('Copying shared files...')
            for file in files:
                # Copy each file to your own space
                try:
                  copy_request = drive_service.files().copy(fileId=file['id']).execute()
                  print(f"Copied file: {copy_request['name']}")
                except Exception as e:
                  print("Error copy files ", e)
                  return(e)
    except Exception as e:
      print("Error shared files ", e)
      return(e)
    # try:
    # # gauth = GoogleAuth(client_secrets_file ='./GdriveAccess/COSAI/client_secrets.json')
    #   auth_credentials = (
    #     service_account.IDTokenCredentials.from_service_account_file(
    #     'D:\django_project\DMS-latest\GdriveAccess\VMSCOSAI\cosai-vms-987eae029b67.json'))
    #   # Replace 'your-id-token' with the actual ID token you want to verify
    # id_token = auth_credentials[]

# Replace 'your-audience' with the expected audience for the ID token
      # expected_audience = 'your-audience'
      # service = build('drive', 'v3', credentials=auth_credentials)
      # gauth.settings_file =  'D:/django_project/DMS-latest/GdriveAccess/COSAI/client_secrets.json' # './GdriveAccess/COSAI/client_secrets.json'
      # gauth.LocalWebserverAuth()
    # except Exception as e:
    #   print("Error 1 ", e)
    #   return(e)     
    # try:
    # # Set owner as vmscosai@gmail.com
    #     permission_request = drive_service.permissions().create(
    #         fileId=file_id,
    #         transferOwnership = True,
           
    #         body={
                
    #             'type': 'user',
    #             'role': 'owner',
    #             'emailAddress': 'vmscosai@gmail.com',
    #         }
    #     )
    #     permission_response = permission_request.execute()
    #     # Print the link for the user to grant consent
    #     print('Consent URL:', permission_response['transferOwnershipUrl'])
    # except Exception as e:
    #     print("permission create owner",e)
    #     return (e)
    # try:
    #   print('Consent URL:', permission_response['transferOwnershipUrl'])
    # # transfer ownership for the permission created above
    #   permission_response.update(transferOwnership=True)
    
    # except Exception as e:
    #     print("permission transferOwnership ",e)
    #     return (e)    # Set read access for anyone with the link
    #     permission_request = drive_service.permissions().create(
    #         fileId=file_id,
    #         body={
    #             'type': 'anyone',                    
    #             'role': 'reader',
    #               'allowFileDiscovery': True,
                
                
    #         }
    #     )
    #     permission_response = permission_request.execute()
    # except Exception as e:
    #     print("permission create error",e)
    #     return (e)
          
    link = drive_service.files().get(
    fileId=response.get("id"),
    fields='webViewLink'
    ).execute()
    print("newfile :",newfile)
    # file_link = response.get('webViewLink')
    print(link['webViewLink'])
    file_link = f"https://drive.google.com/uc?id={newfile}"
    print("file link",file_link)
    return(link['webViewLink'],file_link)

    # copyfiles(newfile)
        ###copy the file so that it becomes our own file
        # try:
        #   copied_file = drive_service.files().copy(fileId=file_id, body={'name': 'Copy of ' + link['name'],'transferOwnership': True,}).execute()
        # except Exception as e:
        #    print("error drive copy",e)
        #    return (e)
        # Get the file ID from the copied_file
        # fileId=link[response.get("id")]
        # copied_file_id = copied_file['id']
        # print("copied_file_id :",copied_file_id)
        # newfile_id = copied_file.get('id')      
      
        
        # change_ownership(drive_service,newfile)
        # try:
        #   current_owners = drive_service.files().get(fileId=copied_file_id, fields='owners').execute()['owners']
        # except Exception as e:
        #    print("error current_owners fetch",e)
        #    return (e)
        # for owner in current_owners:
        #     permission_id = owner.get("permissionId")
        #     print("permission_id:", permission_id)
        # print('current_owners', current_owners)
       
        # try:
        # # Update ownership of the copied file
        #   permission_request = drive_service.permissions().update(
        #       fileId=copied_file_id,
        #       permissionId=permission_id,
        #       body={
        #          
        #           'type': 'user',
        #           'role': 'owner',
        #           'emailAddress': 'vmscosai@gmail.com',
        #       },
        #      'transferOwnership': True,
        #   ).execute()
        # except Exception as e:
        #    print("error new_permission update",e)
        #    return (e)
       
        # # Print or use the file_link as neededs
    # print("Direct download link:", file_link)

    # try:
    # # Add the file to the specified folder
    #   drive_service.files().update(
    #         fileId=newfile,
    #         addParents=folder_id,
    #         fields='id, parents'
    #     ).execute()
    # except Exception as e:
    #     print("error drive update",e)
    #     return (e)
    # try:
    #   # newname='copy-' + filename
    #   # print(newname)
    #   copy_gdrive_file(newfile,filename,folder_id)
    # except Exception as e:
    #     print("error drive copy",e)
    #     return (e) 
    # print(f"File {newfile} added to folder {folder_id}")
    # return(link['webViewLink'],file_link)

      # return {
      #     'id' : response.get("id"),
      #     'link' : link['webViewLink'],
      #     'name' : filename,
      #     'file_link' : file_link
      # }
      

      # print(f'File uploaded successfully. File ID: {response["id"]}')

    # except Exception as e:
    #   print(f'Error uploading file to Google Drive: {e}')
    #   return(e)


 # Change ownership of the copied file ----------newly added-----------begin
       # Modify the ownership directly using drive.files().update
        # permission = {
        #   'type': 'user',
        #   'role': 'owner',
        #   'emailAddress': "info@cosai.in",
        #    }
        # try:
        #     permission_response=drive_service.permissions().create(fileId=file_id, body=permission).execute()
        #     permission_id = permission_response['id'] 
        #     print("permission_id :",permission_id)

        # except Exception as e:
        #     print("error enabling transferOwnership ", e)
        #     return e
        # try:
           
        #     permission1 = permission_response.permissions().get(fileId=file_id, permissionId=permission_id).execute()
        #     permission1['role'] = 'owner'
        #     print('    Upgrading existing permissions to ownership.')
        #     permission_response.permissions().update(fileId=file_id, permissionId=permission_id, body=permission1, transferOwnership=True).execute()
        # except Exception as e:
        #     print("error updating transferOwnership ", e)
        #     return e
        # try:
        #     drive_service.files().update(
        #         fileId=file_id,                 
        #         owner="info@cosai.in",
        #         transferOwnership=True,
        #     ).execute()
        # except Exception as e:
        #     print("error enabling transferOwnership ", e)
        #     return e
        # Change ownership of the copied file ----------newly added-----------end

# def change_ownership(service, file_id):
#     print("change_ownership function ",service,"      ",file_id)
#     # Get the owners of the destination folder
#     api_key = 'AIzaSyAEX7dlTz3CG0-vx5BuUd1XhkEsq-iLdFs'
#     destination_service = build('drive', 'v3', developerKey=api_key)
#     destination_folder_id = '1-gc5Tv09ponupCxQu2pOE73EKk8OxUVC'
#     try:  
#       destination_owners = destination_service.files().get(fileId=destination_folder_id, fields='owners').execute()['owners']
#     except Exception as e:
#         print("error destination_owners ", e)
#         return e
#     print("destination_owners",destination_owners)
#     try:
#       destination_owners_emails = [owner['emailAddress'] for owner in destination_owners]
#     except Exception as e:
#         print("error destination_owners emails ", e)
#         return e
#     try:
#       current_owners = service.files().get(fileId=file_id, fields='owners').execute()['owners']
#     except Exception as e:
#         print("error current_owners  ", e)
#         return e
#     try:
#       for owner in current_owners:
#         current_permissions = service.permissions().list(fileId=file_id).execute()
#         print("Current Permissions:", current_permissions)
#         # service.permissions().delete(fileId=file_id, permissionId=owner['emailAddress']).execute()
#     except Exception as e:
#         print("error service  permissions deletion ", e)
#         return e
#     try:
#       for owner_email in destination_owners:
#         new_permission = {
#             'type': 'user',
#             'role': 'owner',
#             'emailAddress': owner_email,
#         }
#         service.permissions().create(fileId=file_id, body=new_permission).execute()
#     except Exception as e:
#         print("error new_permission  creation ", e)
#         return e

def get_folder_id(drive_service, folder_name):
    print("called get_folder_id")
    results = (
        drive_service.files()
        .list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'")
        .execute()
    )
   # print("get folder 1 ",results)
    items = results.get('files', [])
  #  print("get folder 2 ",items)
    if not items:
       # print("get folder 3 ")
        # Create the folder if it doesn't exist
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
        }
       # print("get folder 4 ",folder_metadata)
        folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
       # print("get folder 5 ",folder)
        return folder['id']
    else:
       # print("get folder 6 ")
        return items[0]['id']
    

# def copy_gdrive_file(file_id,file_name,parent_folder_id): 
         
#     print("copy grive called")
    
#     parser = argparse.ArgumentParser(description='Google Drive file copy.')
#     parser.add_argument('source_id',
#                         help='source file id')
#     parser.add_argument('-t', '--title',
#                         help='destination title')
#     args = parser.parse_args()
#     print("args:",args)
#     drive = get_drive_handle()
#     print("drive handle",drive)

#     # f = drive.CreateFile()  # i.e. `f` is a Google Drive File object.
#     f=drive.CreateFile()
#     file_id = f['id']
#     # file_title = f['title']
#     print("file_id",file_id)
#     service = drive.auth.service
#     try:
#       f_copy = copy_file(service, file_id, file_name)
#     except Exception as e:
#        print("copy_file error :",e)
#        return (e)
    # try:
    #   source = drive.CreateFile({'id': args.source_id})
    # except Exception as e:
    #    print("source error :",e)
    #    return (e)
    # try:
       
    #  source.FetchMetadata('title')
    # except Exception as e:
    #    print("source FetchMetadata :",e)
    #    return (e) 

    # print(source)

    # dest_title = args.title if args.title else source['title']
    # dest_id = copy_file(drive.auth.service, args.source_id, dest_title)
    
    # dest = drive.CreateFile({'id': dest_id})
    # dest.FetchMetadata('title')
    
    # print(dest)

# def get_drive_handle():
#     print("inside get_drive_handle ")
#     gauth = GoogleAuth()
#     gauth.settings_file =  'D:/django_project/DMS-latest/GdriveAccess/VMSCOSAI/client_secret_993378751422-desktop.json'
#     # gauth.LocalWebserverAuth()
#     drive = GoogleDrive(gauth)
#     print("drive returned ",drive)
#     return drive

# def copy_file(service, source_id, dest_title):
#     print("copy file")
#     copied_file = {'title': dest_title}
#     f = service.files().copy(fileId=source_id, body=copied_file).execute()
#     print("return id", f['id'])
#     return f['id']
    



# def gdrive():
   
#     # Define the auth scopes to request.
#     scope = 'https://www.googleapis.com/auth/drive.metadata.readonly'
#     key_file_location = '.\GdriveAccess\\vms-project-405809-ebc7c6ce645e.json'

#     try:
#         # Authenticate and construct service.
#         service = get_service(
#             api_name='drive',
#             api_version='v3',
#             scopes=[scope],
#             key_file_location=key_file_location)

#         # Call the Drive v3 API
#         results = service.files().list(
#             pageSize=10, fields="nextPageToken, files(id, name)").execute()
#         items = results.get('files', [])

#         if not items:
#             print('No files found.')
#             return
#         print('Files:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))
#     except HttpError as error:
#         # TODO(developer) - Handle errors from drive API.
#         print(f'An error occurred: {error}')

# def get_service(api_name, api_version, scopes, key_file_location):
#     """Get a service that communicates to a Google API.

#     Args:
#         api_name: The name of the api to connect to.
#         api_version: The api version to connect to.
#         scopes: A list auth scopes to authorize for the application.
#         key_file_location: The path to a valid service account JSON key file.

#     Returns:
#         A service that is connected to the specified API.
#     """

#     credentials = service_account.Credentials.from_service_account_file(
#     key_file_location)

#     scoped_credentials = credentials.with_scopes(scopes)

#     # Build the service object.
#     service = build(api_name, api_version, credentials=scoped_credentials)

#     return service

# def authenticate_and_upload( filepath, file_name, folder_id=None):
    # # Authenticate using the client_secrets.json file
    # print("Inside function : authenticate_and_upload ")
    # try:
    #   # gauth = GoogleAuth(client_secrets_file ='./GdriveAccess/COSAI/client_secrets.json')
    #   gauth = GoogleAuth()
      
    #   gauth.settings_file =  'D:/django_project/DMS-latest/GdriveAccess/COSAI/client_secrets.json' # './GdriveAccess/COSAI/client_secrets.json'
    #   gauth.LocalWebserverAuth()
    # except Exception as e:
    #    print("Error 1 ", e)
    #    return(e)
    # print("gauth : ",gauth)
    # # gauth.LocalWebserverAuth()
    # try:
    #   # Create GoogleDrive instance with authenticated GoogleAuth instance
    #   drive = GoogleDrive(gauth)
    # except Exception as e:
    #    print("error 2 : ", e)
    #    return(e)
    # print("drive : ",drive)
    # folder_id = "1AimceH2tbCqmGoybE-wmHrnFmA8uF6Km"# get_folder_id(drive, "VMS-VIDEOS")

    # # Create a file on Google Drive
    # try:  
    #   file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}] if folder_id else []})
    # except Exception as e:
    #   print("Error 3:",e)
    #   return(e)
    # print ("file_drive",file_drive)
    
    # file_path=filepath+'/'
    # try:
    # # Upload the contents of the local file
    #   file_drive.SetContentFile(file_path+file_name)
    # except Exception as e:
    #   print("Error 4:",e)
    #   return(e)
    # try:
    #   file_drive.Upload()
    # except Exception as e:
    #   print("Error 5:",e)
    #   return(e)
    # print(f"File '{file_name}' uploaded to Google Drive.")
    # return("success")

    # print("Inside function: authenticate_and_upload")
    # try:
    #     print("Inside function: authenticate_and_upload")

    # # Print the current working directory
    #     print("Current working directory:", os.getcwd())
    #     current_directory=os.getcwd()
    #     # Print the absolute path to the script
    #     script_directory = os.path.dirname(os.path.realpath(__file__))
    #     print("Script directory:", script_directory)
  
    #     # Construct the absolute path to client_secrets.json
    #     client_secrets_path = os.path.join(current_directory, 'GdriveAccess', 'COSAI', 'client_secrets.json')
    #     print("Client secrets path:", client_secrets_path)
    #     print("File permissions:", oct(os.stat(client_secrets_path).st_mode)[-3:])
    #      # Print the contents of the GdriveAccess directory
    #     print("Contents of GdriveAccess directory:", os.listdir(os.path.join(current_directory, 'GdriveAccess')))
    #     try:
    #       gauth = GoogleAuth()
    #       print("gauth:", gauth)
    #     # gauth.GoogleDriveAuth()
    #     # gauth.settings_file = client_secrets_path
    #     except Exception as e:
    #       print("Error:", e)
    #       return (None)
    #     try:
    #       # gauth.LocalWebserverAuth()
    #       client_secrets_path = r'\\DESKTOP-AICOHCH\django_project\DMS-latest\GdriveAccess\COSAI\client_scret.json'
    #       file_1 = 'client_secrets.json'

    #       if os.path.exists(client_secrets_path):
    #           gauth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path 
    #       else:
    #           print(f"Error: File '{client_secrets_path }' not found.")
          
    #       print("Client secrets path 2 :", client_secrets_path)
    #       print("File permissions:", oct(os.stat(client_secrets_path).st_mode)[-3:])

    #       with open(client_secrets_path, 'r') as file:
    #           content = file.read()
    #       print("File content:", content)
    #       print("calling  gauth.CommandLineAuth()")
    #       # gauth.CommandLineAuth(argv=['--noauth_local_webserver'])
    #       print("gauth 1 :")
    #     except Exception as e:
    #       print("Error:", e)
    #       return (None)
    # except Exception as e:
    #     print("Error:", e)
    #     return (None)

    # print("gauth:", gauth)

    # try:
    #     drive = GoogleDrive(gauth)
    # except Exception as e:
    #     print("Error drive :", e)
    #     return (None)

    # print("drive:", drive)
    # folder_id = "1AimceH2tbCqmGoybE-wmHrnFmA8uF6Km"  # Replace with the correct folder_id

    # try:
    #     file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}] if folder_id else []})
    # except Exception as e:
    #     print("Error:", e)
    #     return (None)

    # print("file_drive", file_drive)
    # print("provide file path : ",filepath)
    # filefolder_path = os.path.join(filepath,file_name)
    # print("filefolder_path : ",filefolder_path)
    # file_path = filepath#r'\\DESKTOP-AICOHCH\django_project\DMS-latest\UploadedVideos\COSAI\L1_20231124_174746_1.mp4'
    # #filefolder_path
    # try:
    #     file_drive.SetContentFile(filefolder_path )
    # except Exception as e:
    #     print("Error SetContentFile:", e)
    #     return (None)

    # try:
    #     file_drive.Upload()
    # except Exception as e:
    #     print("Error Upload :", e)
    #     return (None)
    # print('Title: %s' % file_drive['title'])
    # print('ID: %s' % file_drive['id'])
    # print('Link: %s' % file_drive['alternateLink'])
    # print(f"File '{file_name}' uploaded to Google Drive.")
    # return (file_drive['alternateLink'])

# def Service_Acct_Gdrive():
#     gauth = GoogleAuth()
#     gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     'path/to/service_account_key.json',  # Replace with the path to your service account key file
#     ['https://www.googleapis.com/auth/drive']
# )
#     drive = GoogleDrive(gauth)

#     # Now you can use PyDrive methods like Upload
#     file_drive = drive.CreateFile({'title': 'Hello.txt'})
#     file_drive.Upload()

# def gdrive_upl(filepath, file_name, folder_id=None):
#     from googleapiclient.discovery import build
#     from googleapiclient.http import MediaFileUpload
#     # Replace 'YOUR_API_KEY' with the actual API keys
#     print("filepath :",filepath)
#     api_key = 'AIzaSyCUB1GZVXLLNhcORjVXDXkNoMbTl3Iseyw'
#     drive_service = build('drive', 'v3', developerKey=api_key)
#     folder_id = "1AimceH2tbCqmGoybE-wmHrnFmA8uF6Km"  # Replace with the correct folder_id
    
#     # Create a new file in Google Drive
#     file_metadata = {'name': file_name}
#     filename=os.path.join(filepath,file_name)
#     print("filename :",filename)
#     media = MediaFileUpload(filename, mimetype='video/mkv')  # Replace with the path to your local file
#     try:
#       file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     except Exception as e:
#        print("error ", e)
#        return(e)
#     web_view_link = file.get('webViewLink')
#     print(f'File created with ID: {file["id"]}')
#     print("web_view_link",web_view_link)
    

#     return(web_view_link)

# Replace these values with your own
# def p12_drive(company_name,filename):
#     print("inside p12 drive")
#     service_account_email = 'vmscosai@cosai-vms.iam.gserviceaccount.com'
#     key_file_path = 'D:\django_project\DMS-latest\GdriveAccess\VMSCOSAI\cosai-vms-a9819194ffc1 - Copy.p12'

#     target_user_email = 'vmscosai@gmail.com'
#     # private_key = load_p12_key(key_file_path, 'notasecret')
#     private_key='D:\django_project\DMS-latest\GdriveAccess\VMSCOSAI\cosai-vms-a9819194ffc1.pem'
#     try:
#       credentials = ServiceAccountCredentials.from_p12_keyfile(
#         service_account_email, private_key, scopes=(['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata']))
#     except Exception as e:
#        print("cred error",e)
#        return(e)
#     print("credentials:",credentials)
#     try:
#       target_credentials = impersonated_credentials.Credentials(
#         source_credentials=credentials,
#         target_principal='vmscosai@cosai-vms.iam.gserviceaccount.com',
#         target_scopes = (['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata']),
#         lifetime=500)
#     except Exception as e:
#        print("target_credentials error",e)
#        return(e)   
#     print('target_credentials : ',target_credentials)
#     try:
#     # Create a Google Drive API service
      
#       drive_service = build('drive', 'v3', credentials=credentials)
#     except Exception as e:
#        print("drive service error",e)
#        return(e)
#     try:
#     # Create a file in Google Drive
#       file_metadata = {'name': filename,
#                        }
#       created_file = drive_service.files().create(body=file_metadata).execute()
#     except Exception as e:
#        print("create file error",e)
#        return(e)
    
    # # Change the owner of the file
    #   new_owner_permission = {
    #       'role': 'owner',
    #       'type': 'user',
    #       'emailAddress': target_user_email
    #   }
    # except Exception as e:
    #    print("ownership error",e)
    #    return(e)
    
    # try:
    #   permission_request=drive_service.permissions().create(
    #       fileId=created_file['id'],
    #       transferOwnership = True,
    #       body={
    #       'role': 'writer',
    #       'type': 'user',
    #       'emailAddress': target_user_email
    #      }
    #   ).execute()
    # except Exception as e:
    #    print("permission get error",e)
    #    return(e)
    # print("Permission details:", permission_request)
    # permId=permission_request['id']
    # print('permId :',permId)
    # ## get link
    # try:
    #   permission_info=drive_service.permissions().update(
    #       fileId=created_file['id'],
    #       permissionId=permission_request['id'],
    #       body={
    #       'role': 'owner',         
    #      }
    #   ).execute()
    # except Exception as e:
    #    print("permission get error",e)
    #    return(e)
    # print("Permission info:", permission_info)
    # try:
    #   link = drive_service.files().get(
    #   fileId=created_file.get("id"),
    #   fields='webViewLink'
    #   ).execute()
    # except Exception as e:
    #    print("get link error",e)
    #    return(e)
    
    # copyfiles(created_file.get("id"))
    # print("newfile link :",link['webViewLink'])
    # return(link['webViewLink'])

# def public DriveService GetService(string certificatePath, string certificatePassword, string googleAppsEmailAccount, string emailAccountToMimic, bool allowWrite = true)
# {
#     var certificate = new X509Certificate2(certificatePath, certificatePassword, X509KeyStorageFlags.Exportable);

#     var credential = new ServiceAccountCredential(
#        new ServiceAccountCredential.Initializer(googleAppsEmailAccount)
#        {
#            Scopes = new[] { allowWrite ? DriveService.Scope.Drive : DriveService.Scope.DriveReadonly },
#            User = emailAccountToMimic
#        }.FromCertificate(certificate));

#     // Create the service.
#     return new DriveService(new BaseClientService.Initializer
#     {
#         HttpClientInitializer = credential,
#         ApplicationName = ApplicationName
#     });
# }

# def load_p12_key(p12_path, password):
#     with open(p12_path, 'rb') as p12_file:
#         p12_data = p12_file.read()

#     private_key = load_pem_private_key(
#         p12_data,
#         password=password.encode('utf-8'),  # Convert password to bytes
#         backend=default_backend()
#     )

#     return private_key

# def copyfiles(fileId):
#       from google.oauth2 import service_account
#       from googleapiclient.discovery import build

#       # Replace with the path to your service account key file
#       SERVICE_ACCOUNT_FILE = '.\GdriveAccess\VMSCOSAI\client_secret_webapp.json'

#       # Replace with the ID of the file you want to copy
#       SOURCE_FILE_ID = fileId

#       # Replace with the ID of the folder where you want to copy the file
#       DESTINATION_FOLDER_ID = '1AimceH2tbCqmGoybE-wmHrnFmA8uF6Km'

#       authenticate_and_copy_file(SERVICE_ACCOUNT_FILE,SOURCE_FILE_ID,DESTINATION_FOLDER_ID)

# def authenticate_and_copy_file(SERVICE_ACCOUNT_FILE,SOURCE_FILE_ID,DESTINATION_FOLDER_ID):
#     # Authenticate using the service account key file
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE,
#         scopes=['https://www.googleapis.com/auth/drive']
#     )

#     # Create a Drive API service
#     service = build('drive', 'v3', credentials=credentials)

#     try:
#         # Get metadata of the source file
#         source_file_metadata = service.files().get(fileId=SOURCE_FILE_ID).execute()

#         # Copy the file to the destination folder
#         copied_file = service.files().copy(
#             fileId=SOURCE_FILE_ID,
#             body={
#                 'name': source_file_metadata['name'],
#                 'parents': [DESTINATION_FOLDER_ID]
#             }
#         ).execute()

#         print(f"File copied successfully. New file ID: {copied_file['id']}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

#     try:
#     # Set the owner permission of the copied file
#         new_owner_permission = {
#             'role': 'owner',
#             'type': 'user',
#             'emailAddress': 'vmscosai@gmail.com'
#         }

#         service.permissions().create(
#             fileId=copied_file['id'],
#             transferOwnership=True,
#             body=new_owner_permission,
            
#         ).execute()
#     except Exception as e:
#         print(f"An error occurred for permission: {e}")
#         # consent_link = "https://accounts.google.com/o/oauth2/auth?client_id='993378751422-ds347d4euqjll0sgjbqop06plunne9i8.apps.googleusercontent.com'&redirect_uri='http://127.0.0.1:8003'&scope=https://www.googleapis.com/auth/drive&response_type=code&access_type=offline&prompt=consent"
#         # print(f"New owner must grant consent for ownership transfer: {consent_link}")
#     else:
#         return (e)
#         # Return the ID of the newly created file
#     return copied_file['id']


# views.py



def upload_to_google_drive(request):
    print("inside upload_to_google_drive",request.method )
    if request.method =="GET":
    
        # Handle GET request (display the form)
        return render(request, 'templates/dms/testupload.html')
    elif request.method == 'POST':
    # Specify the MIME type of the file you want to upload
        mime_type = 'application/pdf'  # Change this based on your file type
        print("request.files",request.FILES)
        try:
          if (request.FILES['file'] != None):
        # Get the file from the request
            uploaded_file = request.FILES['file']
        except Exception as e:
            print('File key not found in request',e)
            return JsonResponse({'error': 'File key not found in request'})
        GOOGLE_DRIVE_API_KEY_FILE = 'D:\django_project\DMS-latest\GdriveAccess\\vms-project-405809-ebc7c6ce645e.json'
        # Authenticate with Google Drive API
        credentials = Credentials.from_authorized_user_file(GOOGLE_DRIVE_API_KEY_FILE, ['https://www.googleapis.com/auth/drive.file'])
        drive_service = build('drive', 'v3', credentials=credentials)
        print("drive service built")
        # Create file metadata
        file_metadata = {'name': uploaded_file.name}

        # Upload the file
        media = MediaFileUpload(uploaded_file, mimetype=mime_type)
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("file uploaded")
        # Return the file ID or any other relevant information
        return JsonResponse({'file_id': file.get('id')})
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

def move_files1():
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive

    # Authenticate and create a PyDrive client
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authenticates using the local webserver
    drive = GoogleDrive(gauth)
    print("drive :",drive)
    # Find the file(s) in "Shared with me"
    shared_with_me_files = drive.ListFile({'q': "'me' in owners and trashed=false"}).GetList()
    print("shared_with_me_files:",shared_with_me_files)
    # Specify the folder ID where you want to move the files
    destination_folder_id = '1N06gtoWZ3Qn9Y6gChpqCWaB65IgVbioH'

    # Iterate through the files and move them to the destination folder
    for file in shared_with_me_files:
        # Change the parent folder(s) of the file
        file['parents'] = [{'id': destination_folder_id}]
        print(file['id'])
        file.Upload()

    print("Files moved successfully.")


def move_files():
  import os
  from google.oauth2 import service_account
  from googleapiclient.discovery import build
  print(" inside move files function : ")
  # Replace 'path/to/credentials.json' with the path to your service account key file
  # credentials = service_account.Credentials.from_service_account_file('path/to/credentials.json', scopes=['https://www.googleapis.com/auth/drive'])
  # credentials = credentials
  # Replace 'source_folder_id' and 'destination_folder_id' with the appropriate folder IDs
  # source_folder_id = 'your_source_folder_id'
  SCOPES = ['https://www.googleapis.com/auth/drive.file']
  SERVICE_ACCOUNT_FILE = '.\GdriveAccess\VMSCOSAI\cosai-vms-987eae029b67.json'
  credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  # source_folder_id = '1-gc5Tv09ponupCxQu2pOE73EKk8OxUVC' #  '1AimceH2tbCqmGoybE-wmHrnFmA8uF6Km'
  source_folder_id = '1AimceH2tbCqmGoybE-wmHrnFmA8uF6Km'
  # destination_folder_id = '1N06gtoWZ3Qn9Y6gChpqCWaB65IgVbioH' 
  destination_folder_id = '12hkrPdL758x5SmyX7FR3mOskXWRhMIw4'
  print("source_folder_id ",source_folder_id)
  # # Replace 'file_id_to_move' with the ID of the file you want to move
  # file_id_to_move = fileid

  drive_service = build('drive', 'v3', credentials=credentials)

  # Retrieve the existing parents to remove the file from the source folder
  
  
  # detination folder
  print("destination_folder_id ",destination_folder_id)
  destination_folder_files = drive_service.files().list(q=f"'{destination_folder_id}' in parents",
                                                      fields='files(id, name)').execute().get('files', [])
  # if (destination_folder_files != None):
  #   for file in destination_folder_files:
  #         file_id = file['id']
  #         print('fileid',file_id)
  # else:
  #    print('no files in destination')
  # List all files in the source folder
  # source_folder_files = drive_service.files().list(q=f"'{source_folder_id}' in parents",
                                                      # fields='files(id, name)').execute().get('files', [])
  # Incorrect usage of a method


  # Find the file(s) in "Shared with me"
  # shared_with_me_files = drive_service.files().list({'q': "'me' in owners and trashed=false"}).execute().get('files', [])
  # result = drive_service.files().list(q ="sharedWithMe=true", pageSize=10, fields="nextPageToken, files(id, name)").execute()
  result = drive_service.files().list(q="'vmscosai@cosai-vms.iam.gserviceaccount.com' in owners and trashed=false and mimeType contains 'video'").execute()
  # result = drive_service.files().list(q="'me' in owners and trashed=false and mimeType contains 'video'").execute()
  shared_with_me_files = result.get('files', [])    
  print("shared_with_me_files list")
  
  # Move each file to the destination folder
  # for file in source_folder_files:
  for file in shared_with_me_files:
        file_id = file['id']
        print('fileid',file_id,file['name'])
        # try:
        #   result=move_file_to_folder(drive_service, file_id, destination_folder_id,shared_with_me_files)

        # except Exception as e:
        #     print("error 1 move_file_to_folder ",e)
        #     return(e) 
        # if (result == "success"):
        #  print(f"File '{file['name']}' moved to '{destination_folder_id}' folder.")
        # else:
        #    print(f" Error - File '{file['name']}'not moved to '{destination_folder_id}' folder.")

  # Move the file to the destination folder
  # file = drive_service.files().update(fileId=file_id_to_move,
  #                                     addParents=destination_folder_id,
  #                                     removeParents=previous_parents,
  #                                     fields='id, parents').execute()

  # print(f"File '{file_id_to_move}' moved to '{destination_folder_id}' folder.")

def move_file_to_folder(drive_service, file_id, destination_folder_id,source_folder_id):
    print("inside move_file_to_folder for file_id",file_id)
    # Retrieve the existing parents to remove the file from the source folder
    file = drive_service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = file.get('parents', [])
    if len(previous_parents) > 0:
        first_parent = previous_parents[0]
        print("first_parent.",first_parent)
        try:
         # Move the file to the destination folder 
          drive_service.files().update(fileId=file_id,
                                    addParents=destination_folder_id,
                                    removeParents=first_parent,
                                    # removeParents=previous_parents[0],
                                    fields='id, parents').execute()
        except Exception as e:
          print("error update parent ",e)
          return(e)
        
    else:
        print("The list is empty.")
        
    # print("previous_parents :",previous_parents[0])
    # print("destination folder :",destination_folder_id)
    # try:
   
    #    return(e)
    return("success")