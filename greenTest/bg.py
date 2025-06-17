import os


def generate_bg_list(folder, output_file):
    with open(output_file, "w") as f:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)

            # Проверяем, что это файл, а не папка
            if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                f.write(f"{file_path}\n")
    print(f"✅ Файл {output_file} создан")


# Пример использования
if __name__ == "__main__":
    generate_bg_list("augmented_negatives", "bg2.txt")