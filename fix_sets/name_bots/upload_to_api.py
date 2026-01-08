"""

from fix_sets.name_bots.upload_to_api import get_from_api

"""
import sys
from pathlib import Path

from api_bots import printe
from mass.radio.bots.bmp import work_bmp
from fix_sets.ncc_api import post_ncc_params
from nccommons.ext import get_new_ext


def get_from_api(url, filename="", do_ext=True, file_text="", comment=""):
    """

    Uploads a file to Wikipedia using a URL.

    """
    # ---
    file_name = filename
    # ---
    if not url:
        printe.output("<<lightred>>upload_by_url: no url")
        return ""
    # ---
    if "noapi" in sys.argv:
        return ""
    # ---
    if file_name.startswith("File:"):
        file_name = file_name.replace("File:", "")
    # ---
    # extension = get_image_extension(image_url)
    # ---
    if file_name.endswith(".bmp"):
        url, extension = work_bmp(url, just_do=True)
        # file_name = file_name.replace(".bmp", extension)
        file_name = str(Path(file_name).with_suffix(f".{extension}"))
    # ---
    if not file_name:
        return ""
    # ---
    file_name = file_name.replace("_", " ")
    # ---
    params = {
        "action": "upload",
        "format": "json",
        "filename": file_name,
        "url": url,
        "comment": comment,
        "text": file_text,
        "utf8": 1,
        "formatversion": "2",
    }
    # ---
    # {'upload': {'result': 'Success', 'filename': 'Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'imageinfo': {'timestamp': '2023-11-29T20:12:26Z', 'user': 'Mr. Ibrahem', 'userid': 13, 'size': 52289, 'width': 506, 'height': 379, 'parsedcomment': '', 'comment': '', 'html': '', 'canonicaltitle': 'File:Pediculosis Palpebrarum (Dermatology Atlas 1).jpg', 'url': 'https://nccommons.org/media/f/fd/Pediculosis_Palpebrarum_%28Dermatology_Atlas_1%29.jpg', 'descriptionurl': 'https://nccommons.org/wiki/File:Pediculosis_Palpebrarum_(Dermatology_Atlas_1).jpg', 'sha1': '1df195d80a496c6aadcefbc6d7b8adf13caddafc', 'metadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}, {'name': 'MEDIAWIKI_EXIF_VERSION', 'value': 2}], 'commonmetadata': [{'name': 'JPEGFileComment', 'value': [{'name': 0, 'value': 'File written by Adobe Photoshop¨ 4.0'}]}], 'extmetadata': {'DateTime': {'value': '2023-11-29T20:12:26Z', 'source': 'mediawiki-metadata', 'hidden': ''}, 'ObjectName': {'value': 'Pediculosis Palpebrarum (Dermatology Atlas 1)', 'source': 'mediawiki-metadata', 'hidden': ''}}, 'mime': 'image/jpeg', 'mediatype': 'BITMAP', 'bitdepth': 8}}}
    # ---
    # { "upload": { "result": "Success", "filename": "Test1x.jpeg", "imageinfo": { "timestamp": "2024-07-24T22:28:32Z", "user": "Mr. Ibrahem", "userid": 13, "size": 67938, "width": 512, "height": 512, "parsedcomment": "", "comment": "", "html": "", "canonicaltitle": "File:Test1x.jpeg", "url": "https://nccommons.org/media/3/3f/Test1x.jpeg", "descriptionurl": "", "sha1": "e145b86530458d59bd0d9f3b709954d5301a18c9", "metadata": [ { "name": "MEDIAWIKI_EXIF_VERSION", "value": 2 } ], "commonmetadata": [], "extmetadata": { "DateTime": { "value": "2024-07-24T22:28:32Z", "source": "mediawiki-metadata", "hidden": "" }, "ObjectName": { "value": "Test1x", "source": "mediawiki-metadata" } }, "mime": "image/jpeg", "mediatype": "BITMAP", "bitdepth": 8 } } }
    # ---
    # { "upload": { "result": "Warning", "warnings": { "duplicate": [ "Angiodysplasia_-_cecal_active_bleed_(Radiopaedia_168775-136954_Coronal_91).jpeg" ] }, "filekey": "1b00hc5unqxw.olk8pi.13.", "sessionkey": "1b00hc5unqxw.olk8pi.13." } }
    # ---
    # { "upload": { "result": "Warning", "warnings": { "exists": "Axillary_hidradenitis_suppurativa_(Radiopaedia_91902-109711_None_2).png", "nochange": { "timestamp": "2024-01-09T02:30:04Z" } }, "filekey": "x.", "sessionkey": "x" } }
    # ---
    data = post_ncc_params(params, do_error=False)
    # ---
    upload_result = data.get("upload", {})
    # ---
    duplicate = upload_result.get("warnings", {}).get("duplicate", [""])[0].replace("_", " ")
    # ---
    success = upload_result.get("result") == "Success"
    error = data.get("error", {})
    # ---
    exists = upload_result.get("warnings", {}).get("exists", "").replace("_", " ")
    # ---
    error = data.get("error", {})
    # ---
    du = ""
    # ---
    if success:
        new_filename = upload_result.get("filename") or file_name
        printe.output(f"<<green>> new upload Success, File:{new_filename}")
        return f"File:{new_filename}"

    elif duplicate:
        du = "File:" + duplicate
        # ---
        printe.output(f"duplicate, find url_file_upload: {du}")
        return du
    elif exists:
        du = "File:" + exists
        du = du.replace("_", " ")
        # ---
        printe.output(f"exists, find url_file_upload: {du}")
        return du

    elif error:
        error_code = error.get("code", "")
        error_info = error.get("info", "")
        # ---
        printe.output("____________________________________________")
        printe.output(f"<<yellow>> {file_name=}, {url=}")
        printe.output(f"<<lightred>> error when upload_by_url, error_code:{error_code}")
        # ---
        if error_code == "verification-error":
            if do_ext and "MIME type of the file" in error_info:
                new_file_name = get_new_ext(error_info, file_name)
                if new_file_name:
                    return get_from_api(url, filename=new_file_name, do_ext=False, file_text=file_text)
    else:
        print(data)
    # ---
    return du
