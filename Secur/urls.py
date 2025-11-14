from django.urls import path
from . import views


urlpatterns=[
    path('', views.homepage, name='homepage'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('Properties/', views.propertiesPage, name='propertiesPage'),
    path('Services/', views.servicesPage, name="servicesPage"),
    path('Signup/', views.createaccount, name="createaccount"),
    path('Login/', views.Login, name="login"),
    path('propdetails/<int:id>/', views.propdetails, name="propdetails"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('addproperty/', views.addproperty, name="addproperty"),
    path('listproperties/<int:id>/', views.listproperties, name="listproperties"),
    # path('listproperties/', views.listproperties, name="listproperties"),
    path('dashboardProp', views.dashboardProp, name="dashboardProp"),
    path('search_results/', views.search_results, name="search_results"),
]

