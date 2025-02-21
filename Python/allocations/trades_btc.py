########atentar para trades ate as 11
import os
import datetime
import polars as pl
import requests
import zipfile
from io import BytesIO


class Main:
    def __init__(self):
        dates = Dates()
        unformatted_dataframe = Download_trades(dates).df
        self.operations = Df_operations(unformatted_dataframe)


class Dates:
    def __init__(self) -> None:
        self.today = datetime.datetime.now()
        self.get_last_business_day()

    def get_last_business_day(self):
        pass


class Download_trades:
    URL_B3 = "https://arquivos.b3.com.br/apinegocios/tickercsvbtb"

    def __init__(self, dates) -> None:
        self.today_string = dates.today.strftime("%Y-%m-%d")
        # self.today_string = '2025-04-02'

        self.obtain_ticker()
        self.download_from_b3()
        self.unzip()

    def obtain_ticker(self):
        print("Digite o ticker que procura:")
        self.ticker = input().lower()

    def download_from_b3(self):
        url = self.URL_B3 + "//" + self.ticker + "//" + self.today_string
        self.r = requests.get(url)
        if self.r.status_code != 200:
            raise (Exception("Erro ao obter arquivo"))

    def unzip(self):
        z = zipfile.ZipFile(BytesIO(self.r.content))
        self.df = pl.read_csv(z.read(z.namelist()[0]), separator=";")


class Df_operations:
    PATH_BROKERS = (
        os.environ["onedrive"]
        + r"\Trading\files_static\dictionaries\broker_codes.parquet"
    )
    COLUMNS_RENAME = {
        "TaxaDeJurosDoTermoDoNegocio": "rate",
        "QuantidadeNegociada": "qty",
        "HoraEntrada": "hour",
        "CodigoParticipanteDoador": "lender",
        "CodigoParticipanteTomador": "borrower",
    }

    def __init__(self, dataframe) -> None:
        self.df = dataframe
        self.brokers = pl.read_parquet(self.PATH_BROKERS)
        self.rename_columns()
        self.format_columns()
        self.build_dataframes()
        self.print_dataframes()

    def rename_columns(self):
        self.df = self.df.rename(self.COLUMNS_RENAME)
        self.df = self.df.select(pl.col(self.COLUMNS_RENAME.values()))

    def format_columns(self):
        self.df = (
            self.df.with_columns(
                pl.col("rate").str.replace(",", ".").cast(pl.Float64),
                pl.col("lender").cast(pl.Int32),
                pl.col("borrower").cast(pl.Int32),
                pl.when(pl.col("hour") < 1.09e8)
                .then(pl.lit("janela"))
                .otherwise(pl.lit("dia"))
                .alias("hour"),
            )
            .group_by(["rate", "lender", "borrower"])
            .agg(pl.col("qty").sum())
        )

    def build_dataframes(self):
        functions = (
            pl.col("qty").sum().alias("traded"),
            ((pl.col("rate") * pl.col("qty")).sum() / pl.col("qty").sum()).alias(
                "average"
            ),
            pl.col("rate").min().alias("min"),
            pl.col("rate").max().alias("max"),
            (
                (
                    (
                        pl.col("qty")
                        * (
                            (
                                pl.col("rate")
                                - (
                                    (pl.col("rate") * pl.col("qty")).sum()
                                    / pl.col("qty").sum()
                                )
                            )
                            ** 2
                        )
                    ).sum()
                    / pl.col("qty").sum()
                )
                ** 0.5
            ).alias("std"),
        )
        self.top_lender = (
            self.df.group_by(["lender"])
            .agg(functions)
            .join(self.brokers, left_on="lender", right_on="code", coalesce=False)
            .sort(by="traded", descending=True)
        )
        self.top_borrower = (
            self.df.group_by(["borrower"])
            .agg(functions)
            .join(self.brokers, left_on="borrower", right_on="code", coalesce=False)
            .sort(by="traded", descending=True)
        )
        self.df2 = (
            self.df.group_by(["rate"])
            .agg(
                pl.col("qty").sum().alias("traded"),
            )
            .sort(by="traded", descending=True)
        )
        self.df3 = self.df.select(functions).sort(by="traded", descending=True)

    def print_dataframes(self):
        print(self.top_lender[:5])
        print(self.top_borrower[:5])
        print(self.df2[:5])
        print(self.df3)


m = Main()
m.operations.df.filter(pl.col("lender") == pl.col("borrower")).sort(by="rate")
