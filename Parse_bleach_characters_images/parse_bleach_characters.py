import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import threading

URL_PREFIX = "https://bleach.fandom.com"


def __loading_bar__(
    start: bool, number_of_step: int, total_steps: int, number_of_thread: int
) -> None:
    done = int(number_of_step / total_steps * 100) if int(
        number_of_step / total_steps * 100
    ) < 100 or number_of_step == total_steps else 99
    stars = int(
        40 / 100 * done
    ) if int(20 / 100 * done) < 20 or number_of_step == total_steps else 39
    tires = 40 - stars

    if start:
        stars = 0
        tires = 40
        done = 0

    print(f"thread{number_of_thread} <", end="")
    for i in range(stars):
        print("*", end="")

    for i in range(tires):
        print("-", end="")
    print(f"> {done}% ||| {number_of_step} / {total_steps}")


def __get_characters_urls__(urls: list[str]) -> dict[str, str]:
    path_file_page_with_all_characters_urls = "./page_with_all_characters_urls.html"
    all_characters_urls = {}

    for url in urls:

        r = requests.get(url=url)
        with open(
            path_file_page_with_all_characters_urls, "w", encoding="utf-8"
        ) as file:
            file.write(r.text)

        with open(
            path_file_page_with_all_characters_urls, "r", encoding="utf-8"
        ) as file:
            src = file.read()
        page = BeautifulSoup(src, "lxml")

        all_characters_tags_a = page.find("div", class_="mw-body-content").find(
            "div", class_="category-page__members"
        ).find_all("a", class_="category-page__member-link")

        for character_tag_a in all_characters_tags_a:
            all_characters_urls[
                character_tag_a.get("title").strip()
            ] = URL_PREFIX + character_tag_a.get("href").strip()

    return all_characters_urls


def __get_character_images__(name: str, url: str, images_path: str) -> None:
    url = url + "/Галерея"
    path_character_page = "./character_page.html"

    r = requests.get(url=url)
    with open(path_character_page, "w", encoding="utf-8") as file:
        file.write(r.text)

    with open(path_character_page, "r", encoding="utf-8") as file:
        src = file.read()
    page = BeautifulSoup(src, "lxml")

    all_imgs_tags = page.find("div", class_="mw-content-ltr").find_all(
        "a", class_="image lightbox"
    )

    try:
        os.mkdir(f"{images_path}/{name}")

        i = 0
        j = 0
        for img_tag in all_imgs_tags:
            if len(all_imgs_tags) > 200:
                j += 1
                if j % 5 != 0:
                    continue
            try:
                img_tag.get("href"), f"{images_path}/{name}/{i}.png"
                img = requests.get(img_tag.find("img").get("src").strip())
                with open(
                    f"{images_path}/{name}/{i}.jpg", "wb"
                ) as character_path:
                    character_path.write(img.content)
                with open(
                    f"{images_path}/all_images/{name}_{i}.jpg", "wb"
                ) as character_path:
                    character_path.write(img.content)
                i += 1
            except:
                continue

            time.sleep(1)
    except Exception as e:
        print(e)


def __get_characters_images__(
    all_characters_urls: list[(str, str)], start: int, end: int,
    number_of_thread: int
) -> None:
    __loading_bar__(
        start=True,
        number_of_step=0,
        total_steps=(end - start + 1),
        number_of_thread=number_of_thread
    )

    for i in range(start, end):
        __get_character_images__(
            all_characters_urls[i][0], all_characters_urls[i][1],
            "D:/parse_images"
        )
        __loading_bar__(
            start=False,
            number_of_step=(i - start + 1),
            total_steps=(end - start),
            number_of_thread=number_of_thread
        )


def main() -> None:
    url1 = "https://bleach.fandom.com/ru/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8"
    url2 = "https://bleach.fandom.com/ru/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%9C%D0%B0%D1%81%D0%BA%D1%83%D0%BB%D0%B8%D0%BD%2C+%D0%9C%D0%B0%D1%81%D0%BA+%D0%94%D0%B5%0A%D0%9C%D0%B0%D1%81%D0%BA+%D0%94%D0%B5+%D0%9C%D0%B0%D1%81%D0%BA%D1%83%D0%BB%D0%B8%D0%BD"
    url3 = "https://bleach.fandom.com/ru/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8?from=%D0%9C%D0%B0%D1%81%D0%BA%D1%83%D0%BB%D0%B8%D0%BD%2C+%D0%9C%D0%B0%D1%81%D0%BA+%D0%94%D0%B5%0A%D0%9C%D0%B0%D1%81%D0%BA+%D0%94%D0%B5+%D0%9C%D0%B0%D1%81%D0%BA%D1%83%D0%BB%D0%B8%D0%BD"
    urls = [url1, url2, url3]

    all_characters_urls = __get_characters_urls__(urls=urls)
    all_characters_urls = [
        (name, all_characters_urls[name]) for name in all_characters_urls
    ]
    total_steps = len(all_characters_urls)

    thread1 = threading.Thread(
        target=__get_characters_images__,
        args=(all_characters_urls, 0, total_steps // 4, 1)
    )
    thread2 = threading.Thread(
        target=__get_characters_images__,
        args=(all_characters_urls, total_steps // 4, total_steps // 4 * 2, 2)
    )
    thread3 = threading.Thread(
        target=__get_characters_images__,
        args=(
            all_characters_urls, total_steps // 4 * 2, total_steps // 4 * 3, 3
        )
    )
    thread4 = threading.Thread(
        target=__get_characters_images__,
        args=(all_characters_urls, total_steps // 4 * 3, total_steps, 4)
    )

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


main()