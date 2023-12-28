import os
import re
import zipfile
import json
import aiohttp
import asyncio

default_config = {
    "zip_name_regex": "resources/(.*?)\\.",
    "zipped_path": "./zipped",
    "unzipped_path": "./unzipped",
    "urls": []
}


def read_config():
    filename = "config.json"
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            json.dump(default_config, f)
    with open(filename) as f:
        data = json.load(f)
    return data


async def download_and_maybe_unzip(
    session, url, unzipped_path, zipped_path, zip_name_regex
):
    if not os.path.exists(zipped_path):
        os.makedirs(zipped_path)

    unzip = bool(unzipped_path)
    if unzip and not os.path.exists(unzipped_path):
        os.makedirs(unzipped_path)

    match = re.search(zip_name_regex, url)
    if not match:
        print(f"No match found in URL {url} with regex '{zip_name_regex}'. Skipping.")
        return

    resource_id = match.group(1)
    filename = resource_id + ".zip"
    local_filename = os.path.join(zipped_path, filename)  # Use zipped_path

    if os.path.isfile(local_filename):
        print(
            f"File {os.path.basename(local_filename)} already exists, skipping download."
        )
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    print(f"Downloading...: {os.path.basename(local_filename)}")
    try:
        async with session.get(url, headers=headers) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                while True:
                    chunk = await r.content.read(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    f.flush()
    except Exception as e:
        print(f"Failed to download {local_filename}: {e}")
        return

    if unzip:
        print(f"Unzipping...: {os.path.basename(local_filename)}")
        with zipfile.ZipFile(local_filename, "r") as zip_ref:
            zip_ref.extractall(unzipped_path)
        print(f"Unzipped...: {os.path.basename(local_filename)}")
    else:
        print(f"Downloaded (not unzipped): {os.path.basename(local_filename)}")


async def main():
    config = read_config()
    unzipped_path = config.get("unzipped_path")
    zipped_path = config.get("zipped_path", "./zipped")
    zip_name_regex = config.get("zip_name_regex", "resources/(.*?)\\.")
    urls = config.get("urls", [])

    if not urls:
        print("No Urls Specified. Please update the list in config.json")
        return

    async with aiohttp.ClientSession() as session:
        tasks = [
            download_and_maybe_unzip(
                session, url, unzipped_path, zipped_path, zip_name_regex
            )
            for url in urls
        ]
        await asyncio.gather(*tasks)

    print("Finished....")


if __name__ == "__main__":
    asyncio.run(main())
    input("Press Enter to exit...")
