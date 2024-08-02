from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Screen, Product, TodayChecklist, RejectionList, PDFFile,MediaFile

from .forms import TodayChecklistForm ,RejectionListForm,PDFFileForm,MediaFileForm,MediaFileUploadForm


from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.templatetags.static import static  # Import the static function
import xlsxwriter
from django.utils import timezone
import json 
import os



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


#  ----------------------------------------------------------------
# Today CheckList views

# View for displaying today's checklist items and handling form submissions
def today_checklist(request):
    if request.method == 'POST':
        form = TodayChecklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('today_checklist')
    else:
        form = TodayChecklistForm(initial={'date': timezone.now().date(), 'shift': get_default_shift()})
    today_checklist_items = TodayChecklist.objects.filter(date=timezone.now().date())
    context = {
        'form': form,
        'today_checklist_items': today_checklist_items,
    }
    return render(request, 'today_checklist/today_checklist.html', context)

# View for exporting today's checklist items to Excel
def export_to_excel(request):
    today_checklist_items = TodayChecklist.objects.filter(date=timezone.now().date())
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=checklist.xlsx'
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet('Today Checklist')
    headers = ['Date', 'Shift', 'Checklist Item']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    for row, item in enumerate(today_checklist_items, start=1):
        worksheet.write(row, 0, item.date.strftime('%Y-%m-%d'))
        worksheet.write(row, 1, item.get_shift_display())
        worksheet.write(row, 2, item.checklist_item)
    workbook.close()
    return response



# Helper function to determine the default shift based on current time
def get_default_shift():
    now = timezone.now()
    if now.hour >= 7 and now.hour < 19:
        return 'A'  # Morning shift if it's between 7 AM and 7 PM
    elif now.hour >= 19 or now.hour < 7:
        return 'C'  # Night shift if it's between 7 PM and 7 AM
    else:
        return 'B'  # Evening shift for any other times







#  ----------------------------------------------------------------
# Rejections list 

# View for displaying rejection list items and handling form submissions
def rejection_list(request):
    if request.method == 'POST':
        form = RejectionListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rejection_list')
    else:
        form = RejectionListForm()
    rejection_list_items = RejectionList.objects.all()
    context = {
        'form': form,
        'rejection_list_items': rejection_list_items
    }
    return render(request, 'rejectionList/rejection_list.html', context)

    
    
# View for exporting rejection list items to Excel
def export_rejection_list(request):
    rejection_list_items = RejectionList.objects.all()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=rejection_list.xlsx'
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet('Rejection List')
    headers = [
        'Date', 'Opening Balance', 'Receive from Rework', 'Total Pass Qty', 'Closing Balance',
        'Total Rejection Qty', 'Defects', 'Operator Signature', 'Verified By', 'Month', 'Stage',
        'Part Description'
    ]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    for row, item in enumerate(rejection_list_items, start=1):
        worksheet.write(row, 0, item.date.strftime('%Y-%m-%d'))
        worksheet.write(row, 1, item.opening_balance)
        worksheet.write(row, 2, item.receive_from_rework)
        worksheet.write(row, 3, item.total_pass_qty)
        worksheet.write(row, 4, item.closing_balance)
        worksheet.write(row, 5, item.total_rejection_qty)
        worksheet.write(row, 6, item.defects)
        worksheet.write(row, 7, item.operator_signature)
        worksheet.write(row, 8, item.verified_by)
        worksheet.write(row, 9, item.month)
        worksheet.write(row, 10, item.stage)
        worksheet.write(row, 11, item.part_description)
    workbook.close()
    return response




# ----------------------------------------------------------------
#  scrren changes 

# View for listing all screens
def screen_list(request):
    screens = Screen.objects.all()
    return render(request, 'screen_list.html', {'screens': screens})

# View for displaying details of a specific screen
def screen_detail(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    return render(request, 'screen_detail.html', {'screen': screen})


# View for uploading PDF files associated with a screen
def upload_pdf(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    if request.method == 'POST':
        form = PDFFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.save(commit=False)
            pdf_file.screen = screen
            if screen.pdf_files.count() < 10:
                pdf_file.save()
                return redirect('view_pdf', screen_id=screen.screen_id)
            else:
                return HttpResponse("You can only upload a maximum of 10 PDF files per screen.")
    else:
        form = PDFFileForm()
    return render(request, 'upload_pdf.html', {'form': form, 'screen': screen})


# View for displaying PDF files associated with a screen
def view_pdf(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    pdf_files = screen.pdf_files.all()
    return render(request, 'view_pdf.html', {'screen': screen, 'pdf_files': pdf_files})


# View for the main navigation hub
def navigation_hub(request):
    return render(request, 'index.html')

# View for listing screens with PDF files
def screen_list_pdf(request):
    screens = Screen.objects.all()
    return render(request, 'screen_pdf_list.html', {'screens': screens})


# View for displaying a media slider with videos and PDFs from all screens
def media_slider(request):
    screens = Screen.objects.all()
    video_paths = []
    pdf_paths = []
    for screen in screens:
        if screen.video_path:
            video_paths.extend(screen.video_path.split(','))
        if screen.pdf_path:
            pdf_paths.extend(screen.pdf_path.split(','))
    return render(request, 'media_slider.html', {
        'video_paths': video_paths,
        'pdf_paths': pdf_paths,
    })



# ----------------------------------------------------------------


def upload_Media(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = form.save(commit=False)
            media_file.screen = screen
            if screen.media_files.count() < 10:
                media_file.save()
                return redirect('view_media', screen_id=screen.screen_id)
            else:
                return HttpResponse("You can only upload a maximum of 10 Media files per screen.")
    else:
        form = MediaFileForm()
    return render(request, 'upload_Media.html', {'form': form, 'screen': screen})



# View for displaying PDF files associated with a screen
def view_media(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    media_files = screen.media_files.all()
    return render(request, 'view_media.html', {'screen': screen, 'media_files': media_files})






from .models import UploadFile
from .forms import UploadFileForm
from screen_app.models import Screen

def upload_file(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = form.save(commit=False)
            upload_file.screen = screen
            upload_file.save()
            return redirect('view_uploaded_files', screen_id=screen_id)
    else:
        form = UploadFileForm()
    return render(request, 'upload_media/upload_file.html', {'form': form, 'screen': screen})

def view_uploaded_files(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    uploaded_files = screen.upload_files.all()
    return render(request, 'upload_media/view_uploaded_files.html', {'screen': screen, 'uploaded_files': uploaded_files})




def screen_videos_slider(request):
    screens = Screen.objects.all()  # Query to retrieve all screens (adjust as per your model)
    return render(request, 'screen_videos_slider.html', {'screens': screens})





# ----------------------------------------------------------------

# def per_screen_slider(request,screen_id):
#     screen = get_object_or_404(Screen, screen_id=screen_id)
#     media_files=UploadFile.objects.all();
#     video_paths=[]
#     pdf_paths=[]
#     for media_file in media_files:
#         if media_file.video_file:
#             video_paths.extend(media_file.video_file.split(','))
#         if media_file.pdf_file:
#             pdf_paths.extend(media_file.pdf_file.split(','))
#             return render(request, 'per_screen_slider.html', {
#         'video_paths': video_paths,
#         'pdf_paths': pdf_paths,
#         'screens':screen,
#     })

#  for video 

def per_screen_slider(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    media_files = UploadFile.objects.filter(screen=screen)
    
    video_paths = [media_file.video_file.url for media_file in media_files if media_file.video_file]
    video_durations = [media_file.video_duration for media_file in media_files if media_file.video_file]

    # Ensure video_paths and video_durations are of equal length
    assert len(video_paths) == len(video_durations), "Video paths and durations must match"

    # Create a list of dictionaries, each containing a video's path and duration
    video_items = [{'path': path, 'duration': duration} for path, duration in zip(video_paths, video_durations)]
    
    return render(request, 'per_screen_slider/video_slider.html', {
        'screen': screen,
        'video_items': video_items,
    })



def per_screen_slider2(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    media_files = UploadFile.objects.filter(screen=screen)

    video_paths = [media_file.video_file.url for media_file in media_files if media_file.video_file]
    pdf_paths = [media_file.pdf_file.url for media_file in media_files if media_file.pdf_file]

    # Set custom interval time (in milliseconds)
    mytime = 6000  # Example: 10 seconds

    return render(request, 'per_screen_slider/pdf_slider.html', {
        'screen': screen,
        'video_paths': video_paths,
        'pdf_paths': pdf_paths,
        'mytime': mytime,
    })







# ------------------------------------------------------------------------------------------------

from .models import addMultipleFiles, Screen
from .forms import addMultipleFilesForm

def add_multiple_files(request):
    if request.method == 'POST':
        form = addMultipleFilesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_multiple_files_list')  # Update this to the appropriate view name
    else:
        form = addMultipleFilesForm()
    return render(request, 'addmultiplefiles_form.html', {'form': form})



def add_multiple_files_detail(request, screen_id):
    # Fetch the addMultipleFiles instance with the given pk (primary key)
    files_instance = get_object_or_404(addMultipleFiles, screen_id=screen_id)
    
    # Assuming you want to include related PDF files as well
    pdf_files = files_instance.upload_pdf.all()  # Accessing related PDF files
    
    # Render the detail template with the instance and related PDF files
    return render(request, 'addmultiplefiles_detail.html', {'files_instance': files_instance, 'pdf_files': pdf_files})




from .models import mediaFile2

def slideshow_view(request, screen_id):
    # Fetch the screen object based on screen_id
    screen = get_object_or_404(addMultipleFiles, screen_id=screen_id)
    
    # Assuming 'upload_video' is the ManyToManyField related name for videos in 'addMultipleFiles'
    media_files = screen.upload_video.all()

    context = {
        'media_files': media_files,
        'screen_id': screen_id
    }
    return render(request, 'slideshow/slider.html', context)





def pdf_slideshow_view(request, screen_id):
    screen = get_object_or_404(Screen, screen_id=screen_id)
    screen_files = addMultipleFiles.objects.filter(screen=screen)
    
    pdf_files = []
    for screen_file in screen_files:
        pdf_files.extend(screen_file.upload_pdf.all())

    return render(request, 'slideshow/pdf_slideshow.html', {
        'pdf_files': pdf_files,
            'screen_id': screen_id

    })










