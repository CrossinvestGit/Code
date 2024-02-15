// Get all table elements with class .table-general
const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);
const extractFieldName = (str) => str.split('__')[str.split('__').length - 1];

const tables = document.querySelectorAll('.table-general');
let tableIdCounter = 1;

// TODO: Wrap this in function
for (const table of tables) {
    const url = table.dataset.url;
    axios.get(url)
        .then(response => {
            table.id += tableIdCounter;
            tableIdCounter++;  // Increment counter

            let data = response.data;
            let tableHeaders = Object.keys(data[0]);
            let tableHeadersHTML = '';
            let tableBodyHTML = '';

            for (const header of tableHeaders) {
                const extractHeader = extractFieldName(header);
                const capHeader = capitalize(extractHeader);
                tableHeadersHTML += `<th>${capHeader}</th>`;
            }

            table.querySelector('.table-headers').innerHTML = tableHeadersHTML;
            table.querySelector('.table-footer').innerHTML = tableHeadersHTML;

            for (const item of data) {
                let rowHTML = '';
                for (const header of tableHeaders) {
                    rowHTML += `<td>${item[header]}</td>`;
                }
                tableBodyHTML += `<tr>${rowHTML}</tr>`;
            }
            table.querySelector('.table-body').innerHTML = tableBodyHTML;


            $(table).DataTable({
                stateSave: true,
                select: true,
                pagingType: 'first_last_numbers',
                dom: 'PBfrtip',
                responsive: true,
                colReorder: true,
                keys: false,
                searchPanes: {
                    cascadePanes: true,
                    initCollapsed: true,
                },
                buttons: [
                    { extend: 'createState' },
                    { extend: 'savedStates' },
                    { extend: 'colvis', text: 'Column Visibility' },
                    { extend: 'copy' },
                    { extend: 'csv' },
                    { extend: 'excel' },
                    { extend: 'pdf', orientation: 'landscape' },
                    { extend: 'print' },
                ],
                initComplete: function () {
                    this.api()
                        .columns()
                        .every(function () {
                            let column = this;
                            let title = column.footer().textContent;
                            let input = document.createElement('input');
                            input.placeholder = title;
                            column.footer().replaceChildren(input);
                            input.addEventListener('input', () => {
                                if (column.search() !== input.value) {
                                    column.search(input.value).draw();
                                }
                            });
                        });
                }
            });
        })
        .catch(error => {
            console.error(error);
        });
};



