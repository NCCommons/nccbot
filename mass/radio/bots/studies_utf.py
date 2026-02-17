"""

from mass.radio.bots.studies_utf import dump_studies_urls_to_files

"""

import json

from fix_mass.dir_studies_bot import studies_urls_to_files_dir


def dump_studies_urls_to_files(tab):
    # tab[study][f"File:{file_name}"] = {"url": image_url, "id": image_id}

    for study, files in tab.items():
        file = studies_urls_to_files_dir / f"{study}.json"
        # ---
        if not files:
            print(f"no file to dump to {file}.")
            continue
        # ---
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(files, f, ensure_ascii=False, indent=2)
                print(f"Completed dumping {len(files)} items from {study} to {file}.")
        except Exception as e:
            print(f"Failed dumping {len(files)} items from {study} to {file}: {e}")
        # ---
    print(f"dump_studies_urls_to_files {len(tab)}")
