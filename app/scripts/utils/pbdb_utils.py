import re


def clean_taxon_name(taxon_name):
    # replace (text)
    new_text = re.sub(" \(.*?\)$", "", taxon_name)
    # replace <text>
    new_text = re.sub(" <.*?>$", "", new_text)
    # replace spp., sp., var., indet., cf., gr.
    # replace spp. text, sp. text, var. text, indet. text, cf. text, gr. text
    new_text = re.sub(" (spp|sp|var|indet|cf|gr)\.( .*?)?$", "", new_text)
    return new_text

