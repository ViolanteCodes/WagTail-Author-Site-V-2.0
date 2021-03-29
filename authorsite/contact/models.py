from django.conf import settings
from django.db import models
from django import forms
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render, redirect

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

class ContactForm(forms.Form):
    your_name = forms.CharField(max_length = 100)
    your_email = forms.EmailField()
    subject = forms.CharField(max_length = 100)
    your_message = forms.CharField(widget = forms.Textarea)
  
class ContactPage(Page):
    """A custom contact page with contact form."""
    body = RichTextField(blank=True)
    TEMPLATE_CHOICES = [
        ('base_dark.html', 'Dark'),
        ('base_light.html', 'Light')
    ]
    template_theme = models.CharField(
        max_length = 250,
        choices = TEMPLATE_CHOICES,
        default = 'Dark', 
        help_text = """
        Choose dark theme to match main site and light theme
        to match light site."""
    )
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('template_theme'),
    ]
    subpage_types = ['contact.ContactSuccessPage']
    parent_page_types = ['home.HomePage', 'home.FanSiteHomePage']

    def serve(self, request):
        if request.method == 'GET':
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                # Clean the data
                senders_name = form.cleaned_data['your_name']
                senders_email = form.cleaned_data['your_email']
                message_subject = form.cleaned_data['subject']
                message = form.cleaned_data['your_message']
                site_name = settings.WAGTAIL_SITE_NAME
                to_email = settings.CONTACT_EMAIL
                #Process the form info to get it ready for send_mail
                subject_line = f"""New message from {site_name} contact form: {message_subject}"""
                message_body = f"""You have received the following message from your website, {site_name}:
                \n\n 
                Sender's Name: {senders_name}
                \n\n
                Sender's Email: {senders_email} 
                \n\n
                Subject: {message_subject} 
                \n\n
                Message Body: {message}"""
                # And send                
                try:
                    send_mail(subject_line, message_body, senders_email, [to_email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                success_pages = self.get_specific().get_children()
                for success in success_pages:
                    return redirect(success.specific.url) 
        return render(request, 'contact/contact_page.html', {
            'page':self,
            'form':form,
            'template_theme':self.template_theme,
            })

class ContactSuccessPage(Page):
    """A redirection page for successful email sendings."""
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    parent_page_types = ['contact.ContactPage']
    subpage_types = []

    def template_theme(self):
        """A custom function to get the template theme from parent page."""
        parent_page = self.get_parent()
        parent_theme = parent_page.specific.template_theme
        return parent_theme

class MailChimpPage(Page):
    """A signup form for mailchimp."""
    description = RichTextField()
    form_action = models.CharField(max_length=250)
    mailchimp_id = models.CharField(max_length=250)
    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        FieldPanel('form_action', classname="full"),
        FieldPanel('mailchimp_id', classname="full"),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []
