from scripts.utils.pbdb_utils import format_taxon_name
from tests.factories import TaxonFactory


class TestFormatTaxonName:
    def test_when_taxon_has_taxon_name_above_genus(self, client):
        taxon = TaxonFactory(taxon_name_above_genus="family indet.")
        assert format_taxon_name(taxon) == "family"

    def test_returns_genus(self, client):
        taxon = TaxonFactory(genus_name="genus")
        assert format_taxon_name(taxon) == "genus"

    def test_returns_genus_and_ignores_unidentified_species(self, client):
        for identifer in ["sp.", "spp."]:
            taxon = TaxonFactory(genus_name="genus", species_name=identifer)
            assert format_taxon_name(taxon) == "genus"

    def test_returns_genus_species(self, client):
        taxon = TaxonFactory(genus_name="genus", species_name="species")
        assert format_taxon_name(taxon) == "genus species"

    def test_returns_genus_species_modifier(self, client):
        taxon = TaxonFactory(genus_name="genus", species_modifier="sm")
        assert format_taxon_name(taxon) == "genus sm"

    def test_returns_genus_species_modifier_species(self, client):
        taxon = TaxonFactory(
            genus_name="genus", species_name="species", species_modifier="sm"
        )
        assert format_taxon_name(taxon) == "genus sm species"

    def test_returns_genus_species_subspecies_modifier(self, client):
        taxon = TaxonFactory(
            genus_name="genus", species_name="species", subspecies_modifier="sm"
        )
        assert format_taxon_name(taxon) == "genus species sm"

    def test_returns_genus_species_subspecies_modifier_subspecies(self, client):
        taxon = TaxonFactory(
            genus_name="genus",
            species_name="species",
            subspecies_modifier="sm",
            subspecies_name="subspecies",
        )
        assert format_taxon_name(taxon) == "genus species sm subspecies"

    def test_returns_genus_species_subspecies(self, client):
        taxon = TaxonFactory(
            genus_name="genus", species_name="species", subspecies_name="subspecies"
        )
        assert format_taxon_name(taxon) == "genus species subspecies"

    def test_ignores_subspecies_when_no_species(self, client):
        taxon = TaxonFactory(genus_name="genus", subspecies_name="subspecies")
        assert format_taxon_name(taxon) == "genus"
