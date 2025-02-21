import datetime
import os

import fastexcel
import polars as pl


class Main:
    def __init__(self, update_only=True, month="01", year=datetime.datetime.now().year) -> None:
        self.start_time = datetime.datetime.now()
        Reader_and_Writer(month, year, update_only)
        self.end_time = datetime.datetime.now()
        self.show_elapsed_time()

    def show_elapsed_time(self):
        elapsed_time = self.end_time - self.start_time
        minutes = round(elapsed_time.seconds / 60, 0)
        seconds = elapsed_time.seconds % 60 + elapsed_time.microseconds / 1e6
        print(f"Elapsed time: {minutes} minutes and {seconds} seconds")


class Reader_and_Writer:
    COLUMNS_FUNDS_RENAME = {
        "tx_adm": "pnl_adm_fee",
        "p&l_trades": "pnl_trades",
        "r_bench": "1d_change_bench",
        "r_nominal": "portfolio_return",
        "p&l_fxinc_open": "pnl_cash",
        "return_ytd": "portfolio_return_ytd",
        "1d_change": "portfolio_return",
        "nickname": "fund_nickname",
    }

    def __init__(self,  month, year, update_only=True,) -> None:
        self.obtain_folders(year)
        self.read_excels(update_only, month, year)
        pass

    def obtain_folders(self, year):
        BACKUP_FOLDER = (
            os.environ["onedrive"] + rf"\Trading\files_daily\backup\{year}"
        )
        self.FOLDER_EXCEL = BACKUP_FOLDER + r"\excel"
        self.FOLDER_BASE = BACKUP_FOLDER + r"\base"
        self.FOLDER_FUNDS = BACKUP_FOLDER + r"\data_funds"

    def read_excels(self, update_only, month, year):
        entries_excel = os.scandir(self.FOLDER_EXCEL)
        self.obtain_parquet_names()
        if update_only:
            for entry in entries_excel:
                ends_with_xlsm = entry.name.find(".xlsm") > -1
                ignore = not (
                    entry.name.find("~") > -1 or entry.name.find("Gerencial") > -1
                )
                date_string = entry.name[:8]
                parquet_not_exists = not self.check_parquet_exists(date_string)
                if ends_with_xlsm and ignore and parquet_not_exists:
                    print(entry.name)
                    path = self.FOLDER_EXCEL + "\\" + entry.name

                    self.write_parquet_funds(path, date_string)
                    self.write_parquet_base(path, date_string)
        else:
            for entry in entries_excel:
                ends_with_xlsm = entry.name.find(".xlsm") > -1
                starts_with = entry.name.find(f"{year}{month}") > -1
                starts_with = True
                ignore = not (
                    entry.name.find("~") > -1 or entry.name.find("Gerencial") > -1
                )
                if ends_with_xlsm and starts_with and ignore:
                    print(entry.name)
                    path = self.FOLDER_EXCEL + "\\" + entry.name
                    date_string = entry.name[:8]

                    self.write_parquet_funds(path, date_string)
                    self.write_parquet_base(path, date_string)

    def obtain_parquet_names(self):
        entries = os.scandir(self.FOLDER_BASE)
        self.parquet_list_names = []
        for entry in entries:
            self.parquet_list_names.append(entry.name)

        return self.parquet_list_names

    def check_parquet_exists(self, date_string):
        name_parquet = "base_" + date_string + ".parquet"
        if name_parquet in self.parquet_list_names:
            return True
        else:
            return False

    def write_parquet_funds(self, path, date):
        df_funds = Funds(path).funds
        columns_rename = obtain_columns_to_rename(df_funds, self.COLUMNS_FUNDS_RENAME)

        (
            df_funds.filter(pl.any_horizontal(pl.col("*").is_not_null()))
            .rename(columns_rename)
            .write_parquet(self.FOLDER_FUNDS + "\\funds_" + date + ".parquet")
        )
        print("parquet fundos criado")

    def write_parquet_base(self, path, date):
        Base(path).base.write_parquet(self.FOLDER_BASE + "\\base_" + date + ".parquet")
        print("parquet base criado")


def obtain_columns_to_rename(df, columns_to_check):
    columns_rename = {}
    for column in columns_to_check.keys():
        if column in df.columns:
            columns_rename[column] = columns_to_check[column]

    return columns_rename


class Funds:
    def __init__(self, path) -> None:
        self.obtain_funds_info(path)
        self.treat_funds()

    def obtain_funds_info(self, path):
        try:
            self.funds = pl.read_excel(
                path,
                sheet_name="Data_Funds",
                infer_schema_length=200,
                schema_overrides={
                    "__UNNAMED__0": pl.Utf8,
                    "portfolio_return": pl.Utf8,
                    "r_alfa": pl.Utf8,
                    "r_trades": pl.Utf8,
                    "r_nominal": pl.Utf8,
                    "exposure": pl.Utf8,
                },
                read_options={"header_row": 2},
            )
        except (pl.exceptions.ColumnNotFoundError, fastexcel.CalamineCellError):
            try:
                self.funds = pl.read_excel(
                    path,
                    sheet_name="Data_Funds",
                    infer_schema_length=200,
                    schema_overrides={
                        "__UNNAMED__0": pl.Utf8,
                        "portfolio_return": pl.Utf8,
                        "r_alfa": pl.Utf8,
                        "r_trades": pl.Utf8,
                        "r_nominal": pl.Utf8,
                        "exposure": pl.Utf8,
                    },
                    read_options={"header_row": 1},
                )
            except (
                pl.exceptions.ColumnNotFoundError,
                fastexcel.CalamineCellError,
                fastexcel.UnsupportedColumnTypeCombinationError,
            ):
                self.funds = pl.read_excel(
                    path,
                    sheet_name="Data_Funds",
                    engine="xlsx2csv",
                    infer_schema_length=200,
                    read_options={"skip_rows": 2},
                )

    def treat_funds(self):
        columns = ["portfolio_return", "r_alfa", "r_trades", "exposure", "r_nominal"]
        columns_float = []
        for column in columns:
            if column in self.funds.columns:
                columns_float.append(column)

        self.funds = self.funds.with_columns(
            pl.col(columns_float).str.replace("#DIV/0!", "0").cast(pl.Float64),
        )


class Base:
    COLUMNS_BASE_RENAME = {
        "sec_exp_curr": "price_current_brl",
        "sec_popen": "price_close_yesterday_brl",
        "sec_div": "dividend",
        "pos_i": "position_initial",
        "att_vs_bench": "selection",
        "var_vs_bench": "selection",
        "att": "return",
        "attribuition": "return",
        "ticker_return": "return",
        "mercadoria": "type_risco",
        "parent_strategy": "fund_strategy",
        "und/over": "under_over_initial",
        "und_over_initial": "under_over_initial",
    }

    def __init__(self, path) -> None:
        self.obtain_base(path)
        self.treat_base()
        self.create_performance_parameters()

    def obtain_base(self, path):
        try:
            self.base = pl.read_excel(
                path,
                sheet_name="Base",
                infer_schema_length=2000,
                schema_overrides={
                    "size": pl.Float64,
                    "margem_request": pl.Float64,
                    "pnl_trade": pl.Float64,
                    "alpha_trade": pl.Float64,
                    "trade_financial": pl.Float64,
                    "dividend": pl.Float64,
                },
            )
        except pl.exceptions.ColumnNotFoundError:
            self.base = pl.read_excel(
                path,
                sheet_name="Base",
                engine="xlsx2csv",
                infer_schema_length=2000,
            )

    def treat_base(self):
        columns_rename = obtain_columns_to_rename(self.base, self.COLUMNS_BASE_RENAME)
        self.base = (
            self.base.filter(pl.any_horizontal(pl.col("*").is_not_null()))
            .rename(columns_rename)
            .filter(~pl.col("ticker_old").str.contains("Quantidade |Redutor"))
            .with_columns(
                pl.when(pl.col("ticker") == "#N/A")
                .then(pl.col("ticker_old").str.to_lowercase())
                .otherwise(pl.col("ticker").str.to_lowercase())
                .alias("ticker"),
                pl.col(["dividend"]).cast(pl.Float64),
            )
        )

    def create_performance_parameters(self):
        """Selection, alpha and return are the performance parameters that we want to calculate.
        Selection does not consider the return of the trade (PM's decision)"""
        self.base = self.base.with_columns(
            (pl.col("pnl_trade") / pl.col("aum_inicial")).alias("return_trade"),
            (pl.col("position_initial") * pl.col("1d_change")).alias("return_position"),
            (pl.col("under_over_initial") * pl.col("1d_change")).alias(
                "alpha_position"
            ),
            (pl.col("pnl_trade") / pl.col("aum_inicial")).alias("alpha_trade"),
            pl.when(pl.col("type_risco") == "COTAS")
            .then(0)
            .otherwise((pl.col("1d_change") * (pl.col("position_initial"))))
            .alias("selection_position"),
        ).with_columns(
            (10000 * (pl.col("return_position") + pl.col("return_trade"))).alias(
                "return"
            ),
            (10000 * (pl.col("alpha_position") + pl.col("alpha_trade"))).alias("alpha"),
            (10000 * (pl.col("selection_position"))).alias("selection"),
        )

if __name__ == "__main__":
    m = Main()
    #m = Main(update_only=False, month="01", year="2024")


# add cdi ao bench TR
# add caixa aos fundos (talvez at'e uma linha de caixa para cada fundo)
# await
