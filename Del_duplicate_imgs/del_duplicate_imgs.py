import time
from PIL import Image
import imagehash
import os
import shutil


def loading_bar_and_info(start: bool, number_of_steps: int, total_steps: int) -> None:
    done = int(number_of_steps / total_steps * 100) if int(number_of_steps / total_steps * 100) < 100 or number_of_steps == total_steps else 99
    stars = int(40 / 100 * done) if int(20 / 100 * done) < 20 or number_of_steps == total_steps else 39
    tires = 40 - stars

    if start:
        stars = 0
        tires = 40
        done = 0

    print("<", end="")
    for i in range(stars):
        print("*", end="")

    for i in range(tires):
        print("-", end="")
    print("> {0}% ||| {1} / {2}".format(done, number_of_steps, total_steps))

def __shutdown__():
    print("!!! Выключение ПК через минуту !!!")
    time.sleep(60) # ожидание 1 минуту
    os.system("shutdown -s")

def __find_similar_images__(path: str, threshold: int = 5) -> list[str]:
    all_imgs_path = path + "/all_images"
    hashes = {}
    duplicates = []
    num_find_duplicate = 1
    step = 0
    total_steps = len(os.listdir(all_imgs_path))

    for filename in os.listdir(all_imgs_path):
        loading_bar_and_info(False, step, total_steps)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            filepath = os.path.join(all_imgs_path, filename)

            try:
                # Открываем изображение и вычисляем phash
                with Image.open(filepath) as img:
                    img_hash = imagehash.phash(img)

                # Проверяем, есть ли похожий хеш
                found_duplicate = False
                for existing_hash, existing_file in hashes.items():
                    if img_hash - existing_hash < threshold:  # Разница в хешах
                        duplicates.append(filepath)
                        duplicates.append(path + f"{filename[:filename.rfind("_")]}/{filename[filename.rfind("_") + 1 :]}.jpg")
                        found_duplicate = True


                        shutil.copy(existing_file, f"{path}/true_imgs/{num_find_duplicate}.jpg")
                        shutil.copy(filepath, f"{path}/duplicate_imgs/{num_find_duplicate}.jpg")

                        num_find_duplicate += 1

                        break

                if not found_duplicate:
                    hashes[img_hash] = filepath
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {e}")

        step += 1

    return duplicates

def del_duplicates(path: str, threshold: int = 5, off_pc: bool = False) -> None:
    duplicates = __find_similar_images__(path=path, threshold=threshold)

    for duplicate in duplicates:
        try:
            os.remove(duplicate)
            print(f"Удалён дубликат: {duplicate}")
        except Exception as e:
            print(e)

    if off_pc:
        __shutdown__()

path = "D:/parse_images"
threshold = 5

del_duplicates(path=path, threshold=threshold, off_pc=True)
