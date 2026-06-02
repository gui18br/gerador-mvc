import os
import re

def parse_adrs(filepath="ADRs_Strong_Nutrition.md"):
    """
    Parses ADRs from markdown file and returns a list of dictionaries with ADR details.
    """
    if not os.path.exists(filepath):
        # Try to find it in the current file's directory
        dir_path = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(dir_path, filepath)
        if not os.path.exists(filepath):
            return {}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on --- separators or matches
    pattern = r"((?:#|##)\s+ADR-\d+.*?)(?=\n(?:#|##)\s+ADR-\d+|\n---|\Z)"
    blocks = re.findall(pattern, content, re.DOTALL)

    adrs = {}
    for block in blocks:
        id_match = re.search(r"(?:#|##)\s+(ADR-\d+)", block)
        title_match = re.search(r"(?:#|##)\s+ADR-\d+[:\-]\s*(.+)", block)
        
        decisao_match = re.search(
            r"##\s+Decisão\s*(.*?)\s*##\s+Consequências",
            block,
            re.DOTALL
        ) or re.search(
            r"\*\*Decisão:\*\*\s*(.*?)\s*(?:\*\*Consequências|\*\*Status|\Z)",
            block,
            re.DOTALL
        )
        
        consequencias_match = re.search(
            r"##\s+Consequências\s*(.*?)(?=\n(?:#|##)|\n---|\Z)",
            block,
            re.DOTALL
        ) or re.search(
            r"\*\*Consequências:\*\*\s*(.*?)(?=\n(?:#|##)|\n---|\Z)",
            block,
            re.DOTALL
        )

        adr_id = id_match.group(1).strip() if id_match else None
        if adr_id:
            adrs[adr_id] = {
                "id": adr_id,
                "titulo": title_match.group(1).strip() if title_match else "",
                "decisao": decisao_match.group(1).strip() if decisao_match else "",
                "consequencias": consequencias_match.group(1).strip() if consequencias_match else "",
                "bloco_completo": block.strip()
            }
    return adrs

def find_adr_for_module(module_name, adrs):
    """
    Finds the ADR that matches the module name (case-insensitive).
    E.g. "Produto" will match "Cadastro de Produtos".
    """
    module_normalized = module_name.strip().lower()
    
    # Try singular/plural forms to be safe
    variations = [module_normalized]
    if module_normalized.endswith("s"):
        variations.append(module_normalized[:-1])
    else:
        variations.append(module_normalized + "s")
        if module_normalized.endswith("a"):
            variations.append(module_normalized[:-1] + "as")
        elif module_normalized.endswith("o"):
            variations.append(module_normalized[:-1] + "os")

    for adr_id, adr in adrs.items():
        title_lower = adr["titulo"].lower()
        for var in variations:
            if var in title_lower:
                return adr
    return None

if __name__ == "__main__":
    # Test block
    adrs = parse_adrs()
    print(f"Total ADRs parsed: {len(adrs)}")
    prod_adr = find_adr_for_module("Produto", adrs)
    if prod_adr:
        print(f"Found match: {prod_adr['id']} - {prod_adr['titulo']}")
    else:
        print("Produto ADR not found.")
