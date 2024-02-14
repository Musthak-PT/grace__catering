from Crypto.Cipher import AES
# import base64
# from Crypto.Util.Padding import pad
# from Crypto.Util.Padding import unpad
import threading
from solo_core import settings
from Crypto.Cipher import AES
import binascii
from solo_core.helpers.mail_fuction import SendBulkEmailsSend
from solo_core.helpers.signer import URLEncryptionDecryption
import logging
logger = logging.getLogger(__name__)
# Assuming 'key' is defined somewhere in your code

def pad(data, block_size):
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding

def unpad(data, block_size):
    padding_len = data[-1]
    return data[:-padding_len]

# """------------------------------ PROMOTION EMAIL SEND ---------------------------------------------"""

key = b'B4VK5NGB?m*Y5(#knHAx^9Jas[*=&g;V'

def encrypt_email(email):
    print("3333333333333333333333333333333333", email)
    email_bytes = email.encode('utf-8')
    pad_len = 16 - len(email_bytes) % 16
    padded_email = pad(email_bytes, 16)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_email = cipher.encrypt(padded_email)
    iv = cipher.iv
    ciphertext = iv + encrypted_email
    hex_ciphertext = binascii.hexlify(ciphertext).decode('utf-8')
    return hex_ciphertext


def decrypt_email(encrypted_email):
    encrypted_email_bytes = binascii.unhexlify(encrypted_email.encode('utf-8'))
    iv = encrypted_email_bytes[:16]  # Extract IV from ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_email_bytes = cipher.decrypt(encrypted_email_bytes[16:])
    decrypted_email = unpad(decrypted_email_bytes, AES.block_size).decode('utf-8')
    return decrypted_email

"""============Promotion=============="""

def promotion_mail_send(request, instance, user_emails):
    print("11111111111111111111111111111111111111", user_emails)
    if user_emails:
        encrypted_emails = [encrypt_email(email[0]) for email in user_emails]
        email_map = dict(zip(map(tuple, user_emails), encrypted_emails))
        user_encrypted_emails = email_map.get(tuple(user_emails[0]))
        

        
        subject = instance.subject
        
        context = {
            "blog_id"             : instance.slug,
            "title"               : instance.title,
            "subject"             : instance.subject,
            "message"             : instance.message,
            "promotion_image"     : request.build_absolute_uri(instance.image.url),
            "email"               : user_emails,
            "email_map"           : user_encrypted_emails,
            'domain'              : settings.EMAIL_DOMAIN,
            'protocol'            : 'https',
        }
        send_email = SendBulkEmailsSend()
        x = threading.Thread(target=send_email.sendBulkEmailSend, args=(subject, request, context, 'admin/email/promotion/promotion_mail.html', settings.EMAIL_HOST_USER, user_emails, email_map))
        x.start()


def auto_review_mail_send(instance):
    user_emails           = [user.booked_price.customer_details.email_address for user in instance]
    logger.info(f"Transcript Data: {instance}")
    user_booked_obj       = [user for user in instance]
    
    try:
        if user_emails :
            logger.info(f"Transcript Data: {user_emails}")
            encrypted_emails = [encrypt_email(email) for email in user_emails]
            email_map = dict(zip(user_emails, encrypted_emails))
            user_encrypted_emails = list(email_map.values())[0]
            result_dict = {email: (encrypted_email, booking_id) for email, encrypted_email, booking_id in zip(user_emails, encrypted_emails, user_booked_obj)}
            subject = "review"
            
            context = {
                "blog_id"             : instance,
                "title"               : 'This is Review Mail',
                "email"               : user_emails,
                "email_map"           : result_dict,
                'domain'              : settings.EMAIL_DOMAIN,
                'protocol'            : 'https',
            }
            
            send_email = SendBulkEmailsSend()
            x = threading.Thread(target=send_email.sendBulkReviewEmailSend, args=(subject, context, 'admin/email/review-email/review-email.html', settings.EMAIL_HOST_USER, user_emails, result_dict))
            
            x.start()
    except Exception as e:
        logger.info(f"Transcript Data: >>>>>>>>>>>>>>>>>>>>>>", e)