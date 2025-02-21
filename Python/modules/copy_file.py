def copy_py_file():
    NAME_OF_THIS_FILE = r"\obtain_v2_info.py"
    PATH_THIS_FILE = r"C:\Victor\codes\az_quest\trading"
    PATH_TO_PASTE = r"C:\Users\victor.reial\OneDrive - QUEST INVESTIMENTOS LTDA\Trading\codes_trading"

    import shutil

    shutil.copy2(PATH_THIS_FILE + NAME_OF_THIS_FILE, PATH_TO_PASTE + NAME_OF_THIS_FILE)


# copy_py_file()
