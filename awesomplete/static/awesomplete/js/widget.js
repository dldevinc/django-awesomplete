(function($) {

    function initWidgets($root) {
        $root.find('.admin-awesomplete').each(function() {
            var $input = $(this);
            var $formRow = $input.closest('.form-row');

            if ($input.closest('.empty-form').length) {
                return
            }

            // Django's "overflow:hidden" fix
            if ($formRow.length) {
                $formRow.css('overflow', 'visible');
            }

            var object = new Awesomplete(this, {
                sort: function() {}
            });

            // when minChars is set to zero, show popup on focus.
            if (object.minChars === 0) {
                object.input.addEventListener('focus', function() {
                    var input = this;
                    if (input.value.length === 0) {
                        object.evaluate()
                    }
                });
            }

            // fix horizontal position (because of "float:left" on label)
            object.ul.style.marginLeft = object.input.offsetLeft + 'px';
        });
    }

    $(document).ready(function() {
        initWidgets($(document.body));
    }).on('formset:added', function(event, $row, formsetName) {
        initWidgets($row);
    });

})(django.jQuery);