"use strict";

var files = []

// Class definition
var MCUpdateOrCreateVehicle = function () {

    var validator;
    var form;

    var uniqueId = 0

    var brandElement, categoryElement, modelElement, trimElement, rooms;
    var dropZone_is;

    const handleSubmit = () => {
        


        

        // Get elements
        form = document.getElementById('create-or-update-vehicle-form');
        const submitButton = document.getElementById('create-or-update-vehicle-submit');



        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    description: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    assigned_to: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    no_of_rooms: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            numeric : {
                                message : 'The value is not a number'
                            }
                        }
                    },
                    street: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    city: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[A-Za-z ]+$/,
                                message: 'Only characters are allowed'
                            }
                        }
                    },
                    city_area: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[A-Za-z ]+$/,
                                message: 'Only characters are allowed'
                            }
                        }
                    },
                    postal_code: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            numeric : {
                                message : 'The value is not a number'
                            },
                        }
                    },
                    'phone': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            numeric: {
                                message: 'The value is not a number'
                            },
                            stringLength: {
                                min: 10,
                                max: 10,
                                message: 'The phone number must be exactly 10 digits'
                            }
                        }
                    },
                    // alternative_phone: {
                    //     validators: {
                    //         notEmpty: {
                    //             message: 'This field is required'
                    //         },
                    //         numeric: {
                    //             message: 'The value is not a number'
                    //         },
                    //         stringLength: {
                    //             min: 10,
                    //             max: 10,
                    //             message: 'The phone number must be exactly 10 digits'
                    //         }
                    //     }
                    // },
                    // latitude: {
                    //     validators: {
                    //         notEmpty: {
                    //             message: 'This field is required'
                    //         }
                    //     }
                    // },
                    place: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    // longitude: {
                    //     validators: {
                    //         notEmpty: {
                    //             message: 'This field is required'
                    //         },
                    //     }
                    // },
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
        
        function checkEmptyValues(data) {
            for (const key in data) {
              const room = data[key];
              for (const prop in room) {
                // Exclude room_size from validation
                if (prop !== "room_size" && (room[prop] === "" || (Array.isArray(room[prop]) && room[prop].length === 0))) {
                  return true; // Empty value found
                }
              }
            }
            return false; // No empty value found
          }

        submitButton.addEventListener('click', e => {
            e.preventDefault();
            console.log("masterObject :>>>>>> ", masterObject);




            let rooms = document.querySelectorAll('[data-dynamic-room="room-details"]')

            rooms.forEach(room => {
                let unique_id        = room.getAttribute('data-room-unique')
                let room_type        = document.querySelector(`[name=room_type_${unique_id}]`).value;
                let room_facility    = getSelectedValues(`[name=room_facility_${unique_id}]`);
                let room_description = document.querySelector(`[name=description_${unique_id}]`).value;
                let room_size        = document.querySelector(`[name=room_size_${unique_id}]`).value;
                let room_price       = document.querySelector(`[name=price_${unique_id}]`).value;
                let room_count       = document.querySelector(`[name=room_count_${unique_id}]`)?.value;
                var base = [];
                if (files && files[unique_id]) {
                    files[unique_id].forEach(item => {
                        if (item && item.baseData) {
                            base.push(item.baseData);
                        }
                    });
                }
                masterObject[unique_id] = {
                    "room_type" : room_type,
                    "room_facility" : room_facility,
                    "room_description" : room_description,
                    "room_size" : room_size,
                    "room_price" : room_price,
                    "room_count" : room_count,
                    "room_image_set" : base,
                }
                let room_image_elements =  document.querySelector(`[id="property_room_images_dropzone_${unique_id}"]`);
                let dzPreviewElements = room_image_elements.querySelectorAll('.dz-preview');
                let idArray = Array.from(dzPreviewElements).map(element => element.getAttribute('instance_id'));

                masterObject[unique_id]['room_image_ids'] = idArray

                let property_room_image_hidden_element =  document.querySelector(`[name="property_room_images"]`);
                let jsonString = JSON.stringify(masterObject);
                property_room_image_hidden_element.setAttribute('value', jsonString)
            });
            let is_validate =  checkEmptyValues(masterObject)
            if (is_validate){
                Swal.fire({
                    html: "Please enter the required field",
                    icon: "error",
                    buttonsStyling: false,
                    confirmButtonText: "Ok, got it!",
                    customClass: {
                        confirmButton: "btn btn-primary"
                    }
                });
            }
            if(!is_validate){
                if (validator) {
                    validator.validate().then(function (status) {
                        
                        console.log('validated!');
                        submitButton.setAttribute('data-kt-indicator', 'on');
    
                        // Disable button to avoid multiple click
                        submitButton.disabled = true;
    
                        if (status == 'Valid' && $("#property_images_dropzone").find('img').length > 0) {
                            // Handle submit button
                            e.preventDefault();
    
                            submitButton.setAttribute('data-kt-indicator', 'on');
    
                            // Disable submit button whilst loading
                            submitButton.disabled = true;
                            submitButton.removeAttribute('data-kt-indicator');
                            // Enable submit button after loading
                            submitButton.disabled = false;
                            // var base = [];
                            // files.forEach(file => {
                            //     file.forEach(item => {
                            //         base.push(item?.baseData)
                            //     })
                            // })
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
            }
            
        });



        


    }









    const handleDropzone = () => {

        dropZone_is=false
        let PropertyImageDropzone = new Dropzone("#property_images_dropzone", {
            url: `${api_config.property_image_upload_api_url}`,
            acceptedFiles: ".jpeg,.jpg,.png",
            maxFiles: 20,
            paramName: "file",
            maxFilesize: 1, // MB
            addRemoveLinks: true,
            accept: function(file, done) {
                done();
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
                    

                    
                    if(responseText.status_code == 200 && (PropertyImageDropzone.files.length > 0 || $("#property_images_dropzone").find('img').length))
                    {
                        dropZone_is=true;
                        let childElements = file?.previewElement?.children;
                        childElements.forEach(childElement => {
                            childElement.setAttribute('instance_id', responseText.data);
                            childElement.setAttribute('action_type', 1);
                        });
                    }

                });
                this.on('removedfile', function(file) {
                    let removeElement = file.previewElement.getElementsByTagName('a')?.[0];
                    let instance_id = removeElement.getAttribute('instance_id')
                    let action_type = removeElement.getAttribute('action_type')
                    $.post(`${api_config.temporary_image_destroy_api_url}`, { id: instance_id, action_type:action_type }, 
                        function(data, status, xhr) {
                            if (PropertyImageDropzone.files.length <= 0) {
                                dropZone_is = false
                                console.log(data)
                            }
                        
                            console.log(data)

                        }).done(function() { console.log('Request done!'); })
                        .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
                        console.log(">11111111111111111111111")

                }); 
            }
        });
        PropertyImageDropzone.on("addedfile", file => {
            console.log('added',PropertyImageDropzone.files.length)
            if(PropertyImageDropzone.files.length > 15){
                PropertyImageDropzone.removeFile(file)
            }
            else{
                let instance_id = file?.instance_id;
                let childElements = file?.previewElement?.children;
                childElements.forEach(childElement => {
                    childElement.setAttribute('instance_id', instance_id);
                    childElement.setAttribute('action_type', 1);
                });
            }
        });
        // PropertyImageDropzone.on("addedfile", file => {
        //     let instance_id = file?.instance_id;
        //     let childElements = file?.previewElement?.children;
        //     childElements.forEach(childElement => {
        //         childElement.setAttribute('instance_id', instance_id);
        //         childElement.setAttribute('action_type', 2);
        //     });
        // });
        
        if(api_config?.property_management_id != 'undefined' && api_config?.property_management_id != '' ){

            $.post(`${api_config.get_property_images_api_url}`, { property_management_id: `${api_config.property_management_id}` }, 
                function(data, status, xhr) {
                    if(data.status_code == 200)
                    {
                        $.each(data.data, function (key,value) {
                            var mockFile = { name: value.image_name, size: value.size, instance_id: value.id};
                            PropertyImageDropzone.emit("addedfile", mockFile);
                            generateBase64encodedURL(value.image, function(dataURL){ 
                                PropertyImageDropzone.emit("thumbnail", mockFile, dataURL)
                            })
                            PropertyImageDropzone.emit("complete", mockFile);
                        
                        });
                        
                    }
                }
            ).done(function() { console.log('Request done!'); 
            }).fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
        }
        
    }
    
    const handleDropzonePropertyRoomImages = (unique_id) => {
        console.log(unique_id)
        dropZone_is=false
        let PropertyRoomImageDropzone = new Dropzone(`#property_room_images_dropzone_${unique_id}`, {
            url: `${api_config.property_room_image_upload_api_url}`,
            acceptedFiles: ".jpeg,.jpg,.png",
            maxFiles: 20,
            paramName: "file",
            maxFilesize: 10, // MB
            addRemoveLinks: true,
            accept: function(file, done) {
                // done();
                convertImageToBase64(file,function(baseData){
                    if(files[unique_id]){
                        console.log('inside')
                        files[unique_id].push({baseData : baseData,instance_id:file.instance_id})
                    }
                    else{
                        console.log('outside')
                        files[unique_id] = [];
                        files[unique_id].push({baseData : baseData,instance_id:file.instance_id})
                    }
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
                    formData.append("module", 'property-room-images');
                });
                this.on("success", function(file, responseText) {
                    
                    if(responseText.status_code == 200 && (PropertyRoomImageDropzone.files.length > 0 || $(`#property_room_images_dropzone_${uniqueId}`).find('img').length))
                    {
                        dropZone_is=true;
                        // file?.previewElement?.setAttribute('instance_id', responseText.data);
                        // file?.previewElement?.setAttribute('action_type', 3);
                        let childElements = file?.previewElement?.children;
                        childElements.forEach(childElement => {
                            childElement.setAttribute('instance_id', responseText.data);
                            childElement.setAttribute('action_type', 3);
                        });
                    }

                });
                this.on('removedfile', function(file) {
                    // let removeElement = file.previewElement.getElementsByTagName('a')?.[0];
                    // let instance_id = removeElement.getAttribute('instance_id')
                    // let action_type = removeElement.getAttribute('action_type')
                    // $.post(`${api_config.temporary_room_image_destroy_api_url}`, { id: instance_id, action_type:action_type }, 
                    //     function(data, status, xhr) {
                    //         if (PropertyRoomImageDropzone.files.length <= 0) {
                    //             dropZone_is = false
                    //         }
                        
                    //     }).done(function() { console.log('Request done!'); })
                    //     .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
                    var index = ''
                    files[unique_id].forEach((item,ind)=>{
                        if(item.instance_id == file.instance_id){
                            index = ind
                        }
                    })
                    files[unique_id].splice(index,1)

                }); 
            }
        });
        if(api_config?.property_management_id != 'undefined' && api_config?.property_management_id != '' ){
            let room = document.getElementById(unique_id)
                $.post(`${api_config.get_property_room_images_api_url}`, { property_room_id: room && room.getAttribute('data-room-id')  }, 
                    function(data, status, xhr) {
                        if(data.status_code == 200)
                        {
                            $.each(data.data, function (key,value) {
                                var mockFile = { name: value.image_name, size: value.size, instance_id: value.id};
                                PropertyRoomImageDropzone.emit("addedfile", mockFile);
                                generateBase64encodedURL(value.image, function(dataURL){ 
                                    PropertyRoomImageDropzone.emit("thumbnail", mockFile, dataURL)
                                    if(files[unique_id]){
                                        files[unique_id].push({baseData:dataURL,instance_id: value.id})
                                    }
                                    else{
                                        files[unique_id] = []
                                        files[unique_id].push({baseData:dataURL,instance_id: value.id})
                                    }
                                })
                                PropertyRoomImageDropzone.emit("complete", mockFile);
                            
                            });
                            
                        }
                    }
                ).done(function() { console.log('Request done!'); 
                }).fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });
        }

        
    }

    const handleSelectOnChnage = () => {
        
        
        // let room_elements = document.querySelectorAll('[data-dynamic-room="room_types"]')

        // room_elements.forEach(room_element => {

        //     $(room_element).on('change', function() {

        //         let current_unique_id = room_element.parentNode.parentNode.parentNode.parentNode.getAttribute('data-room-unique')

        //         console.log('Change event triggered!', current_unique_id   );
        //         // alert('Changed! Selected value: ' + $(this).val());
        //     });


        // })






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
            console.log(">11111111111111111111111")
        }
    }



    


    const generateNewRoom = () => {

        let property_room = document.getElementById('NewPropertyRoomRow');
        let rooms = document.querySelectorAll('[data-dynamic-room="room-details"]')
        console.log(rooms)
        if(rooms && rooms.length){
            uniqueId = parseInt(rooms[rooms.length -1].getAttribute('data-room-unique')) + 1

        }
        else{
            uniqueId = uniqueId + 1;
        }

        var html = `
        <div data-dynamic-room="room-details" data-room-unique="${uniqueId}" class="add-room-div card-body pt-0" style="border: 3px solid #ccc; padding: 20px; margin: 20px 0; border-radius: 20px; background-color: #f8f9fa;" id="${uniqueId}">
            <div class="d-flex mb-4 flex-wrap gap-5 mt-10" >
                ${uniqueId}.
                <div class="fv-row w-100 flex-md-root">
                    <div class="mb-5 fv-row">
                        <label class="required form-label">Room Type</label>
                        <select class="form-select mb-2" data-dynamic-room="room_types" id="room_type_${uniqueId}" name="room_type_${uniqueId}" data-handle-select-change="display_on" data-control="select2"  data-hide-search="false" data-placeholder="Select display on ">
                            <option ></option>
                            ${room_type_options}
                        </select>
                        <span class='text-danger' id='room_type_span_${uniqueId}' ></span>
                    </div>
                </div>
                <div class="fv-row w-100 flex-md-root">
                    <div class="mb-5 fv-row">
                        <label class="required form-label">Facility</label>
                        <select class="form-select mb-2" name="room_facility_${uniqueId}" data-handle-select-change="display_on" data-control="select2"  data-hide-search="false" data-placeholder="Select display on " multiple>
                            <option  ></option>
                            <option value="all">Select all</option>
                            ${room_facility_options}
                        </select>
                        <span class='text-danger' id='facility_span_${uniqueId}' ></span>
                    </div>
                </div>
                <div class="fv-row w-100 flex-md-root">
                    <div class="mb-5 fv-row">
                        <label class="required form-label">Description</label>
                        <textarea id="description"  class="form-control" name="description_${uniqueId}" placeholder="Enter Description"  maxlength="250"></textarea>
                        <div class="error-message" style="color: red;"></div>
                        <span class='text-danger' id='desc_span_${uniqueId}' ></span>
                    </div>
                </div>
            </div>
        
            <div class="d-flex mb-4 flex-wrap gap-5 mt-10">
                <div class="fv-row w-100 flex-md-root">
                    <div class="mb-5 fv-row" style="padding-left: 26px;">
                        <label class="form-label">Room Size</label>
                        <input type="text" name="room_size_${uniqueId}" value="" class="form-control mb-2" placeholder="Enter Room Size" />
                    </div>
                </div>
                <div class="fv-row w-100 flex-md-root">
                    <div class="mb-5 fv-row">
                        <label class="required form-label">Price</label>
                        <input type="text" name="price_${uniqueId}" value="" class="form-control mb-2" placeholder="Enter Price" maxlength="6"  oninput="this.value = this.value.replace(/[^0-9]/g, '');"/>
                        <span class='text-danger' id='price_span_${uniqueId}' ></span>
                        </div>
                </div>
                <div class="fv-row w-100 flex-md-root">
                    <div class="mb-5 fv-row">
                        <label class="required form-label">Room Count</label>
                        <input type="text" name="room_count_${uniqueId}" value="" class="form-control mb-2" placeholder="Enter Room Count" maxlength="6" oninput="this.value = this.value.replace(/[^0-9]/g, '');"/>
                        <span class='text-danger' id='room_count_span_${uniqueId}' ></span>
                        </div>
                </div>
            </div>
            <div class="fv-row" style="padding-left: 26px;">
                <div class="dropzone property_room_images_dropzone_${uniqueId}" id="property_room_images_dropzone_${uniqueId}">
                    <div class="dz-message needsclick">
                        <i class="bi bi-file-earmark-arrow-up text-primary fs-3x"></i>
                        <div class="ms-4">
                            <h3 class="fs-5 fw-bold text-gray-900 mb-1">Drop files here or click to upload.</h3>
                        </div>
                    </div>
                </div>
                <span class="fs-7 fw-semibold text-gray-400" id="uploadInfo" >Dimensions 432 x 263px , .jpeg, .jpg, .png are accepted.</span>
                <span class="fs-7 fw-semibold text-gray-400 required" id="uploadInfo" >Upload up to 5 files (max 1MB each)</span>
            </div>
            <button id="DeleteRoomButton" data-control-room="delete_room_buttons" class="btn btn-danger mt-10" style='margin-left: 24px;'>Delete</button>
        </div>`;
        property_room.insertAdjacentHTML('beforeend', html);
        
        
        
        $('[data-control="select2"]').select2();
        
        
        

        handleDropzonePropertyRoomImages(uniqueId)

        const buttons = document.querySelectorAll('[data-control-room="delete_room_buttons"]')
        buttons.forEach(btn => {

            btn.addEventListener('click', function(e) {

                e.preventDefault();
                if (buttons.length > 1) {
                    btn.parentNode.remove();
                } else {
                    Swal.fire({
                        html: "At least one Room must be present.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    });
                }

            })

        });

        


        handleSelectOnChnage()


    }


    const generateFormBlockChange = () => {
        const generateFormBlock = document.getElementById('add_new_room_btn');

        generateFormBlock.addEventListener('click', event => {
            event.preventDefault();
        // let properties = document.querySelectorAll('[data-dynamic-room="room-details"]')
        // let index = properties[properties?.length-1].getAttribute('data-room-unique');

        // let room_type = document.getElementById(`room_type_${index}`);
        // let facility = document.querySelector(`[name="room_facility_${index}"]`);
        // let desc = document.querySelector(`[name="description_${index}"]`);
        // let room_count = document.querySelector(`[name="room_count_${index}"]`);
        // let price = document.querySelector(`[name="price_${index}"]`);
        // console.log("111111111111111111111111111111", room_type.value)
        // if(room_type.value == ''){
        //     let span = document.getElementById(`room_type_span_${index}`)
        //     span.innerHTML = 'This field is required.'
        //     return false;
        // }
        // else{
        //     let span = document.getElementById(`room_type_span_${index}`)
        //     span.innerHTML = ''
        // }

        // if(facility.value == ''){
        //     let span = document.getElementById(`facility_span_${index}`)
        //     span.innerHTML = 'This field is required.'
        //     return false;
        // }
        // else{
        //     let span = document.getElementById(`facility_span_${index}`)
        //     span.innerHTML = ''
        // }
        
        // if(desc.value == ''){
        //     let span = document.getElementById(`desc_span_${index}`)
        //     span.innerHTML = 'This field is required.'
        //     return false;
        // }
        // else{
        //     let span = document.getElementById(`desc_span_${index}`)
        //     span.innerHTML = ''
        // }
        
        // if(price.value == ''){
        //     let span = document.getElementById(`price_span_${index}`)
        //     span.innerHTML = 'This field is required.'
        //     return false;
        // }
        // else{
        //     let span = document.getElementById(`price_span_${index}`)
        //     span.innerHTML = ''
        // }
        // if(room_count.value == ''){
        //     let span = document.getElementById(`room_count_span_${index}`)
        //     span.innerHTML = 'This field is required.'
        //     return false;
        // }
        // else{
        //     let span = document.getElementById(`room_count_span_${index}`)
        //     span.innerHTML = ''
        // }


        // if(files[index] && files[index].length){

        // }
        // else{
        //     return false;
        // }
            generateNewRoom()


            
            animateScroll(document.body.scrollHeight, 500);

            // // Optional: If you want to continuously scroll, you can use a setInterval
            // var scrollInterval = setInterval(function() {
            //     window.scrollTo(0, document.body.scrollHeight);
            // }, 100); // Adjust the interval (milliseconds) as needed

            // // Optional: Stop scrolling after a certain duration (e.g., 5000 milliseconds)
            // setTimeout(function() {
            //     clearInterval(scrollInterval);
            // }, 100); // Adjust the duration as needed
            
            
        });


        

    }

    
    // Public methods
    return {
        init: function () {

            // categoryElement = document.querySelector('[data-control-select-option="category"]')
            // brandElement = document.querySelector('[data-control-select-option="brand"]')
            // modelElement = document.querySelector('[data-control-select-option="model"]')
            // trimElement = document.querySelector('[data-control-select-option="trim"]')
            
            handleSubmit();
            handleDropzone();
            handleSelectOnChnage();
            generateFormBlockChange()
            let rooms = document.querySelectorAll('[data-dynamic-room="room-details"]')
            if(rooms.length == 0){
                generateNewRoom()
            }
            else{
                rooms.forEach(room => {
                    handleDropzonePropertyRoomImages(room.getAttribute('data-room-unique'))
                })
            }
            $('#add_new_room_btn').hide()
            $('#create-or-update-vehicle-submit').hide()
            $('#previous_page_btn').hide()


            // $('[data-control="select2"]').select2();



        
            

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
    // let place = document.querySelector('[data-google-place="place"]')
    
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





function onlyNumberKey(evt) {
    
    // Only ASCII character in that range allowed
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
        return false;
    return true;
}



// function SendPropertyRoomDetails(data) {
//     // Replace 'your_api_endpoint' with the actual URL of your backend API
//     const apiUrl = "{% url 'property_management:save.property.room' %}";
//     const csrfToken = api_config.csrfmiddlewaretoken;
//     fetch(apiUrl, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken, 
//         },
//         body: JSON.stringify(data),
//     })
//     .then(response => response.json())
//     .then(responseData => {
//         // Handle the response from the backend
//         console.log('Response from backend:', responseData);
//     })
//     .catch(error => {
//         // Handle any errors that occurred during the fetch
//         console.error('Error:', error);
//     });
// }


function getSelectedValues(selector) {
    // Get the selected options from the multiselection box
    let selectedOptions = document.querySelectorAll(`${selector} option:checked`);

    // Extract values and store them in an array
    let selectedValues = Array.from(selectedOptions).map(option => option.value);

    return selectedValues;
}







function animateScroll(to, duration) {
    var start = window.scrollY;
    var change = to - start;
    var startTime = performance.now();

    var animateInterval = 10; // adjust the interval as needed

    function animate() {
        var elapsed = performance.now() - startTime;
        var progress = elapsed / duration;

        window.scrollTo(0, start + change * progress);

        if (progress < 1) {
            // Continue the animation by setting another interval
            setTimeout(animate, animateInterval);
        }
    }

    // Start the animation by setting the first interval
    animate();
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
function toggleButtons(type){
    console.log('here')
    if(type == 'property'){
        $('#add_new_room_btn').hide()
        $('#create-or-update-vehicle-submit').hide()
        $('#previous_page_btn').hide()
        $('#next_page_btn').show()
        
    }
    else if(type == 'room'){
        $('#add_new_room_btn').show()
        $('#create-or-update-vehicle-submit').show()
        $('#next_page_btn').hide()
        $('#previous_page_btn').show()
    }
}









