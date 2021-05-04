from scripts.utils.db_utils import allowed_params, trim_doc_string, add_null_queries


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

    def test_strips_leading_and_trailing_spaces(self):
        allowed_list = ["a", "b", "c"]
        params = {"a": "  aa", "b": "bb  ", "c": "  cc  "}
        expected = {"a": "aa", "b": "bb", "c": "cc"}

        assert allowed_params(allowed_list, params) == expected


class TestTrimDocString:
    def test_removes_line_breaks_and_excessive_spaces(self):
        string = """
        ab    cd
        ef gh
        ij
        """
        expected = "ab cd ef gh ij"

        assert trim_doc_string(string) == expected


class TestAddNullQueries:
    def test_replaces_equality_check_with_IS_NULL_if_value_is_None(self):
        attribute = {"bbb": None}
        string = " table.b = :bbb;"
        expected = " table.b IS NULL;"

        assert add_null_queries(string, attribute) == expected

    def test_handles_different_whitespaces(self):
        attribute = {"bbb": None}
        string = " table.b=   :bbb;"
        expected = " table.b IS NULL;"

        assert add_null_queries(string, attribute) == expected

    def test_handles_multiple_attributes(self):
        attribute = {"aaa": None, "bbb": "value", "ccc": None}
        string = "AND table.z = :aaa AND table.y = :bbb AND table.x = :ccc;"
        expected = "AND table.z IS NULL AND table.y = :bbb AND table.x IS NULL;"

        assert add_null_queries(string, attribute) == expected

    def test_handles_underscores(self):
        attribute = {"aa_bb": None}
        string = " table.z_y = :aa_bb "
        expected = " table.z_y IS NULL "

        assert add_null_queries(string, attribute) == expected

    def test_handles_keys_that_start_with_same_letters(self):
        attribute = {
            "top": None,
            "bottom": None,
            "top_depth": None,
            "bottom_depth": None,
        }

        string = (
            "AND samples.top = :top "
            "AND samples.bottom = :bottom "
            "AND samples.top_depth = :top_depth "
            "AND samples.bottom_depth = :bottom_depth;"
        )

        expected = (
            "AND samples.top IS NULL "
            "AND samples.bottom IS NULL "
            "AND samples.top_depth IS NULL "
            "AND samples.bottom_depth IS NULL;"
        )

        assert add_null_queries(string, attribute) == expected
