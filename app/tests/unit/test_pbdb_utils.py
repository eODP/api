from scripts.utils.pbdb_utils import clean_taxon_name


class TestCleanTaxonName:
    def test_remove_parathesis(self):
        input = "Genus species (notes)"
        expected = "Genus species"

        assert clean_taxon_name(input) == expected

    def test_remove_brackets(self):
        input = "Genus species <notes>"
        expected = "Genus species"

        assert clean_taxon_name(input) == expected

    def test_remove_variants(self):
        inputs = [
            "Genus species spp.",
            "Genus species sp.",
            "Genus species var.",
            "Genus species indet.",
            "Genus species cf.",
            "Genus species gr.",
        ]
        expected = "Genus species"

        for input in inputs:
            assert clean_taxon_name(input) == expected

    def test_remove_variants_text(self):
        inputs = [
            "Genus species spp. more text",
            "Genus species sp. more text",
            "Genus species var. more text",
            "Genus species indet. more text",
            "Genus species cf. more text",
            "Genus species gr. more text",
        ]
        expected = "Genus species"

        for input in inputs:
            assert clean_taxon_name(input) == expected

    def test_does_not_affect_other_text(self):
        inputs = ["Genus species spout", "Genus species", "Genus"]

        for input in inputs:
            assert clean_taxon_name(input) == input
