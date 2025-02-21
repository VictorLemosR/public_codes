import os
import polars as pl
import datetime


class Position:
    PATH_FUNDS_INFO = (
        os.environ["onedrive"] + r"\Trading\files_static\dictionaries\funds_info.parquet"
    )

    def __init__(self):
        self.obtain_path()
        self.refresh_current_position()

    def obtain_path(self):
        today = datetime.datetime.today().strftime("%Y%m%d")
        year = datetime.datetime.today().strftime("%Y")
        path = (
            os.environ["onedrive"] + rf"\Trading\files_daily\{year}\{today}\gerencial"
        )
        self.BASE_PATH = path + r"\base.parquet"
        self.FUNDS_AUM_PATH = path + r"\data_funds.parquet"

    def refresh_current_position(self):
        self.obtain_parquets()
        self.obtain_ticker_prices()
        self.join_funds_info()
        self.aum_onshore_offshore()

    def obtain_parquets(self):
        try:
            position = pl.read_parquet(self.BASE_PATH)
        except FileNotFoundError:
            from Routines.create_v2_parquet import save_once

            save_once()
            position = pl.read_parquet(self.BASE_PATH)

        self.position = position.with_columns(
            pl.col(pl.Utf8).str.to_lowercase(),
        ).with_columns(
            (
                pl.col("quantity")
                * pl.col("price_current_brl")
                * pl.col("size")
                / pl.col("aum_current")
            ).alias("position_initial"),
            pl.col("fund_nickname").str.replace(" cl", ""),
        )

        self.funds_info = pl.read_parquet(self.PATH_FUNDS_INFO).with_columns(
            pl.col(pl.Utf8).str.to_lowercase()
        )

        self.funds_aum = (
            pl.read_parquet(self.FUNDS_AUM_PATH)
            .filter(pl.col("id_sgi").is_not_null())
            .with_columns(pl.col(pl.Utf8).str.to_lowercase())
        )

    def obtain_ticker_prices(self):
        """Eventualmente, mudar para pegar de um parquet ou pensar numa forma caso
        eu n~ao tenha o preco de algum ativo"""
        self.security_info = self.position.select(
            pl.col(["ticker", "price_current_brl", "type", "size"])
        ).unique()

        self.position = self.position

    def join_funds_info(self):
        self.funds_aum = self.funds_aum.join(self.funds_info, on="id_sgi", how="left", coalesce=False)

    def aum_onshore_offshore(self):
        self.funds_aum = self.funds_aum.with_columns(
            pl.col("aum_current")
            .sum()
            .over(pl.col("aum_onshore_strategy"))
            .alias("aum_onshore_strategy_financial"),
            pl.col("aum_current")
            .sum()
            .over(pl.col("aum_offshore_strategy"))
            .alias("aum_offshore_strategy_financial"),
        ).with_columns(
            pl.when(pl.col("aum_onshore_strategy").is_null())
            .then(pl.lit(0))
            .otherwise(pl.col("aum_onshore_strategy_financial"))
            .alias("aum_onshore_strategy_financial"),
            pl.when(pl.col("aum_offshore_strategy").is_null())
            .then(pl.lit(0))
            .otherwise(pl.col("aum_offshore_strategy_financial"))
            .alias("aum_offshore_strategy_financial"),
        )


def obtain_position():
    position_class = Position()
    return position_class


if __name__ == "__main__":
    position = obtain_position()
    print(
        f'position: {position.position.select(pl.col(["ticker","fund_nickname","position_initial"])).filter(pl.col("ticker") == "petz3")}'
    )
    print(f"funds_aum: {position.funds_aum}")
    print(f"security_info: {position.security_info}")
    print(f"funds_info: {position.funds_info}")
