(function($) {

    $(document).ready(function() {
        $('.admin-awesomplete').each(function() {
            var $input = $(this);
            var $formRow = $input.closest('.form-row');

            // Django's "overflow:hidden" fix
            if ($formRow.length) {
                $formRow.css('overflow', 'visible');
            }

            var object = new Awesomplete(this, {
                sort: function() {}
            });

            // fix horizontal position (because of "float:left" on label)
            object.ul.style.marginLeft = object.input.offsetLeft + 'px';
        });
    });

})(django.jQuery);