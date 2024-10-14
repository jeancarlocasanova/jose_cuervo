"""jose_cuervo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from cuervo.views import *

admin.site.site_header = "Jose Cuervo Admin"
admin.site.site_title = "Jose Cuervo Admin Portal"
admin.site.index_title = "Welcome to Jose Cuervo Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', configurationMenu_view),
    path('configuration/', configurationMenu_view, name='configuration'),
    path('Ordermenu/', orderMenu_view, name='order-menu'),
    path('labelMenu/', labelMenu_view, name='label-menu'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_token, name="register"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('inventoryLocation/', inventoryLocation_view, name='inventoryLocation'),
    path('inventoryLocation/delete/<int:pk>', deleteLocation_view.as_view(), name='location-delete'),
    path('inventoryLocation/edit/<int:pk>', updateLocation_view.as_view(), name='location-edit'),
    path('inventoryLocationCreate/', createLocation_view, name='location-create'),

    path('labelStatus/', labelStatus_view, name='labelStatus'),
    path('labelStatus/delete/<int:pk>', deleteStatus_view.as_view(), name='status-delete'),
    path('labelStatus/edit/<int:pk>', updateLabelStatus_view.as_view(), name='status-edit'),
    path('labelStatusCreate/', createStatus_view, name='status-create'),

    path('labelinit/', charge_zip_server, name='init-create'),
    path('labelinit-csv/', charge_csv_server, name='init-create-csv'),

    path('progress/', progress_charge_labels, name='progress_charge_labels'),
    path('progress/data/', progress_data_ajax, name='progress_data_ajax'),
    path('mark-as-seen/<int:id>/', mark_as_seen, name='mark_as_seen'),
    path('view-log-files/<int:id>/', view_log_files, name='view_log_files'),
    path('folios/<str:file_name>/', view_folios, name='view_folios'),

    path('labeluploadinventory/', init_label_in_inventory, name='label-inventory'),

    path('labeluploadcanceled/', init_label_canceled, name='label-canceled'),

    path('solicitudmarbete/', solicitudmarbete_request, name='solicitudmarbete'),

    path('labeldamaged/', init_label_damaged, name='label-damaged'),
    path('obtener_uniqueid/', obtener_uniqueid, name='obtener_uniqueid'),
    path('agregar_codigo/', agregar_codigo, name='agregar_codigo'),
    path('quitar_codigo/', quitar_codigo, name='quitar_codigo'),
    path('confirmar_listado/', confirmar_listado, name='confirmar_listado'),

    path('coilcreate/', init_coil_create, name='coil-create'),

    path('labeldamaged/', init_label_damaged, name='label-damaged'),
    path('agregar_codigo/', agregar_codigo, name='agregar_codigo'),
    path('quitar_codigo/', quitar_codigo, name='quitar_codigo'),
    path('confirmar_listado/', confirmar_listado, name='confirmar_listado'),

    path('coilcreate/', init_coil_create, name='coil-create'),

    path('granel-lote/', init_granel_lot, name='granel-lote'),

    path('granel-lot-delete/<int:pk>/', delete_granel_lot, name='granel-lot-delete-id'),

    path('consumo-envasado/', Consumo_Envasado, name='consumo-envasado'),

    path('consumo-manualidades/', Consumo_Manualidades, name='consumo-manualidades'),

    path('noasignacion/', num_asignacion, name='no-asignacion'),

    path('coilStatus/', coilStatus_view, name='coilStatus'),
    path('coilStatus/delete/<int:pk>', deleteCoilStatus_view.as_view(), name='coil-status-delete'),
    path('coilStatus/edit/<int:pk>', updateCoilStatus_view.as_view(), name='coil-status-edit'),
    path('coilStatusCreate/', createCoilStatus_view, name='coil-status-create'),

    path('coilType/', coilType_view, name='coilType'),
    path('coilType/delete/<int:pk>', deleteCoilType_view.as_view(), name='coil-type-delete'),
    path('coilType/edit/<int:pk>', updateCoilType_view.as_view(), name='coil-type-edit'),
    path('coilTypeCreate/', createCoilType_view, name='coil-type-create'),

    path('coilProvider/', coilProvider_view, name='coilProvider'),
    path('coilProvider/delete/<int:pk>', deleteCoilProvider_view.as_view(), name='coil-provider-delete'),
    path('coilProvider/edit/<int:pk>', updateCoilProvider_view.as_view(), name='coil-provider-edit'),
    path('coilProviderCreate/', createCoilProvider_view, name='coil-provider-create'),

    path('coil/', coil_view, name='coil'),
    path('coil/edit/<int:pk>', updateCoil_view.as_view(), name='coil-edit'),
    path('coilCreate/', createCoil_view, name='coil-create'),
    path('deleteLabelsfromCoil/<int:id>', deleteLabelsOfaCoil, name="deleteLabelsFromCoil"),

    path('coil-request/', coilRequest_view, name='coil-request'),
    path('coil-request-create/', createCoilRequest, name='coil-request-create'),
    path('coil-request/edit/<int:pk>', solicitudmarbete_request, name='coil-request-edit'),
    path('coil-request/delete/<int:pk>', deleteCoilType_view.as_view(), name='coil-request-delete'),

    path('coil-request-delete/<int:pk>/', delete_coil_request, name='coil-request-delete-id'),

    path('solicitud/<int:pk>/bobinas/', view_coils, name='view-coils'),

    path('coil-request-status/', coilRequestStatus_view, name='coil-request-status'),
    path('coil-request-status-create/', createCoilRequestStatus_view.as_view(), name='coil-request-status-create'),
    path('coil-request-status/edit/<int:pk>', updateCoilRequestStatus_view.as_view(), name='coil-request-status-edit'),
    path('coil-request-status/delete/<int:pk>', deleteCoilRequestStatus_view.as_view(), name='coil-request-status-delete'),

    path('SKU/', sku_view, name='SKU'),
    path('sku/delete/<int:pk>', deleteSku_view.as_view(), name='sku-delete'),
    path('sku/edit/<int:pk>', updateSku_view.as_view(), name='sku-edit'),
    path('skuCreate/', createSku_view, name='sku-create'),

    path('skuType/', skuType_view, name='skuType'),
    path('skuType/delete/<int:pk>', deleteSkuType_view.as_view(), name='sku-type-delete'),
    path('skuType/edit/<int:pk>', updateSkuType_view.as_view(), name='sku-type-edit'),
    path('skuTypeCreate/', createSkuType_view, name='sku-type-create'),

    path('Order/', Order_view, name='Order'),
    path('order/delete/<int:pk>', deleteOrder_view.as_view(), name='order-delete'),
    path('order/edit/<int:pk>', updateOrder_view.as_view(), name='order-edit'),
    path('orderCreate/', createOrder_view, name='order-create'),

    path('Line/', Line_view, name='Line'),
    path('line/delete/<int:pk>', deleteLine_view.as_view(), name='line-delete'),
    path('line/edit/<int:pk>', updateLine_view.as_view(), name='line-edit'),
    path('lineCreate/', createLine_view, name='line-create'),

    path('line/api', list_lines, name='line-api'),
    path('line/api/choice-L', choiceField_lines, name='choice-line-api'),
    path('line/api/choice-O', choiceField_order, name='choice-order-api'),
    path('order/api/create', create_Order, name='api-createOrder'),

    path('request-status/', requestStatus_view, name='request-status'),
    path('request-status/delete/<int:pk>', deleteRequestStatus_view.as_view(), name='request-status-delete'),
    path('request-status/edit/<int:pk>', updateRequestStatus_view.as_view(), name='request-status-edit'),
    path('RequestStatusCreate/', createRequestStatus_view, name='request-status-create'),

    path('assign/', assign_view, name='assign'),
    path('stopOrder/delete/<int:pk>', StopOrder_view.as_view(), name='stop-order'),
    path('assignOrder/', assignOrder_view, name='assign-order'),

    path('labelHandling/', labelHandling_view, name='labelHandling'),
    path('label/edit/<int:pk>', updateLabel_view.as_view(), name='label-edit'),
    path('label/find/<int:pk>', searchLabelByCoilFK, name='label-find'),

    path('coilRequestHandling/', CoilRequestHandling_view, name='coilRequestHandling'),
    path('coilRequest/accept/<int:pk>', AcceptCoilRequest, name='accept-coilrequest'),
    path('coilRequest/decline/<int:pk>', DeclineCoilRequest, name='decline-coilrequest'),

    path('coilreturn/', returnOfCoilsFilter, name='return-coil'),
    path('coilreturn/<int:order_id>', returnOfCoils, name='return-coil'),
    path('coil-return-create/', createReturnOfCoil, name='coil-return-create'),
    path('coil-return-edit/<int:pk>', updateCoilTrace_view.as_view(), name='coil-return-edit'),
    path('coil-return-delete/<int:pk>', deleteCoilTrace_view.as_view(), name='coil-return-delete'),

    path('coilHandling/', coilHandling_view, name='coilHandling'),
    path('usersManagement/', usersManagement_view, name='usersManagement'),
    path('labelTraceability/', labelTraceability_view, name='labelTraceability'),
    path('reports/', reports_view, name='reports'),

    path('label/api', update_label, name='label-api'),
    path('labelstatus/api', list_status, name='status-api'),
    path('autocomplete-sku/', autocomplete_sku, name='autocomplete_sku'),
    path('autocomplete-brand/', autocomplete_brand, name='autocomplete_brand'),
    path('autocomplete-subbrand/', autocomplete_subbrand, name='autocomplete_subbrand'),
]

urlpatterns += staticfiles_urlpatterns()



