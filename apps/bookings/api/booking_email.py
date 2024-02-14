from solo_core import settings
import threading
from solo_core.helpers.mail_fuction import SendEmails


def booking_confirmed_mail_send(request, user_instances, room_instances, check_in, check_out, assigned_user_email):
    try:
        user_email = user_instances.email_address,
        subject = "This is From SOLO"
        context = {
            'full_name'           : user_instances.full_name,
            'email_type'          : '1',
            'phone_number'        : user_instances.mobile_number,
            'customer_email'      : user_instances.email_address,
            'email'               : assigned_user_email,
            'room_instances'      : room_instances,
            'total_price'         : user_instances.total_booked_price,
            # 'room_count'          : total_quantity,
            'check_in'            : check_in.strftime("%A, %B %d, %Y"),
            'check_out'           : check_out.strftime("%A, %B %d, %Y"),
            'domain'              : settings.EMAIL_DOMAIN,
            'protocol'            : 'https',
        }
        
        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/booking_confirm_email/booking_confirm_email.html', user_email, settings.EMAIL_HOST_USER))
        x.start()
    except Exception as es:
        pass
    
    
def booking_confirmed_mail_send_customer(request, user_instances, room_instances, check_in, check_out, assigned_user_email):
    try:        
        user_email = user_instances.email_address,
        subject = "This is From SOLO"
        context = {
            'email_type'          : '2',
            'full_name'           : user_instances.full_name,
            'phone_number'        : user_instances.mobile_number,
            'customer_email'      : user_instances.email_address,
            'email'               : assigned_user_email,
            'room_instances'      : room_instances,
            'total_price'         : user_instances.total_booked_price,
            # 'room_count'          : total_quantity,
            'check_in'            : check_in.strftime("%A, %B %d, %Y"),
            'check_out'           : check_out.strftime("%A, %B %d, %Y"),
            'domain'              : settings.EMAIL_DOMAIN,
            'protocol'            : 'https',
        }
        
        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/booking_confirm_email/booking_confirm_email.html', user_email, settings.EMAIL_HOST_USER))
        x.start()
    except Exception as es:
        pass
    
def manual_booking_confirmed_mail_send_customer(request, user_instances, room_instances, check_in, check_out, assigned_user_email):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", room_instances)
    try:        
        user_email = user_instances.email_address,
        subject = "This is From SOLO"
        context = {
            'email_type'          : '2',
            'full_name'           : user_instances.full_name,
            'phone_number'        : user_instances.mobile_number,
            'customer_email'      : user_instances.email_address,
            'email'               : assigned_user_email,
            'room_instances'      : room_instances,
            'total_price'         : user_instances.total_booked_price,
            # 'room_count'          : total_quantity,
            'check_in'            : check_in.strftime("%A, %B %d, %Y"),
            'check_out'           : check_out.strftime("%A, %B %d, %Y"),
            'domain'              : settings.EMAIL_DOMAIN,
            'protocol'            : 'https',
        }
        
        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin\email\booking_confirm_email\manual_booking_confirmation_email.html', user_email, settings.EMAIL_HOST_USER))
        x.start()
    except Exception as es:
        pass