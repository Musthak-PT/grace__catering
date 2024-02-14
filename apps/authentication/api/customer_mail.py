import threading
from solo_core import settings
from solo_core.helpers.mail_fuction import SendEmails

#Registeration mail sending start
def customer_registeration_mail_send(request, instance):
    try:
        user_email = instance.email,
        subject = "This is From SOLO"
        context = {
            'full_name'           : instance.full_name,
            'email'               : instance.email,
            'domain'              : settings.EMAIL_DOMAIN,
            'protocol'            : 'https',
        }

        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/customer/customer_registeration.html', settings.EMAIL_HOST_USER, user_email))
        x.start()
    except Exception as es:
        pass
#End