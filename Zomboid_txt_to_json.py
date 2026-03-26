import json
import re
from pathlib import Path
from charset_normalizer import from_path


# =========================
# LEITURA COM DETECÇÃO REAL
# =========================
def read_file_safely(file_path):
    result = from_path(file_path).best()

    if result is None:
        raise Exception(f"[ERRO] Encoding não detectado: {file_path}")

    content = str(result)
    encoding = result.encoding

    print(f"[OK] {file_path} | encoding: {encoding}")

    return content


# =========================
# LIMPEZA DO NOME DO ARQUIVO
# =========================
def clean_filename(name):
    return name.rsplit("_", 1)[0] if "_" in name else name


# =========================
# PREFIXOS
# =========================
def get_prefix_to_remove(filename):
    filename = filename.lower()

    if filename == "itemname":
        return "ItemName_"
    elif filename == "recipes":
        return "Recipe_"

    return None


# =========================
# PARSER LUA → DICT
# =========================
def parse_lua_to_dict(content, prefix_to_remove=None):
    data = {}

    # remove comentários
    content = re.sub(r"--.*", "", content)

    pattern = re.compile(r'([A-Za-z0-9_\.\s]+)\s*=\s*"([^"]*)"')

    for key, value in pattern.findall(content):
        key = re.sub(r"\s+", " ", key.strip())

        if prefix_to_remove and key.startswith(prefix_to_remove):
            key = key[len(prefix_to_remove):]

        data[key] = value.strip()

    return data


# =========================
# TRANSFORMAÇÃO DE RECIPES
# =========================
def transform_recipes_keys(data):
    new_data = {}
    collisions = 0

    for key, value in data.items():
        new_key = key.replace("_", " ")

        if new_key in new_data:
            print(f"[COLISÃO] {new_key} já existe, mantendo original")
            new_key = key
            collisions += 1

        new_data[new_key] = value

    return new_data, collisions


# =========================
# CONVERSÃO PRINCIPAL
# =========================
def convert_file(input_path):
    content = read_file_safely(input_path)

    clean_name = clean_filename(input_path.stem)
    prefix_to_remove = get_prefix_to_remove(clean_name)

    data = parse_lua_to_dict(content, prefix_to_remove)

    # 🔥 APLICA REGRA ESPECIAL PARA RECIPES
    if clean_name.lower() == "recipes":
        data, collisions = transform_recipes_keys(data)
        if collisions > 0:
            print(f"[WARN] {input_path} teve {collisions} colisões")

    output_path = input_path.with_name(clean_name + ".json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"[JSON] {output_path}")


# =========================
# EXECUÇÃO RECURSIVA
# =========================
def convert_recursive(folder_path):
    folder = Path(folder_path)

    files = list(folder.rglob("*.txt"))

    if not files:
        print("Nenhum arquivo .txt encontrado.")
        return

    print(f"\nEncontrados {len(files)} arquivos\n")

    for file in files:
        try:
            convert_file(file)
        except Exception as e:
            print(f"[ERRO] {file}: {e}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso:")
        print("python convert_txt_to_json.py pasta/")
        exit()

    convert_recursive(sys.argv[1])