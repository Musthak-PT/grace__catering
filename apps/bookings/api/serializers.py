from datetime import datetime
from rest_framework import serializers
from django.db.models import Q
from apps.offer.models import PropertyOffer
from ..models import BookingPrice, HotelRoomBooking, HotelRoomBookingBookingPrice, RoomBookedCustomerDetails
from apps.property_management.models import HotelRoom, PropertyManagementHotelRoom
from .booking_email import booking_confirmed_mail_send, booking_confirmed_mail_send_customer
from apps.users.models import Users

class RoomBooConfirmationSerializer(serializers.Serializer):
    room_id             = serializers.PrimaryKeyRelatedField(queryset=HotelRoom.objects.all())
    quantity            = serializers.IntegerField(required=True)
    adults              = serializers.IntegerField(required=False)
    childrens           = serializers.IntegerField(required=False)
    
class BookingConfirmationSerializer(serializers.Serializer):
    check_in            = serializers.DateField(required=False)
    check_out           = serializers.DateField(required=False)
    bookingdetails      = RoomBooConfirmationSerializer(required=False, many=True)
    full_name           = serializers.CharField(required=False)
    email_address       = serializers.CharField(required=False)
    mobile_number       = serializers.CharField(required=False)
    
    

    class Meta:
        model = HotelRoomBooking
        fields = ['check_in', 'check_out', 'bookingdetails', 'full_name', 'email_address', 'mobile_number', 'adults', 'childrens']
        
    def validate(self, attrs):
        return attrs

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        request = self.context.get('request')
        booking_details = validated_data.pop('bookingdetails', [])
        check_in = validated_data.get('check_in')
        check_out     = validated_data.get('check_out')
        full_name     = validated_data.get('full_name')
        email_address = validated_data.get('email_address')
        mobile_number = validated_data.get('mobile_number')
        user_instances = RoomBookedCustomerDetails(full_name = full_name, email_address=email_address, mobile_number=mobile_number, is_enquired=True)
        user_instances.save()
        
        total_room_price_list = []
        room_obj_list = []
        for item in booking_details:
            room_row = HotelRoom.objects.filter(id=item['room_id'].id).first()
            room_obj = HotelRoomBooking(room_id_id   = item['room_id'].id,
                                        # quantity  = item['no_of_rooms'],
                                        check_in  = check_in,
                                        check_out = check_out,
                                        adults    = item['adults'],
                                        childrens = item['childrens']
                                        )

            offer_obj = PropertyOffer.objects.filter(Q(room_property__hotel_room=room_row) & Q(start_date__lte=check_in) & Q(end_date__gte=check_out)).first()
            num_days  = (check_out - check_in).days  if (check_out - check_in).days > 0 else 1
            actual_price = int(room_row.price) * num_days
            if offer_obj:
                actual_price = int((actual_price - (actual_price * (int(offer_obj.offer_percentage) / 100))))
            total_room_price_list.append(actual_price)
            room_obj.booked_room_price = str(actual_price)
            room_obj.save()
            room_obj_list.append(room_obj.id)
            
        booking_price = BookingPrice.objects.create(
            total_booked_price=sum(total_room_price_list),
            is_paid=False,
            is_enquiry=True,
            customer_details = user_instances
        )

        HotelRoomBookingBookingPrice.objects.bulk_create([
            HotelRoomBookingBookingPrice(booked_room_id=room, booked_price=booking_price)
            for room in room_obj_list
        ])
        assigned_user_email = PropertyManagementHotelRoom.objects.filter(
            hotel_room_id=booking_details[0]['room_id'].id).first()
        assigned_user_email = assigned_user_email.property_management.assigned_to.email
        booking_confirmed_mail_send(request, user_instances, booking_details, check_in, check_out,
                                    assigned_user_email)
        booking_confirmed_mail_send_customer(request, user_instances, booking_details, check_in, check_out,
                                    email_address)
        return booking_details

    # def create(self, validated_data):
    #     request           = self.context.get('request')
    #     booking_details   = validated_data.pop('bookingdetails', [])
    #     check_in          = validated_data.get('check_in')
    #     check_out         = validated_data.get('check_out')
    #     full_name         = validated_data.get('full_name')
    #     email_address     = validated_data.get('email_address')
    #     mobile_number     = validated_data.get('mobile_number')

        
        
    #     user_instance = Users(
    #                 full_name = full_name,
    #                 email = email_address,
    #                 phone = mobile_number,
    #                 user_type='3',
    #             )
    #     user_instance.save()

    #     user_instances.save()
        
    #     for room in booking_details:
    #         room_row = HotelRoomBooking(room_id   = room['room_id'],
    #                                         quantity  = room['quantity'],
    #                                         check_in  = check_in,
    #                                         check_out = check_out,
    #                                         customer_details = user_instance,
    #                                         adults = room['adults'],
    #                                         childrens = room['childrens'])
    #         room_row.save()
            
    #     total_quantity = sum(item['quantity'] for item in booking_details)
    #     assigned_user_email   = PropertyManagementHotelRoom.objects.filter(hotel_room_id=booking_details[0]['room_id'].id).first().property_management.assigned_to.email
    #     booking_confirmed_mail_send(request, user_instance, booking_details, check_in, check_out, total_quantity, assigned_user_email)
    #     return booking_details