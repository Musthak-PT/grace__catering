"use strict";
// Class definition
var MCUpdateOrCreateVehicle = function () {

    var validator;
    var form;
    var brandElement,categoryElement;


    const handleSubmit = () => {


        // Get elements
        form = document.getElementById('create-or-update-customer-promotion-form');
        const submitButton = document.getElementById('create-or-update-customer-promotion-submit');


        var isImageEdit = document.getElementById('promotion-image-view').dataset.imageEdit === 'true';
        var validatorsConfig  = 
            {
                fields: {
                    
                    title: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    subject: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    message: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    customers: {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    
                    'promotion_image': {
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
            delete validatorsConfig.fields['promotion_image'].validators.notEmpty;
        }
        var validator = FormValidation.formValidation(form, validatorsConfig);

    
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
    
    
        
        // Initialize the form validation
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

            categoryElement = document.querySelector('[data-control-select-option="property-name"]')
            brandElement = document.querySelector('[data-control-select-option="room-name"]')


            handleSubmit();

        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateVehicle.init();
});