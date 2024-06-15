from .index import *

from django.conf import settings
from django.conf.urls.static import static


from vfms import views
from . import views

from vfms.models import *

from django.urls import path , include

from django.views.generic import CreateView,ListView

urlpatterns = [

    # Onedrive file url
    path('add-cloud-uri/', views.add_cloud_uri_view, name='AddcloudURI'),
    path('view-cloud-uri/', views.view_cloud_uri, name="ViewcloudURI"),
    path('upload-cloud-uri/',views.upload_cloud_uri, name="UploadcloudURI"),
    path('fetch-projects/',views.fetch_cloud_uri, name="FetchcloudURI"),
    path('filter-data/',views.filter_cloud_uri, name="filter_cloud_uri"),
    path('download_cloud_data_excel/',views.download_cloud_data_excel, name="download_cloud_data_excel"),
    path('deleteall_cloud_data_table/',views.deleteall_cloud_data_table, name="deleteall_cloud_data_table"),
    path('desired_download_excel/',views.desired_download_excel, name="desired_download_excel"),

    #company crud operation
    path('AddCompany', views.my_form, name='AddCompany'),
    path("ListCompany/", views.ListCompany.as_view(),name='ListCompany'),
    path('ModifyCompany', views.edit_form, name='ModifyCompany'),
    path('Companyupdate/<int:pk_id>/',views.CompanyUpdate.as_view(),name='Companyupdate'),
    path('Company_delete/<int:pk_id>/', views.Company_delete, name="Company_delete"),

    #project crud operation
    #path("AddProject/", views.project_form,name='AddProject'),
    path("AddProject/",views.Add_project.as_view(),name='AddProject'),  # Addd project get and post method
    path("ListProject/", views.ListProject.as_view(),name='ListProject'),
    path("ModifyProject/",views.editproj_form,name='ModifyProject'),
    path("ProjectUpdate/<int:pk_id>/",views.ProjectUpdate.as_view(),name='UpdateProject'),
    path('Project_delete/<int:pk_id>/',views.Project_delete, name="Project_delete"),


    #common urls
    path("", page,name="home" ),
    path("SuccessMessage/",successpage,name="success_url"),
    path("downloadreport/",downloadreport,name="Download_url"),
    path("WorkInProgress/",WorkInProgress,name="WorkInProgress"),
    path("ErrorMessage/",ErrorMessage,name="Error_url"),
    path("Dashboard/", views.dashboarddata,name='dashboarddata'),



    #rolebased [Menulevel] access urls
    path("Admin_Home/",AdminMenu,name="AdminMenu"),
    path("Approver_Home/",ApproverMenu,name="ApproverMenu"),
    path("User_Home/",UserMenu,name="UserMenu"),

    #company relevant urls

    #project relevant urls
    

    #station/Location relevant urls
    path("ListStation/", views.ListStation.as_view(),name='ListStation'),
    path("AddStation/", views.station_form,name='AddStation'),
    path("ModifyStation/",views.editstn_form,name='Modifytation'),
    path("StationUpdate/<int:pk_id>/",views.StationUpdate.as_view(),name='UpdateStation'),


    #Camera Models relevant urls
    path("ListCameraModel/", views.ListcModel.as_view(),name='ListCameraModel'),
    path("AddCameraModel/", views.Cmodel_form,name='AddCameraModel'),
    path("ModifyCameraModel/",views.editcModel_form,name='ModifyCameraModel'),
    path("UpdateCameraModel/<int:pk_id>/",views.CModelUpdate.as_view(),name='UpdatecModel'),


    #Camera Positions relevant urls
    path("ListCameraPosition/", views.ListcPosition.as_view(),name='ListCameraPosition'),
    path("AddCameraPosition/", views.CPosition_form,name='AddCameraPosition'),
    path("ModifyCameraPosition/",views.editcPosition_form,name='ModifyCameraPosition'),
    path("UpdateCameraPosition/<int:pk_id>/",views.CPositionUpdate.as_view(),name='UpdatecPosition'),



    #User Profile relevant urls
    path("ListUser/", views.ListUser.as_view(),name='ListUser'),
    path("AddUser/", views.add_user,name='AddUser'),
    path("ModifyUserProfile/",views.edit_user,name='ModifyUserProfile'),
    path("UpdateUserProfile/<int:pk_id>/",views.UserProfileUpdate.as_view(),name='UpdateUserProfile'),

    #User Roles relevant urls
    path("ListRole/", views.ListRole.as_view(),name='ListRole'),
    path("AddRole/", views.add_role,name='AddRole'),
    path("ModifyRole/",views.edit_role,name='ModifyRole'),
    path("UpdateRole/<int:pk_id>/",views.RoleUpdate.as_view(),name='UpdateRole'),

    ################# Video File Format ###############

    #Video Formats
    path("ListVideoFormat/", views.ListVFF.as_view(),name='ListVideoFormat'),
    path("AddVideoFormat/", views.add_vff,name='AddVideoFormat'),
    path("ModifyVideoFormat/",views.edit_vff,name='ModifyVideoFormat'),
    path("UpdateVideoFormat/<int:pk_id>/",views.VFFUpdate.as_view(),name='UpdateVideoFormat'),

    #Light Intensity
    path("ListLightIntensity/", views.ListLI.as_view(),name='ListLightIntensity'),
    path("AddLightIntensity/", views.add_li,name='AddLightIntensity'),
    path("ModifyLightIntensity/",views.edit_li,name='ModifyLightIntensity'),
    path("UpdateLightIntensity/<int:pk_id>/",views.LIUpdate.as_view(),name='UpdateLightIntensity'),


    #Label Administration
    
    path("AddLabel/", views.add_label,name='AddLabel'),
    path("ModifyLabel/", views.edit_label,name='ModifyLabel'),
    path("UpdateLabel/<int:pk_id>/", views.LabelUpdate.as_view(),name='UpdateLabel'),
    path("ListLabel/", views.ListLabel.as_view(),name='ListLabel'),
    path("ImportLabel/", views.ImportLabel,name='ImportLabel'),

    ####### video files upload #####################
    path("ListVideos/", views.ListVideos.as_view(),name='ListVideos'),
    path("AddVideo/", views.Videos_form,name='AddVideo'),
    path("ModifyVideo/",views.editvideos_form,name='ModifyVideo'),
    path("UpdateVideo/<int:pk_id>/",views.VideosUpdate.as_view(),name='UpdateVideo'),
   
    path("ApproveRejectVideos/",views.VideosApprovalRejection,name='ApproveRejectVideos'),
    

   
    ## filtering process of Videod file upload
    path("get_projects/", views.GetProjects.as_view(),name='get_projects'),
    path("get_stations/", views.GetLocations.as_view(),name='get_stations'),
    ###dehradun project ###
    path("Dehradun/", views.dehradhun,name='Dehradun'),
    path("AddCustVideo/<str:user_name>/", views.AddCustVideoCustomized.as_view(),name='AddCustVideo'),
    path("ListCustVideo/", views.ListCustVideos.as_view(),name='ListCustVideo'),
    path("ModifyCustVideo/",views.editcustvideos_form,name='ModifyCustVideo'),
    path("UpdateVideoCust/<int:pk_id>/",views.VideosUpdateCust.as_view(),name='UpdateVideoCust'),
    path("ApproveRejectCustVideos/",views.CustVideosApprovalRejection,name='ApproveRejectCustVideos'),
   
    ########## testing #########
    # path("AddCustVideo1/", views.CustVideos_form1,name='AddCustVideo1'),
    ###########
    ##### video detections ##############DetectReport
    path("DetectVideos/", views.detect,name='DetectVideos'),
    path("DetectReport/", views.detect,name='DetectReport'),
    ####external client video upload
    path("DetectExternal/<str:user_name>/", views.detectexternal.as_view(),name='DetectExternal'),
    path("DetectStatus/", views.ExternalVideoDetectionStatus,name='DetectStatus'),
    path("UpdateExtVideo/<int:pk_id>/",views.ExternalVideosUpdate.as_view(),name='UpdateExtVideo'),
    path("DetectionList/<str:user_name>/", views.ExternalVideoDetectionList,name='DetectionList'),
    path("ReportExtVideo/<int:pk_id>/",views.ExternalVideosReport.as_view(),name='ReportExtVideo'),
    path("ReportDownload/<int:pk_id>/",views.ReportDownload.as_view(),name='ReportDownload'),
    
    path("save_extvideo/", views.saveextvideo,name='save_extvideo'),
    path('readsqllite/<int:pk>/',views.readsqllite,name='readsqllite'),
    path('download/', views.download_file, name='download_file'),
    path('redirect-to-folder/<path:folder_path>/', views.redirect_to_folder, name='redirect_to_folder'),
    path('upload_files/<str:user_name>', views.upload_files.as_view(), name='upload_files'), 
    path('generate_token/',views.generate_token,name='generate_token'),
    path('updateDownloadLink/',views.updateDownloadLink,name='updateDownloadLink'),
    path('get_resumable_uri/',views.get_resumable_uri,name='get_resumable_uri'),
    path('upload_chunk_google_drive/', views.upload_chunk_google_drive, name='upload_chunk_google_drive'), 
    
   
]

    

