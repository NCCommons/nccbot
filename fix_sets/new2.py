"""
python3 core8/pwb.py mass/st3/o del2 ask 167295
python3 core8/pwb.py mass/st3/o del2 ask
python3 core8/pwb.py mass/st3/o del2 ask
python3 core8/pwb.py mass/st3/o del2 ask
python3 core8/pwb.py mass/st3/o del2 ask 45822
python3 core8/pwb.py mass/st3/o del2 ask 16850
python3 core8/pwb.py mass/st3/o del2 ask 90352

tfj run cdcf --image python3.9 --command "$HOME/local/bin/python3 core8/pwb.py mass/st3/o updatetex 90505 nodone noid noc del2 multi"

python3 core8/pwb.py fix_sets/new ask 109711 # 2files
python3 core8/pwb.py fix_sets/new ask 143304
python3 core8/pwb.py fix_sets/new ask 80304 printtext
python3 core8/pwb.py fix_sets/new ask 14038 printtext
python3 core8/pwb.py fix_sets/new ask 62191 printtext
python3 core8/pwb.py fix_sets/new ask 144866 nodudb
python3 core8/pwb.py fix_sets/new ask nodb 101035
python3 core8/pwb.py fix_sets/new ask nodb
python3 core8/pwb.py fix_sets/new ask nodb 135999
python3 core8/pwb.py fix_sets/new ask 50090 50088
python3 core8/pwb.py fix_sets/new ask nodb 22435
python3 core8/pwb.py fix_sets/new ask nodb
python3 core8/pwb.py fix_sets/new ask nodb 108736
python3 core8/pwb.py fix_sets/new ask 101946
python3 core8/pwb.py fix_sets/new ask 104863
python3 core8/pwb.py fix_sets/new ask 101829
python3 core8/pwb.py fix_sets/new ask 13950
python3 core8/pwb.py fix_sets/new ask 24240
python3 core8/pwb.py fix_sets/new ask 71160
python3 core8/pwb.py fix_sets/new ask 80302
python3 core8/pwb.py fix_sets/new ask 14090
python3 core8/pwb.py fix_sets/new ask all
"""
import re
import sys
from api_bots import printe
from fix_sets.ncc_api import ncc_MainPage

from fix_sets.bots.stacks import get_stacks  # get_stacks(study_id)
from fix_sets.bots.has_url import has_url_append, find_has_url  # , already_has_url

from fix_sets.bots2.text_cat_bot import add_cat_to_set, fix_cats
from fix_sets.bots2.filter_ids import filter_no_title
from fix_sets.bots2.done2 import filter_done_list
from fix_sets.bots2.set_text2 import make_text_study
from fix_sets.bots2.move_files2 import to_move_work

from fix_mass.files import studies_titles, studies_titles2
from fix_sets.bots.study_files import get_study_files
from fix_sets.new_works.get_info import get_study_infos


def update_set_text(title, n_text, study_id):
    # ---
    printe.output(f"<<yellow>> update_set_text: {title}")
    # ---
    page = ncc_MainPage(title, "www", family="nccommons")
    # ---
    p_text = page.get_text()
    # ---
    n_text += "\n[[Category:Sort studies fixed]]"
    # ---
    if p_text.find("[[Category:Radiopaedia case ") == -1:
        n_text = add_cat_to_set(n_text, study_id, title)
    # ---
    n_text = fix_cats(n_text, p_text)
    # ---
    if p_text.strip() == n_text.strip():
        printe.output("no changes..")
        return
    # ---
    if n_text.find("[[Category:Image set]]") != -1 and n_text.find("[[Category:Radiopaedia sets]]") != -1:
        if n_text.find("[[Category:Sort studies fixed]]") != -1:
            n_text = n_text.replace("[[Category:Image set]]\n", "")
    # ---
    page.save(newtext=n_text, summary="Fix sort.")

def fix_one_url(text, study_id, files=None):
    # ---
    # if "fix_one_url" not in sys.argv and "ask" not in sys.argv:
    if "fix_one_url" not in sys.argv:
        return text
    # ---
    # count how many http links in the text
    http_links = text.count("|http")
    # ---
    if http_links != 1:
        return text
    # ---
    printe.output(f"<<red>> text has http links ({http_links})... study_id: {study_id}")
    # ---
    if not files:
        files = get_study_files(study_id)
    # ---
    print(files)
    # ---
    files2 = [x for x in files if x not in text]
    # ---
    printe.output(f"len of files2: {len(files2)}")
    # ---
    if len(files2) != 1:
        return text
    # ---
    n_file = files2[0]
    # ---
    # match url in text
    pat = r"\|https?://.*?\|"
    # ---
    fi = re.findall(pat, text)
    # ---
    if len(fi) != 1:
        return text
    # ---
    url = fi[0]
    # ---
    if url.find("https://") == -1:
        return text
    # ---
    printe.output(f"<<yellow>> fix_one_url: {url}")
    # ---
    text = text.replace(url, f"|File:{n_file}|")
    # ---
    return text


def has_http_links(text, study_id):
    # ---
    if text.find("|http") == -1:
        return False
    # ---
    # count how many http links in the text
    http_links = text.count("|http")
    # ---
    printe.output(f"<<red>> text has http links ({http_links})... study_id: {study_id}")
    # ---
    has_url_append(study_id, text)
    # ---
    if "printtext" in sys.argv:
        printe.output(text)
    # ---
    return True


def work_one_study(study_id, study_title=""):
    # ---
    study_title = study_title or studies_titles.get(study_id) or studies_titles2.get(study_id)
    # ---
    if not study_title:
        printe.output(f"<<red>> study_title is empty... study_id: {study_id}")
        return
    # ---
    printe.output(f"{study_id=}, {study_title=}")
    # ---
    if find_has_url(study_id):
        return
    # ---
    study_infos = get_study_infos(study_id)
    # ---
    study_infos = {v["url"]: v for x, v in study_infos.items()}
    # ---
    json_data = get_stacks(study_id)
    # ---
    if not json_data:
        printe.output(f"\t\t<<lightred>>SKIP: <<yellow>> {study_id=}, no json_data")
        return "", {}
    # ---
    text, to_move, urls2 = make_text_study(json_data, study_title, study_id, study_infos=study_infos)
    # ---
    text = text.strip()
    # ---
    text = fix_one_url(text, study_id)
    # ---
    if has_http_links(text, study_id):
        return
    # ---
    if not text:
        printe.output(f"<<red>> text is empty... study_id: {study_id}")
        return
    # ---
    text = to_move_work(text, to_move, study_id)
    # ---
    update_set_text(study_title, text, study_id)


def main(ids):
    # ---
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    printe.output(f"<<purple>> len of ids: {len(ids)}")
    # ---
    ids = filter_done_list(ids)
    # ---
    ids_to_titles = filter_no_title(ids)
    # ---
    for n, (study_id, study_title) in enumerate(ids_to_titles.items()):
        print(f"_____________\n {n=}/{len(ids_to_titles)}:")
        work_one_study(study_id, study_title)


if __name__ == "__main__":
    ids = [arg.strip() for arg in sys.argv if arg.strip().isdigit()]
    # ---
    main(ids)
