import json
from pathlib import Path


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def sync_keys(en_data, target_data):
    """
    Garante:
    - mesmas chaves do EN
    - mesma ordem
    - mantém tradução existente
    - adiciona faltantes com valor do EN
    """
    result = {}
    added = 0

    for key in en_data:
        if key in target_data:
            result[key] = target_data[key]  # mantém tradução
        else:
            result[key] = en_data[key]      # fallback EN
            added += 1

    return result, added


def process_file(en_file, target_file):
    en_data = load_json(en_file)

    if en_data is None:
        print(f"[ERRO] EN inválido: {en_file}")
        return

    target_data = load_json(target_file) or {}

    new_data, added = sync_keys(en_data, target_data)

    save_json(new_data, target_file)

    print(f"[SYNC] {target_file} | total: {len(new_data)} | +{added}")


def sync_all(root_path):
    root = Path(root_path)
    en_folder = root / "EN"

    if not en_folder.exists():
        print("Pasta EN não encontrada.")
        return

    en_files = list(en_folder.rglob("*.json"))

    print(f"\n{len(en_files)} arquivos EN encontrados\n")

    for en_file in en_files:
        relative = en_file.relative_to(en_folder)

        for lang_folder in root.iterdir():
            if not lang_folder.is_dir() or lang_folder.name == "EN":
                continue

            target_file = lang_folder / relative
            process_file(en_file, target_file)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python sync_json_from_en.py pasta/mod")
        exit()

    sync_all(sys.argv[1])