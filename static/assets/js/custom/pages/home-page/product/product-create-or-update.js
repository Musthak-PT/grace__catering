"use strict";

// Class definition
var MCUpdateOrCreateAdmin = function () {
    const handleSubmit = () => {
        let validator;

        // Get elements
        const form = document.getElementById('create-or-update-campaign-form');
        const submitButton = document.getElementById('create-or-update-campaign-submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    'header': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[A-Za-z ]+$/,
                                message: 'Only characters and spaces are allowed'
                            }
                        }
                    },
                    'sub_title': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[A-Za-z ]+$/,
                                message: 'Only characters and spaces are allowed'
                            }
                        }
                    },
                    'spending_amount': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[0-9]+(\.[0-9]+)?$/,
                                message: 'Only numbers and a decimal point are allowed'
                            }
                        }
                    },
                    'tac': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'communication_platform': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            }
                        }
                    },
                    'discount': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[0-9]+(\.[0-9]+)?$/,
                                message: 'Only numbers and a decimal point are allowed'
                            }
                        }
                    },
                    'points': {
                        validators: {
                            notEmpty: {
                                message: 'This field is required'
                            },
                            regexp: {
                                regexp: /^[0-9]+(\.[0-9]+)?$/,
                                message: 'Only numbers and a decimal point are allowed'
                            }
                        }
                    },
                    'schedule_time': {
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
                },
            }
        );

        submitButton.addEventListener('click', (e) => {
            e.preventDefault();

            // Validate form before submit
            if (validator) {
                validator.validate().then((status) => {
                    console.log('validated!');
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;

                    if (status === 'Valid') {
                        // Handle submit button
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
                            html: "Please Enter Required Fields",
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
    };

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
