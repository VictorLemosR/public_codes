import polars as pl
import xlwings as xw
import pandas as pd
import pywintypes
import time


class _Workbook:
    def __init__(self, wb_path):
        self.obtain_wb(wb_path)

    def obtain_wb(self, wb_path):
        """Function to obtain the workbook
        It tries to obtain more than once because of slow workbooks not in manual"""
        try:
            self.wb = xw.Book.caller()
        except:
            i = 0
            self.wb = ""
            while self.wb == "":
                try:
                    self.wb = xw.Book(wb_path)
                except:
                    print(f"attempt {i} to get workbook")
                    i += 1
                if i == 3:
                    raise Personal_exception("Error to get wb")

    def obtain_range(self, sheet_name, sheet_range):
        """Obtain a range inside a specific sheet.
        Recommended to obtain just one range per sheet and filter it later via polars"""
        i = 0
        continue_trying = True
        while continue_trying and i < 5:
            try:
                self.range_pandas = (
                    self.wb.sheets[sheet_name]
                    .range(sheet_range)
                    .options(pd.DataFrame, index=False)
                    .value
                )
                continue_trying = False
            except AttributeError:
                print(f"attempt {i} to get range")
                i += 1
                time.sleep(1)
            except pywintypes.com_error:
                print(f"attempt {i} to get range")
                i += 1
                time.sleep(1)


        return self.treat_dataframe()

    def treat_dataframe(self):
        object_columns = self.range_pandas.select_dtypes(include="object").columns
        self.range_pandas.loc[:, object_columns] = self.range_pandas.loc[
            :, object_columns
        ].astype(str)

        range_polars = (
            pl.from_pandas(self.range_pandas)
            .with_columns(pl.col(pl.Utf8).replace("None", None))
            .filter(pl.any_horizontal(pl.col("*").is_not_null()))
        )
        range_polars.columns = [column.lower() for column in range_polars.columns]

        return range_polars

    def display(
        self,
        df: pl.DataFrame,
        sheet_name: str,
        cell_to_print: str,
        range_to_clear: str = None,
    ):
        sheet = self.wb.sheets[sheet_name]
        try:
            if sheet.api.AutoFilterMode:
                   sheet.api.AutoFilter.ShowAllData()
                #sheet.api.AutoFilterMode = False
        except:
                print("AutoFilterMode error")
        counter = 0
        while counter < 4:
            try:
                if range_to_clear:
                    sheet.range(range_to_clear).value = ""
                sheet.range(cell_to_print).options(
                    pd.DataFrame, index=False
                ).value = df.to_pandas()
                break
            except:
                counter += 1

    def send_msgbox(self):
        pass
    
    def save_img(self, path: str, sheet_name: str, range_str: str):
        sheet_img = self.wb.sheets[sheet_name]
        sheet_img.range(range_str).api.CopyPicture(Appearance=2)
        sheet_img.api.Paste()
        pic = sheet_img.pictures[0]
        pic.api.Copy()

        from PIL import ImageGrab
        img = ImageGrab.grabclipboard()
        img.save(path)
        pic.delete()
        from ctypes import windll
        if windll.user32.OpenClipboard(None):
            windll.user32.EmptyClipboard()
            windll.user32.CloseClipboard()


def obtain_wb(wb_path: str):
    """Obtain wb, sheet and ranges

    Parameters
    ----------
    wb_path : str

    Returns
    -------
    workbook: class or list of classes if more than one workbook passed
    """

    wb = _Workbook(wb_path)
    return wb
