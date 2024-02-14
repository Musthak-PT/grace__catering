import threading
from solo_core import settings
from solo_core.helpers.mail_fuction import SendEmails

#be a partner start
def be_a_partner_form_submits_mail_send(request, instance):
    try:
        admin_email = settings.ADMIN_MAIL
        subject = "Be a Partner Enquiry From " + instance.name
        
        context = {
            'enquiry_type'  : instance.enquiry_type,
            'email'         : admin_email,
            'name'          : instance.name,
            'user_email'    : instance.email,
            'mobile_number' : instance.mobile_number,
            'state'         : instance.state,
            'domain'        : settings.EMAIL_DOMAIN,
            'protocol'      : 'https',
        }

        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/contact-us-enquiry/contact_us.html', settings.EMAIL_HOST_USER, admin_email))
        x.start()
    except Exception as es:
        pass
#End
#contact-us start
def contact_us_form_submits_mail_send(request, instance):
    try:
        admin_email = settings.ADMIN_MAIL
        subject = "Contact Us Enquiry From " + instance.name
        context = {
            'enquiry_type'  : instance.enquiry_type,
            'email'         : admin_email,
            'name'          : instance.name,
            'user_email'    : instance.email,
            'message'       : instance.message,
            'domain'        : settings.EMAIL_DOMAIN,
            'protocol'      : 'https',
        }

        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/contact-us-enquiry/contact_us.html', settings.EMAIL_HOST_USER, admin_email))
        x.start()
    except Exception as es:
        pass
#End

