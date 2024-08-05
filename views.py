from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Screen, Product
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.templatetags.static import static  # Import the static function

@login_required
def display_screen_content(request):
    # Retrieve the logged-in user
    user = request.user

    # Filter Screen objects based on the logged-in user's manager status
    # and related to a Running product
    screens = Screen.objects.filter(manager=user, product__status='RUNNING')

    # Pass the filtered screens to the template
    return render(request, 'screen.html', {'screens': screens})

@login_required
def update_content(request):
    products = Product.objects.all()
    if request.method == 'POST':
        # Handle form submission to update content
        pass  # Add your logic here
    return render(request, 'update_content.html', {'products': products})

@staff_member_required
def activate_product(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        try:
            product = Product.objects.get(id=product_id)
            product.status = "RUNNING"
            product.save()

            # Set all other products to "Stopped" state
            other_products = Product.objects.exclude(id=product_id)
            for other_product in other_products:
                other_product.status = "STOPPED"
                other_product.save()

            # Redirect to display_screen_content view with the id of the running product
            return redirect('display_screen_content')
        except Product.DoesNotExist:
            # Handle case where selected product does not exist
            pass

    products = Product.objects.all()
    return render(request, 'activate_product.html', {'products': products})

def fetch_updated_video_data(request):
    # Retrieve updated video data from the database (e.g., Screen objects)
    updated_video_data = Screen.objects.filter(manager=request.user, product__status='RUNNING').exclude(video_path__isnull=True)

    # Construct the absolute URLs for the static video files
    serialized_video_data = []
    for screen in updated_video_data:
        video_url = static(screen.video_path)
        serialized_video_data.append({'video_path': video_url})

    # Return the serialized video data as JSON response
    return JsonResponse(serialized_video_data, safe=False)

def fetch_updated_pdf_data(request):
    # Retrieve updated PDF data from the database (e.g., Screen objects)
    updated_pdf_data = Screen.objects.filter(manager=request.user, product__status='RUNNING').exclude(pdf_path__isnull=True)

    # Construct the absolute URLs for the static PDF files
    serialized_pdf_data = []
    for screen in updated_pdf_data:
        pdf_url = static(screen.pdf_path)
        serialized_pdf_data.append({'pdf_path': pdf_url})

    # Return the serialized PDF data as JSON response
    return JsonResponse(serialized_pdf_data, safe=False)

def fetch_updated_data(request):
    # Assuming Screen model has fields video_path and pdf_path
    updated_data = []
    screens = Screen.objects.all()

    for screen in screens:
        updated_data.append({
            'video_path': static(screen.video_path),
            'pdf_path': static(screen.pdf_path),
        })

    return JsonResponse(updated_data, safe=False)





# ---------------------------------------------------------------

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Videos ,Pdf,Slider
from .forms import VideoForm , PdfForm,SliderForm
from django.forms import modelformset_factory



#  for videos 
# ---------------------------------------------------------------
def videos_list(request):
    videos = Videos.objects.all()
    context = {'videos': videos}
    return render(request, 'video/videos_list.html', context)

def video_detail(request, video_id):
    video = Videos.objects.get(id=video_id)
    context = {'video': video}
    return render(request, 'video/video_detail.html', context)

def create_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('videos_list')
    else:
        form = VideoForm()
    return render(request, 'video/create_video.html', {'form': form})

def edit_video(request, video_id):
    video = Videos.objects.get(id=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('videos_list')
    else:
        form = VideoForm(instance=video)
    return render(request, 'video/edit_video.html', {'form': form})

def delete_video(request, video_id):
    video = Videos.objects.get(id=video_id)
    video.delete()
    return HttpResponseRedirect('/videos/')


#  for Pdfs 
# ----------------------------------------------------------------
def pdfs_list(request):
    pdfs = Pdf.objects.all()
    context = {'pdfs': pdfs}
    return render(request, 'pdf/pdfs_list.html', context)

def pdf_detail(request, pdf_id):
    pdf = Pdf.objects.get(id=pdf_id)
    context = {'pdf': pdf}
    return render(request, 'pdf/pdf_detail.html', context)

def create_pdf(request):
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdfs_list')
    else:
        form = PdfForm()
    return render(request, 'pdf/create_pdf.html', {'form': form})

def edit_pdf(request, pdf_id):
    pdf = Pdf.objects.get(id=pdf_id)
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES, instance=pdf)
        if form.is_valid():
            form.save()
            return redirect('pdfs_list')
    else:
        form = PdfForm(instance=pdf)
    return render(request, 'pdf/edit_pdf.html', {'form': form})

def delete_pdf(request, pdf_id):
    pdf = Pdf.objects.get(id=pdf_id)
    pdf.delete()
    return HttpResponseRedirect('/pdfs/')




# ----------------------------------------------------------------
#  for screen Sliders


# from django.shortcuts import render, redirect, get_object_or_404
# from django.forms import modelformset_factory, CheckboxInput
# from .models import Slider, Pdf, Videos
# from .forms import SliderForm

# def slider_list(request):
#     sliders = Slider.objects.all()
#     for slider in sliders:
#         print(f"Slider Screen: {slider.screen}, Name: {slider.name}")
#     return render(request, 'screen/slider_list.html', {'sliders': sliders})


# def create_slider(request):
#     PdfFormSet = modelformset_factory(Pdf, fields=('id',), widgets={'id': CheckboxInput()})
#     VideoFormSet = modelformset_factory(Videos, fields=('id',), widgets={'id': CheckboxInput()})

#     if request.method == 'POST':
#         slider_form = SliderForm(request.POST)
#         pdf_formset = PdfFormSet(request.POST, queryset=Pdf.objects.all())
#         video_formset = VideoFormSet(request.POST, queryset=Videos.objects.all())

#         if all(form.is_valid() for form in [slider_form, pdf_formset, video_formset]):
#             slider = slider_form.save()
#             for formset, field in [(pdf_formset, 'upload_pdf'), (video_formset, 'upload_video')]:
#                 for form in formset.cleaned_data:
#                     if form.get('id'):
#                         getattr(slider, field).add(form['id'])
#             return redirect('slider_list')
#     else:
#         slider_form = SliderForm()
#         pdf_formset = PdfFormSet(queryset=Pdf.objects.none())
#         video_formset = VideoFormSet(queryset=Videos.objects.none())

#     context = {
#         'slider_form': slider_form,
#         'pdf_formset': pdf_formset,
#         'video_formset': video_formset
#     }
#     return render(request, 'screen/create_slider.html', context)

# def edit_slider(request, screen):
#     slider = get_object_or_404(Slider, screen=screen)
#     PdfFormSet = modelformset_factory(Pdf, fields=('id',), can_delete=True, widgets={'id': CheckboxInput()})
#     VideoFormSet = modelformset_factory(Videos, fields=('id',), can_delete=True, widgets={'id': CheckboxInput()})

#     if request.method == 'POST':
#         slider_form = SliderForm(request.POST, instance=slider)
#         pdf_formset = PdfFormSet(request.POST, queryset=slider.upload_pdf.all(), prefix='pdfs')
#         video_formset = VideoFormSet(request.POST, queryset=slider.upload_video.all(), prefix='videos')

#         if all(form.is_valid() for form in [slider_form, pdf_formset, video_formset]):
#             slider = slider_form.save()
#             for formset, field in [(pdf_formset, 'upload_pdf'), (video_formset, 'upload_video')]:
#                 for form in formset.cleaned_data:
#                     if form.get('id'):
#                         getattr(slider, field).add(form['id'])
#                     elif form.get('DELETE'):
#                         getattr(slider, field).remove(form['id'])
#             return redirect('slider_list')
#     else:
#         slider_form = SliderForm(instance=slider)
#         pdf_formset = PdfFormSet(queryset=slider.upload_pdf.all(), prefix='pdfs')
#         video_formset = VideoFormSet(queryset=slider.upload_video.all(), prefix='videos')

#     context = {
#         'slider_form': slider_form,
#         'pdf_formset': pdf_formset,
#         'video_formset': video_formset,
#         'slider': slider
#     }
#     return render(request, 'screen/edit_slider.html', context)

# def delete_slider(request, screen):
#     slider = get_object_or_404(Slider, screen=screen)
#     slider.delete()
#     return redirect('slider_list')


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Slider
from .forms import SliderForm

class SliderListView(ListView):
    model = Slider
    template_name = 'screen/slider_list.html'
    context_object_name = 'sliders'

class SliderDetailView(DetailView):
    model = Slider
    template_name = 'screen/slider_detail.html'
    context_object_name = 'slider'

class SliderCreateView(CreateView):
    model = Slider
    form_class = SliderForm
    template_name = 'screen/slider_form.html'
    success_url = reverse_lazy('slider_list')

class SliderUpdateView(UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'screen/slider_form.html'
    success_url = reverse_lazy('slider_list')

class SliderDeleteView(DeleteView):
    model = Slider
    template_name = 'screen/slider_confirm_delete.html'
    success_url = reverse_lazy('slider_list')
    
    
    
from django.shortcuts import render, get_object_or_404
from .models import Slider

def display_slider(request, screen):
    slider = get_object_or_404(Slider, screen=screen)
    videos = slider.upload_video.all()
    pdfs = slider.upload_pdf.all()
    
    media_items = []
    for video in videos:
        media_items.append({'type': 'video', 'item': video})
    for pdf in pdfs:
        media_items.append({'type': 'pdf', 'item': pdf})
    
    media_items.sort(key=lambda x: x['item'].uploaded_at)
    
    context = {
        'slider': slider,
        'media_items': media_items,
    }
    return render(request, 'screen/display_slider.html', context)


# ----------------------------------------------------------------
from .models import ProductionPlan,DailyProductionPlan

def production_plan_list(request):
    plans = ProductionPlan.objects.all()
    return render(request, 'Production/production_plan_list.html', {'plans': plans})


def production_plan_list2(request):
    plans = DailyProductionPlan.objects.all()
    return render(request, 'Production/DailyProductionPlan_list.html', {'plans': plans})

# ---------------------------------------------------------------
