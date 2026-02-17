"""

from mass.st4.One_x_helps import CASE_HELPS

"""

import mimetypes
import os
import sys

from api_bots.page_ncc import NEW_API, ncc_MainPage
from fix_sets.name_bots.files_names_bot import get_files_names
from mass.radio.bots.add_cat import add_cat_to_images  # add_cat_to_images(sets, cat_title)
from mass.radio.bots.bmp import work_bmp
import logging
logger = logging.getLogger(__name__)

api_new = NEW_API()
# api_new.Login_to_wiki()

def printt(s):
    if "nopr" in sys.argv:
        return
    logger.info(s)

class CASE_HELPS:
    def __init__(self, case_url, caseId, title, studies_ids, author):
        self.case_url = case_url
        self.caseId = caseId
        self.title = title
        self.studies_ids = studies_ids
        self.author = author

    def get_files_names_from_urls(self, study, images):
        # ---
        maain_uurls = list({x["public_filename"] for x in images})
        # ---
        files_names = get_files_names(maain_uurls, {}, study, noapi=True)
        # ---
        self.studies_names_cach[study] = files_names

    def get_image_extension(self, image_url):
        # Split the URL to get the filename and extension
        _, filename = os.path.split(image_url)

        # Split the filename to get the name and extension
        _name, extension = os.path.splitext(filename)

        # Return the extension (without the dot)
        ext = extension[1:]
        return ext or "jpeg"

    def image_url_extension(self, image, image_url):
        extension = mimetypes.guess_extension(image["content_type"])
        # ---
        if not extension:
            # extension = image_url.split(".")[-1].lower()
            extension = self.get_image_extension(image_url)
        # ---
        if not extension:
            extension = image["fullscreen_filename"].split(".")[-1].lower()
            extension = self.get_image_extension(image["fullscreen_filename"])
        # ---
        if extension == "bmp":
            if not self.work_dump_to_files:
                image_url2, extension = work_bmp(image_url)
                self.urls_rep[image_url2] = image_url
                image_url = image_url2
        # ---
        extension = extension.strip()
        if extension.startswith("."):
            extension = extension[1:]
        # ---
        return extension, image_url

    def title_exists(self, title):
        # ---
        pages = api_new.Find_pages_exists_or_not([title], noprint=True)
        # ---
        if pages.get(title):
            printt(f"<<lightyellow>> api_new {title} already exists")
            return True
        # ---
        # file_page = ncc_MainPage(title, 'www', family='nccommons')
        # ---
        # if file_page.exists():
        #     printt(f'<<lightyellow>> File:{title} already exists')
        #     return True
        # ---
        return False

    def create_set_category(self, set_title, set_files, study_id, studies, caseId, category):
        # ---
        if "create_set_category" in sys.argv:
            return
        # ---
        study_url = f"https://radiopaedia.org/cases/{caseId}/studies/{study_id}"
        # ---
        cat_title = f"Category:{set_title}"
        # ---
        logger.info(f"len of set_files: {len(set_files)} /// cat_title:{cat_title}")
        # ---
        if len(studies) == 1 and "c_it" not in sys.argv:
            logger.info(f"len of studies: {len(studies)}, return (don't create set cats for 1 study)")
            logger.info("add 'c_it' to sys.argv to create set cats for 1 study")
            return
        # ---
        text = f"* [{study_url} study: {study_id}]"
        text += f"\n[[{category}|*]]"
        text += f"\n[[Category:Radiopaedia studies|{study_id}]]"
        # ---
        done = False
        # ---
        if self.title_exists(cat_title):
            done = True
        # ---
        if not done:
            cat = ncc_MainPage(cat_title)
            # ---
            if cat.exists():
                printt(f"<<lightyellow>> {cat_title} already exists")
                done = True
        # ---
        if not done:
            new = cat.Create(text=text, summary="create")
            # ---
            if new:
                done = True
            # ---
            printt(f"Category {cat_title} created..{new=}")
        # ---
        if done:
            add_cat_to_images(set_files, cat_title, category)

    def create_set(self, set_title, set_files):
        text = ""
        # ---
        if "noset" in sys.argv:
            return
        # ---
        set_files = [x.strip() for x in set_files if x.strip()]
        # ---
        if len(set_files) < 2:
            return
        # ---
        if self.title_exists(set_title):
            return
        # ---
        text += "{{Imagestack\n|width=850\n"
        text += f"|title={set_title}\n|align=centre\n|loop=no\n"
        # ---
        for image_name in set_files:
            image_name = image_name.replace("_", " ")
            text += f"|{image_name}|\n"
        # ---
        text += "\n}}\n[[Category:Image set]]\n"
        text += f"[[Category:{set_title}|*]]\n"
        text += "[[Category:Radiopaedia sets]]\n"
        # text += "[[Category:Sort studies fixed]]"
        # ---
        page = ncc_MainPage(set_title)
        # ---
        if not page.exists():
            new = page.Create(text=text, summary="")
            return new
        # ---
        # if text != page.get_text():
        #     printt(f'<<lightyellow>>{set_title} already exists')
        p_text = page.get_text()
        # ---
        if p_text.find(".bmp") != -1:
            p_text = p_text.replace(".bmp", ".jpg")
            ssa = page.save(newtext=p_text, summary="update", nocreate=0, minor="")
            return ssa

        elif "fix" in sys.argv:
            if text == p_text:
                printt("<<lightyellow>> no changes")
                return True
            ssa = page.save(newtext=text, summary="update", nocreate=0, minor="")
            return ssa

    def add_category(self, file_name, category):
        # ---
        if "add_category" not in sys.argv:
            return
        # ---
        add_text = f"\n[[{category}]]"
        # ---
        file_title = f"File:{file_name}"
        # ---
        page = ncc_MainPage(file_title)
        # ---
        p_text = page.get_text()
        # ---
        if p_text.find("[[Category:Radiopaedia case") != -1:
            logger.info(f"<<lightyellow>>{file_title} has cat:")
            logger.info(p_text)
        # ---
        if p_text.find(category) == -1:
            new_text = p_text + add_text
            ssa = page.save(newtext=new_text, summary=f"Bot: added [[:{category}]]")
            return ssa
