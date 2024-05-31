from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from django.conf import settings
from pathlib import Path
import os,datetime,time
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

# from django.core.validators import FileExtensionValidator
# from django.core.exceptions import ValidationError

# Create your models here.
#company model

class Cloud_File(models.Model):
    file = models.FileField(upload_to="excel")
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Adding a timestamp field

class CloudURI(models.Model):
    userid = models.CharField(max_length=200, null=True)  

    company_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    location_name = models.CharField(max_length=255)
    video_start_time = models.DateTimeField()
    video_end_time = models.DateTimeField()
    camera_angle = models.CharField(max_length=255, null=True)
    onedrive_url = models.URLField()          

    def __str__(self):
        return self.company_name


class Company(models.Model):
    userid = models.CharField(max_length=200, null=True)  # New field for user_id

    name=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=500,null=True)
    phone = models.BigIntegerField (
        validators=[
            MinValueValidator(1000000000, message='Phone number must be 10 digits.'),
            MaxValueValidator(9999999999, message='Phone number must be 10 digits.')
        ])
    email=models.EmailField(null=True)
    
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)
    
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    #function to display acutal customer/company name 
    def __str__(self):
        return self.name



#Project  model
class Project(models.Model):
    userid = models.CharField(max_length=200, null=True)  # New field for user_id
    name=models.CharField(max_length=200,null=True)
    company=models.ForeignKey(Company,on_delete=models.PROTECT, null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)
    company_name=models.CharField(max_length=200,null=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    #function to display acutal project name 
    def __str__(self):
        return self.name





#Location  model
class Location(models.Model):
    name=models.CharField(max_length=200,null=True)
    project=models.ForeignKey(Project,on_delete=models.PROTECT,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
#function to display acutal location name 
    def __str__(self):
        return self.name


#Camera Model types   model
class CameraModel(models.Model):
    name=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)


#function to display acutal location name 
    def __str__(self):
        return self.name



#Camera Position  types   model
class CameraPosition(models.Model):
    CHeight=models.FloatField(max_length=200,null=True)
    Cview=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)


#function to display acutal camera Position  
    def __str__(self):
        return (str(self.CHeight) + "__" + str(self.Cview))

#User  Roles
class Role(models.Model):
    name=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)


    #function to display acutal customer/company name 
    def __str__(self):
        return self.name

#User  model
class User(models.Model):
    name=models.CharField(max_length=200,null=True)
    loginID=models.CharField(max_length=200,null=True)
    password=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.EmailField(null=True)
    company=models.ForeignKey(Company,on_delete=models.PROTECT, null=True)
    role=models.ForeignKey(Role,on_delete=models.PROTECT,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)


    #function to display acutal customer/company name 
    def __str__(self):
        return self.name

#Video File format  types   
class VideoFF(models.Model):
    allowed_extensions=( 
            ("mp4","mp4"),
            ("mov","mov"),
            ("avi","avi"),
            ("wmv","wmv"),
            ("avchd","avchd"),
            ("webm","webm"),
            ("flv","flv"),
            ("mkv","mkv"),
            )
    vtype=models.CharField(max_length=200,null=True,choices=allowed_extensions)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)


#function to display acutal location name 
    def __str__(self):
        return self.vtype

#Light Intensity  types   
class LItypes(models.Model):
    Timings=( 
            ("Day","Day"),
            ("Mid-day","Mid-day"),
            ("Mid-Evening","Mid-Evening"),
            ("Night","Night"),
           
            # ("EarlyMorning","EarlyMorning"),
            )
            
 
    LItype=models.CharField(max_length=200,null=True,choices=Timings)
    date_created=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateField(auto_now=True)


#function to display acutal location name 
    def __str__(self):
        return self.LItype


### Label information -import
class LabelInformation(models.Model):
    LName=models.CharField(max_length=200,null=True)
    AnnotationCnt=models.IntegerField(null=True)
    ImageCnt=models.IntegerField(null=True)
    LightCdn=models.CharField(max_length=10,null=True)
    CameraHeight=models.CharField(max_length=25, null=True)
    RoadType=models.CharField(max_length=25, null=True)
    Reviewed=models.BooleanField(default=False)
    DatasetLocation=models.CharField(max_length=250,null=True)
    
    
### Add/Edit Label information
class AddLabelInfo(models.Model):
    LName=models.ForeignKey(Location,on_delete=models.PROTECT, null=True)
    AnnotationCnt=models.IntegerField(null=True)
    ImageCnt=models.IntegerField(null=True)
    Twowheelercnt=models.IntegerField(null=True)
    Threewheelercnt=models.IntegerField(null=True)
    Buscnt=models.IntegerField(null=True)
    MiniBuscnt=models.IntegerField(null=True)
    Truck2Acnt=models.IntegerField(null=True)
    Axle3cnt=models.IntegerField(null=True)
    Axle4cnt=models.IntegerField(null=True)
    Axle6cnt=models.IntegerField(null=True)
    MultiAxlecnt=models.IntegerField(null=True)
    Echiercnt=models.IntegerField(null=True)
    Otherscnt=models.IntegerField(null=True)
    Carcnt=models.IntegerField(null=True)
    Vancnt=models.IntegerField(null=True)
    Tractorcnt=models.IntegerField(null=True)
    TTrailercnt=models.IntegerField(null=True)
    Lcvcnt=models.IntegerField(null=True)
    DatasetLocation=models.CharField(max_length=250,null=True)
#function to display acutal location name 
    def __str__(self):
        return self.LName  

thumbpath = Path(settings.DRIVE_ROOT) 
thumbpath.mkdir(parents=True, exist_ok=True)
thumbpath_str = str(thumbpath)

fs=FileSystemStorage(location=thumbpath_str) 
class VideoFiles(models.Model):
    
    vstatus=( 
            ("New","New"),
            ("Approved","Approved"),
            ("Rejected","Rejected"),
            ("Modified","Modified"),
            )

    CompanyName=models.ForeignKey(Company,on_delete=models.DO_NOTHING, default=1)
    ProjectName=models.ForeignKey(Project,on_delete=models.DO_NOTHING,default=1)
    StationName=models.ForeignKey(Location,on_delete=models.DO_NOTHING,default=1)
    CameraNo=models.IntegerField(default=1)
    CModel=models.ForeignKey(CameraModel,on_delete=models.DO_NOTHING,default=1)
    CHeight=models.FloatField(null=True)
    CView=models.CharField(max_length=20,null=True)
    VideoStartTime=models.TimeField(null=True)
    VideoEndTime=models.TimeField(null=True)
    LICate=models.ForeignKey(LItypes,on_delete=models.DO_NOTHING,default=1)
    VideoFormat=models.ForeignKey(VideoFF,on_delete=models.PROTECT,null=True)
    # Image1=models.ImageField(upload_to='ThumbNailImages/',null=True, storage=fs)
    # Image2=models.ImageField(upload_to='ThumbNailImages/',null=True, storage=fs)
    # Image3=models.ImageField(upload_to='ThumbNailImages/',null=True, storage=fs)
    FileName=models.CharField(max_length=200,null=True)
    VideoFile=models.FileField(upload_to='UploadedVideos/',null=True,storage=fs)
    Remarks=models.CharField(max_length=1000,null=True)
    RejectedReason=models.CharField(max_length=1000,null=True,default='NA')
    videostatus=models.CharField(max_length=10,default='New',choices=vstatus)

    def __str__(self):
        return self.FileName

class AuditLog(models.Model):
    form_name=models.CharField(max_length=200)
    action_performed=models.CharField(max_length=200)
    acted_by=models.CharField(max_length=200,default='Admin')
    acted_on=models.DateTimeField(auto_now_add=True)


# def validate_file_extension(value):
#     validator = FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])  # Replace with your allowed extensions
#     try:
#         validator(value)
#     except ValidationError as e:
#         raise ValidationError("Invalid file extension")    

###dehradun file upload
class File(models.Model):
    existingPath = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()

class CustVideoFiles(models.Model):
    def validate_file_extension(value):
        extension_validator = FileExtensionValidator(allowed_extensions=["mp4","mov","avi","wmv","avchd","webm","flv","mkv"])
        try:
            extension_validator(value)
        except ValidationError as e:
            raise ValidationError('Invalid file extension. Allowed extensions are "mp4","mov","avi","wmv","avchd","webm","flv","mkv".')
    vstatus=( 
            ("New","New"),
            ("Approved","Approved"),
            ("Rejected","Rejected"),
            ("Modified","Modified"),
            )

    CompanyName=models.ForeignKey(Company,on_delete=models.DO_NOTHING)
    ProjectName=models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    StationName=models.ForeignKey(Location,on_delete=models.DO_NOTHING)
    CameraNo=models.IntegerField(default=1)
    CModel=models.ForeignKey(CameraModel,on_delete=models.DO_NOTHING)
    CHeight=models.FloatField(null=True)
    CView=models.CharField(max_length=20,null=True)
    VideoTakenDate=models.DateField(null=True)
    VideoStartTime=models.TimeField(null=True)
    VideoEndTime=models.TimeField(null=True)
    LICate=models.ForeignKey(LItypes,on_delete=models.DO_NOTHING,default=1)
    VideoFormat=models.ForeignKey(VideoFF,on_delete=models.PROTECT,null=True)
    Remarks=models.CharField(max_length=1000,null=True)
    RejectedReason=models.CharField(max_length=1000,null=True,default='NA')
    videostatus=models.CharField(max_length=10,default='New',choices=vstatus)
    existingPath = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()

    def __str__(self):
        return self.name
    

class CustExternalFiles(models.Model):
    def validate_file_extension(value):
        extension_validator = FileExtensionValidator(allowed_extensions=["mp4","mov","avi","wmv","avchd","webm","flv","mkv"])
        try:
            extension_validator(value)
        except ValidationError as e:
            raise ValidationError('Invalid file extension. Allowed extensions are "mp4","mov","avi","wmv","avchd","webm","flv","mkv".')
   
    vstatus=( 
            ("Completed","Completed"),
            ("InProgress","InProgress"),
            ("Not Started","Not Started"),
            
            )

    CompanyName=models.ForeignKey(Company,on_delete=models.DO_NOTHING)
    ProjectName=models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    StationName=models.ForeignKey(Location,on_delete=models.DO_NOTHING)
    VideoTakenDate=models.DateField(null=True)
    VideoStartTime=models.TimeField(null=True)
    VideoEndTime=models.TimeField(null=True)
    VideoFormat=models.ForeignKey(VideoFF,on_delete=models.PROTECT,null=True,choices=vstatus)
    videostatus=models.CharField(max_length=50,default='Not Started',choices=vstatus)
    Remarks=models.CharField(max_length=1000,null=True)
 
    urlpath=models.URLField(unique=True,null=True)
    DetectedVideoPath=models.CharField(null=True, max_length=100)
    detectionReportpath=models.CharField(null=True, max_length=100)
    existingPath = models.CharField(max_length=100)#,validators=[validate_file_extension]
    name = models.CharField(max_length=50)
    eof = models.BooleanField()

    def __str__(self):
        return (str(self.id) + "__" + str(self.name))
    

    
# class DetectionServerDBDetails(models.Model):
#     engine_type=( 
#             ("sql_lite","sql_lite"),
#             ("Postgres","Postgres"),
#             ("MySQL","MySQL"),            
#             )
     
#     video_id = models.ForeignKey(CustExternalFiles,on_delete=models.DO_NOTHING)
#     dbEngine_type  = models.CharField(max_length=50,default='sql_lite',choices=engine_type)
#     db_name = models.CharField(max_length=50,unique=True)
#     host=models.CharField(max_length=50,null=True)
#     port=models.CharField(max_length=5,null=True)
#     dbusername=models.CharField(max_length=50)
#     dbpassword=models.CharField(max_length=50)
#     tablename=models.CharField(max_length=50)
#     servername=models.CharField(max_length=50)
#     serverusername=models.CharField(max_length=50,null=True)
#     serverpassword=models.CharField(max_length=50,null=True)
    
#     def __str__(self):
#         return (str(self.video_id)) 

# models.py
from uuid import uuid4
def get_company_dir_upload_path(compname, filename):
    # Get the company name from the instance
    # company_name = instance.CompanyName.name
    sanitized_filename = filename.replace(':', '_')
    print("compname, filename :",compname,"____",sanitized_filename)
    company_name = compname+"/"
    upload_dir = os.path.join(settings.DRIVE_ROOT, company_name)
    print("upload_dir :",upload_dir)
    os.makedirs(upload_dir, exist_ok=True)
    

    # Generate a unique identifier using uuid4()
    unique_identifier = str(uuid4())[:6]
    return (f'{unique_identifier}_{sanitized_filename}')
    # Build the upload path with subfolders based on company name
    # return os.path.join('UploadedVideos/', company_name, f'{unique_identifier}_{filename}')
def get_company_upload_path(company_name, filename):
    company_name = company_name.replace('\\', '/')
    
    os.makedirs(os.path.join(settings.DRIVE_ROOT, company_name), exist_ok=True)
    print("full path : ",os.path.join(settings.DRIVE_ROOT, company_name))
    return os.path.join(settings.DRIVE_ROOT, company_name)
   
    # 
class FileUploadExternal(models.Model):
    
    # def validate_filename(value):
    #  """
    # Validate that the filename meets certain criteria:
    # - Alphanumeric characters only
    # - Should not start with an underscore
    # - No special characters except hyphen ("-") allowed
    # """
    # if not value[0].isalnum():
    #     raise ValidationError("Filename should start with an alphanumeric character.")
    
    # if not all(char.isalnum() or char == '-' for char in value[1:]):
    #     raise ValidationError("Invalid characters in the filename. Only alphanumeric characters and hyphen are allowed.")
    
    def validate_file_extension(value):        
        extension_validator = FileExtensionValidator(allowed_extensions=["mp4","mkv"])
        try:
            extension_validator(value)
        except ValidationError as e:
            raise ValidationError('Invalid file extension. Allowed extensions are "mp4","mkv".')
    
    vstatus=( 
            ("Completed","Completed"),
            ("InProgress","InProgress"),
            ("Not Started","Not Started"),
            )

    CompanyName=models.ForeignKey(Company,on_delete=models.DO_NOTHING)
    ProjectName=models.ForeignKey(Project,on_delete=models.DO_NOTHING)
    StationName=models.ForeignKey(Location,on_delete=models.DO_NOTHING)
    GIS=models.CharField(max_length=50,null=True)
    TrafficType=models.CharField(max_length=20,null=True)
    Ndays=models.IntegerField(null=True)
    Remarks=models.CharField(max_length=200,null=True)
    VideoStartDate=models.DateField(null=True)
    VideoEndDate=models.DateField(null=True)
    videostatus=models.CharField(max_length=50,default='Not Started',choices=vstatus)
    urlpath=models.URLField(null=True)
    # client_filename=models.CharField(max_length=30,null=True)
    DetectedVideoPath=models.CharField(null=True, max_length=200,default="")
    DetectionReportPath=models.CharField(null=True, max_length=200,default="")
    files = models.FileField(
        upload_to=get_company_upload_path, validators=[validate_file_extension],  # Use your custom validator
        null=True, blank=True
    )
    gdrive_view=models.URLField(null=True)
    gdrive_dwnld=models.URLField(null=True)
   
    # files = models.FileField(
    #     upload_to=get_company_upload_path, validators=[FileExtensionValidator(allowed_extensions=["mp4", "mkv"])],
    #      null=True, blank=True
    # )

    
    def __str__(self):
        return f"{self.files.name} - {self.CompanyName} - {self.ProjectName}"

class ObjectDetection(models.Model):

    date_time  = models.TimeField()
    vehicle_id = models.IntegerField()
    vehicle_class_id = models.IntegerField()
    vehicle_name = models.CharField(max_length=50)
    direction   = models.IntegerField()
    Cross_line = models.IntegerField()
    frame_number = models.IntegerField()
    image_path = models.CharField(max_length=250)
    # video_id = models.ForeignKey(CustExternalFiles,on_delete=models.DO_NOTHING)
    video_id = models.ForeignKey(FileUploadExternal,on_delete=models.DO_NOTHING)
    def __str__(self):
        return (str(self.video_id)) 


