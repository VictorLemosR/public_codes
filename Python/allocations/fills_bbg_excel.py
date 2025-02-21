import polars as pl
import time
import os
import datetime
from Modules.warning_message import show_warning


class Main:
    def __init__(self):
        path_class = Bbg_fill()
        if path_class.exist_file:
            broker_class = Broker()
            self.fills = Dataframe_operations(
                path_class.df, broker_class.broker_info
            ).fills
        else:
            self.fills = pl.DataFrame()


class Bbg_fill:
    COLUMNS_INPUT = {
        "FillQty": "filled",
        "AvgPx": "average_price",
        "Security+Exch": "ticker",
        "Full Exch Symbol": "future_ticker",
        "Side": "side",
        "Brkr Code": "broker_bbg",
        "Port Name": "portfolio",
        "Last Fill Datetime": "last_fill",
    }
    FOLDER = (
            os.environ["onedrive"] + r"\Trading\files_temporary\Bloomberg"
        )

    def __init__(self) -> None:
        exist_grid_file = self.obtain_file()
        if exist_grid_file:
            self.validate_file()

    def obtain_file(self):
        entries = os.scandir(self.FOLDER)
        newest_entry = -1
        for entry in entries:
            text_start_grid = entry.name.find("grid") == 0
            if text_start_grid:
                if entry.name.find("tmp") == -1:
                    entry_time = entry.stat().st_mtime
                    if entry_time > newest_entry:
                        newest_entry = entry_time
                        self.file = entry

        if newest_entry != -1:
            return True

        self.exist_file = False
        return False

    def validate_file(self):
        file_date = datetime.date.fromtimestamp(self.file.stat().st_mtime)
        today = datetime.date.today()
        self.exist_file = today == file_date
        if self.exist_file:
            continue_trying = True
            read_excel_tries = 0
            while continue_trying:
                try:
                    self.df = pl.read_excel(self.file.path, engine="openpyxl")
                    continue_trying = False
                except pl.exceptions.NoDataError:
                    print("Excel do emsx está vazio")
                    self.exist_file = False
                    return
                except PermissionError:
                    time.sleep(3)
                    print("Excel do emsx está aberto")
                    if read_excel_tries > 5:
                        read_excel_tries = 0
                        show_warning(
                            start_text="Fechar o excel do emsx",
                        title="Excel emsx",
                        stop=False,
                    )
                    read_excel_tries += 1
            if self.df.is_empty():
                self.exist_file = False
                return

            try:
                self.df = (
                        self.df
                    .select(pl.col(self.COLUMNS_INPUT.keys()))
                    .rename(self.COLUMNS_INPUT)
                    .with_columns(pl.col(pl.Utf8).str.to_lowercase())
                )
            except pl.exceptions.ColumnNotFoundError:
                print("Colunas do excel do emsx não estão corretas, baixar um novo arquivo")
                self.exist_file = False
                return
            

class Broker:
    BROKERS_PATH = (
        os.environ["onedrive"] + r"\Trading\files_static\dictionaries\broker_codes.parquet"
    )

    def __init__(self) -> None:
        self.obtain_broker_info()
        self.treat_broker()

    def obtain_broker_info(self):
        self.broker_info = pl.read_parquet(self.BROKERS_PATH)

    def treat_broker(self):
        self.broker_info = (
            self.broker_info.melt(
                id_vars="broker",
                value_vars=[
                    "bbg_code_desk",
                    "bbg_code_quest_dma",
                    "bbg_code_quest_offshore",
                    "bbg_code_azimut_dma",
                    "bbg_code_azimut_offshore",
                ],
                value_name="bbg_code",
            )
            .drop_nulls(subset="bbg_code")
            .unique(subset="bbg_code")
            .select(pl.col(["broker", "bbg_code"]))
        )


class Dataframe_operations:
    COLUMNS_TRADES = [
        "ticker",
        "side",
        "filled",
        "average_price",
        "broker",
        "portfolio",
        "last_fill",
    ]

    def __init__(self, fills, brokers) -> None:
        self.fills = fills
        self.join_brokers(brokers)
        self.treat_trades()

    def join_brokers(self, brokers):
        self.fills = self.fills.join(
            brokers, left_on="broker_bbg", right_on="bbg_code", how="left"
        )

    def treat_trades(self):
        self.fills = (
            self.fills.with_columns(
                pl.when(pl.col("ticker").str.contains(" bmf"))
                .then(pl.col("future_ticker"))
                .otherwise(pl.col("ticker"))
                .alias("ticker"),
                pl.when(pl.col("side").str.slice(0,1) == "b")
                .then(pl.lit("buy"))
                .otherwise(pl.lit("sell"))
                .alias("side"),
            )
            .with_columns(
                pl.col("ticker").str.replace(" bz| bmf", ""),
                pl.col("last_fill").str.strptime(pl.Datetime, "%H:%M"),
            )
            .filter(pl.col("filled") > 0)
            .group_by(["ticker", "side", "broker", "portfolio"])
            .agg(
                pl.col("filled").sum(),
                (pl.col("average_price") * pl.col("filled")).sum()
                / (pl.col("filled").sum()).alias("average_price"),
                pl.col("last_fill").max(),
            )
            .select(
                pl.col(self.COLUMNS_TRADES),
                pl.when(pl.col("side") == "buy")
                .then((pl.col("filled") * pl.col("average_price")))
                .otherwise(-(pl.col("filled") * pl.col("average_price")))
                .alias("financeiro"),
                pl.when(pl.col("portfolio").is_in(["multi", "lxemmkla", "lxbrtr"]))
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias("azimut"),
            )
            .sort(by=["side", "ticker", "broker"])
        )


if __name__ == "__main__":
    m = Main()
    print(m.fills)


def obtain_fills_bbg():
    """Para ser chamado a cada x segundos, basta colocar o _Fills() no while"""
    m = Main()
    fills = m.fills
    return fills
