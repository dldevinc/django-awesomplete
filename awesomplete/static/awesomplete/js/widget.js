(function($) {

    function initWidgets($root, formsetName) {
        $root.find('.admin-awesomplete').each(function() {
            var input = this;
            var $input = $(input);
            if ($input.closest('.empty-form').length) {
                return
            }

            // Django's "overflow:hidden" fix
            var $formRow = $input.closest('.form-row');
            if ($formRow.length) {
                $formRow.css('overflow', 'visible');
            }

            // Replace "__prefix__" in "list" and "data-list" attributes
            if (formsetName) {
                replaceFormsetPrefix(input, formsetName);
            }

            var instance = new Awesomplete(this, {
                sort: function() {}
            });

            // when minChars is set to zero, show popup on focus.
            if (instance.minChars === 0) {
                instance.input.addEventListener('focus', function() {
                    var input = this;
                    if (input.value.length === 0) {
                        instance.evaluate()
                    }
                });
            }

            // fix horizontal position (because of "float:left" on label)
            instance.ul.style.marginLeft = instance.input.offsetLeft + 'px';
        });
    }

    function replaceFormsetPrefix(input, formsetName) {
        var id_regex = new RegExp("(" + formsetName + "-(\\d+|__prefix__))");
        var name_match = id_regex.exec(input.name);
        var formsetIndex = name_match && name_match[2];
        if (formsetIndex) {
            var replacement = formsetName + "-" + formsetIndex;
            if (input.hasAttribute("list")) {
                input.setAttribute("list", input.getAttribute("list").replace(id_regex, replacement));
            } else if (input.hasAttribute("data-list")) {
                input.setAttribute("data-list", input.getAttribute("data-list").replace(id_regex, replacement));
            }
        }
    }

    $(document).ready(function() {
        initWidgets($(document.body));
    }).on('formset:added', function(event, $row, formsetName) {
        initWidgets($row, formsetName);
    });

})(django.jQuery);