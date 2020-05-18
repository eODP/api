from scripts.utils.db_utils import allowed_params, trim_doc_string


class TestAllowedAttribute:
    def test_returns_key_value_pairs_whose_keys_are_in_an_allowed_list(self):
        allowed_list = ["a", "b", "c"]
        params = {"a": 1, "c": 2, "d": 3}
        expected = {"a": 1, "c": 2}

        assert allowed_params(allowed_list, params) == expected

    def test_returns_empty_dictionary_if_no_keys_are_in_an_allowed_list(self):
        allowed_list = ["a", "b", "c"]
        params = {"d": 1, "e": 2}
        expected = {}

        assert allowed_params(allowed_list, params) == expected

    def test_replaces_empty_string_with_None(self):
        allowed_list = ["a", "b"]
        params = {"a": ""}
        expected = {"a": None}

        assert allowed_params(allowed_list, params) == expected

    def test_replaces_only_spaces_string_with_None(self):
        allowed_list = ["a", "b"]
        params = {"a": "   "}
        expected = {"a": None}

        assert allowed_params(allowed_list, params) == expected

    def test_works_all_types(self):
        allowed_list = ["a", "b", "c", "d", "e"]
        params = {"a": 1, "b": 1.1, "c": "ccc", "d": {"a": 1}, "e": [1]}

        assert allowed_params(allowed_list, params) == params


class TestTrimDocString:
    def test_removes_line_breaks_and_excessive_spaces(self):
        string = """
        ab    cd
        ef gh
        ij
        """
        expected = "ab cd ef gh ij"

        assert trim_doc_string(string) == expected
