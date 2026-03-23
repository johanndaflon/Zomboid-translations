import json
import re
from pathlib import Path


def read_file_safely(file_path):
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    raise Exception(f"Erro ao ler {file_path}")


def clean_filename(name):
    # Remove sufixo após último "_"
    return name.rsplit("_", 1)[0] if "_" in name else name


def get_prefix_to_remove(filename):
    """
    Define qual prefixo remover baseado no nome do arquivo
    """
    if filename.lower() == "itemname":
        return "ItemName_"
    elif filename.lower() == "recipes":
        return "Recipe_"
    return None


def parse_lua_to_dict(content, prefix_to_remove=None):
    data = {}

    content = re.sub(r"--.*", "", content)

    pattern = re.compile(r'([A-Za-z0-9_\.\s]+)\s*=\s*"([^"]*)"')

    for key, value in pattern.findall(content):
        key = re.sub(r"\s+", " ", key.strip())

        if prefix_to_remove and key.startswith(prefix_to_remove):
            key = key[len(prefix_to_remove):]

        data[key] = value.strip()

    return data


def convert_file(input_path):
    content = read_file_safely(input_path)

    clean_name = clean_filename(input_path.stem)
    prefix_to_remove = get_prefix_to_remove(clean_name)

    data = parse_lua_to_dict(content, prefix_to_remove)

    output_path = input_path.with_name(clean_name + ".json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"[OK] {output_path}")


def convert_recursive(folder_path):
    folder = Path(folder_path)

    for file in folder.rglob("*.txt"):
        try:
            convert_file(file)
        except Exception as e:
            print(f"[ERRO] {file}: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python convert_txt_to_json.py pasta/")
        exit()

    convert_recursive(sys.argv[1])