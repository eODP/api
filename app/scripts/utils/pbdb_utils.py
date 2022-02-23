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


def format_pbdb_data_for_row(row):
    if not row['pbdb_taxon_id']:
        return

    data = {}
    fields = [
        "genus_taxon_id",
        "genus_taxon_name",
        "family_taxon_id",
        "family_taxon_name",
        "order_taxon_id",
        "order_taxon_name",
        "class_taxon_id",
        "class_taxon_name",
        "phylum_taxon_id",
        "phylum_taxon_name",
        "kingdom_taxon_id",
        "kingdom_taxon_name",
        "unranked clade_taxon_id",
        "unranked clade_taxon_name",
    ]
    for field in fields:
        if field in row and row[field]:
            data[field] = row[field]

    row_rank = row['pbdb_taxon_rank']
    data[f'{row_rank}_taxon_id'] = row['pbdb_taxon_id']
    data[f'{row_rank}_taxon_name'] = row['pbdb_taxon_name']

    return data
