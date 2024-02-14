
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
        form = document.getElementById('create-or-update-company-profile-form');
        const submitButton = document.getElementById('create-or-update-company-profile-submit');
    
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
                        const btn = document.getElementById('create-or-update-company-profile-submit');
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
        const handleDropzone = () => {

            dropZone_is=false
            let PropertyImageDropzone = new Dropzone("#vehicle_images_dropzone", {
                url: `${api_config.vehicle_image_upload_api_url}`,
                acceptedFiles: ".jpeg,.jpg,.png",
                maxFiles: 5,
                paramName: "file",
                maxFilesize: 10, // MB
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
    
                    }); 
                }
            });
    
    
    
            PropertyImageDropzone.on("addedfile", file => {
                let instance_id = file?.instance_id;
                let childElements = file?.previewElement?.children;
                childElements.forEach(childElement => {
                    childElement.setAttribute('instance_id', instance_id);
                    childElement.setAttribute('action_type', 2);
                });
            });
            
    
            $.post(`${api_config.get_vehicle_images_api_url}`, { vehicle_id: `${api_config.vehicle_id}` }, 
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



    
    // Public methods
    return {
        init: function () {
            handleSubmit();
            handleDropzone();
            handleSelectOnChnage();

            
        }
    };
}();




// On document ready
KTUtil.onDOMContentLoaded(function () {
    MCUpdateOrCreateProperty.init();
});



