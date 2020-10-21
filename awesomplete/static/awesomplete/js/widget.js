(function($) {

    function initWidgets($root, formsetName) {
        $root.find('.admin-awesomplete').each(function() {
            var $input = $(this);
            if ($input.closest('.empty-form').length) {
                return
            }

            // Replace "__prefix__"
            if (formsetName) {
                var id_regex = new RegExp("(" + formsetName + "-(\\d+|__prefix__))");
                var name_match = id_regex.exec($input.prop('name'));
                var formsetIndex = name_match && name_match[2];
                if (formsetIndex) {
                    var replacement = formsetName + "-" + formsetIndex;
                    if ($input.get(0).hasAttribute("list")) {
                        $input.attr("list", $input.attr("list").replace(id_regex, replacement));
                    } else if ($input.get(0).hasAttribute("data-list")) {
                        $input.attr("data-list", $input.attr("data-list").replace(id_regex, replacement));
                    }
                }
            }

            // Django's "overflow:hidden" fix
            var $formRow = $input.closest('.form-row');
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
        initWidgets($row, formsetName);
    });

})(django.jQuery);