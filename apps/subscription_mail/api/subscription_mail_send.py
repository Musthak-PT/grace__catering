import threading
from solo_core import settings
from solo_core.helpers.mail_fuction import SendEmails

##Subscription mail sending start
def subscription_mail_send(request, instance):
    try:
        user_email = instance.subscribers_email,
        subject = "Subscription verification From SOLO "
        context = {
            'subscribers_email'   : instance.subscribers_email,
            'email'               : instance.subscribers_email,
            'domain'              : settings.EMAIL_DOMAIN,
            'protocol'            : 'https',
        }

        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/subscription/subscription_mail.html', settings.EMAIL_HOST_USER, user_email))
        x.start()
    except Exception as es:
        pass
#End
