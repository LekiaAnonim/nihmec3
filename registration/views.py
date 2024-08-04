from django.shortcuts import render
from registration.models import Attendant
from registration.forms import AttendantForm
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from datetime import date
# from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from home.models import HomePage
import base64
import qrcode
import io
from email.mime.image import MIMEImage
# Create your views here.
class AttendantDetail(DetailView):
    model = Attendant
    template_name = 'registration/attendant_detail.html'

def generate_qr_code(data, size=10, border=0):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=size, border=border)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image()
class AttendantCreateView(CreateView):
    model = Attendant
    template_name = 'registration/visitor_registration.html'
    form_class = AttendantForm
    redirect_field_name = "redirect_to"

    def get_context_data(self, *args, **kwargs):
        context = super(AttendantCreateView,
                        self).get_context_data(**kwargs)
        return context
    
    def form_valid(self, form, *args, **kwargs):

        instance = form.save(commit=False)
        # Customize any additional processing if needed
        instance.save()
        # Save the form instance first
        self.object = form.save()
        self.send_email(self.object)
        # Redirect to the landing page with the submitted form data
        return HttpResponseRedirect(reverse_lazy('registration:visitor-card', kwargs={'pk': instance.pk}))
    
    def send_email(self, instance):
         # Subject can be adjusted (adding submitted date), be sure to include the form's defined subject field
        submitted_date_str = date.today().strftime('%x')
        subject = f"Your registration has been received - {submitted_date_str}"
        qr_img = generate_qr_code(instance.user_unique_id)
        
        buffered = io.BytesIO()
        qr_img.save(buffered, format="PNG")
        qr_img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        home = HomePage.objects.get()
        context = {
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'company': instance.company,
            'position': instance.position,
            'user_unique_id': instance.user_unique_id,
            'home': home,
            "qr_image": qr_img_base64,
        }

        text_content  = '\n' + '\n' + 'Hi,' + '\t' + str(instance.first_name) + '\n' + '\n' +'\n'
        html_content = render_to_string('registration/email_header.html', context) + text_content + render_to_string('registration/visitor_email_template.html', context)

        msg = EmailMultiAlternatives(subject, text_content, 'v.eroli@fleissen.com', [instance.email,'v.eroli@fleissen.com', 's.kanshio@fleissen.com'])
        # msg.content_subtype = "html"  # Main content is now text/html
        msg.mixed_subtype = 'related'
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
class AttendantListView(ListView):
    model = Attendant
    template_name = 'registration/attendant_list.html'
    context_object_name = 'attendants'