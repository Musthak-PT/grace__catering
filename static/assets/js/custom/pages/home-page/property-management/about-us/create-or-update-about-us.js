function previewImage(event) {
    var logoPreview = document.getElementById('logo-preview');
    logoPreview.src = URL.createObjectURL(event.target.files[0]);
    logoPreview.style.display = "block";
}


"use strict";

// Class definition
var MCUpdateOrCreateProperty = function () {

var validator;

var form;
const handleSubmit = () => {
    // Get elements
    form = document.getElementById('create-or-update-about-us-form');
    const submitButton = document.getElementById('create-or-update-about-us-submit');

    validator = FormValidation.formValidation(
        
        form,
        {
            
            
            fields: {
                'title': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                },
                'description': {
                    validators: {
                        notEmpty: {
                            message: 'This field is required'
                        }
                    }
                }
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
                
                console.log('validated!');
                submitButton.setAttribute('data-kt-indicator', 'on');

                // Disable button to avoid multiple click
                submitButton.disabled = true;

                if (status == 'Valid') {

                    // Handle submit button
                    e.preventDefault();
                    const btn = document.getElementById('create-or-update-about-us-submit');
                    const text = document.getElementById('banner-loader-text');
                    btn.disabled = true;
                    btn.style.display = 'none';
                    text.style.display = 'block';
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
MCUpdateOrCreateProperty.init();
});

