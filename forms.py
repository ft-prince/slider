from django import forms
from .models import Screen

class ScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ['video_path', 'pdf_path']  # Include the file path fields you want to customize

    def __init__(self, *args, **kwargs):
        super(ScreenForm, self).__init__(*args, **kwargs)
        # Customize the file path fields here if needed
        
# ---------------------------------------------------------------

from .models import Videos, Pdf ,Slider


class VideoForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = '__all__'

class PdfForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = '__all__'

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['name', 'upload_pdf', 'upload_video']


# ---------------------------------------------------------------

from .models import DailyProductionPlan, Unit ,ProductionPlan

class DailyProductionPlanForm(forms.ModelForm):
    class Meta:
        model = ProductionPlan
        fields = ['unit', 'qty_planned', 'qty_actual', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.all()
        self.fields['unit'].widget.attrs.update({'onchange': 'updateUnitModel(this.value)'})


class DailyProductionPlanForm2(forms.ModelForm):
    class Meta:
        model = DailyProductionPlan
        fields = ['unit', 'qty_planned', 'qty_actual', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.all()
        self.fields['unit'].widget.attrs.update({'onchange': 'updateUnitModel(this.value)'})
