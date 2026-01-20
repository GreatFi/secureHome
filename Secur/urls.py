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
    path('edit_uploaded_properties/<int:id>', views.edit_uploaded_properties, name="edit_upload"),
    path('edit_listed_properties/<int:id>', views.edit_listed_properties, name="edit_listed"),
    path('delete-draft/<int:id>/confirm/', views.confirm_delete_draft, name='confirm_delete_draft'),
    path('delist/<int:id>/confirm/', views.confirm_delist, name='confirm_delist'),
    path('delete-draft/<int:id>/', views.deleteprops, name='delete_draft'),
    path('delist/<int:id>/', views.delisting_props, name='delist_property'),
    path('saveprops/<int:id>/', views.saveprops, name='saveprops'),
    path('saved_props/', views.saved_props, name='saved_props'),
    path('logout/', views.logout_view, name='logout'),
    path('webs/', views.webs, name='ws'),
    path('code/', views.alt_homepage, name='alt_homepage'),
]

