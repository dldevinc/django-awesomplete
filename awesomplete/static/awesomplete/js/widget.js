(function($) {

    function initWidgets($root, formsetName) {
        $root.find('.admin-awesomplete').each(function() {
            initAwesomplete(this, formsetName);
        });

        $root.find('.admin-awesomplete-tags').each(function() {
            initAwesomplete(this, formsetName, {
                filter: function(text, input) {
                    var tagList = parseTags(input);

                    var newTag = tagList.pop() || "";
                    if (!newTag) {
                        return (
                            (tagList.indexOf(text.value) < 0)
                            && (this.minChars === 0)
                        );
                    }

                    return (
                        (tagList.indexOf(text.value) < 0)  // skip already selected
                        && Awesomplete.FILTER_CONTAINS(text, newTag)
                    );
                },

                item: function(text, input) {
                    var tagList = parseTags(input);
                    var newTag = tagList.pop() || "";
                    return Awesomplete.ITEM(text, newTag);
                },

                replace: function(text) {
                    var tagList = parseTags(this.input.value);
                    tagList.pop(); // remove printed tag
                    tagList.push(text);

                    this.input.value = tagList.map(function(item) {
                        if ((item.indexOf(",") >= 0) || (item.indexOf(" ") >= 0)) {
                            return '"' + item + '"';
                        }
                        return item
                    }).join(", ") + ", ";
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

        // show popup on focus when minChars is equal to zero.
        if (instance.minChars === 0) {
            instance.input.addEventListener('focus', function() {
                if (this.value.length === 0) {
                    instance.evaluate()
                }
            });
        }

        // fix horizontal position (because of "float:left" on label)
        instance.ul.style.marginLeft = instance.input.offsetLeft + 'px';

        // scroll to the input's end after item selected
        $input.on("awesomplete-selectcomplete", function() {
            if (this.scrollWidth > this.clientWidth) {
                this.scrollLeft = this.scrollWidth;
            }
        });
    }

    /**
     * Split by comma, respect and preserve double quotes.
     * Then trim each item: removes double quotes ans spaces.
     *
     * @param {String} value
     * @returns {String[]}
     */
    function parseTags(value) {
        var tags = value.match(/(".*?"|[^",]+)(?=\s*,|\s*$)/g);
        if (!tags) {
            return [];
        }

        return tags.map(function(item) {
            return item.replace(/^"|"$/g, '').trim();
        })
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