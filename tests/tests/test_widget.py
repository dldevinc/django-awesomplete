from awesomplete.widgets import build_suggestions


class TestBuildSuggestions:
    def test_plain(self):
        assert list(build_suggestions(["one", "two", "three"])) == [
            ("one", "one"),
            ("two", "two"),
            ("three", "three"),
        ]

    def test_dicts(self):
        assert list(build_suggestions([
            {
                "label": "English",
                "value": "en"
            },
            {
                "label": "Russian",
                "value": "ru"
            },
            {
                "label": "Italian",
                "value": "it"
            },
            {
                "label": "Japanese",
                "value": "jp"
            },
        ])) == [
            ("English", "en"),
            ("Russian", "ru"),
            ("Italian", "it"),
            ("Japanese", "jp"),
        ]

    def test_iterable(self):
        assert list(build_suggestions([
            ("f00", "Red", "#ff0000"),
            ("0f0", "Green", "#00ff00"),
            ["00f", "Blue", "#0000ff"],
        ])) == [
            ("Red", "f00"),
            ("Green", "0f0"),
            ("Blue", "00f"),
        ]
