"use strict";

// Class definition
var MCUpdateOrCreateAdmin = function () {
    
    const handleSubmit = () => {
        let validator;
        

        // Get elements
        const form = document.getElementById('create-or-update-admin-form');
        const submitButton = document.getElementById('create-or-update-admin-submit');


        var isImageEdit = document.getElementById('testimonial-image-view').dataset.imageEdit === 'true';
        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    // 'title': {
                    //     validators: {
                    //         notEmpty: {
                    //             message: 'This field is required'
                    //         }
                    //     }
                    // },
                    'full_name': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[A-Za-z\s]+$/, // Allow characters and spaces
                                message: 'Only characters and spaces are allowed'
                            }
                        }
                    },
                    'description': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                        }
                    },

                    'testimonial_image': {
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

                    // 'testimonial_image': {
                    //     validators: {
                    //         file: {
                    //             extension: 'jpg,jpeg,png',
                    //             type: 'image/jpeg,image/png',
                    //             maxSize: 1024 * 1024, // Maximum file size in bytes (1 MB)
                    //             message: 'The selected file is not valid or is above 1 MB'
                    //         },
                    //         notEmpty: {
                    //             message: 'This field is required'
                    //         }
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

        if (isImageEdit) {
            delete validator.fields['testimonial_image'].validators.notEmpty;
        }

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

    
    // Public methods
    return {
        init: function () {
            handleSubmit();
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateAdmin.init();
});