#from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100)
    status_choices = [
        ('RUNNING', 'Running'),
        ('STOPPED', 'Stopped'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='STOPPED')

    def __str__(self):
        return self.name


class Screen(models.Model):
    screen_id = models.AutoField(primary_key=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video_path = models.CharField(max_length=100, null=True, blank=True)
    pdf_path = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Screen {self.screen_id} at {self.manager} for {self.product}"
    


# ---------------------------------------------------------------------------------------------------
class Videos(models.Model):
    duration=models.IntegerField(default=120,help_text='Duration of video in seconds ')
    video_file = models.FileField(upload_to='static/media/Videos/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    video_name = models.CharField(max_length=100,default='TA100-70020' ,help_text="Name of Media file")
    def __str__(self):
        return self.video_name

 
class Pdf(models.Model):
    pdf_name = models.CharField(max_length=100,default='TA100-70020' ,help_text="Name of PDF file")    
    pdf_duration = models.IntegerField(default=80,help_text="Duration of pdf in seconds")
    pdf_file = models.FileField(upload_to='static/media/Pdf_files/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.pdf_name
   

class Slider(models.Model):
    screen = models.AutoField(primary_key=True)    
    name = models.CharField(max_length=100, null=True, blank=True)
    upload_pdf = models.ManyToManyField(Pdf, blank=True)
    upload_video = models.ManyToManyField(Videos, blank=True)
    
    def __str__(self):
        return self.name or f"Screen {self.screen}"    
# --------------------------------------------------------------------------------------------------- 
#  DailyProductionPlan
# from django.db import models

# class ProductionPlan(models.Model):
#     date = models.DateField(auto_now_add=True)
#     unit_code = models.CharField(max_length=20)
#     unit_model = models.CharField(max_length=100)
#     qty_planned = models.IntegerField()
#     qty_actual = models.IntegerField()
#     remarks = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.date} - {self.unit_model}"

#     class Meta:
#         verbose_name = "Production Plan"
#         verbose_name_plural = "Production Plans"
        
    
# class DailyProductionPlan(models.Model):
#     date = models.DateField(auto_now_add=True)
#     s_no = models.AutoField(primary_key=True)
#     unit_code = models.CharField(max_length=20)
#     unit_model = models.CharField(max_length=100)
#     qty_planned = models.IntegerField()
#     qty_actual = models.IntegerField()
#     remarks = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.date} - {self.unit_model}"

#     class Meta:
#         verbose_name = "Daily Production Plan"
#         verbose_name_plural = "Daily Production Plans"
#         ordering = ['date', 's_no']


class Unit(models.Model):
    code = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.model}"

# Daily Production Plan Vs Actual
class DailyProductionPlan(models.Model):
    s_no = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty_planned = models.IntegerField()
    qty_actual = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.unit.model}"

    class Meta:
        verbose_name = "Daily Production Plan Vs Actual Total"
        verbose_name_plural = "Daily Production Plan Vs Actual Total"
        ordering = ['date', 's_no']


# ----------------------------------------------------------------
class AssemblyLine(models.Model):
    line_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Assembly Line {self.line_number}"


# Daily Production Plan Vs Actual 
class ProductionPlan(models.Model):
    s_no = models.AutoField(primary_key=True)    
    date = models.DateField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    qty_planned = models.IntegerField()
    qty_actual = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.unit.model}"

    class Meta:
        verbose_name = "Daily Production Plan Vs Actual LineWise"
        verbose_name_plural = "Daily Production Plan Vs Actual Total LineWise"        
        
        


#Rolling Weekly Production Plan

class TentativePlan(models.Model):
    Date1= models.DateField(auto_now_add=True)
    Date2= models.DateField(auto_now_add=True)
    Date3= models.DateField(auto_now_add=True)
    qty_planned1 = models.IntegerField()
    qty_planned2 = models.IntegerField()
    qty_planned3 = models.IntegerField()
    


class FreezedPlanDate(models.Model):
    Date1= models.DateField(auto_now_add=True)
    Date2= models.DateField(auto_now_add=True)
    Date3= models.DateField(auto_now_add=True)
    qty_planned1 = models.IntegerField()
    qty_planned2 = models.IntegerField()
    qty_planned3 = models.IntegerField()
    
 
class RollingProduction(models.Model):
    s_no = models.AutoField(primary_key=True)   
    date = models.DateField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    remarks = models.TextField(blank=True, null=True)
    plant=models.TextField(blank=True, null=True)
      


from django.db import models

class Unit(models.Model):
    code = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.model}"

class Plan(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    plan_type = models.CharField(max_length=10, choices=[('Freezed', 'Freezed'), ('Tentative', 'Tentative')])

class PlanDetail(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    date = models.DateField()
    qty_planned = models.IntegerField()

class RollingProduction(models.Model):
    s_no = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    remarks = models.TextField(blank=True, null=True)
    plant = models.CharField(max_length=50, blank=True, null=True)  # Assuming plant is a text field
     