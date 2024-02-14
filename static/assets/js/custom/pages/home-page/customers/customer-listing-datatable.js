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
                {data   : 'full_name'},
                {data   : 'email'},
                {data   : 'phone'},
                {data   : 'alternative_phone'},
                {data   : 'date_joined'},
                {data   : 'is_active'},
            ],

            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data) {
                        return `
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
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
                    searchable: true,
                    orderable: true,
                    targets: 2,
                    render: function(data, type, row) {
                        return `<div class="d-flex align-items-center">
                                    
                                    <div class="">
                                        <div class="text-gray-800 text-hover-primary fs-5 fw-bolder" >${data}</div>
                                    </div>
                                </div>`;
                    }
                },
                
                {
                    searchable: false,
                    orderable: false,
                    targets: 7,
                    render: function(data, type, row) {
                        let label_badge_change = '';
                        if(data == 'True'){
                            label_badge_change = `<span style="cursor:pointer" data-id=${row.id}  class="btn btn-sm btn-outline btn-outline-dashed btn-outline-success btn-active-light-success active_inactive_language">Active</span>`;
                        }else if(data == 'False'){
                            label_badge_change =  `<span style="cursor:pointer" data-id=${row.id}  class="btn btn-sm btn-outline btn-outline-dashed btn-outline-danger btn-active-light-danger active_inactive_language">Inactive</span>`;
                        }
                        return label_badge_change;
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
            // console.log(">>>>>>>>>>>>>>>>>>>>>>>>>1111111111",startDateValue )

            dt.column(4).search(startDateValue).draw();
        });
    }
    var handleenddateFilter = () => {
        const filterEndDate = document.querySelector('[data-users-filter="enddate"]');
        $(filterEndDate).on('change', () => {
            let endDateValue = filterEndDate.value;
            // console.log(">>>>>>>>>>>>>>>>>>>>>>>>>",endDateValue )
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

        



    // Init toggle toolbar
    

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
      
        // Toggle toolbars
        // if (checkedState) {
        //     selectedCount.innerHTML = count;
        //   toolbarBase.classList.add('d-none');
        //   toolbarSelected.classList.remove('d-none');
        // } else {
        //   toolbarBase.classList.remove('d-none');
        //   toolbarSelected.classList.add('d-none');
        // }
      
        // Check/uncheck checkboxes based on "select all" checkbox state
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
