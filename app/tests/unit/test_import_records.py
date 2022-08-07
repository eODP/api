import pandas as pd
import pytest
from scripts.utils.import_records import get_taxa_and_taxon_groups, fetch_taxa_ids


class TestGetTaxaAndTaxonGroups:
    def test_returns_a_dictionary_of_verbatim_names_and_taxon_groups(self):
        data = [
            {"verbatim_name": "taxon A", "taxon_group": "group 1", "name": "A a"},
            {"verbatim_name": "taxon B", "taxon_group": "group 2", "name": "B b"},
            {"verbatim_name": "taxon C", "taxon_group": "group 3", "name": "C c"},
        ]
        taxa_df = pd.DataFrame(data)

        expected = {
            "taxon A": ["group 1"],
            "taxon B": ["group 2"],
            "taxon C": ["group 3"],
        }
        assert get_taxa_and_taxon_groups(taxa_df) == expected

    def test_handles_verbatim_names_with_multiple_taxon_groups(self):
        data = [
            {"verbatim_name": "taxon A", "taxon_group": "group 1", "name": "A a"},
            {"verbatim_name": "taxon A", "taxon_group": "group 2", "name": "A a"},
            {"verbatim_name": "taxon B", "taxon_group": "group 2", "name": "C c"},
        ]
        taxa_df = pd.DataFrame(data)

        expected = {"taxon A": ["group 1", "group 2"], "taxon B": ["group 2"]}
        assert get_taxa_and_taxon_groups(taxa_df) == expected

    def test_ignores_record_with_duplicate_verbatim_name_and_taxon_group(self):
        data = [
            {"verbatim_name": "taxon A", "taxon_group": "group 1", "name": "A a"},
            {"verbatim_name": "taxon A", "taxon_group": "group 1", "name": "B b"},
            {"verbatim_name": "taxon A", "taxon_group": "group 2", "name": "A a"},
        ]
        taxa_df = pd.DataFrame(data)

        expected = {"taxon A": ["group 1", "group 2"]}
        assert get_taxa_and_taxon_groups(taxa_df) == expected

    def test_strips_extra_whitespace_from_verbatim_name(self):
        data = [
            {"verbatim_name": "taxon A", "taxon_group": "group 1", "name": "A a"},
            {"verbatim_name": " taxon A", "taxon_group": "group 1", "name": "B b"},
            {"verbatim_name": " taxon A ", "taxon_group": "group 1", "name": "C c"},
            {"verbatim_name": " taxon A", "taxon_group": "group 1", "name": "D d"},
        ]
        taxa_df = pd.DataFrame(data)

        expected = {"taxon A": ["group 1"]}
        assert get_taxa_and_taxon_groups(taxa_df) == expected


class Taxon:
    def __init__(self, id, taxon_id):
        self.id = id
        self.taxon_id = taxon_id


class TestFetchTaxaIds:
    def test_raise_error_if_taxa_values_not_in_verbatim_names(self):
        taxon_group = "group 1"
        verbatim_names = {"taxon A": ["group 1"]}
        taxa = ["taxon D"]

        with pytest.raises(ValueError) as e:
            fetch_taxa_ids(taxa, taxon_group, verbatim_names)
        assert str(e.value) == "taxon D not in verbatim_names."

    def test_raise_error_if_taxa_values_do_not_have_groups(self):
        taxon_group = "group 1"
        verbatim_names = {"taxon A": []}
        taxa = ["taxon A"]

        with pytest.raises(ValueError) as e:
            fetch_taxa_ids(taxa, taxon_group, verbatim_names)
        assert str(e.value) == "taxon A does not have taxon groups."

    def test_returns_taxon_id_and_original_taxon_id_for_a_list_of_taxa(self, mocker):
        taxon_group = "group 1"
        verbatim_names = {
            "taxon A": ["group 1"],
            "taxon B": ["group 1"],
            "taxon C": ["group 1"],
        }
        taxa_list = ["taxon A", "taxon B"]
        taxon1 = Taxon(1, 101)
        taxon2 = Taxon(2, 102)
        mocker.patch(
            "scripts.utils.import_records.find_taxon_crosswalk_by_name",
            side_effect=[taxon1, taxon2],
        )

        expected = {
            "taxon A": {"taxon_id": 101, "original_taxon_id": 1},
            "taxon B": {"taxon_id": 102, "original_taxon_id": 2},
        }
        assert fetch_taxa_ids(taxa_list, taxon_group, verbatim_names) == expected

    def test_uses_taxon_group_from_verbatim_names_for_find_taxon_if_1_group(
        self, mocker
    ):
        taxon_group = "group 1"
        verbatim_names = {"taxon A": ["group 2"]}
        taxa_list = ["taxon A"]
        taxon1 = Taxon(1, 101)
        find_mock = mocker.patch(
            "scripts.utils.import_records.find_taxon_crosswalk_by_name",
            side_effect=[taxon1],
        )

        results = fetch_taxa_ids(taxa_list, taxon_group, verbatim_names)

        find_mock.assert_has_calls(
            [mocker.call({"name": "taxon A", "taxon_group": "group 2"})]
        )

        expected = {"taxon A": {"taxon_id": 101, "original_taxon_id": 1}}
        assert results == expected

    def test_uses_given_taxon_group_for_find_taxon_if_multiple_group(self, mocker):
        taxon_group = "group 1"
        verbatim_names = {"taxon A": ["group 1", "group 2"]}
        taxa_list = ["taxon A"]
        taxon1 = Taxon(1, 101)
        find_mock = mocker.patch(
            "scripts.utils.import_records.find_taxon_crosswalk_by_name",
            side_effect=[taxon1],
        )

        results = fetch_taxa_ids(taxa_list, taxon_group, verbatim_names)

        find_mock.assert_has_calls(
            [mocker.call({"name": "taxon A", "taxon_group": "group 1"})]
        )

        expected = {"taxon A": {"taxon_id": 101, "original_taxon_id": 1}}
        assert results == expected

    def test_raise_error_if_given_taxon_group_not_in_multiple_groups(self, mocker):
        taxon_group = "group 3"
        verbatim_names = {"taxon A": ["group 1", "group 2"]}
        taxa_list = ["taxon A"]

        with pytest.raises(ValueError) as e:
            fetch_taxa_ids(taxa_list, taxon_group, verbatim_names)
        assert str(e.value) == "taxon A does not belong to group 3"
