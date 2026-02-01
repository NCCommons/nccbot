"""
from mass.st4.One_x import OneCase

"""
import sys
import tqdm
from nccommons import api
from api_bots import printe
from api_bots.page_ncc import NEW_API, ncc_MainPage

from mass.st4.One_x_helps import CASE_HELPS
from mass.radio.get_studies import get_stacks_fixed  # (study_id, case_id, get_cach=False)
from mass.radio.bots.update import update_text_add_pd_medical, update_text
from mass.radio.bots.studies_utf import dump_studies_urls_to_files
from mass.radio.jsons_files import jsons

from mass.st4.lists import authors_infos
from sets_dbs.dp_infos.db_duplict_new import insert_url_file

api_new = NEW_API()
# api_new.Login_to_wiki()
# ---
urls_done = []
# ---
PD_medical_pages = []
if "updatetext" in sys.argv:
    from mass.radio.lists.PD_medical import PD_medical_pages_def

    PD_medical_pages = PD_medical_pages_def()


add_studies_cat_del_case = [
    "20060",
]


def printt(s):
    if "nopr" in sys.argv:
        return
    printe.output(s)


class OneCase(CASE_HELPS):
    def __init__(self, case_url, caseId, title, studies_ids, author, work_dump_to_files=False):
        super().__init__(case_url, caseId, title, studies_ids, author)
        self.author = author
        self.caseId = caseId
        self.case_url = case_url
        self.title = title
        self.studies_ids = studies_ids
        self.images_count = 0
        self.img_to_url = {}
        self.files = []
        self.urls_rep = {}
        self.studies_names_cach = {}
        self.studies = {}
        self.category = f"Category:Radiopaedia case {self.caseId} {self.title}"
        # ---
        auth_location = authors_infos.get(self.author, {}).get("location", "")
        self.usa_auth = auth_location.lower().find("united states") != -1
        # ---
        self.image_texts_cach = {}
        self.published = ""
        self.system = ""
        self.work_dump_to_files = "dump_studies_urls_to_files" in sys.argv or work_dump_to_files
        # ---
        if self.case_url in jsons.infos:
            self.published = jsons.infos[self.case_url]["published"]
            # ---
            if not self.author:
                self.author = jsons.infos[self.case_url]["author"]
            # ---
            self.system = jsons.infos[self.case_url]["system"]
        else:
            if self.case_url in jsons.url_to_sys:
                self.system = jsons.url_to_sys[self.case_url]

    def create_category(self, category):
        text = f"* [{self.case_url} Radiopaedia case: {self.title} ({self.caseId})]\n"
        text += f"[[Category:Radiopaedia images by case|{self.caseId}]]"
        # ---
        if self.system:
            text += f"\n[[Category:Radiopaedia cases for {self.system}]]"
        # ---
        if self.title_exists(category):
            return
        # ---
        cat = ncc_MainPage(category)
        # ---
        if cat.exists():
            printt(f"<<lightyellow>> {category} already exists")
            return
        # ---
        new = cat.Create(text=text, summary="create")

        printt(f"Category {category} created..{new=}")

    def get_studies_d(self):
        for study in self.studies_ids:
            # ---
            images = get_stacks_fixed(study, self.caseId, get_cach=True)
            # ---
            # sort images by position key
            images = sorted(images, key=lambda x: x["position"])
            # ---
            self.get_files_names_from_urls(study, images)
            # ---
            print(f"len of self.studies_names_cach[{study}] : {len(self.studies_names_cach.get(study))}")
            # ---
            self.studies[study] = images
            printt(f"study:{study} : len(images) = {len(images)}..")

    def make_image_text(self, image_url, image_id, plane, modality, study_id):
        auth_line = f"{self.author}"
        # ---
        if self.image_texts_cach.get(image_url):
            return self.image_texts_cach[image_url]
        # ---
        auth_url = authors_infos.get(self.author, {}).get("url", "")
        auth_location = authors_infos.get(self.author, {}).get("location", "")
        if auth_url:
            auth_line = f"[{auth_url} {self.author}]"
        # ---
        image_url = self.urls_rep.get(image_url, image_url)
        # ---
        usa_license = ""
        # ---
        if self.usa_auth:
            usa_license = "{{PD-medical}}"
        # ---
        study_url = f"https://radiopaedia.org/cases/{self.caseId}/studies/{study_id}"
        # ---
        set_cat = ""
        # ---
        if len(self.studies) > 1 or str(study_id) in add_studies_cat_del_case or "del2" in sys.argv:
            set_cat = f"[[Category:Radiopaedia case {self.title} id: {self.caseId} study: {study_id}]]"
        # ---
        cat_case = f"[[{self.category}]]"
        # ---
        if (str(study_id) in add_studies_cat_del_case or "del2" in sys.argv) and set_cat:
            cat_case = ""
        # ---
        if cat_case != "":
            set_cat = ""
        # ---
        image_text = "== {{int:summary}} ==\n"

        image_text += (
            "{{Information\n"
            f"|Description = \n"
            f"* Radiopaedia case ID: [{self.case_url} {self.caseId}]\n"
            f"* Study ID: [{study_url} {study_id}]\n"
            f"* Image ID: [{image_url} {image_id}]\n"
            f"* Plane projection: {plane}\n"
            f"* Modality: {modality}\n"
            f"* System: {self.system}\n"
            f"* Author location: {auth_location}\n"
            f"|Date = {self.published}\n"
            f"|Source = [{self.case_url} {self.title}]\n"
            f"|Author = {auth_line}\n"
            "|Permission = http://creativecommons.org/licenses/by-nc-sa/3.0/\n"
            "}}\n"
            "== {{int:license}} ==\n"
            "{{CC-BY-NC-SA-3.0}}\n"
            f"{usa_license}\n"
            f"{cat_case}\n"
            "[[Category:Uploads by Mr. Ibrahem]]\n"
            f"{set_cat}"
        )
        # ---
        self.image_texts_cach[image_url] = image_text
        # ---
        return image_text

    def upload_image(self, image_url, image_name, image_id, plane, modality, study_id):
        if "noup" in sys.argv:
            return image_name
        # ---
        file_title = f"File:{image_name}"
        # ---
        exists = self.title_exists(file_title)
        # ---
        if exists:
            return image_name
        # ---
        image_url = self.urls_rep.get(image_url, image_url)
        # ---
        image_text = self.make_image_text(image_url, image_id, plane, modality, study_id)

        file_name = api.upload_by_url(image_name, image_text, image_url, return_file_name=True, do_ext=True)

        printt(f"upload result: {file_name}")
        # ---
        result = insert_url_file(image_url, file_name)
        # ---
        printe.output(f"<<green>> append_data: {image_url} -> {file_name} -> {result}")
        # ---
        if file_name and file_name != image_name:
            # ---
            if self.usa_auth and "updatetext" in sys.argv and f"File:{file_name}" not in PD_medical_pages:
                update_text_add_pd_medical(f"File:{file_name}")
            # ---
            self.add_category(file_name, self.category)

        return file_name

    def update_images_text(self, to_up, already_in):
        # ---
        tits1 = [x for x in already_in if x in to_up]
        # ---
        if self.usa_auth:
            tits2 = [x for x in tits1 if f"File:{x}" not in PD_medical_pages]
            printt(f"{len(tits1)=}, not in PD_medical_pages: {len(tits2)=}")
        else:
            tits2 = tits1
            printt(f"{len(tits1)=}, {len(tits2)=}")
        # ---
        for fa in tqdm.tqdm(tits2):
            image_url, file_name, image_id, plane, modality, study_id = to_up[fa]
            # ---
            image_url = self.urls_rep.get(image_url, image_url)
            # ---
            image_text = self.make_image_text(image_url, image_id, plane, modality, study_id)
            # ---
            file_title = f"File:{file_name}"
            # ---
            if self.usa_auth:
                update_text_add_pd_medical(file_title)
            else:
                update_text(file_title, image_text)

    def study_set_works(self, to_up, pages, study, already_in):
        # ---
        set_files = []
        # ---
        for fa in already_in:
            if fa not in set_files:
                self.images_count += 1
                set_files.append(fa)
        # ---
        not_in = {k: v for k, v in to_up.items() if not pages.get(k)}
        # ---
        printt(f"not_in: {len(not_in)}")
        # ---
        for i, (image_url, file_name, image_id, plane, modality, study_o) in enumerate(not_in.values(), 1):
            # ---
            printt(f"file: {i}/{len(not_in)} :{file_name}")
            # ---
            new_name = self.upload_image(image_url, file_name, image_id, plane, modality, study_o)
            # ---
            file_n = f"File:{new_name}" if new_name else f"File:{file_name}"
            # ---
            if file_n not in set_files:
                self.images_count += 1
                set_files.append(file_n)
        # ---
        set_title = f"Radiopaedia case {self.title} id: {self.caseId} study: {study}"
        # ---
        if ("updatetext" not in sys.argv or "del2" in sys.argv) and self.images_count > 1:
            self.create_set(set_title, set_files)
            self.create_set_category(set_title, set_files, study, self.studies, self.caseId, self.category)

    def upload_images(self, study, images):
        planes = {}
        modality = ""
        # ---
        to_up = {}
        # ---
        self.img_to_url[study] = {}
        # ---
        for _i, image in enumerate(images, 1):
            public_filename = image.get("public_filename", "")
            image_url = image.get("public_filename", "")
            # ---
            if not image_url:
                printt("no image")
                printt(image)
                continue
            # ---
            if image_url in urls_done:
                self.images_count += 1
                continue
            # ---
            extension, image_url = self.image_url_extension(image, image_url)
            # ---
            urls_done.append(image_url)
            # ---
            image_id = image["id"]
            plane = image["plane_projection"]
            # ---
            if plane not in planes:
                planes[plane] = 0
            planes[plane] += 1
            # ---
            file_name = f"{self.title} (Radiopaedia {self.caseId}-{study} {plane} {planes[plane]}).{extension}"
            # ---
            file_name = file_name.replace("  ", " ").replace("  ", " ").replace("  ", " ")
            # ---
            # fix BadFileName
            file_name = file_name.replace(":", ".").replace("/", ".")
            # ---
            na_in_cach = self.studies_names_cach[study].get(public_filename)
            # print(f"{na_in_cach=}")
            # ---
            file_name = file_name.replace("..", ".")
            # ---
            if na_in_cach and "noc" not in sys.argv:
                file_name = na_in_cach.replace("File:", "")
                # printe.output(f"<<yellow>> make File name from studies_names_cach: {file_name}")
            # ---
            to_up[f"File:{file_name}"] = (image_url, file_name, image_id, plane, modality, study)
            # ---
            taba = {
                "file": f"File:{file_name}",
                "url": image_url,
                "url2": "",
                "id": image_id,
                "text": "",
            }
            # ---
            image_url2 = self.urls_rep.get(image_url, image_url)
            # ---
            if image_url != image_url2:
                taba["url2"] = image_url2
            # ---
            image_text = self.make_image_text(image_url2, image_id, plane, modality, study)
            # ---
            taba["text"] = image_text
            # ---
            self.img_to_url[study][f"File:{file_name}"] = taba
        # ---
        if self.work_dump_to_files:
            return
        # ---
        to_c = list(to_up.keys())
        # ---
        pages = api_new.Find_pages_exists_or_not(to_c)
        # ---
        # print(pages)
        # ---
        already_in = [k for k in to_up if pages.get(k)]
        # ---
        printt(f"already_in: {len(already_in)}")
        # ---
        if "updatetext" in sys.argv:
            # ---
            self.update_images_text(to_up, already_in)
        # ---
        self.study_set_works(to_up, pages, study, already_in)

    def start(self):
        self.get_studies_d()

        for n, (study, images) in enumerate(self.studies.items(), 1):
            printt("<<blue>> ===========================")
            printt(f"<<purple>> work {n}/{len(self.studies)} on study:{study}:")
            # ---
            printt(f"len(images) = {len(images)}")
            # ---
            self.upload_images(study, images)

        if self.img_to_url:
            dump_studies_urls_to_files(self.img_to_url)

        if self.work_dump_to_files:
            return

        printt(f"Images count: {self.images_count}")

        if self.images_count == 0:
            printt("no category created")
            return

        self.create_category(self.category)

    def start_work_dump_to_files(self):
        self.get_studies_d()

        for study, images in self.studies.items():
            printt(f"{study} : len(images) = {len(images)}")
            # ---
            self.upload_images(study, images)

        if self.img_to_url:
            dump_studies_urls_to_files(self.img_to_url)

        return self.img_to_url
