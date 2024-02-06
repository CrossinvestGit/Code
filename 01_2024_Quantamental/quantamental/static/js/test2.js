// Get all table elements with class .table-general
const tables = document.querySelectorAll('.table-general');
const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

// Iterate over each table
tables.forEach(table => {
    // Get the URL from the data attribute
    const url = table.dataset.url;

    // Make AJAX request using Axios
    axios.get(url)
        .then(response => {
            // Handle successful response
            let data = response.data;
            let tableHeaders = Object.keys(data[0]);
            let tableHeadersHTML = '';
            let tableBodyHTML = '';

            // Generate table headers dynamically
            tableHeaders.forEach(header => {
                capHeader = capitalize(header);
                tableHeadersHTML += `<th>${capHeader}</th>`;
            });

            table.querySelector('.table-headers').innerHTML = tableHeadersHTML;
            table.querySelector('.table-footer').innerHTML = tableHeadersHTML; // Add footer headers

            // Generate table rows dynamically
            data.forEach(item => {
                let rowHTML = '';
                tableHeaders.forEach(header => {
                    rowHTML += `<td>${item[header]}</td>`;
                });
                tableBodyHTML += `<tr>${rowHTML}</tr>`;
            });
            table.querySelector('.table-body').innerHTML = tableBodyHTML;

            // After dynamically generating the table, initialize DataTable
            $(table).DataTable({
                select: true,
                responsive: true,
                searchPanes: {
                    show: true,
                    cascadePanes: true,
                    threshold: 1,
                    initCollapsed: true
                },
                dom: 'PBfrtip',
                pagingType: 'full_numbers',
                initComplete: function () {
                    this.api()
                        .columns()
                        .every(function () {
                            let column = this;
                            let title = column.footer().textContent;

                            // Create input element
                            let input = document.createElement('input');
                            input.placeholder = title;
                            column.footer().replaceChildren(input);

                            // Event listener for user input
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
            // Handle errors
            console.error(error);
        });
});
