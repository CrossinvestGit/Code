$(document).ready(function () {
    var table = $('.datatables-general').DataTable({
        select: true,
        responsive: true,
        searchPanes: {
            show: true,
            cascadePanes: true,
            threshold: 1,
            initCollapsed: true,
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
                    input.addEventListener('keyup', () => {
                        if (column.search() !== this.value) {
                            column.search(input.value).draw();
                        }
                    });
                });
        }
    });

    // Slider
    $(function () {
        var $slider = $("#slider-range");
        var min = parseInt($slider.data("min"));
        var max = parseInt($slider.data("max"));
        var initialValues = $slider.data("initial-values").split(',').map(Number);
        var filterColumn = parseInt($slider.data("column"));

        $("#slider-range").slider({
            range: true,
            min: min,
            max: max,
            values: initialValues,
            animate: 'slow',
            slide: function (event, ui) {
                $("#amount").val(ui.values[0] + " - " + ui.values[1]);

                $.fn.dataTable.ext.search.pop();
                $.fn.dataTable.ext.search.push(
                    function (settings, data, dataIndex) {
                        var min = ui.values[0];
                        var max = ui.values[1];
                        var columnValue = parseFloat(data[filterColumn]) || 0;

                        if ((isNaN(min) && isNaN(max)) ||
                            (isNaN(min) && columnValue <= max) ||
                            (min <= columnValue && isNaN(max)) ||
                            (min <= columnValue && columnValue <= max)) {
                            return true;
                        }
                        return false;
                    }
                );

                // Redraw the DataTable
                $('.datatables-general').DataTable().draw();
            }
        });
    });
});