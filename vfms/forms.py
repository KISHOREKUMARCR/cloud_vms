from django import forms
from .models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError



 
class CloudURIForm(forms.ModelForm):
    class Meta:
        model = CloudURI
        fields = ['company_name', 'project_name', 'location_name', 'onedrive_url', 'video_start_time', 'video_end_time','userid','camera_angle'] 
       

class MyForm(forms.ModelForm): #company model form
  class Meta:
    model = Company
    fields=['name','address','phone','email','userid']

  # Custom validation for phone number
  def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Use RegexValidator to check if the phone number is exactly 10 digits
        validator = RegexValidator(regex=r'^\d{10}$', message='Phone number must be 10 digits.')
        # if not phone.isdigit() or len(phone) != 10:
          #  raise forms.ValidationError('Phone number must be 10 digits.')
        validator(phone)  # This will raise a ValidationError if the phone number is not valid
        return phone
  
  def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert the name to uppercase
        if instance.name:
            instance.name = instance.name

        if commit:
            instance.save()

        return instance



class ProjForm(forms.ModelForm):  #project model form
  class Meta:
    model = Project
    fields=['company','name','company_name','userid']

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert the name to uppercase
        if instance.name:
            instance.name = instance.name

        if commit:
            instance.save()

        return instance

class LocationForm(forms.ModelForm): #location/station model form
  class Meta:
    model = Location
    fields=['project','name',]

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert the name to uppercase
        if instance.name:
            instance.name = instance.name
        if commit:
            instance.save()

        return instance


class CModelForm(forms.ModelForm): #cameramodel model form
    class Meta: 
      model =  CameraModel
      fields=['name',]

class CPositionForm(forms.ModelForm): #camerapostion model form
    class Meta: 
      model =  CameraPosition
      fields=['CHeight','Cview',]


class UserForm(forms.ModelForm): #user model form
  class Meta:
    model = User
    fields=['name','password','loginID','phone','email','company','role']


class RoleForm(forms.ModelForm): #Roles model form
    class Meta: 
      model =  Role
      fields=['name',]

class VideoFileForm(forms.ModelForm): #Video File Formats model form
    class Meta: 
      model =  VideoFF
      fields=['vtype',]

class LIForm(forms.ModelForm): #Light Intensity model form
    class Meta: 
      model =  LItypes
      fields=['LItype',]

class LabelForm(forms.ModelForm): #Light Intensity model form
    class Meta: 
      model =  LabelInformation
      fields=['LName',
              'AnnotationCnt',
              'ImageCnt',
              'LightCdn',
              'CameraHeight',
              'RoadType',
              'Reviewed',
              'DatasetLocation',
              
              ]



class AddLabelForm(forms.ModelForm): #Light Intensity model form
    class Meta: 
      model =  AddLabelInfo
      fields=['LName',
               'AnnotationCnt',
                'ImageCnt',
                'Twowheelercnt',
                'Threewheelercnt',
                'Buscnt',
                'MiniBuscnt',
                'Truck2Acnt',
                'Axle3cnt',
                'Axle4cnt',
                'Axle6cnt',
                'MultiAxlecnt',
                'Echiercnt',
                'Otherscnt',
                'Carcnt',
                'Vancnt',
                'Tractorcnt',
                'TTrailercnt',
                'Lcvcnt',
                'DatasetLocation',
              
              ]



class VFiles(forms.ModelForm): #video files
    class Meta: 
      model =  VideoFiles
      videostatus = forms.CharField(widget=forms.HiddenInput())
      RejectedReason= forms.CharField(widget=forms.HiddenInput())
      fields=['CompanyName',
              'ProjectName',
              'StationName',
              'CameraNo',
              'CModel',
              'CHeight',
              'CView',
              'VideoStartTime',
              'VideoEndTime',
              'LICate',
              'VideoFormat',
              # 'Image1',
              # 'Image2',
              # 'Image3',
              'FileName',
              'VideoFile',
              'Remarks',
             
              ]
      
class VCustFiles(forms.ModelForm): #dehradun video files
    class Meta: 
      model =  CustVideoFiles
      videostatus = forms.CharField(widget=forms.HiddenInput())
      RejectedReason= forms.CharField(widget=forms.HiddenInput())
      fields=['CompanyName',
              'ProjectName',
              'StationName',
              'CameraNo',
              'CModel',
              'CHeight',
              'CView',
              'VideoTakenDate',
              'VideoStartTime',
              'VideoEndTime',
              'LICate',
              'VideoFormat',
              'name',
              'existingPath',
              'Remarks',
             
              ]
    

class VCustExtFiles(forms.ModelForm): #dehradun video files
    class Meta: 
      model =  CustExternalFiles
      videostatus = forms.CharField(widget=forms.HiddenInput())
      
      fields=['CompanyName',
              'ProjectName',
              'StationName',
              'VideoTakenDate',
              'VideoStartTime',
              'VideoEndTime',
              'VideoFormat',
              'videostatus',
              'DetectedVideoPath',
              'detectionReportpath',
              'name',
              'existingPath',
              'Remarks',
              'urlpath',
              ]
class ObjectDetectionReport(forms.ModelForm): #client external video files
    class Meta: 
      model =  ObjectDetection
      videostatus = forms.CharField(widget=forms.HiddenInput())
      
      fields=['date_time',
              'vehicle_id',
              'vehicle_class_id',
              'vehicle_name',
              'direction',
              'Cross_line',
              'frame_number',
              'image_path',
              'video_id',
           ]
# forms.py
# from django import forms
# from .models import FileUpload

class FileUploadForm(forms.ModelForm):
    
        urlpath = forms.URLField(max_length=200,
                     help_text="Please enter the URL of the page.",
                     required=False)
        DetectedVideoPath = forms.URLField(max_length=200,
                     help_text="Please enter the DetectedVideoPath.",
                     required=False)
        DetectionReportPath = forms.URLField(max_length=200,
                     help_text="Please enter the DetectionReportPath .",
                     required=False)
       
        class Meta:
          model = FileUploadExternal
          exclude = ['gdrive_link','gdrive_dwnld']


    
class FileUploadForm1(forms.ModelForm):
    class Meta:
        model = FileUploadExternal
        fields = ['CompanyName',
              'ProjectName',
              'StationName',
              'GIS',
              'TrafficType',
              'Ndays',
              'VideoStartDate',
              'VideoEndDate',              
              'Remarks',
              'urlpath' ,  
              'DetectedVideoPath',
              'DetectionReportPath', 
              'videostatus',   
              'files',
              'gdrive_view',
              'gdrive_dwnld'
              ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set fieldz as read-only when editing an existing videofile
        if self.instance.pk:
            self.fields['CompanyName'].widget.attrs['readonly'] = True
            self.fields['ProjectName'].widget.attrs['readonly'] = True
            self.fields['StationName'].widget.attrs['readonly'] = True
            self.fields['Ndays'].widget.attrs['readonly'] = True
            self.fields['VideoStartDate'].widget.attrs['readonly'] = True
            self.fields['VideoEndDate'].widget.attrs['readonly'] = True            
            self.fields['DetectedVideoPath'].required = False
            self.fields['DetectionReportPath'].required = False 
            self.fields['urlpath'].required = False           
            self.fields['GIS'].required = False
            self.fields['files'].required = False
            self.fields['gdrive_view'].required = False
            self.fields['gdrive_dwnld'].required = False


    def clean_CompanyName(self):
        # Ensure company is not changed during editing
        if self.instance.pk:
            return self.instance.CompanyName
        else:
            return self.cleaned_data['CompanyName']
    
    def clean_ProjectName(self):
        # Ensure email is not changed during editing
        if self.instance.pk:
            return self.instance.ProjectName
        else:
            return self.cleaned_data['ProjectName']
    
    def clean_StationName(self):
        # Ensure email is not changed during editing
        if self.instance.pk:
            return self.instance.StationName
        else:
            return self.cleaned_data['StationName']
    
    def clean_Ndays(self):
        # Ensure email is not changed during editing
        if self.instance.pk:
            return self.instance.Ndays
        else:
            return self.cleaned_data['Ndays']
        
    def clean_VideoStartDate(self):
        # Ensure email is not changed during editing
        if self.instance.pk:
            return self.instance.VideoStartDate
        else:
            return self.cleaned_data['VideoStartDate']
        
    def clean_VideoEndDate(self):
        # Ensure email is not changed during editing
        if self.instance.pk:
            return self.instance.VideoEndDate
        else:
            return self.cleaned_data['VideoEndDate']
        

    def clean(self):
        cleaned_data = super().clean()
        urlpath = cleaned_data.get('urlpath')
        files = cleaned_data.get('files')
        if (urlpath != None):
            if len(urlpath)==0:
                raise forms.ValidationError("Invalid urlpath.")
            
         # Check if both urlpath and files are missing
        if not urlpath and not files:
            raise forms.ValidationError("Please provide either 'urlpath' or 'files'.")

        # Check if both urlpath and files are provided
        if urlpath and files:
            raise forms.ValidationError("Please provide either 'urlpath' or 'files', not both.")
        
        # Check if files are provided and validate the file extension
        if files:
            extension_validator = FileExtensionValidator(allowed_extensions=["mp4","mkv"])
            try:
                extension_validator(files)
            except ValidationError as e:
                raise forms.ValidationError(e)

        return cleaned_data
    
    # def clean_files(self):
    #     # Ensure email is not changed during editing
    #     if self.instance.pk:
    #         return self.instance.files
    #     else:
    #         return self.cleaned_data['files']