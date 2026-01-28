import os
import hashlib
import json

# Список папок и файлов, которые нужно включить в манифест
ITEMS_TO_INCLUDE = [
    'config',
    'defaultconfigs',
    'journeymap',
    'mods',
    'scripts',
    'shaderpacks',
    'options.txt' # Предполагаем, что файл options называется options.txt
]
OUTPUT_JSON = "manifest.json"

def get_sha1(file_path):
    h = hashlib.sha1()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(524288):
                h.update(chunk)
    except FileNotFoundError:
        return None # Если файла нет локально, хеш не нужен
    return h.hexdigest()

def generate():
    manifest = {}
    print("--- Генерация манифеста для вашей сборки ---")
    
    for item in ITEMS_TO_INCLUDE:
        full_path = os.path.abspath(item)
        
        if os.path.isdir(full_path):
            # Если это папка, обходим все файлы внутри
            for root, _, files in os.walk(full_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, ".").replace("\\", "/")
                    print(f"Обработка: {rel_path}")
                    manifest[rel_path] = get_sha1(file_path)
        elif os.path.isfile(full_path):
            # Если это одиночный файл (options.txt)
            rel_path = os.path.relpath(full_path, ".").replace("\\", "/")
            print(f"Обработка: {rel_path}")
            manifest[rel_path] = get_sha1(full_path)
        else:
            print(f"Внимание: '{item}' не найден и будет пропущен.")

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    
    print(f"--- Готово! Файл {OUTPUT_JSON} создан ---")

if __name__ == "__main__":
    generate()
