"use strict";

var files = []

// Class definition
var MCUpdateOrCreateVehicle = function () {

    var validator;
    var form;

    
    var uniqueId = 0
    var userUniqueId = 0
    var brandElement, categoryElement, modelElement, trimElement, rooms;
    var dropZone_is;
    var is_edit_mode = false

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
                    address: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    check_in: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    checkout: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                
                    phone: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            numeric : {
                                message : 'The value is not a number'
                            },
                        }
                    },
                    address: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
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

        function hasEmptyValue(data) {
            for (let i = 0; i < data.length; i++) {
                const entry = data[i];
                for (const key in entry) {
                    if (Array.isArray(entry[key])) {
                        // Check if the value is an array
                        if (entry[key].some(item => Object.values(item).some(value => value === '' || value === undefined))) {
                            return true;
                        }
                    } else {
                        // Check if the value is empty or undefined
                        if (entry[key] === '' || entry[key] === undefined) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }
        submitButton.addEventListener('click', e => {
            e.preventDefault();
            let masterData = []
            let rooms = document.querySelectorAll('[data-dynamic-room="room-details"]')
            rooms.forEach(room => {
                let unique_id = room.getAttribute('data-room-unique')
                let room_no = document.querySelector(`[name=room_number_${unique_id}]`).value;
                let property_name = document.querySelector(`[name=property_name_${unique_id}]`).value;
                let room_name = document.querySelector(`[name=room_name_${unique_id}]`).value;
                let no_of_adults = document.querySelector(`[name=no_of_adults_${unique_id}]`).value;
                let no_of_childrens = document.querySelector(`[name=no_of_childrens_${unique_id}]`).value;
                let custData = []
                let customerDetails = document.querySelectorAll(`[data-customer-details="customer-details_${unique_id}"]`)

                customerDetails.forEach(cust => {
                    
                    let unique_user_id = cust.getAttribute('user-unique-id')
                    let full_name      = document.querySelector(`[name=full_name_${unique_user_id}]`).value;
                    let email          = document.querySelector(`[name=email_${unique_user_id}]`).value;
                    let phone_number   = document.querySelector(`[name=phone_number_${unique_user_id}]`).value;
                    let dob            = document.querySelector(`[name=dob_${unique_user_id}]`).value;
                    let edit_file      = document.querySelector(`[name=document_base_64_${unique_user_id}]`)?.value;

                    custData.push({
                        full_name : full_name,
                        email : email,
                        phone_number : phone_number,
                        dob : dob,
                        documents : files[unique_user_id]==undefined?edit_file:files[unique_user_id] 
                    })
                })
                masterData.push({
                    room_sl_no  : room_no,
                    property_name : property_name,
                    room_name : room_name,
                    no_of_adults : no_of_adults,
                    no_of_childrens : no_of_childrens,
                    customer_details : custData
                })
            })

            let is_validate =  hasEmptyValue(masterData)
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
                let jsonString = JSON.stringify(masterData);
                let booked_room_details_and_document =  document.querySelector(`[name="booked_room_details_and_document"]`);
                booked_room_details_and_document.setAttribute('value', jsonString)

                    
                if (validator) {
                    validator.validate().then(function (status) {
                        
                        console.log('validated!');
                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable button to avoid multiple click
                        submitButton.disabled = true;

                        if (status == 'Valid') {
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
                                html: "Please enter the required fields!!!!!!!!!",
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









    const handleDropzone = (unique_id) => {
        let fileCount = 0;
        dropZone_is=false

        let PropertyImageDropzone = new Dropzone(`#property_room_images_dropzone_${unique_id}`, {
            url: `${api_config.property_image_upload_api_url}`,
            acceptedFiles: ".jpeg,.jpg,.png,.pdf",
            maxFiles: '1',
            paramName: "file",
            uploadMultiple: false,
            maxFilesize: 1, // MB
            addRemoveLinks: true,
            accept: function(file, done) {
                try {
                    let test = null
                    convertImageToBase64(file)
                    .then(base64Data => {
                        // Here, you have access to the base64 data
                        let testDAta = this.files.reverse()
                        testDAta.map((item,ind)=>{
                            if(ind!=0){
                                this.removeFile(item)
                            }
                        })
                        this.files = [testDAta[0]]
                        files[unique_id] = base64Data;
                        console.log(this.files,'sucesss.....',[testDAta[0]], files);

                    })
                    .catch(error => {
                        console.error('Error occurred during image conversion:', error);
                    });

                } catch (error) {
                    console.error('Error occurred during image conversion:', error);
                }
            },
            init: function() {


                this.on("addedfile", function(file) {
                    
                    console.log('this.files.length', this.files.length, 'is_edit_mode', !is_edit_mode);

                    if (this.element.children.length != 2) {
                        const children = this.element.children;
                        for (let i = 0; i < children.length; i++) {
                            const child = children[i];
                            if (!child.classList.contains("dz-message") || !child.classList.contains("needsclick")) {
                                child.remove();
                                is_edit_mode = false

                            }
                        }

                    }

                    
                });
                this.on("maxfilesexceeded", function (data) {
                    let res = eval('(' + data.xhr.responseText + ')');
                });
                this.on("error", function (file, message) {
                    // this.removeFile(file);

                });
                this.on("processingmultiple", function (file, message) {
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
                    console.log(this)
                    let removeElement = file.previewElement.getElementsByTagName('a')?.[0];
                    let instance_id = removeElement.getAttribute('instance_id')
                    let action_type = removeElement.getAttribute('action_type')
                    $.post(`${api_config.temporary_image_destroy_api_url}`, { id: instance_id, action_type:action_type }, 
                        function(data, status, xhr) {
                            // if (PropertyImageDropzone.files.length <= 0) {
                            //     dropZone_is = true
                            // }

                        }).done(function() { console.log('Request done!'); })
                        .fail(function(jqxhr, settings, ex) { console.log('failed, ' + ex); });

                }); 
            }
        });






        PropertyImageDropzone.on("addedfile", file => {
            console.log('added')
            if(files[unique_id]?.length){
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
        let customer = document.querySelector(`[data-customer-unique-id='customer-unique-id${unique_id}']`)
        
        if (customer){
            $.post(`${api_config.get_customer_images_api_url}`, { pk: customer.getAttribute('data-customer-id') }, 
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
    


    const handleSelectOnChnage = (id,e) => {
        let tag = document.querySelector(`[data-control-select-option="room-name_${id}"]`) 
        if(typeof api_config?.vehicle_data?.category_id  !== 'undefined')
        {
            handleResetSelectOptions({elements: tag})
            generateSelectOptionElement({pk:api_config?.vehicle_data?.category_id, api_url : `${api_config.get_city}`, tagElement: tag, elementEdit_id: api_config?.vehicle_data?.brand_id})
        }
        handleResetSelectOptions({elements: {tag}})
        generateSelectOptionElement({pk:e.target.value, api_url : `${api_config.get_city}`,tagElement: tag})
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
            <div data-dynamic-room="room-details" data-room-unique='${uniqueId}'  class="add-room-div card-body pt-0" style="border: 3px solid #ccc; padding: 20px; margin: 20px 0; border-radius: 20px; background-color: #f8f9fa;" id="${uniqueId}">
                <div class="d-flex mb-4 flex-wrap gap-5 mt-10" >
                    <div class="fv-row w-100 flex-md-root" style="padding-left: 26px;">
                        <div class="mb-5 fv-row">
                            <label class="required form-label">Room Number</label>
                            <input type="text" name="room_number_${uniqueId}"  class="form-control mb-2" placeholder="Enter Room Number" />
                        </div>
                    </div>
                    <div class="fv-row w-100 flex-md-root">
                        <div class="mb-5 fv-row">
                            <label class="required form-label">Property</label>
                            <select class="form-select mb-2 property-select-class" data-control-select-option="property-name" data-dynamic-room="room_types" id="property_name_${uniqueId}" name="property_name_${uniqueId}" data-unique-id='${uniqueId}' data-handle-select-change="display_on" data-control="select2"  data-hide-search="false" data-placeholder="Select display on ">
                                <option ></option>
                                ${property_options}
                            </select>
                        </div>
                    </div>
                    <div class="fv-row w-100 flex-md-root">
                        <div class="mb-5 fv-row">
                            <label class="required form-label">Rooms</label>
                            <select class="form-select mb-2" data-control-select-option="room-name_${uniqueId}" name="room_name_${uniqueId}" data-handle-select-change="display_on" data-control="select2"  data-hide-search="false" data-placeholder="Select display on ">
                                <option  ></option>
                                ${room_options}
                            </select>
                        </div>
                    </div>
                    <div class="fv-row w-100 flex-md-root" style="padding-left: 26px;">
                        <div class="mb-5 fv-row">
                            <label class="required form-label">Number of Adults</label>
                            <input type="text" name="no_of_adults_${uniqueId}"  class="form-control mb-2" placeholder="Number Of Adults" />
                        </div>
                    </div>
                    <div class="fv-row w-100 flex-md-root" style="padding-left: 26px;">
                        <div class="mb-5 fv-row">
                            <label class="required form-label">Number of Children</label>
                            <input type="text" name="no_of_childrens_${uniqueId}"  class="form-control mb-2" placeholder="Number Of Children" />
                        </div>
                    </div>
                </div>
                <div id='user_details_${uniqueId}'>
                    
                </div>
                <button id="add_user_details_${uniqueId}" unique-id="${uniqueId}" data-control-room="add_user_details" class="btn btn-primary mt-10">Add  new</button>
                    <button id="DeleteRoomButton" data-control-room="delete_room_buttons" class="btn btn-danger mt-10" style="margin-left: 26px;">Delete</button>
            </div>
        </div>`;

        property_room.insertAdjacentHTML('beforeend', html);
        $('[data-control="select2"]').select2();
        
        
        $('#property_name_'+uniqueId).on('change',function(e){
            const id =e.target.getAttribute('data-unique-id')
            console.log(id)
            handleSelectOnChnage(id,e)
        })

        // handleDropzonePropertyRoomImages(uniqueId)

        const buttons = document.querySelectorAll('[data-control-room="delete_room_buttons"]')
        // let selectBox = document.getElementById('property_name_' + uniqueId);
        buttons.forEach(btn => {

            btn.addEventListener('click', function(e) {

                e.preventDefault();
                const delbuttons = document.querySelectorAll('[data-control-room="delete_room_buttons"]')
                if (delbuttons.length > 1) {
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
        let propertySelect = document.getElementById(`property_name_${uniqueId}`);

// Add an onchange event listener to the select box
propertySelect.addEventListener('change', function() {
    // Your onchange logic here
    console.log("Selected property changed!");

    // Example: Get the selected option value
    let selectedValue = propertySelect.value;
    console.log("Selected Value: ", selectedValue);
    // Add your custom logic or function calls based on the selected value
});
        // console.log(selectBox)
        // debugger
        // selectBox.addEventListener('click', function() {
        //     console.log('88888888888888888888888')
        //     handleSelectOnChnage(uniqueId);


            
        // });

        


        genarateNewUserDEtails(uniqueId);
        attachUserDEtailsAddFuction(uniqueId)
    }

    
    const genarateNewUserDEtails = (id)=> {
        let userDiv = document.getElementById('user_details_' + id);
        let userDetails = document.querySelectorAll('[data-user-details="user_details"]')
        if(userDetails?.length == 0){
            userUniqueId = 0;
        }
        else{
            userUniqueId = parseInt(userDetails[userDetails?.length-1].getAttribute('user-unique-id')) + 1
        }
        let html = `
            <div class="card mt-6">
                <div class='row d-flex align-items-center' data-user-details='user_details' data-customer-uniqueid='customer-uniqueid${id}' data-customer-details='customer-details_${id}' user-unique-id='${userUniqueId}'>
                    <div class='col-lg-10'>
                        <div class="d-flex mb-4 mr-5 flex-wrap gap-5 mt-10">
                            <div class="fv-row w-100 flex-md-root" style="padding-left: 26px;">
                                <div class="mb-5 fv-row">
                                    <label class="required form-label">Full Name</label>
                                    <input type="text" name="full_name_${userUniqueId}"  class="form-control mb-2" placeholder="Enter Full Name" />
                                </div>
                            </div>
                            <div class="fv-row w-100 flex-md-root">
                                <div class="mb-5 fv-row">
                                    <label class="required form-label">Email</label>
                                    <input type="text" name="email_${userUniqueId}"  class="form-control mb-2" placeholder="Enter Email" />
                                </div>
                            </div>
                            <div class="fv-row w-100 flex-md-root">
                                <div class="mb-5 fv-row">
                                    <label class="required form-label">Phone Number</label>
                                    <input type="text" name="phone_number_${userUniqueId}"  class="form-control mb-2" placeholder="Enter Phone Number" />
                                </div>
                            </div>
                            <div class="fv-row w-100 flex-md-root">
                                <div class="mb-5 fv-row">
                                    <label for="" class="form-label required">Date of Birth</label>
                                    <input type="Date" class="form-control form-control" name="dob_${userUniqueId}" placeholder="Enter Date of Birth"/>
                                </div>
                            </div>
                        </div>
                        <div class="fv-row" style="padding-left: 26px;">
                            <div class="dropzone property_room_images_dropzone_${userUniqueId}" id="property_room_images_dropzone_${userUniqueId}">
                                <div class="dz-message needsclick">
                                    <i class="bi bi-file-earmark-arrow-up text-primary fs-3x"></i>
                                    <div class="ms-4">
                                        <h3 class="fs-5 fw-bold text-gray-900 mb-1">Drop files here or click to upload.</h3>
                                    </div>
                                </div>
                            </div>
                            <span class="fs-7 fw-semibold text-gray-400" id="uploadInfo" >Dimensions 432 x 263px , .jpeg, .jpg, .png are accepted.</span>
                            <span class="fs-7 fw-semibold text-gray-400" id="uploadInfo" >Upload up to 5 files (max 1MB each)</span>
                            
                        
                        </div>
                    </div>
                    <div class='col-lg-2'>
                        <div class='text-center'>
                            <button type='button'  delete-id='${userUniqueId}' data-control-room="delete_user_details" class="btn btn-danger mt-10 delete_user_details" onclick='deleteUserDEtails(${userUniqueId})' >Delete</button>
                        </div>
                    </div>
                </div>
            </div>
                `
    
        userDiv.insertAdjacentHTML('beforeend', html);
        handleDropzone(userUniqueId);
    }
    const attachUserDEtailsAddFuction = (dataid)=>{
        const generateFormBlock = document.getElementById('add_user_details_' + dataid);
            generateFormBlock.addEventListener('click', event => {
                event.preventDefault();
                let id = generateFormBlock.getAttribute('unique-id') 
                genarateNewUserDEtails(id);


                
            });
    }
    const attachRoomDEtailsAddFuction = ()=>{
        const generateFormBlock = document.getElementById('add_new_room_btn');
            generateFormBlock.addEventListener('click', event => {
                event.preventDefault();

                generateNewRoom();


                
                animateScroll(document.body.scrollHeight, 500);

            
            });
    }


    return {
        init: function () {

            brandElement = document.querySelector('[data-control-select-option="room-name"]')
            if(api_config.booked_room_id){
                is_edit_mode = true
                const buttons = document.querySelectorAll('[data-control-room="delete_room_buttons"]')
                const addbuttons = document.querySelectorAll('[data-dynamic-room="room-details"]')
                buttons.forEach(btn => {
                    btn.addEventListener('click', function(e) {
                        e.preventDefault();
                        const delbuttons = document.querySelectorAll('[data-control-room="delete_room_buttons"]')
                        if (delbuttons.length > 1) {
                            btn.parentNode.remove();
                        } else {
                            alert("At least one Room must be present.");
                        }
                    })
                });
                addbuttons.forEach(btn => {
                    attachUserDEtailsAddFuction(btn.getAttribute('data-room-unique'))
                })
            }
            else{
                generateNewRoom()
            }
            handleSubmit();
            attachRoomDEtailsAddFuction()



            $('#add_new_room_btn').hide()
            $('#create-or-update-vehicle-submit').hide()
            $('#previous_page_btn').hide()

            $('.room-details-edit').on('change',function(e){
                const id =e.target.getAttribute('data-unique-id')
                console.log(id)
                handleSelectOnChnage(id,e)
            })


            // let customers = document.getElementsByClassName('customer-edit-details')
            // $.each(customers, function (key,value) {
            //     handleDropzone(value.getAttribute('user-unique-id'))
            // })
            
            // console.log('customers "??????????? ', customers)

            let customers = document.querySelectorAll('[data-coustomer_loopcount]')
            customers.forEach(customer => {
                
                let coustomer_loopcount = customer.getAttribute('data-coustomer_loopcount')
            
                handleDropzone(coustomer_loopcount)
            })
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



function onlyNumberKey(evt) {
    
    // Only ASCII character in that range allowed
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
        return false;
    return true;
}





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
function convertImageToBase641(file, callback) {
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

  function convertImageToBase64(file) {
    return new Promise((resolve, reject) => {
        // Check if a file is selected
        if (file) {
            // Create a FileReader object
            var reader = new FileReader();

            // Set a callback function to handle the file reading
            reader.onload = function (e) {
                // Get the base64 data
                var base64Data = e.target.result;
                resolve(base64Data);
            };

            // Set a callback function to handle errors
            reader.onerror = function (error) {
                reject(error);
            };

            // Read the selected file as Data URL (base64)
            reader.readAsDataURL(file);
        } else {
            reject(new Error('Please select an image file.'));
        }
    });
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









