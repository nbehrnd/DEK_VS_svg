# name:    dek_csv.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-05-31 (YYYY-MM-DD)
# edit:    2020-06-07 (YYYY-MM-DD)
#
""" Consolidation of dek_quick_csv.py's dek2anki.csv relational table.

The content of file dek2anki.csv, written by script dek_quick_csv.py,
is extended by this script with tags in a third column.  Eventually,
the lines in this relational table follow a pattern of

Aufstand; <img src="DEK_VS_steno_svg_-_Aufstand.svg">; DEK_b auf st

to relate a key (here, "Auftstand"), with the address of the .svg file
(second column), and tags about this entry (third column).  To allow a
parallel use of either this project's Anki deck or others, each entry
is tagged by "DEK_b".  To ease self study, additional tags may be set,
too.  At present, this approach is based on the comparison of strings
in the file name,

+ to indicate entries contrasting symbolizations like the illustration
  of Automaten_ABER_Automatten.svg.

+ to indicate the _possible_ occurence of a symbolization about groups
  of vowels, or whole syllabels.  This identification, and the discern
  of symbolizations e.g., of "mp" but not "mpf", "dr" but not "ndr" is
  at an experimental stage.  At present, not all 100 kuerzel, nor all
  vowel symbolizations are known to the set of rules here.  Equally it
  is known that this simple approach equally yields "false positives"
  suggesting the presence of a special symbolization, than there is
  none (e.g., Bausparer does not use the symbolization of "aus").  It
  is the intent to improve the attribution gradually.

Again, because Anki expects an .csv in UTF-8 and because of the use of
special characters like umlauts, the scripts action, launched on the
the CLI by

python dev_csv.py

is restricted to Python 3. """

import os
import shutil
import sys

from hyphen import Hyphenator
h_de = Hyphenator('de_DE')


def check_python():
    """ Assure the script is used with Python 3, only. """
    if sys.version_info[0] == 2:
        print("\nThe script works with Python 3, only.\n")
        sys.exit()
    elif sys.version_info[0] == 3:
        pass
    else:
        print("\nBe sure to call the script with Python 3, only.\n")


def only_check_presence_workshop():
    """ This time, only probe if there is folder dek_workshop. """
    presence_raw_data = False
    for element in os.listdir("."):
        if (str(element) == str("dek_workshop")) and os.path.isdir(element):
            presence_raw_data = True
            break
    if presence_raw_data is False:
        print("Folder 'dek_workshop' is missing.  Exit.")
        sys.exit()


def remove_from_list():
    """ Remove files deemed incompatible to the Anki deck format. """
    root = os.getcwd()
    old_register = []
    new_register = []
    # The black list about files to exclude from the relational table
    # intentionally uses the shorter, easier to maintain list of keys
    # instead of the lengthier file names.
    black_list = [
        '2_Grundlinien', '2_Grundlinien_Linienstärke_sechs',
        '2_Grundlinien_groß', '3_Grundlinien_Linienstärke_sechs',
        'Grundlinien', 'SETZKASTEN_NUR_Buchstaben', 'SETZKASTEN_NUR_Kürzel',
        'SETZKASTEN_mit_vielfältigen_Buchstabenformen', '1_ABER_2',
        'a_b_br_d_e_f_g_gr_gl_h_j_k_l_ll_m_n_o_p_r_t_tr_v_w_ö',
        'a_b_br_d_e_f_g_gr_gl_h_j_k_l_ll_m_n_o_p_r_t_tr_v_w_ö_v2',
        'a_b_br_d_e_f_g_gr_gl_h_i_j_k_l_ll_m_n_o_p_r_t_tr_v_w_ö',
        'a_b_br_d_e_f_g_gr_gl_h_i_j_k_l_ll_m_n_o_p_r_t_tr_v_w_ö_v2',
        'a_b_br_d_e_f_g_gr_h_k_l_ll', 'a_b_br_d_f', 'ä,_ö_ü,_ei,_u,_e,_i,_o',
        'auf,_hat,_das,_für', 'Baumast_Bau-Mast', 'Baumast_Baum-Ast',
        'b_be-_r_er_f_für',
        'b_br_d_f_g_gr_h_j_k_l_m_n_p_r_rs_s_ss_t_Aufstrich_t_tr_v_w',
        'b_br_d_f_g_gr_h_j_k_l_m_n_p_r_rs_s_ss_t_tr_v_w',
        'b_br_d_f_g_gr_h_j_k_l_m_n_p_r_s_t_tr_v_w',
        'be-_das_dem_den_der_deutsch_die_er_er-_es',
        'betr_betreffend_betreffs_betrifft', 'br_cr_gr_tr_kr_rr', 'gl', 'll',
        'm_n_o_p_r_t_tr_w_ö', 'n_v2', 'pr_wr_schw_zw', 'r_n_d', 'schl',
        'sch_schm_schn_schw',
        'sch_schm_schn_schw_sp_z_zw_heit_ung_schr_spr_str_zr',
        'sie_APOSTROPH_s', 'Vokale_und_Diphthonge_v1a',
        'Vokale_und_Diphthonge_v1a1'
        'Vokale_und_Diphthonge_v1b1', 'Vokale_und_Diphthonge_v1c',
        'Vokale_und_Diphthonge_v1c1', 'Vokale_und_Diphthonge_v2a',
        'Vokale_und_Diphthonge_v2a1', 'Vokale_und_Diphthonge_v2c',
        'Vokale_und_Diphthonge_v2c1', 'Vokale_und_Diphthonge_v3a',
        'Vokale_und_Diphthonge_v4a', 'Vokale_und_Diphthonge_v4c',
        'Vokale_und_Diphthonge_v6c', 'Vokale_und_Diphthonge_v7c',
        'Vokale_und_Diphthonge_v8c', 'Vokale_und_Diphthonge_v9c',
        'Vokale_und_Diphthonge_v10c', 'Vokale_und_Diphthonge_v11c',
        'Vokale_und_Diphthonge_v12c', 'Vokale_und_Diphthonge_v13c', 'z_zr_zw'
    ]

    # Remove of empty examples
    #
    # The .svg illustrations used in this project are created by
    # WikiMedia author Thirunavukkarasye-Raveendran in small batches.
    # There are a few the author now no longer considers as good and
    # marks them internally by the string "LEER".  Eventually, upon
    # sufficient completion of his project and to be initiated by
    # Thirunavukkarasye-Raveendran, only a Wikimedia administrator is
    # allowed to remove these files from Wikimedia's servers.
    #
    # For now, these files already may be excluded from the creation
    # of the Anki deck.  In the set of data fetched by May 30, 2020,
    # they were identified with searchmonkey's content analysis of the
    # .svg files for the string "LEER".
    #
    # https://packages.debian.org/bullseye/searchmonkey

    empty_files = []
    empty_files = [
        'April_v2', 'aqu_v2', 'ausleeren', 'beglauben', 'Beine_v2',
        'Ceylon_v2', 'Disponent_v2', 'friedllich', 'fügsam_v2', 'meinen',
        'Militär_v1', 'Militär_v2', 'Militär_v3', 'Mistral_v2', 'Nachfalter',
        'Rohheit_v2', 'Schläge_v2', 'sogenannt_v2', 'Transport_v2',
        'vermittet', 'Volk_v2', 'Weltall_v2', 'Wikipedia_v1', 'Wikipedia_v2',
        'ich_geben_dem_Mann_den_Kaffee'
    ]

    os.chdir("dek_workshop")
    try:
        with open("dek2anki.csv", mode="r") as source:
            old_register = source.readlines()
    except IOError:
        print("\nFile 'dek2anki.csv' is inaccessible.")
        print("Maybe a run of dek_quick_csv.py solves this issue.\n")
        sys.exit()

    for line in old_register:
        global check
        check = str(line).strip()  # remove, e.g. line feed
        check = check.split(";")[0]  # identify the easier to use key
        if (check in black_list) or (len(str(check)) > 70):
            pass
        else:
            analysator()

            retain = ''.join([str(line).strip(), "; ", tag_line])
            new_register.append(retain)

    with open("dek2anki.csv", mode="w") as newfile:
        for entry in new_register:
            retain = str("{}\n".format(entry))
            newfile.write(retain)

    os.chdir(root)


def folder_cleaner():
    """ Remove obsolete files from 'dek_workshop'. """
    root = os.getcwd()
    old_register2 = []
    stem = str("DEK_VS_steno_svg_-_")

    os.chdir("dek_workshop")
    shutil.copy("dek2anki.csv", root)
    with open('dek2anki.csv', mode="r") as source:
        for line in source:
            retain = str(line).strip()
            retain = retain.split(";")[0]

            retain = ''.join([stem, retain, str(".svg")])
            old_register2.append(retain)
    old_register2.sort()

    for file in os.listdir("."):
        if file.endswith(".svg") and (str(file) in old_register2):
            pass
        else:
            os.remove(file)


#    shutil.copy("dek2anki.csv", root)
    os.chdir(root)


def remove_from_folder():
    """ Optionally remove files no longer listed from dek_workshop """
    print("\nAn annotated relation table, 'csv2anki.csv', was written.")
    print("\nTo remove files no longer listed from 'dek_workshop', press")
    print("[y]es    to delete them now.")
    print("[n]o     to keep them.")
    print("[q]uit   to leave the program altogether.")
    print("\nConfirm your choice with ENTER.")

    choice = str(input()).lower()
    if str(choice) == str("y"):
        print("Obsolete files will be deleted.")
        folder_cleaner()
    elif str(choice) == str("n"):
        print("All files will be retained.  Exit.")
        sys.exit()
    elif str(choice) == str("q"):
        print("Exit of the script.")
        sys.exit()
    else:
        print("Invalid input.  The script closes.")
        sys.exit()


def analysator():
    """ Provide meaningful tags for column #3 in file 'csv2anki.csv'. """
    global tag_line
    tag_line = str("DEK_b")

    # rule contrasting illustrations:
    if str("ABER") in check:
        tag_line += str(" Vergleich")

    # Identification of 17 non-ambigous symbolizations -- a concept.
    #
    # It is plausible that these lists are incomplete.
    # It is complemented by later rules discerning e.g., 'st' from 'str'.
    test = str(check).lower()
    grouped_consonants = [
        'br', 'cr', 'fr', 'gr', 'kr', 'mpf', 'ndr', 'pfr', 'rdr', 'schl',
        'schm', 'schn', 'schr', 'spr', 'str', 'wr', 'zw'
    ]

    # Incomplete list of 59, apparently easier to retrieve, kuerzel.
    # Again, there are some for this simple string-based approach is
    # not working well enough (e.g., 'wo' vs. 'woll' or 'worden'; or
    # 'in' vs. 'meine', 'deine'. 'hint', 'keine', 'seine' or 'sind';
    # or 'un' vs. 'unter'; or reserved symbolizations like 'dem' which
    # is not used in 'demokratisch') thus not yet considered here.
    kuerzel = [
        'also', 'ander', 'ant', 'auf', 'aus', 'besonder', 'bis', 'dar',
        'deine', 'dessen', 'deutsch', 'dies', 'doch', 'durch', 'fort', 'für',
        'gegen', 'heit', 'hint', 'ion', 'keine', 'konnt', 'lich', 'lung',
        'meine', 'mit', 'nichts', 'noch', 'nur', 'ohne', 'rung', 'schaft',
        'schon', 'seine', 'selbst', 'sich', 'sind', 'solch', 'soll', 'sonder',
        'über', 'unter', 'vielleicht', 'voll', 'vom', 'von', 'völl', 'wenn',
        'will', 'wird', 'woll', 'worden', 'wurd', 'zer', 'zum', 'zurück',
        'zurück', 'zusammen', 'zwischen'
    ]
    check_list = grouped_consonants + kuerzel

    for element in check_list:
        if element in test:  # check:
            tag_line += str(" {}".format(element))

    # specialty rules, complementing the simpler ones above:
    #
    # "ge" at the beginning of the word, but not as "gegen"
    #
    # Pro:  Identifies, e.g. "Gebiet", excludes entries like "Gegend",
    #       or "gegenüber", and conjunctions to "ei" ("Geige").
    #
    # Con:  Detection of plausible matches like "Angebot", "angeboren"
    #       is missed.  Neither pure string comparison, or a syllable
    #       based approach so far prevent collisions with false-positives
    #       like "Türangel", or "Enge"; beside an open identification
    #       of "ng" != ["lung", "rung"].
    #
    if (test.startswith("ge")) and (test.startswith("gegen") is
                                    False) and (str(test[2]) is not str("i")):
        tag_line += str(" ge")

    # identification of "sch" as different from groups "schl", "schm",
    # "schn", "schr", and separate from kuerzel "schaft" and "deutsch"
    #
    if str("sch") in test:
        start = test.find("sch")
        try:
            if (str(test)[start + 3] in ["l", "m", "n", "r"]) or \
            (str(test)[start : start + 6] == str("schaft")) or \
            (str(test)[start - 4 : start + 3] == str("deutsch")):
                pass
            else:
                tag_line += str(" sch")
        except:
            pass

    # identification and discern of "st" from "str"
    #
    if str("st") in test:
        syllables = h_de.syllables(test)
        match = False
        for syllable in syllables:
            if (syllable.startswith("st")) and \
                (syllable.startswith("str") is False):
                match = True
                break
        if match:
            tag_line += str(" st")

    # identification and discern of "tr" from "str"
    #
    if str("tr") in test:
        start = test.find("tr")
        try:
            if str(test)[start - 1] is not str("s"):
                tag_line += str(" tr")
        except:
            pass

    # identification of "un" besider "unter" as start of a word
    #
    if (test.startswith("un")) and (test.startswith("unter") is False):
        tag_line += str(" un")


def main():
    """ Joining the functions. """
    check_python()
    only_check_presence_workshop()
    remove_from_list()
    remove_from_folder()


main()
