from django.shortcuts import render
from registration.models import Attendant, RegistrationType
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

# Create your views here.
class AttendantDetail(DetailView):
    model = Attendant
    template_name = 'registration/attendant_detail.html'
class AttendantCreateView(CreateView):
    model = Attendant
    template_name = 'registration/visitor_registration.html'
    form_class = AttendantForm
    redirect_field_name = "redirect_to"

    def get_context_data(self, *args, **kwargs):
        context = super(AttendantCreateView,
                        self).get_context_data(**kwargs)
        registration_type = RegistrationType.objects.all()

        context['registration_type'] = registration_type
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
        context = {
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'company': instance.company,
            'position': instance.position,
            'user_unique_id': instance.user_unique_id
        }

        text_content  = '\n' + '\n' + 'Hi,' + '\t' + str(instance.first_name) + '\n' + '\n' +'\n'
        html_content = render_to_string('registration/email_header.html', context, request=self.request) + text_content + render_to_string('registration/visitor_email_template.html', context, request=self.request)

        msg = EmailMultiAlternatives(subject, text_content, 'v.eroli@fleissen.com', [instance.email,'v.eroli@fleissen.com', 's.kanshio@fleissen.com'])
        # msg.content_subtype = "html"  # Main content is now text/html
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
class AttendantListView(ListView):
    model = Attendant
    template_name = 'registration/attendant_list.html'
    context_object_name = 'attendants'