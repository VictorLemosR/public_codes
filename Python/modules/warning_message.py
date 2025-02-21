import ctypes
import polars as pl


def show_warning(start_text: str = None,title: str = None, dataframe: pl.DataFrame = None, columns: list[str] = None, stop: bool = False):
    if dataframe is None:
        ctypes.windll.user32.MessageBoxW(0, start_text, title, 1)
        if stop:
            error = title + "\n\n" + start_text
            raise Exception(error)
        return

    if columns is None:
        columns = dataframe.columns

    if start_text is None:
        start_text = ""
    else:
        start_text = start_text + "\n\n"
    dataframe = dataframe.with_columns(pl.col(columns).cast(pl.Utf8)).fill_null("")
    start_text = start_text + dataframe.select(
        ("(" + pl.concat_str(pl.col(columns), separator=", ") + ")").str.concat("\n")
    )[0, 0]

    ctypes.windll.user32.MessageBoxW(0, start_text, title, 1)

    if stop:
        if title is None:
            title = ""
        error = title + "\n\n" + start_text
        raise Exception(error)
