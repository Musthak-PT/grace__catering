from apps.users.models import Users
from rest_framework import serializers
from apps.property_management.models import *
from apps.offer.models import PropertyOffer
from datetime import date, timedelta
from django.db.models import Q
from apps.review.models import CustomerReview
from django.db.models import Sum
from apps.wishlist.models import WishList
from datetime import datetime
from apps.bookings.models import RoomBookedCustomerDetails, HotelRoomBooking

class GetAccommodationTypeUsWebResponseSchemas(serializers.ModelSerializer):    
    class Meta:
        model  = AccommodationType
        fields = ['id', 'slug', 'name', 'description']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

class GetPropertyCollectionWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = PropertyCollection
        fields = ['id', 'slug', 'name', 'description']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

class GetPropertyFacilityWebResponseSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = PropertyFacility
        fields = ['id', 'slug', 'name', 'description']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
#get all filtered properties
class FilterPropertyImageListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id','property_image']


    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class FilterPropertyAddressListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyAddress
        fields = ['id','street','city']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data

class FilterPropertyFacilityListSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyFacility
        fields = ['name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
#Room selection schema
class RoomImageListSchema(serializers.ModelSerializer):
        class Meta:
            model = RoomImage
            fields = ['id','room_image']

        def to_representation(self, instance):
            data = super().to_representation(instance)
            for field in data:
                try:
                    if data[field] is None:
                        data[field] = ""
                except KeyError:
                    pass
            return data
        
class RoomTypesSchema(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'slug', 'name', 'adults']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
class RoomSelectionSchema(serializers.ModelSerializer):
    room_type       = serializers.SerializerMethodField('get_room_type_name')
    facilities      = serializers.SerializerMethodField('get_room_facility')
    offer_price     = serializers.SerializerMethodField('get_offer_price')
    room_image      = serializers.SerializerMethodField('get_room_image_url')
    room_quantity   = serializers.SerializerMethodField('get_room_quantity')
    class Meta:
        model = HotelRoom
        fields = ['id', 'slug', 'room_type', 'facilities', 'room_size', 'price','offer_price','room_image','room_quantity']

    
    def get_room_type_name(self, instance):
        room_type = instance.room_type
        if room_type:
            room_type_serializer = RoomTypesSchema(room_type)
            return room_type_serializer.data
        return ""
    
    def get_offer_price(self, instance):
        check_in = self.context.get("check_in")
        check_out = self.context.get("check_out")
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

        # Find the offer based on check-in and check-out dates
        offer = PropertyOffer.objects.filter(
            Q(room_property__hotel_room=instance) &
            Q(end_date__gte=check_in_date) &
            Q(start_date__lte=check_out_date)
        ).first()

        if offer is not None:
            offer_percentage = float(offer.offer_percentage)

            discounted_price = float(instance.price)-(float(instance.price) * (offer_percentage / 100))
            return discounted_price

        return ""
    
    def get_room_image_url(self, instance):
        request = self.context.get('request')
        room_image = RoomImage.objects.filter(hotel_room_id=instance.id)
        image_schema = RoomImageListSchema(room_image, many=True, context={"request": request})
        return image_schema.data

    def get_room_facility(self, instance):
        room_facilities = HotelRoomPropertyFacility.objects.filter(hotel_room=instance)
        property_facility_ids = room_facilities.values_list('property_facility', flat=True)
        facilities = PropertyFacility.objects.filter(id__in=property_facility_ids)
        return [facility.name for facility in facilities]

    def get_room_quantity(self, instance):
        hotel_room = HotelRoom.objects.filter(id=instance.id).first()

        if hotel_room:
            request = self.context.get('request')
            check_in = request.data.get('check_in', None)
            check_out = request.data.get('check_out', None)

            booked_quantities = HotelRoomBooking.objects.filter(
                room_id=instance.id,
                check_in__lte=check_out,
                check_out__gte=check_in
            ).aggregate(Sum('quantity'))['quantity__sum']

            if booked_quantities is not None:
                remaining_quantity = int(hotel_room.room_count) - booked_quantities
                return max(remaining_quantity, 0)
        return str(hotel_room.room_count)
#End

class FilterPropertyManagementSchema(serializers.ModelSerializer):
    image         = serializers.SerializerMethodField('get_image')
    address       = serializers.SerializerMethodField('get_address')
    facility      = serializers.SerializerMethodField('get_facility')
    has_offer     = serializers.SerializerMethodField('get_has_offer')
    check_in      = serializers.DateField(required=False)
    check_out     = serializers.DateField(required=False)
    is_wishlisted = serializers.SerializerMethodField('get_is_wishlisted')
    
    class Meta:
        model = PropertyManagement
        fields = ['slug','id', 'image', 'name', 'address', 'facility','has_offer','check_in','check_out','is_wishlisted','location_distance', 'location_distance']


    def get_is_wishlisted(self, instance):
        request = self.context.get('request')
        
        wishlist_obj = WishList.objects.filter(Q(property_id=instance.id) & Q(user_id=request.user.id)).exists()
        return wishlist_obj
    
    def get_image(self, instance):
        request = self.context.get('request')
        image_obj = PropertyImage.objects.filter(property_management_id=instance.id)
        image_schema = FilterPropertyImageListSchema(image_obj, many=True, context={"request": request})
        return image_schema.data

    def get_address(self, instance):
        address_obj = instance.address
        if address_obj:
            address_schema = FilterPropertyAddressListSchema(address_obj)
            return address_schema.data
        else:
            return ""

    def get_facility(self, instance):
        hotel_room_ids = PropertyManagementHotelRoom.objects.filter(
            property_management=instance
        ).values_list('hotel_room', flat=True)

        property_facility_instances = HotelRoomPropertyFacility.objects.filter(
            hotel_room__in=hotel_room_ids
        ).values_list('property_facility', flat=True)

        facility_names = PropertyFacility.objects.filter(
            id__in=property_facility_instances
        ).values_list('name', flat=True).distinct()

        return facility_names
    def get_has_offer(self, instance):
        has_offer = PropertyOffer.objects.filter(
            room_property__property_management=instance
        ).exists()
        return has_offer
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        check_in, check_out = self.get_check_in_out(instance)
        data['check_in'] = check_in
        data['check_out'] = check_out

        return data

    def get_check_in_out(self, instance):
        check_in = self.context['request'].data.get('check_in')
        check_out = self.context['request'].data.get('check_out')

        if check_in and check_out:
            booked_rooms = HotelRoomBooking.objects.filter(
                Q(check_in__lte=check_in, check_out__gte=check_in) |
                Q(check_in__lte=check_out, check_out__gte=check_out) |
                Q(check_in__gte=check_in, check_out__lte=check_out),
                room_id=instance.id
            ).exists()

            if booked_rooms:
                current_date = date.today()
                check_in = current_date
                check_out = current_date + timedelta(days=1)

        else:
            current_date = date.today()
            check_in = current_date
            check_out = current_date + timedelta(days=1)

        return check_in, check_out
#End
#Drop down collection   
class GetDropdowncollectionSchemas(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    label = serializers.CharField(source='name')
    
    class Meta:
        model = PropertyCollection
        fields = ['value', 'label']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
#End
#Drop down Accomadation type
class GetDropdownAccomadationTypeSchemas(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    label = serializers.CharField(source='name')
    
    class Meta:
        model = AccommodationType
        fields = ['value', 'label']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
#End
#Drop down Property Facility
class GetDropdownPropertyFacilitySchemas(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    label = serializers.CharField(source='name')
    
    class Meta:
        model = PropertyFacility
        fields = ['value', 'label']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
#End
#Drop down Property Facility
class GetDropdownPropertyRoomTypeSchemas(serializers.ModelSerializer):
    value = serializers.CharField(source='id')
    label = serializers.CharField(source='name')
    
    class Meta:
        model = RoomType
        fields = ['value', 'label','adults']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
#End

class RoomTypeSchemas(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['name']

class RatingSchemas(serializers.ModelSerializer):
    full_name   = serializers.CharField(source="user.full_name")
    class Meta:
        model = CustomerReview
        fields = ['id', 'full_name', 'rating', 'title', 'description']

class HotelRoomSerializer(serializers.ModelSerializer):
    room_type  = RoomTypeSchemas()
    room_image = serializers.SerializerMethodField('get_room_image')

    class Meta:
        model = HotelRoom
        fields = ['id','room_type', 'room_size', 'price','room_image']
    
    def get_room_image(self, instance):
        room_images = RoomImage.objects.filter(hotel_room__id=instance.id).values('room_image')
        return room_images
  
class GetPropertyDetailedViewSchemas(serializers.ModelSerializer):
    image                = serializers.SerializerMethodField('get_image')
    address              = serializers.SerializerMethodField('get_address')
    facility             = serializers.SerializerMethodField('get_facility')
    rating               = serializers.SerializerMethodField('get_rating')
    is_wishlist          = serializers.SerializerMethodField('get_is_wishlist')
    property_image_count = serializers.SerializerMethodField('get_image_count')
    # rooms     = serializers.SerializerMethodField('get_rooms')
    
    class Meta:
        model  = PropertyManagement
        fields = ['id', 'slug', 'image','name','description','address','facility','rating','latitude','longitude','location_distance','is_wishlist', 'property_image_count']
    
    def get_is_wishlist(self, instance):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            wishlist_obj    = WishList.objects.filter(property_id=instance.id, user_id=request.user.id).exists()
            return wishlist_obj
        return False


    def get_image(self, instance):
        request         = self.context.get('request')
        image_obj       = PropertyImage.objects.filter(property_management_id=instance.id)
        image_schema    = FilterPropertyImageListSchema(image_obj, many=True, context={"request": request})
        return image_schema.data

    def get_address(self, instance):
        address_obj = instance.address
        if address_obj:
            address_schema = FilterPropertyAddressListSchema(address_obj)
            return address_schema.data
        else:
            return ""
    
    def get_facility(self, instance):
        hotel_room_ids = PropertyManagementHotelRoom.objects.filter(
            property_management=instance
        ).values_list('hotel_room', flat=True)

        property_facility_instances = HotelRoomPropertyFacility.objects.filter(
            hotel_room__in=hotel_room_ids
        ).values_list('property_facility', flat=True)

        facility_names = PropertyFacility.objects.filter(
            id__in=property_facility_instances
        ).values_list('name', flat=True).distinct()

        return facility_names
    
    def get_rating(self, instance):
        ratings = CustomerReview.objects.filter(property=instance)
        serializer = RatingSchemas(ratings, many=True)
        return {
            'count': ratings.count(),
            'data': serializer.data,
        }
    
    def get_image_count(self, instance):
        image_obj       = PropertyImage.objects.filter(property_management_id=instance.id).count()
        return str(image_obj)
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
#End

class PropertyImageSchema(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id','property_image']

class PropertyReviewSchema(serializers.ModelSerializer):
    class Meta:
        model = CustomerReview
        fields = ['id','rating','description','title']

class GetProfileDetailsSchemas(serializers.ModelSerializer):
    check_in        = serializers.SerializerMethodField('get_check_in')
    check_out       = serializers.SerializerMethodField('get_check_out')
    actual_price    = serializers.SerializerMethodField('get_actual_price')
    offer_price     = serializers.SerializerMethodField('get_offer_price')
    property_images = serializers.SerializerMethodField('get_property_images')
    property_name   = serializers.SerializerMethodField('get_property_name')
    property_rating = serializers.SerializerMethodField('get_property_ratings')

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'email', 'phone', 'check_in', 'check_out', 'actual_price', 'offer_price','property_images','property_name','property_rating']

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

    def get_check_in(self, instance):
        bookings = HotelRoomBooking.objects.filter(created_by=instance)
        return [booking.check_in for booking in bookings]

    def get_check_out(self, instance):
        bookings = HotelRoomBooking.objects.filter(created_by=instance)
        return [booking.check_out for booking in bookings]

    def get_actual_price(self, instance):
        bookings = HotelRoomBooking.objects.filter(created_by=instance)
        return [booking.actual_price for booking in bookings]

    def get_offer_price(self, instance):
        bookings = HotelRoomBooking.objects.filter(created_by=instance)
        return [booking.offer_price for booking in bookings]

    def get_property_images(self, instance):
        request         = self.context.get('request')
        room_ids = HotelRoomBooking.objects.filter(created_by=instance).values_list('room_id', flat=True)
        property_management_ids = PropertyManagementHotelRoom.objects.filter(hotel_room__in=room_ids).values_list('property_management_id', flat=True)
        property_images = PropertyImage.objects.filter(property_management__in=property_management_ids)

        return PropertyImageSchema(property_images, many=True, context={'request': request}).data
    
    def get_property_name(self, instance):
        room_ids = HotelRoomBooking.objects.filter(created_by=instance).values_list('room_id', flat=True)
        property_management_ids = PropertyManagementHotelRoom.objects.filter(hotel_room__in=room_ids).values_list('property_management_id', flat=True)
        property_names = PropertyManagement.objects.filter(id__in=property_management_ids).values_list('name', flat=True)

        return property_names
    
    def get_property_ratings(self, instance):
        room_ids = HotelRoomBooking.objects.filter(created_by=instance).values_list('room_id', flat=True)
        property_management_ids = PropertyManagementHotelRoom.objects.filter(hotel_room__in=room_ids).values_list('property_management_id', flat=True)
        customer_reviews = CustomerReview.objects.filter(property__in=property_management_ids)
        return PropertyReviewSchema(customer_reviews, many=True).data
#-----------------------------------------------------------------------------------------
class BookingCheckinoutSchema(serializers.ModelSerializer):
    class Meta:
        model = HotelRoomBooking
        fields = ['id', 'slug', 'check_in', 'check_out', 'quantity']


class GetMyBookingPropertiesSchemas(serializers.ModelSerializer):
    booked_details    = serializers.SerializerMethodField('get_checkbooking')
    property_details  = serializers.SerializerMethodField('get_property_details')

    class Meta:
        model = RoomBookedCustomerDetails
        fields = ['id','booked_details', 'property_details']

    def get_checkbooking(self, instance):
        request       = self.context.get('request')
        room_check    = HotelRoomBooking.objects.filter(Q(created_by_id=request.user.id) & Q(customer_details=instance))
        return BookingCheckinoutSchema(room_check, many=True).data
        

    def get_property_details(self, instance):
        request = self.context.get('request')
        room_ids = HotelRoomBooking.objects.filter(Q(created_by_id=request.user.id) & Q(customer_details=instance)).values_list('room_id', flat=True)

        if not room_ids:
            return []  # No room_ids found, return empty list

        # Retrieve property_management_ids
        property_management_ids = PropertyManagementHotelRoom.objects.filter(hotel_room__in=room_ids).values_list('property_management', flat=True)

        if not property_management_ids:
            return []  # No property_management_ids found, return empty list

        # Retrieve PropertyManagement instances
        property_managements = PropertyManagement.objects.filter(id__in=property_management_ids)

        # Create a list to store property details
        properties_data = []

        # Loop through each PropertyManagement instance
        for property_management in property_managements:
            # Retrieve name
            name = property_management.name

            # Retrieve address details from PropertyAddress
            address = {
                'street': property_management.address.street,
                'city': property_management.address.city,
                'city_area': property_management.address.city_area,
            }

            # Retrieve property images
            property_images = PropertyImage.objects.filter(property_management=property_management)
            request = self.context.get('request')

            # Generate absolute URLs for the images
            image_urls = [request.build_absolute_uri(image.property_image.url) for image in property_images]

            # Combine name, address, and images into a dictionary
            property_data = {
                'name': name,
                'address': address,
                'images': image_urls,  # Now, the image URLs will have "http://" prefix
            }

            # Add the property data to the list
            properties_data.append(property_data)

        return properties_data

class MyBookingPropertiesDetailedSchema(serializers.ModelSerializer):
    booked_details    = serializers.SerializerMethodField('get_checkbooking')
    property_details  = serializers.SerializerMethodField('get_property_details')
    room_type         = serializers.SerializerMethodField('get_room_type')

    class Meta:
        model = RoomBookedCustomerDetails
        fields = ['id','slug','full_name', 'email_address','mobile_number','total_booked_price','booked_details','property_details','room_type']
    
    def get_room_type(self, instance):
        request = self.context.get('request')
        
        # Step 1: Retrieve room_id from HotelRoomBooking model
        room_booking = HotelRoomBooking.objects.filter(
            Q(created_by_id=request.user.id) & Q(customer_details=instance)
        ).first()

        if room_booking:
            # Step 2: Get the corresponding HotelRoom object using room_id
            room = room_booking.room_id

            if room:
                # Step 3: Retrieve room_type from HotelRoom model
                room_type = room.room_type

                if room_type:
                    # Step 4: Get the corresponding RoomType object using room_type
                    room_type_instance = RoomType.objects.get(pk=room_type.id)

                    # Step 5: Retrieve name from RoomType model
                    room_type_name = room_type_instance.name
                    return room_type_name

        # Return None if any step fails
        return None
    
    def get_checkbooking(self, instance):
        request       = self.context.get('request')
        room_check    = HotelRoomBooking.objects.filter(Q(created_by_id=request.user.id) & Q(customer_details=instance))
        return BookingCheckinoutSchema(room_check, many=True).data
    
    

    def get_property_details(self, instance):
        request = self.context.get('request')
        room_ids = HotelRoomBooking.objects.filter(Q(created_by_id=request.user.id) & Q(customer_details=instance)).values_list('room_id', flat=True)

        if not room_ids:
            return []  # No room_ids found, return empty list

        # Retrieve property_management_ids
        property_management_ids = PropertyManagementHotelRoom.objects.filter(hotel_room__in=room_ids).values_list('property_management', flat=True)

        if not property_management_ids:
            return []  # No property_management_ids found, return empty list

        # Retrieve PropertyManagement instances
        property_managements = PropertyManagement.objects.filter(id__in=property_management_ids)

        # Create a list to store property details
        properties_data = []

        # Loop through each PropertyManagement instance
        for property_management in property_managements:
            # Retrieve name
            name          = property_management.name
            description   = property_management.description

            # Retrieve address details from PropertyAddress
            address = {
                'street': property_management.address.street,
                'city': property_management.address.city,
                'city_area': property_management.address.city_area,
            }

            # Retrieve property images
            property_images = PropertyImage.objects.filter(property_management=property_management)
            request = self.context.get('request')

            # Generate absolute URLs for the images
            image_urls = [request.build_absolute_uri(image.property_image.url) for image in property_images]

            # Combine name, address, and images into a dictionary
            property_data = {
                'name'          : name,
                'address'       : address,
                'description'   : description,
                'images'        : image_urls,  # Now, the image URLs will have "http://" prefix
            }

            # Add the property data to the list
            properties_data.append(property_data)

        return properties_data

#Schemas Room booking 
# class HotelRoomBookingSchemas(serializers.ModelSerializer):
#     booked_details    = serializers.SerializerMethodField('get_checkbooking')
#     property_details  = serializers.SerializerMethodField('get_property_details')
#     room_type         = serializers.SerializerMethodField('get_room_type')

#     class Meta:
#         model = RoomBookedCustomerDetails
#         fields = ['id','slug','full_name', 'email_address','mobile_number','total_booked_price','booked_details','property_details','room_type']
    
    
class RoomBookingResultSchema(serializers.Serializer):
    room_price    = serializers.SerializerMethodField('get_room_price')
    room_name     = serializers.SerializerMethodField('get_room_name')
    room_id       = serializers.SerializerMethodField('get_room_id')
    room_quantity = serializers.SerializerMethodField('get_room_quantity')
    offer_percentage = serializers.SerializerMethodField('get_offer_percentage')
    
    def get_room_price(self, obj):
        date_difference = self.context.get('date_difference',None).days
        check_in = self.context.get('check_in',None)
        check_out = self.context.get('check_out',None)
                
        offer_obj = PropertyOffer.objects.filter(Q(room_property__hotel_room=obj['room_id']) & Q(end_date__gte=check_in) & Q(start_date__lte=check_out))
        if offer_obj:
            total_cost = int(obj['room_id'].price) - (int(obj['room_id'].price) * (int(offer_obj.first().offer_percentage)/100))
            total_cost = total_cost * int(obj['quantity']) * date_difference
        else:
            total_cost = int(obj['room_id'].price) * int(obj['quantity']) * date_difference
        return str(total_cost)
    
    def get_room_name(self, obj):
        room_name = obj['room_id'].room_type.name
        return room_name
    
    def get_room_id(self, obj):
        room_name = obj['room_id'].id
        return room_name
    
    def get_room_quantity(self, obj):
        room_name = obj['quantity']
        return room_name
    
    def get_offer_percentage(self, obj):
        check_in  = self.context.get('check_in',None)
        check_out = self.context.get('check_out',None)
        offer_obj = PropertyOffer.objects.filter(Q(room_property__hotel_room=obj['room_id']) & Q(end_date__gte=check_in) & Q(start_date__lte=check_out))
        if offer_obj:
            return offer_obj.first().offer_percentage
        else:
            return ''


class BookingDetailesSchema(serializers.Serializer):
    
    room_deatils = serializers.SerializerMethodField('get_room_deatils')
    check_in     = serializers.SerializerMethodField('get_check_in')
    check_out    = serializers.SerializerMethodField('get_check_out')
    room_count   = serializers.SerializerMethodField('get_room_count')
    property_name = serializers.SerializerMethodField('get_property_name')
    property_image = serializers.SerializerMethodField('get_property_image')
    
    def get_room_deatils(self, obj):
        request = self.context.get('request')

        date_difference = obj['check_out'] - obj['check_in']
        
        room_obj = RoomBookingResultSchema(obj['bookingdetails'], many=True, context={"request": request,'date_difference':date_difference, 'check_in': obj['check_in'], 'check_out': obj['check_out']}).data
        return room_obj
    
    def get_room_count(self, obj):
        return str(len(obj['bookingdetails']))
    
    def get_check_in(self, obj):
        return obj['check_in']
    
    def get_check_out(self, obj):
        return obj['check_out']
    
    def get_property_name(self, obj):
        property_name = PropertyManagementHotelRoom.objects.filter(hotel_room_id=obj['bookingdetails'][0]['room_id'].id).first()
        return str(property_name)
    
    def get_property_image(self, obj):
        request = self.context.get('request')
        property_image = PropertyManagementHotelRoom.objects.filter(hotel_room_id=obj['bookingdetails'][0]['room_id'].id).first().property_management.id
        property_image = PropertyImage.objects.filter(property_management_id=property_image).first().property_image
        property_image = request.build_absolute_uri(property_image.url)
        return str(property_image)