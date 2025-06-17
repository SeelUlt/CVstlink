import os

def generate_info_list(folder, output_file, width, height):
    with open(output_file, 'w') as f:
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(folder, filename)
                # Записываем путь и аннотацию
                f.write(f"{path} 1 0 0 {width} {height}\n")
    print(f"✅ Создан файл: {output_file}")

# Пример использования
# generate_info_list("augmented_positives", "info.lst", 35, 35)

def generate_bg_list(folder, output_file):
    with open(output_file, 'w') as f:
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                path = os.path.join(folder, filename)
                f.write(f"{path}\n")
    print(f"✅ Создан файл: {output_file}")

# Пример использования
generate_bg_list("negatives", "bg.txt")