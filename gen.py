import os
import hashlib
import json

# --- НАСТРОЙКИ ---
VERSION = 1  # Укажи здесь версию сборки
OUTPUT_FILE = "manifest.json"
# Папки, которые попадут в манифест
MANAGED_FOLDERS = ['mods', 'config', 'scripts', 'shaderpacks', 'defaultconfigs', 'journeymap']
# Отдельные файлы в корне, которые тоже нужно включить
EXTRA_FILES = ['options.txt'] 

def get_file_hash(file_path):
    """Вычисляет SHA-1 хеш файла."""
    sha1 = hashlib.sha1()
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(65536)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()
    except Exception as e:
        print(f"Ошибка при чтении {file_path}: {e}")
        return None

def generate_manifest():
    """Сканирует папки и генерирует JSON-манифест."""
    manifest = {
        "version": VERSION,
        "files": {}
    }

    print(f"Генерация манифеста версии {VERSION}...")

    # Сканируем папки
    for folder in MANAGED_FOLDERS:
        if not os.path.exists(folder):
            print(f"Предупреждение: Папка {folder} не найдена, пропускаю.")
            continue
            
        for root, dirs, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                # Приводим путь к формату с прямыми слешами для GitHub
                rel_path = os.path.relpath(full_path, ".").replace("\\", "/")
                
                file_hash = get_file_hash(full_path)
                if file_hash:
                    manifest["files"][rel_path] = file_hash
                    # print(f"Добавлен: {rel_path}")

    # Добавляем одиночные файлы из корня
    for file in EXTRA_FILES:
        if os.path.exists(file):
            file_hash = get_file_hash(file)
            if file_hash:
                manifest["files"][file] = file_hash
                # print(f"Добавлен (корень): {file}")
        else:
            print(f"Предупреждение: Файл {file} в корне не найден, пропускаю.")

    # Сохраняем в файл
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("-" * 30)
    print(f"**Готово!** Манифест сохранен в **{OUTPUT_FILE}**")
    print(f"Всего файлов: {len(manifest['files'])}")

if __name__ == "__main__":
    generate_manifest()
