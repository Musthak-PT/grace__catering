from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers
from apps.property_management.models import *
from datetime import timedelta
from ...bookings.api.booking_email import booking_confirmed_mail_send
from apps.bookings.models import RoomBookedCustomerDetails, HotelRoomBooking
class PropertyFilteringSerializer(serializers.Serializer):
    room_type               = serializers.ListField(child=serializers.IntegerField(),required = False)
    minimum_price           = serializers.CharField(required = False)
    maximum_price           = serializers.CharField(required = False)
    place                   = serializers.CharField(required = False)
    property_facility_id    = serializers.ListField(child=serializers.IntegerField(),required = False)
    accomadation_type       = serializers.ListField(child=serializers.IntegerField(),required = False)
    collection_type         = serializers.ListField(child=serializers.IntegerField(),required = False)
    sorting_type            = serializers.CharField(required = False)
    check_in                = serializers.DateField(required = False)
    check_out               = serializers.DateField(required = False)
    search                  = serializers.CharField(required = False)
#Room selection serializer
class RoomSelectionSerializer(serializers.Serializer):
    property                = serializers.PrimaryKeyRelatedField(queryset=PropertyManagement.objects.all(),required=True)
    room_type               = serializers.PrimaryKeyRelatedField(queryset=RoomType.objects.all(),required=False)
    check_in                = serializers.DateField(required = False)
    check_out               = serializers.DateField(required = False)
    full_name               = serializers.CharField(required=False)
    
#Room booking
class RoomBookSerializer(serializers.Serializer):
    room_id = serializers.PrimaryKeyRelatedField(queryset=HotelRoom.objects.all())
    quantity = serializers.IntegerField(required=True)


class RoomBookingSerializer(serializers.Serializer):
    check_in            = serializers.DateField(required=False)
    check_out           = serializers.DateField(required=False)
    bookingdetails      = RoomBookSerializer(required=False, many=True)
    full_name           = serializers.CharField(required=False)
    email_address       = serializers.CharField(required=False)
    mobile_number       = serializers.CharField(required=False)
    
    def validate(self, attrs):
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        booking_details = attrs.get('bookingdetails', [])

        for booking_detail in booking_details:
            room_id_query   = booking_detail.get('room_id')
            quantity        = booking_detail.get('quantity', 0)
            
            # Filter HotelRoomBooking for the selected room, check_in, and check_out

            existing_bookings = HotelRoomBooking.objects.filter(
                Q(room_id=room_id_query) if room_id_query else Q(),
                Q(check_in__lte=check_out) & Q(check_out__gte=check_in)
            )
            # Exclude the current booking if updating an existing record
            instance = self.instance
            if instance and instance.id:
                existing_bookings = existing_bookings.exclude(id=instance.id)

            # Check if there are any existing bookings
            if existing_bookings is not None:
                # Calculate the total quantity of existing bookings for the selected room
                total_quantity = existing_bookings.aggregate(models.Sum('quantity'))['quantity__sum'] or 0
                # Check if the total quantity, including the current booking, exceeds the room_count
                room = HotelRoom.objects.get(id=room_id_query.id)
                room_count = int(room.room_count)
                if total_quantity + quantity > room_count:
                    raise serializers.ValidationError(f"Not enough rooms available for {room.room_type}.")
            else:
                # Handle the case where existing_bookings is None (no existing bookings)
                pass
            
        return attrs

    class Meta:
        model = HotelRoomBooking
        fields = ['check_in', 'check_out', 'bookingdetails']


    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        request           = self.context.get('request')
        booking_details   = validated_data.pop('bookingdetails', [])
        check_in          = validated_data.get('check_in')
        check_out         = validated_data.get('check_out')
        full_name         = validated_data.get('full_name')
        email_address     = validated_data.get('email_address')
        mobile_number     = validated_data.get('mobile_number')

        user_instance = RoomBookedCustomerDetails(
                    full_name=full_name,
                    email_address=email_address,
                    mobile_number=mobile_number,
                )
        user_instance.save()
        instances = []
        
        with transaction.atomic():
            tot_price = 0
            for booking_detail in booking_details:
                room_id = booking_detail.get('room_id')
                room_quantity = booking_detail.get('quantity')

                room = HotelRoom.objects.get(pk=room_id.pk)
                actual_price = int(room.price)

                property_room = PropertyManagementHotelRoom.objects.filter(hotel_room=room).first()
                
                if property_room:
                    property_offer = PropertyOffer.objects.filter(
                        room_property=property_room,
                        start_date__lte=check_in,
                        end_date__gte=check_in
                    ).first()

                    if property_offer:
                        offer_percentage = int(property_offer.offer_percentage)
                    else:
                        offer_percentage = 0

                    num_days = (check_out - check_in).days
                    actual_price = int(actual_price * num_days)
                    offer_price = int((actual_price - (actual_price * (offer_percentage / 100))))
                else:
                    offer_price = int(actual_price)
                tot_price += offer_price
                if request.user.is_authenticated:
                    instance = HotelRoomBooking(
                        room_id=room,
                        check_in=check_in,
                        check_out=check_out,
                        quantity=room_quantity,
                        actual_price=actual_price,
                        offer_price=offer_price,
                        created_by_id=request.user.id,
                        customer_details=user_instance
                    )

                instance.save()
                instances.append(instance)
            user_instance.total_booked_price = str(tot_price)
            user_instance.save()
        booking_confirmed_mail_send(request, user_instance, instances)
        return instances
#End room booking

class MyBookingPropertiesDetailedSerializer(serializers.Serializer):
    room_booked_details = serializers.PrimaryKeyRelatedField(queryset=RoomBookedCustomerDetails.objects.all())

class HotelRoomBookingSerializer(serializers.Serializer):
    bookingdetails      = RoomBookSerializer(required=False, many=True)
    check_in            = serializers.DateField(required=False)
    check_out           = serializers.DateField(required=False)



# class BookingConfirmationSerializer(serializers.Serializer):
#     check_in            = serializers.DateField(required=False)
#     check_out           = serializers.DateField(required=False)
#     bookingdetails      = RoomBookSerializer(required=False, many=True)
#     full_name           = serializers.CharField(required=False)
#     email_address       = serializers.CharField(required=False)
#     mobile_number       = serializers.CharField(required=False)
    
#     def validate(self, attrs):
#         check_in = attrs.get('check_in')
#         check_out = attrs.get('check_out')
#         booking_details = attrs.get('bookingdetails', [])

#         for booking_detail in booking_details:
#             room_id_query   = booking_detail.get('room_id')
#             quantity        = booking_detail.get('quantity', 0)
            
#             # Filter HotelRoomBooking for the selected room, check_in, and check_out

#             existing_bookings = HotelRoomBooking.objects.filter(
#                 Q(room_id=room_id_query) if room_id_query else Q(),
#                 Q(check_in__lte=check_out) & Q(check_out__gte=check_in)
#             )
#             # Exclude the current booking if updating an existing record
#             instance = self.instance
#             if instance and instance.id:
#                 existing_bookings = existing_bookings.exclude(id=instance.id)

#             # Check if there are any existing bookings
#             if existing_bookings is not None:
#                 # Calculate the total quantity of existing bookings for the selected room
#                 total_quantity = existing_bookings.aggregate(models.Sum('quantity'))['quantity__sum'] or 0
#                 # Check if the total quantity, including the current booking, exceeds the room_count
#                 room = HotelRoom.objects.get(id=room_id_query.id)
#                 room_count = int(room.room_count)
#                 if total_quantity + quantity > room_count:
#                     raise serializers.ValidationError(f"Not enough rooms available for {room.room_type}.")
#             else:
#                 # Handle the case where existing_bookings is None (no existing bookings)
#                 pass
            
#         return attrs

#     class Meta:
#         model = HotelRoomBooking
#         fields = ['check_in', 'check_out', 'bookingdetails']


#     def validate(self, attrs):
#         return super().validate(attrs)

#     def create(self, validated_data):
#         request           = self.context.get('request')
#         booking_details   = validated_data.pop('bookingdetails', [])
#         check_in          = validated_data.get('check_in')
#         check_out         = validated_data.get('check_out')
#         full_name         = validated_data.get('full_name')
#         email_address     = validated_data.get('email_address')
#         mobile_number     = validated_data.get('mobile_number')

#         user_instance = RoomBookedCustomerDetails(
#                     full_name=full_name,
#                     email_address=email_address,
#                     mobile_number=mobile_number,
#                 )
#         user_instance.save()
#         date_difference = (check_out - check_in).days
#         total_booking_price = 0
#         room_list = []
#         for room in booking_details:
            
#             offer_obj = PropertyOffer.objects.filter(Q(room_property__hotel_room=room['room_id']) & Q(end_date__gte=check_in) & Q(start_date__lte=check_out))
#             if offer_obj:
#                 total_cost = int(room['room_id'].price) - (int(room['room_id'].price) * (int(offer_obj.first().offer_percentage)/100))
#                 total_cost = total_cost * int(room['quantity']) * date_difference
#             else:
#                 total_cost = int(room['room_id'].price) * int(room['quantity']) * date_difference
#             instance = HotelRoomBooking(
#                     room_id = room['room_id'],
#                     quantity = room['quantity'],
#                     actual_price=room['room_id'].price,
#                     offer_price=total_cost,
#                     created_by_id=request.user.id,
#                     customer_details=user_instance,
#                     check_in = check_in,
#                     check_out = check_out,
#                 )
#             room_list.append(instance)
#             instance.save()
#             total_booking_price += total_cost
#         user_instance.total_booked_price = total_booking_price
#         user_instance.save()
#         booking_confirmed_mail_send(request, user_instance, room_list)
#         return room_list


