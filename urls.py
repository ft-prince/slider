from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


from .views import SliderListView, SliderDetailView, SliderCreateView, SliderUpdateView, SliderDeleteView

urlpatterns = [
    path('', views.display_screen_content, name='display_screen_content'),
    path('update_content/', views.update_content, name='update_content'),
    path('activate_product/', views.activate_product, name='activate_product'),
    path('fetch_updated_video_data/', views.fetch_updated_video_data, name='fetch_updated_video_data'),
    path('fetch_updated_pdf_data/', views.fetch_updated_pdf_data, name='fetch_updated_pdf_data'),
    path('fetch_updated_data/', views.fetch_updated_data, name='fetch_updated_data'),
    # Videos
    path('videos/', views.videos_list, name='videos_list'),
    path('videos/create/', views.create_video, name='create_video'),
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    path('videos/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('videos/<int:video_id>/delete/', views.delete_video, name='delete_video'),

    # PDFs
    path('pdfs/', views.pdfs_list, name='pdfs_list'),
    path('pdfs/create/', views.create_pdf, name='create_pdf'),
    path('pdfs/<int:pdf_id>/', views.pdf_detail, name='pdf_detail'),
    path('pdfs/<int:pdf_id>/edit/', views.edit_pdf, name='edit_pdf'),
    path('pdfs/<int:pdf_id>/delete/', views.delete_pdf, name='delete_pdf'),

    # Sliders
    # path('sliders/', views.slider_list, name='slider_list'),
    # path('sliders/create/', views.create_slider, name='create_slider'),
    # path('sliders/<int:screen>/edit/', views.edit_slider, name='edit_slider'),
    # path('sliders/<int:screen>/delete/', views.delete_slider, name='delete_slider'),
    path('sliders/', SliderListView.as_view(), name='slider_list'),
    path('sliders/<int:pk>/', SliderDetailView.as_view(), name='slider_detail'),
    path('sliders/create/', SliderCreateView.as_view(), name='slider_create'),
    path('sliders/<int:pk>/update/', SliderUpdateView.as_view(), name='slider_update'),
    path('sliders/<int:pk>/delete/', SliderDeleteView.as_view(), name='slider_delete'),
    path('display/<int:screen>/', views.display_slider, name='display_slider'),
    path('production-plans/', views.production_plan_list, name='production_plan_list'),
    path('linewise-plans/', views.production_plan_list2, name='production_plan_list'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


