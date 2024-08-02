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

        # Subject can be adjusted (adding submitted date), be sure to include the form's defined subject field
        submitted_date_str = date.today().strftime('%x')
        subject = f"Your registration has been received - {submitted_date_str}"
        
        # Update the original landing page context with other data
        context = super().get_context_data(**kwargs)

        contact = {
            'First name': form.cleaned_data['first_name'],
            'Last name': form.cleaned_data['last_name'],
            'Company': form.cleaned_data['company'],
            'Position': form.cleaned_data['position'],
        }
        context['user_unique_id'] = form.cleaned_data['user_unique_id']
        context['first_name'] = form.cleaned_data['first_name']
        context['last_name'] = form.cleaned_data['last_name']
        context['company'] = form.cleaned_data['company']
        context['position'] = form.cleaned_data['position']
        context['contact'] = contact

        text_content  = '\n' + '\n' + 'Hi,' + '\t' + str(form.cleaned_data['first_name']) + '\n' + '\n' +'\n'
        html_content = render_to_string('registration/email_header.html', context, request=self.request) + text_content + render_to_string('registration/visitor_email_template.html', context, request=self.request)

        msg = EmailMultiAlternatives(subject, text_content, ['v.eroli@fleissen.com', 'lekiaprosper@gmail.com',]+[form.cleaned_data['email']])
        # msg.content_subtype = "html"  # Main content is now text/html
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        instance = form.save(commit=False)
        # Customize any additional processing if needed
        instance.save()
        # Redirect to the landing page with the submitted form data
        return HttpResponseRedirect(reverse_lazy('registration:visitor-card', kwargs={'pk': instance.pk}))
    
class AttendantListView(ListView):
    model = Attendant
    template_name = 'registration/attendant_list.html'
    context_object_name = 'attendants'
    paginate_by = 50