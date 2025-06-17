from PIL import Image, ImageEnhance
import os
import numpy as np


def augment_image(filepath, output_dir):
    name, ext = os.path.splitext(os.path.basename(filepath))
    try:
        img = Image.open(filepath).convert("RGB")
    except Exception as e:
        print(f"Ошибка открытия: {filepath} → {e}")
        return []

    augmented_files = []

    # Повороты
    for angle in [5, -5, 10, -10]:
        rotated = img.rotate(angle, expand=True).resize(img.size)
        new_name = f"{name}_augmented_rot{angle}{ext}"
        new_path = os.path.join(output_dir, new_name)

        counter = 1
        while os.path.exists(new_path):
            new_path = os.path.join(output_dir, f"{name}_augmented_rot{angle}_{counter}{ext}")
            counter += 1

        try:
            rotated.save(new_path)
            augmented_files.append(new_path)
        except Exception as e:
            print(f"Ошибка сохранения {new_path}: {e}")

    # Яркость
    bright = ImageEnhance.Brightness(img).enhance(1.2)
    new_name = f"{name}_augmented_bright{ext}"
    new_path = os.path.join(output_dir, new_name)

    counter = 1
    while os.path.exists(new_path):
        new_path = os.path.join(output_dir, f"{name}_augmented_bright_{counter}{ext}")
        counter += 1

    try:
        bright.save(new_path)
        augmented_files.append(new_path)
    except Exception as e:
        print(f"Ошибка сохранения {new_path}: {e}")

    # Контраст
    contrast = ImageEnhance.Contrast(img).enhance(1.3)
    new_name = f"{name}_augmented_contrast{ext}"
    new_path = os.path.join(output_dir, new_name)

    counter = 1
    while os.path.exists(new_path):
        new_path = os.path.join(output_dir, f"{name}_augmented_contrast_{counter}{ext}")
        counter += 1

    try:
        contrast.save(new_path)
        augmented_files.append(new_path)
    except Exception as e:
        print(f"Ошибка сохранения {new_path}: {e}")

    # Шум
    img_array = np.array(img, dtype=np.int16)
    noise = np.random.randint(-15, 15, img_array.shape, dtype=np.int16)
    noisy = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    noisy_img = Image.fromarray(noisy)

    new_name = f"{name}_augmented_noise{ext}"
    new_path = os.path.join(output_dir, new_name)

    counter = 1
    while os.path.exists(new_path):
        new_path = os.path.join(output_dir, f"{name}_augmented_noise_{counter}{ext}")
        counter += 1

    try:
        noisy_img.save(new_path)
        augmented_files.append(new_path)
    except Exception as e:
        print(f"Ошибка сохранения {new_path}: {e}")

    return augmented_files


def augment_folder(input_dir, output_dir="augmented_positives", count=5):
    os.makedirs(output_dir, exist_ok=True)
    all_augmented = []

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        if not os.path.isfile(file_path) or filename.startswith("."):
            continue

        _, ext = os.path.splitext(filename)
        if ext.lower() not in ('.png', '.jpg', '.jpeg'):
            print(f"Формат {ext} не поддерживается: {filename}")
            continue

        for i in range(count):
            print(f"\nАугментация файла: {filename} (копия {i + 1})")
            augmented = augment_image(file_path, output_dir)
            all_augmented.extend(augmented)

    print(f"\n✅ Создано аугментированных изображений: {len(all_augmented)}")
    return all_augmented


if __name__ == "__main__":
    augment_folder("greenTest/negatives", "augmented_negatives", count=5)