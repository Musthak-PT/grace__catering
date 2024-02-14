"use strict";

var files = []

// Class definition
var MCUpdateOrCreateVehicle = function () {

    var validator;
    var form;

    var brandElement, categoryElement, modelElement, trimElement;
    var dropZone_is;

    const handleSubmit = () => {
        

        // Get elements
        form = document.getElementById('create-or-update-vehicle-form');
        const submitButton = document.getElementById('create-or-update-vehicle-submit');
        



        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    title: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    
                   
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        );


        submitButton.addEventListener('click', e => {
            e.preventDefault();
            
            


            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;
                    // debugger;
                    if (status == 'Valid'&& $("#vehicle_images_dropzone").find('img').length) {
                        const btn = document.getElementById('create-or-update-vehicle-submit');
                        const loadingBtn = document.getElementById('banner-loader-text');
        
                        btn.style.display = 'none';
                        loadingBtn.style.display = 'inline-block';
                        
                        // Handle submit button
                        e.preventDefault();

                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable submit button whilst loading
                        submitButton.disabled = true;
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable submit button after loading
                        submitButton.disabled = false;
                        var base = [];
                        files.forEach(item => {
                            base.push(item?.baseData)
                        })
                        // debugger;
                        $('#banner_image_files').val(JSON.stringify(base));
                        // fileInput.val(files);
                        // debugger;
                        // Redirect to customers list page
                        form.submit();
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        Swal.fire({
                            html: "Please enter the required fields",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            }
        });



        


    }









    const handleDropzone = () => {

        dropZone_is=false
        let PropertyImageDropzone = new Dropzone("#vehicle_images_dropzone", {
            url: `${api_config.banner_image_upload_api_url}`,
            acceptedFiles: ".jpeg,.jpg,.png",
            maxFiles: 1,
            paramName: "file",
            maxFilesize: 3, // MB
            addRemoveLinks: true,
            accept: function(file, done) {
               convertImageToBase64(file,function(baseData){
                files.push({baseData : baseData,instance_id:file.instance_id})
               })
               
            },
            
            init: function() {

                this.on("maxfilesexceeded", function (data) {
                    let res = eval('(' + data.xhr.responseText + ')');
                });
                this.on("error", function (file, message) {
                    //this.removeFile(file);
                });
                this.on("sending", function(file, xhr, formData){
                    formData.append("uuid", `${api_config.uuid}`);
                    formData.append("csrfmiddlewaretoken", `${api_config.csrfmiddlewaretoken}`);
                    formData.append("files", file);
                    formData.append("module", 'vehicle-images');
                });
                this.on("success", function(file, responseText) {
                    

                    
                    if(responseText.status_code == 200 && (PropertyImageDropzone.files.length > 0 || $("#vehicle_images_dropzone").find('img').length))
                    {
                        dropZone_is=true;
                        let childElements = file?.previewElement?.children;
                        childElements.forEach(childElement => {
                            childElement.setAttribute('instance_id', responseText.data);
                            childElement.setAttribute('action_type', 2);
                        });
                    }
                });
                this.on('removedfile', function(file) {
                    var index = ''
                    files.forEach((item,ind)=>{
                        if(item.instance_id == file.instance_id){
                            index = ind
                        }
                    })
                    files.splice(index,1)
                    // let removeElement = file.previewElement.getElementsByTagName('a')?.[0];
                    // let instance_id = removeElement.getAttribute('instance_id')
                    // let action_type = removeElement.getAttribute('action_type')
                    // $.post(`${api_config.temporary_image_destroy_api_url}`, { id: instance_id, action_type:action_type }, 
                    //     function(data, status, xhr) {
                    //         if (PropertyImageDropzone.files.length <= 0) {
                    //             dropZone_is = false
                    //         }
                        

                    //     }).done(function() { console.log('Request done!'); })
                    //     .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });

                }); 
            }
        });

        
        PropertyImageDropzone.on("addedfile", file => {
            console.log('added',PropertyImageDropzone.files.length)
            if(PropertyImageDropzone.files.length > 1){
                PropertyImageDropzone.removeFile(file)
            }
            else{
                let instance_id = file?.instance_id;
                let childElements = file?.previewElement?.children;
                childElements.forEach(childElement => {
                    childElement.setAttribute('instance_id', instance_id);
                    childElement.setAttribute('action_type', 2);
                });
            }
        });
        
        if(api_config?.banner_image_id != 'undefined' && api_config?.banner_image_id != '' ){

            $.post(`${api_config.get_property_images_api_url}`, { banner_image_id: `${api_config.banner_image_id}` }, 
                function(data, status, xhr) {
                    if(data.status_code == 200)
                    {
                        $.each(data.data, function (key,value) {
                            var mockFile = { name: value.image_name, size: value.size, instance_id: value.id};
                            PropertyImageDropzone.emit("addedfile", mockFile);
                            generateBase64encodedURL(value.image, function(dataURL){ 
                                PropertyImageDropzone.emit("thumbnail", mockFile, dataURL)
                                files.push({baseData:dataURL,instance_id: value.id})
                            })
                            PropertyImageDropzone.emit("complete", mockFile);
                            // files.push(JSON.stringify(mockFile));
                        });
                    }
                }
            ).done(function() { console.log('Request done!'); 
            }).fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
        }
    }



    const handleSelectOnChnage = () => {
        
        if(typeof api_config?.vehicle_data?.category_id  !== 'undefined')
        {
            generateSelectOptionElement({pk:api_config?.vehicle_data?.category_id, api_url : `${api_config.get_category_brands}`, tagElement: brandElement, elementEdit_id: api_config?.vehicle_data?.brand_id})
            if(typeof api_config?.vehicle_data?.brand_id  !== 'undefined')
            {
                generateSelectOptionElement({pk: api_config?.vehicle_data?.brand_id, api_url : `${api_config.get_category_models}`,tagElement: modelElement, elementEdit_id: api_config?.vehicle_data?.model_id})
                if(typeof api_config?.vehicle_data?.model_id  !== 'undefined')
                {
                    generateSelectOptionElement({pk: api_config?.vehicle_data?.model_id, api_url : `${api_config.get_category_trims}`,tagElement: trimElement, elementEdit_id: api_config?.vehicle_data?.trim_id})
                }
            }
        }
        
        $(categoryElement).on('change', e => {
            handleResetSelectOptions({elements: {brandElement,modelElement,trimElement}})
            generateSelectOptionElement({pk:e.target.value, api_url : `${api_config.get_category_brands}`,tagElement: brandElement})
            
        });

        $(brandElement).on('change', e => {
            handleResetSelectOptions({elements: {modelElement,trimElement}})
            generateSelectOptionElement({pk:e.target.value, api_url : `${api_config.get_category_models}`,tagElement: modelElement})
        });

        $(modelElement).on('change', e => {
            handleResetSelectOptions({elements: {trimElement}})
            generateSelectOptionElement({pk:e.target.value, api_url : `${api_config.get_category_trims}`,tagElement: trimElement})
        });
    }


    const handleResetSelectOptions = ({elements}) => {
        let emptyElement = document.createElement('option')
        $.each(elements, function (key,element) {
            element.innerHTML  = emptyElement
            element.dispatchEvent(new Event('change'));
        })
    }

    const generateSelectOptionElement = ({pk,api_url,tagElement, elementEdit_id = null }) => {
        if(pk) {
            $.post(api_url, { pk: pk }, function(response, status, xhr) {
                if(response?.status_code == 200)
                {
                    let subOptionElement = document.createElement('option')
                    tagElement.appendChild(subOptionElement);
                    $.each(response?.data, function (key,value) {
                        let subOptionElement = document.createElement('option')
                        //
                        if(elementEdit_id === value?.id)
                        {
                            subOptionElement.setAttribute('selected','selected')
                        }
                        //
                        subOptionElement.value = value?.id
                        subOptionElement.innerHTML = value?.name
                        tagElement.appendChild(subOptionElement);
                    });
                }
            
            }).done(function() { console.log('Request done!'); 
            }).fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
        }
    }




    
    // Public methods
    return {
        init: function () {

            categoryElement = document.querySelector('[data-control-select-option="category"]')
            brandElement = document.querySelector('[data-control-select-option="brand"]')
            modelElement = document.querySelector('[data-control-select-option="model"]')
            trimElement = document.querySelector('[data-control-select-option="trim"]')


            handleSubmit();
            handleDropzone();
            handleSelectOnChnage();

            google.maps.event.addDomListener(window, 'load', initialize);
            
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateVehicle.init();
});



function generateBase64encodedURL(src, callback){
    var image = new Image();
    image.crossOrigin = 'Anonymous';
    image.onload = function(){
      var canvas = document.createElement('canvas');
      var context = canvas.getContext('2d');
      //canvas.height = this.naturalHeight;
      canvas.height = 140;
      canvas.width = 140;
      //canvas.width = this.naturalWidth;
      context.drawImage(this, 0, 0,140,140);
      var dataURL = canvas.toDataURL('image/jpeg');
      callback(dataURL);
    };
    image.src = src;
}

function initializeMap(lat_val='',long_val='') {

   
    let latitude = document.querySelector('[data-google-location="latitude"]')
    let longitude = document.querySelector('[data-google-location="longitude"]')
    // place = document.querySelector('[data-google-place="place"]')
    
    
    

    if (lat_val != '' & long_val != '')
    {
        var myLatlngPoint = new google.maps.LatLng(lat_val,long_val)
        
        var map = new google.maps.Map(document.getElementById("map"), {
            zoom: 18,
            center: myLatlngPoint,
        });

        google.maps.event.addListenerOnce(map, 'bounds_changed', function() {
            
            map.setZoom(18);
            
          });
          
    }
    else if((typeof api_config?.location_data?.latitude !== 'undefined' && api_config?.location_data?.latitude !== '') && (typeof api_config?.location_data?.longitude !== 'undefined' && api_config?.location_data?.longitude !== ''))
    {
     
        var myLatlngPoint = new google.maps.LatLng(parseFloat(api_config?.location_data?.latitude), parseFloat(api_config?.location_data?.longitude))
       
        var map = new google.maps.Map(document.getElementById("map"), {
            center: myLatlngPoint,
            zoom:18
        }); 
        google.maps.event.addListenerOnce(map, 'bounds_changed', function() {
        
            map.setZoom(18);
            infoWindow.open(map);
            infoWindow.close();
          });
        

    }else{
        var mapOptions = {
            styles: [{ featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }]}]
          };
        var myLatlngPoint = new google.maps.LatLng(25.168156257023266,51.217586634374996)
        var map = new google.maps.Map(document.getElementById("map"), {   
            zoom: 9,
            center: myLatlngPoint,
        },mapOptions);
    }
    var infoWindow = new google.maps.InfoWindow({
      //  content: "Click the map to get Lat/Lng!",
        position: myLatlngPoint,
        
    
    });
    // infoWindow.close();
    

    
    

    const marker = new google.maps.Marker({
        position: myLatlngPoint,
        map,
    });
   


    infoWindow.open({
        anchor: marker,
        map,
      });
      infoWindow.close();

    if((typeof api_config?.location_data?.latitude !== 'undefined' && api_config?.location_data?.latitude !== '') && (typeof api_config?.location_data?.longitude !== 'undefined' && api_config?.location_data?.longitude !== ''))
    {
       // infoWindow.setContent(JSON.stringify({ lat: api_config?.location_data?.latitude, lng:api_config?.location_data?.longitude }, null, 2));
        map.setZoom(9);
       // infoWindow.open(map);
    }

    map.addListener("click", function (mapsMouseEvent) {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        // infoWindow = new google.maps.InfoWindow({
        //     position: mapsMouseEvent.latLng,
        // });
        latitude.value = mapsMouseEvent.latLng.toJSON()?.lat
        longitude.value = mapsMouseEvent.latLng.toJSON()?.lng
        // infoWindow.setContent(JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2));
        // infoWindow.open(map);
    });
}






function initialize() {
    var input = document.getElementById('place');
    
    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();

        initializeMap(place.geometry['location'].lat(),place.geometry['location'].lng())
        document.getElementById("latitude").value = place.geometry['location'].lat();
        document.getElementById("longitude").value = place.geometry['location'].lng();
    });
}

function convertImageToBase64(file,callback) {
    // Get the file input element
    
    // Check if a file is selected
    if (file) {
      // Create a FileReader object
      var reader = new FileReader();

      // Set a callback function to handle the file reading
      reader.onload = function (e) {
        // Get the base64 data
        var base64Data = e.target.result;
        callback(base64Data);
        // Display the base64 data
        // document.getElementById('result').innerText = base64Data;
      };

      // Read the selected file as Data URL (base64)
      reader.readAsDataURL(file);
    } else {
      alert('Please select an image file.');
    }
  }
  
