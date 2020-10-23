(function($) {

    function initWidgets($root, formsetName) {
        $root.find('.admin-awesomplete').each(function() {
            initAwesomplete(this, formsetName);
        });

        $root.find('.admin-awesomplete-tags').each(function() {
            initAwesomplete(this, formsetName, {
                filter: function(text, input) {
                    var entered = input.split(/\s*,\s*/).filter(Boolean);
                    return (entered.indexOf(text.value) < 0) && Awesomplete.FILTER_CONTAINS(text, input.match(/[^,]*$/)[0]);
                },

                item: function(text, input) {
                    return Awesomplete.ITEM(text, input.match(/[^,]*$/)[0]);
                },

                replace: function(text) {
                    var before = this.input.value.match(/^.+,\s*|/)[0];
                    this.input.value = before + text + ", ";
                }
            });
        });
    }

    function initAwesomplete(input, formsetName, options) {
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

        var awesopleteOptions = $.extend({
            sort: function() {}
        }, options);

        var instance = new Awesomplete(input, awesopleteOptions);

        // Load list from JSON
        var listId = getListId(input);
        var $list = listId && $(listId);
        if ($list && $list.length && ($list.prop('tagName') === 'SCRIPT')) {
            instance.list = JSON.parse($list.text());
        }

        // when minChars is set to zero, show popup on focus.
        if (instance.minChars === 0) {
            instance.input.addEventListener('focus', function() {
                if (this.value.length === 0) {
                    instance.evaluate()
                }
            });
        }

        // fix horizontal position (because of "float:left" on label)
        instance.ul.style.marginLeft = instance.input.offsetLeft + 'px';
    }

    function getListId(input) {
        if (input.hasAttribute("list")) {
            return input.getAttribute("list");
        } else {
            return input.getAttribute("data-list");
        }
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