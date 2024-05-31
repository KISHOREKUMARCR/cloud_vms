
from django.conf import settings

def media_path(request):
    return {
         'MEDIA': settings.MEDIA_URL,
        'EXTERNAL':settings.EXTERNAL_URL,
        'DRIVE':settings.DRIVE_URL,
        'DETECTIONVIDEO':settings.DETECTION_URL,
        'DETECTIONREPORT':settings.CSVREPORT_URL,
        'DETECTIONDB':settings.DETECTIONDB_URL,
        'GDRIVE':settings.GDRIVE_URL,
        
            }
