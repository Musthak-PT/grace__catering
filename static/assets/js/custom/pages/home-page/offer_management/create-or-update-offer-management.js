"use strict";
// Class definition
var MCUpdateOrCreateVehicle = function () {

    var validator;
    var form;

    var brandElement,categoryElement;


    const handleSubmit = () => {
        

        // Get elements
        form = document.getElementById('create-or-update-vehicle-form');
        const submitButton = document.getElementById('create-or-update-offer-management-submit');


        var isImageEdit = document.getElementById('offer-image-view').dataset.imageEdit === 'true';
        var validatorsConfig  = 
            {
                fields: {
                    
                    property_name: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    title: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    start_date: {
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
                    end_date: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    room_name: {
                        validators: {
                            dynamicValidation: {
                                // Custom validator for dynamic validation
                                message: 'This field is required',
                                callback: function () {
                                    // Check if Property Name field is selected and Room field is empty
                                    return roomSelect.value.trim() === '' && roomId.value.trim() === '';
                                }
                            }
                        }
                    },
                    'offer_image': {
                        validators: {
                            file: {
                                extension: 'jpg,jpeg,png',
                                type: 'image/jpeg,image/png',
                                maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                                message: 'The selected file is not valid or is above 1 MB'
                            },
                            notEmpty: {
                                message: 'This field is required'
                            },
                            image: {
                                width: 670,
                                height: 350,
                                message: 'The image must be exactly 670 x 350 pixels'
                            }
                        }
                    },
                    
                    percentage: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            numeric : {
                                message : 'The value is not a number'
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
        ;

        if (isImageEdit) {
            console.log(validatorsConfig)
            delete validatorsConfig.fields['offer_image'].validators.notEmpty;
        }
        var validator = FormValidation.formValidation(form, validatorsConfig);


        roomSelect.addEventListener('change', function () {
            // Trigger re-validation when Property Name field changes
            validator.revalidateField('room_name');
        });
    
        roomId.addEventListener('change', function () {
            // Trigger re-validation when Room field changes
            validator.revalidateField('room_name');
        });
    
        submitButton.addEventListener('click', function (e) {
            e.preventDefault();
    
            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    console.log('validated!');
    
                    submitButton.setAttribute('data-kt-indicator', 'on');
                    // Disable button to avoid multiple clicks
                    submitButton.disabled = true;
    
                    if (status === 'Valid') {
                        
                        // Handle successful submission
                        form.submit();
                    } else {
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
    
    
        validator = FormValidation.formValidation(form, validatorsConfig);

        submitButton.addEventListener('click', e => {
            e.preventDefault();

            // Validate form before submit
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

                        // Redirect to customers list page
                        form.submit();
                    } else {
                        submitButton.removeAttribute('data-kt-indicator');

                        // Enable button
                        submitButton.disabled = false;
                        Swal.fire({
                            html: "Please enter required fields",
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




    const handleSelectOnChnage = () => {

        if(typeof api_config?.vehicle_data?.category_id  !== 'undefined')
        {
            generateSelectOptionElement({pk:api_config?.vehicle_data?.category_id, api_url : `${api_config.get_city}`, tagElement: brandElement, elementEdit_id: api_config?.vehicle_data?.brand_id})
        }
        $(categoryElement).on('change', e => {
            handleResetSelectOptions({elements: {brandElement}})
            generateSelectOptionElement({pk:e.target.value, api_url : `${api_config.get_city}`,tagElement: brandElement})

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
                        if(elementEdit_id === value?.id)
                        {
                            subOptionElement.setAttribute('selected','selected')
                        }
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
            categoryElement = document.querySelector('[data-control-select-option="property-name"]')
            brandElement    = document.querySelector('[data-control-select-option="room-name"]')
            handleSubmit();
            handleSelectOnChnage();
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateVehicle.init();
});

