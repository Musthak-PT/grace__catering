"use strict";

// Class definition
var DatatablesServerSide = function() {
    // Shared variables
    var table;
    var dt;

    // Private functions
    var initDatatable = function() {

        dt = $("#room-type-datatable").DataTable({
            searchDelay: 500,
            serverSide: true,
            pageLength: 25,
            responsive: true,
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
                        // Calculate the correct serial number across pages
                        return meta.row + 1 + meta.settings._iDisplayStart;
                    }
                },                 {data   : 'customer_name'},
                {data   : 'customer_email'},
                {data   : 'phone'},
                {data   : 'total_booked_price'},
                {data   : 'payment_status'},
                {data   : 'date_time'},
                {data   : 'id'},
            ],

            columnDefs: [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data) {
                        return `
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
                                <input class="d-none form-check-input checkbox-input-id" type="checkbox" value="${data}" />
                            </div>`;
                    }
                },
                {
                    targets: 1,
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return meta.row + 1; // Set the serial number as the row index + 1
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
                    targets: 7,
                    orderable: false,
                 
                },
                {
                    searchable: true,
                    orderable: true,
                    targets: 2,
                    render: function(data, type, row) {
                        let edit_url = api_config.edit_url.replace('0', row.encrypt_id.toString());
                        return `<div class="d-flex align-items-center">
                                    <a href="${edit_url}" class="symbol symbol-50px"style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;max-width: 200px;display: inline-block;" >
                                    </a>
                                    <div class="ms-5">
                                        <a href="${edit_url}" class="text-gray-800 text-hover-primary fs-5 fw-bolder gift-title" style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;max-width: 200px;display: inline-block;">${data}</a>
                                    </div>
                                </div>`;
                    }
                },

                
                {
                    searchable: false,
                    orderable: false,
                    targets: 6,
                    render: function(data, type, row) {
                        let label_badge_change = '';
                        if (data == 'True') {
                            label_badge_change = `<button type="button" style="color: #ffffff; background-color: #203d75; border-color: #203d75;" data-id=${row.id} class="btn btn-sm btn-outline btn-outline-dashed active_inactive_language"><i class="bi bi-check-circle"></i> Paid</button>`;
                        } else if (data == 'False') {
                            label_badge_change = `<button type="button" style="color: #ffffff; background-color: #203d75; border-color: #203d75;" data-id=${row.id} class="btn btn-sm active_inactive_language"><i class="bi bi-x-circle"></i> Pay</button>`;
                        }
                        return label_badge_change;
                    }
                },
                
                
                
                
                
                
                {
                    targets: -1,
                    data: null,
                    orderable: false,
                    className: 'text-end',
                    render: function (data, type, row) {
                        let edit_url = api_config.edit_url.replace('0', row.encrypt_id.toString());
                        return `
                                <div class="d-flex justify-content-end flex-shrink-0">
                                    <a href="${edit_url}" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                                        <span class="svg-icon svg-icon-3">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                                <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988 17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355 21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099 14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449 21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z" fill="currentColor" />
                                                <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744 21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799 20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z" fill="currentColor" />
                                            </svg>
                                        </span>
                                    </a>
                                    
                                </div>
                        `;
                    },
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
            initToggleToolbar();
            toggleToolbars();
            handleStatusFilter();
            ActiveOrIncativeUser();
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
    var initToggleToolbar = function() {
        // Toggle selected action toolbar
        // Select all checkboxes
        const container = document.querySelector('#room-type-datatable');
        const checkboxes = container.querySelectorAll('[type="checkbox"]');

        // Select elements
        const deleteSelected = document.querySelector('[data-users-table-select="delete_selected"]');

        // Toggle delete selected toolbar
        checkboxes.forEach(c => {
            // Checkbox on click event
            c.addEventListener('click', function() {
                setTimeout(function() {
                    toggleToolbars();
                }, 50);
            });
        });

        // Deleted selected rows
        deleteSelected.addEventListener('click', function() {

            const row_ids = []
            $(".checkbox-input-id:checkbox:checked").each(function() {
                row_ids.push($(this).val());
            });

            Swal.fire({
                text: "Are you sure you want to delete selected ?",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                showLoaderOnConfirm: true,
                confirmButtonText: "Yes, delete!",
                cancelButtonText: "No, cancel",
                customClass: {
                    confirmButton: "btn fw-bold btn-danger",
                    cancelButton: "btn fw-bold btn-active-light-primary"
                },
            }).then(function(result) {
                if (result.value) {

                    $.post(`${api_config.delete_records}`, { ids: row_ids }, function(data, status, xhr) {

                        if (data.status = 200) {
                            Swal.fire({
                                text: "You have deleted all selected ",
                                icon: "success",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn fw-bold btn-primary",
                                }
                            }).then(function() {
                                // delete row data from server and re-draw datatable
                                dt.draw();
                                const headerCheckbox = container.querySelectorAll('[type="checkbox"]')[0];
                                headerCheckbox.checked = false;
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

                    }, 'json').done(function() {
                        console.log('Request done!');
                    }).fail(function(jqxhr, settings, ex) {
                        console.log('failed, ' + ex);
                        Swal.fire({
                            text: "Something went wrong.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn fw-bold btn-primary",
                            }
                        });
                    });

                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Selected user was not deleted.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn fw-bold btn-primary",
                        }
                    });
                }
            });
        });
    }

    var toggleToolbars = function() {
        // Define variables
        const container = document.querySelector('#room-type-datatable');
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
        if (checkedState) {
            selectedCount.innerHTML = count;
          toolbarBase.classList.add('d-none');
          toolbarSelected.classList.remove('d-none');
        } else {
          toolbarBase.classList.remove('d-none');
          toolbarSelected.classList.add('d-none');
        }
      
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
            initToggleToolbar();
            ActiveOrIncativeUser();
            handleStatusFilter ();

        }
    }
}();

// On document ready
KTUtil.onDOMContentLoaded(function() {
    DatatablesServerSide.init();
});
