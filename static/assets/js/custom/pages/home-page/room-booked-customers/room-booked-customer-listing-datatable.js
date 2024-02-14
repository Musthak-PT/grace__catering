function openImagePopup(fileUrl) {
    let fileType;
    
    if (fileUrl.endsWith('.pdf')) {
        fileType = 'pdf';
    } else if (fileUrl.match(/\.(jpeg|jpg|gif|png)$/) != null) {
        fileType = 'image';
    } else {
        // You can handle other file types here if needed
        console.error('Unsupported file type');
        return;
    }

    const content = fileType === 'pdf' ?
        `<div style="position: relative;">
            <iframe src="${fileUrl}" type="application/pdf" width="100%" height="100%"></iframe>
        </div>` :
        `<div style="position: relative;">
            <img id="previewImage" src="${fileUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain;" />
        </div>`;

    const popupContent = `${content}
        <div style="position: absolute; top: 10px; right: 10px;">
            <button class="close-button" onclick="Swal.close()" style="background: transparent; border: none; color: #000; font-size: 20px; cursor: pointer;">×</button>
        </div>
        <div style="position: absolute; bottom: 10px; right: 10px;">
            <a href="${fileUrl}" download class="download-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16">
                    <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5"/>
                    <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708z"/>
                </svg>
            </a>
        </div>`;

    Swal.fire({
        html: popupContent,
        showConfirmButton: false,
        customClass: {
            popup: 'file-preview-popup',
            image: 'file-preview-image'
        },
        width: '40%', 
        height: '40%',
        padding: '15px',
        scrollbarPadding: false
    });
}








"use strict";

// Class definition
var DatatablesServerSide = function() {
    // Shared variables
    var table;
    var dt;

    // Private functions
    var initDatatable = function() {
        dt = $("#company-profile-datatable").DataTable({
            searchDelay: 500,
            serverSide: true,
            responsive: true,
            pageLength: 25,
            processing: true,
            order: [
                [0, 'desc']
            ],
            select: {
                style: 'multi',
                selector: 'td:first-child input[type="checkbox"]',
                className: 'row-selected'
            },
            ajax: {
                method: "POST",
                url: `${api_config.datatable}`,
                data: {
                    'csrfmiddlewaretoken': `${api_config.csrfmiddlewaretoken}`,
                },
            },
            columns: [
                {data   : 'id'},
                {
                    data: null,
                    orderable: false,
                    searchable: false,
                    render: function (data, type, row, meta) {
                        return meta.row + 1 + meta.settings._iDisplayStart;
                    }
                }, 
                {data   : 'property_name'},
                {data   : 'roll_number'},
                {data   : 'name'},
                {data   : 'email'},
                {data   : 'phone'},
                {data   : 'check_in'},
                {data   : 'check_out'},
                {data   : 'document'},
            ],

            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data) {
                        return `
                            <div class="d-none form-check form-check-sm form-check-custom form-check-solid">
                                <input class="form-check-input checkbox-input-id" type="checkbox" value="${data}" />
                            </div>`;
                    }
                },
                {
                    targets: 2,
                    orderable: false,
                },
                {
                    targets: 3,
                    orderable: false,
                },
                {
                    targets: 4,
                    orderable: false,
                },
                {
                    targets: 5,
                    orderable: false,
                },
                {
                    targets: 6,
                    orderable: false,
                   
                },
                {
                    targets: 7,
                    orderable: false,
                   
                },
                {
                    searchable: true,
                    orderable: false,
                    targets: 9,
                    render: function(data, type, row) {
                        // Construct the HTML for the download button
                        let html = `<a href="#" class="document-icon" style="cursor:pointer;" onclick="openImagePopup('${data}')">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-arrow-down-fill" viewBox="0 0 16 16">
                                            <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1m-1 4v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 11.293V7.5a.5.5 0 0 1 1 0"/>
                                        </svg>
                                    </a>`;
                        return html;
                    }
                },
                
                
                
                {
                    searchable: true,
                    orderable: true,
                    targets: 2,
                    render: function(data, type, row) {
                        return `<div class="d-flex align-items-center">
                                    <div class="ms-5">
                                        <div class="text-gray-800 text-hover-primary fs-5 fw-bolder" >${data}</div>
                                    </div>
                                </div>`;
                    }
                },
            ],
            // Add data-filter attribute
            drawCallback: function(settings) {},
            createdRow: function(row, data, dataIndex) {
                $(row).find('td:eq(4)').attr('data-filter', data.CreditCardType);
            }
        });

        table = dt.$;
        // Re-init functions on every table re-draw -- more info: https://datatables.net/reference/event/draw
        dt.on('draw', function() {
            toggleToolbars();
            handleStatusFilter();
            ActiveOrIncativeUser();
            handlestartdateFilter();
            handleenddateFilter();
            // handleDownload();
            KTMenu.createInstances();
        });
    }

    // // Search Datatable --- official docs reference: https://datatables.net/reference/api/search()
    var handleSearchDatatable = function() {
        const filterSearch = document.querySelector('[data-users-table-filter="search"]');
        filterSearch.addEventListener('keyup', function(e) {
            dt.search(e.target.value).draw();
        });
    }
    // var handleDownload = function() {
    //     const downloadButton = document.querySelector('[name="download"]');
    //     downloadButton.addEventListener('click', function() {
    //         console.log('Download button clicked');
    
    //         // Make a POST request to the server to get the Excel data
    //         $.ajax({
    //             url: api_config.datatable,
    //             method: 'POST',
    //             data: { download: true },
    //             dataType: 'text',  // Set the dataType to handle binary data
    //             success: function(data, status, xhr) {
    //                 console.log('Download request completed');
    
    //                 // Create a Blob from the received data
    //                 var blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    
    //                 // Create a link element to trigger the download
    //                 var link = document.createElement('a');
    //                 link.href = window.URL.createObjectURL(blob);
    //                 link.download = 'customer_details.xlsx';
    //                 link.click();
    //             },
    //             error: function(xhr, status, error) {
    //                 console.error('Error during download request:', error);
    //             }
    //         });
    //     });
    // };
    function openImagePopup(imageUrl) {
        Swal.fire({
            text: "Are you sure you want to open the image?",
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: true,
            confirmButtonText: "Yes",
            cancelButtonText: "No, cancel",
            customClass: {
                confirmButton: "btn btn-primary",
                cancelButton: "btn btn-active-light"
            }
            
        }).then((result) => {
            if (result.isConfirmed) {
                // Fetch the file data as a Blob
                fetch(fileUrl)
                    .then(response => response.blob())
                    .then(blob => {
                        // Create a temporary link element
                        var link = document.createElement('a');
                        link.href = URL.createObjectURL(blob);
                        link.download = fileName || 'file';  // Use provided fileName or set a default
                        document.body.appendChild(link);
    
                        // Trigger a click on the link to initiate the download
                        link.click();
    
                        // Remove the temporary link element from the DOM
                        document.body.removeChild(link);
                    })
                    .catch(error => console.error('Error fetching file data:', error));
            }
        });
    }
    
    function closeImagePopup() {
        let popup = document.querySelector('.popup');
        popup.parentNode.removeChild(popup);
    }
    
    // // Handle status filter dropdown
    var handleStatusFilter = () => {
        const filterStatus = document.querySelector('[data-users-filter="status"]');
        $(filterStatus).on('change', e => {
            let value = e.target.value;
            if(value === 'all'){
                value = '';
            }
            
            dt.column(3).search(value).draw();
        });
    }

    // var handleDownload = function() {
    //     const downloadButton = document.getElementById('downloadButton');
    //     downloadButton.addEventListener('click', function() {
    //         console.log('Download button clicked');
    
    //         // Redirect to the download URL
    //         window.location.href = "{% url 'customer_management:download_customer_data' %}";
    //     });
    // };

    var handlestartdateFilter = () => {
        const filterStartDate = document.querySelector('[data-users-filter="startdate"]');
        $(filterStartDate).on('change', () => {
            let startDateValue = filterStartDate.value;

            dt.column(4).search(startDateValue).draw();
        });
    }
    var handleenddateFilter = () => {
        const filterEndDate = document.querySelector('[data-users-filter="enddate"]');
        $(filterEndDate).on('change', () => {
            let endDateValue = filterEndDate.value;
            dt.column(5).search(endDateValue).draw();
        });
    }
    
    var ActiveOrIncativeUser = ()=>{
        const activeButton = document.getElementsByClassName('active_inactive_language')
        activeButton.forEach(d => {
            d.addEventListener('click', function(e) {
                const activeId = $(this).data('id');
                e.preventDefault();
                Swal.fire({
                    text: "Are you sure you want to change status",
                    icon: "warning",
                    showCancelButton: true,
                    buttonsStyling: true,
                    confirmButtonText: "Yes",
                    cancelButtonText: "No, return",
                    customClass: {
                        confirmButton: "btn btn-primary",
                        cancelButton: "btn btn-active-light"
                    }
                }).then(function(result){
                    if(result.value){               
                        $.post(`${api_config.active_inactive_company}`, {id:activeId }, function(data, status, xhr) {
                            if (data.status_code == 200) {
                                Swal.fire({
                                    text: "Successfully changed status ",
                                    icon: "success",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                }).then(function() {
                                    dt.draw();
                                });
    
                            } else {
                                Swal.fire({
                                    text: "Something went wrong.",
                                    icon: "error",
                                    buttonsStyling: false,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn fw-bold btn-primary",
                                    }
                                });
                            }
                        })
                    }
                })
            });
        });
    }


    var toggleToolbars = function() {
        // Define variables
        const container = document.querySelector('#company-profile-datatable');
        const toolbarBase = document.querySelector('[data-table-toolbar="base"]');
        const toolbarSelected = document.querySelector('[data-users-table-toolbar="selected"]');
        const selectedCount = document.querySelector('[data-users-table-select="selected_count"]');
        // Select refreshed checkbox DOM elements
        const allCheckboxes = container.querySelectorAll('tbody [type="checkbox"]');
        const headerCheckbox = container.querySelectorAll('[type="checkbox"]')[0];
      
        // Detect checkboxes state & count
        let checkedState = false;
        let count = 0;
      
        // Count checked boxes
        allCheckboxes.forEach(c => {
          if (c.checked) {
            checkedState = true;
            count++;
          }
        });
      
        headerCheckbox.addEventListener('click', function() {
          allCheckboxes.forEach(c => {
            c.checked = headerCheckbox.checked;
          });
          checkedState = headerCheckbox.checked;
          count = headerCheckbox.checked ? allCheckboxes.length : 0;
          selectedCount.innerHTML = count;
          if (checkedState) {
            toolbarBase.classList.add('d-none');
            toolbarSelected.classList.remove('d-none');
          } else {
            toolbarBase.classList.remove('d-none');
            toolbarSelected.classList.add('d-none');
          }
        });
                // Uncheck header checkbox if not all checkboxes are checked
                if (checkedState && count !== allCheckboxes.length) {
                    headerCheckbox.checked = false;
                  } else if (count === 0) { // added new condition
                    headerCheckbox.checked = false;
                  }
                  else if (checkedState && count == allCheckboxes.length) {
                      headerCheckbox.checked = true;
                  }
          
      };
      


    // Public methods
    return {
        init: function() {
            initDatatable();
            handleSearchDatatable();
            ActiveOrIncativeUser();
            handleStatusFilter ();

        }
    }
}();

// On document ready
KTUtil.onDOMContentLoaded(function() {
    DatatablesServerSide.init();
});
