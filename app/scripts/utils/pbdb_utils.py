def format_taxon_name(taxon):
    if taxon.taxon_name_above_genus:
        name = taxon.taxon_name_above_genus.replace(" indet.", "")
    else:
        name = taxon.genus_name
        if taxon.species_name and taxon.species_name not in ["sp.", "spp."]:
            name += f" {taxon.species_name}"
            if taxon.subspecies_name:
                name += f" {taxon.subspecies_name}"
    return name
