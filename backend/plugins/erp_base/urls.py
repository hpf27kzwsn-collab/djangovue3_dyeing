from django.urls import path
from .reports import BusinessReport,BusinessReportExport,REPORTS
from .scanning import Identify,SCANS

urlpatterns=[]
for report in REPORTS:
    urlpatterns += [path('reports/'+report+'/',BusinessReport.as_view(),{'report':report}),
        path('reports/'+report+'/export/',BusinessReportExport.as_view(),{'report':report})]
for kind in SCANS:urlpatterns.append(path('identify/'+kind+'/',Identify.as_view(),{'kind':kind}))
