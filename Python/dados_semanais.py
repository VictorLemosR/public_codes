import datetime

import os

import polars as pl
from xbbg import blp

pl.Config.set_tbl_rows(30)

EXPOSURE_TXT = """Variação de exposição do TREND (exposição hoje na primeira linha e exposição no final da semana anterior na segunda linha) - está com tabulação:\n"""
TRADES_TXT = """Movimentaçãoes do Trend (números positivos são compras/adições e números negativos são vendas) - está com tabulação:\n"""
INDEX_TXT = """Maiores contribuições de pontos para o indice ibovespa (não inclua essa informação no texto) - está com tabulação:\n"""
INFOS_TXT = """Performance (ticker | last price | variação semanal (5d) | variação mensal (1m)) dos ativos\n(oil - petróleo, ibov - ibovespa, iron - minério de ferro, small - indice small caps, dolar_futuro - FX rate dolar) - está com tabulação:\n"""


def check_file_exists(path):
    if os.path.exists(path):
        return True
    return False


def trades_latin_trend(today):
    COLUMNS = ["fund_nickname", "ticker", "order_percentual"]
    year = today.year
    trades = pl.DataFrame(schema=COLUMNS)
    for i in range(0, 5):
        new_date = (today - datetime.timedelta(days=i)).strftime("%Y%m%d")
        allocations_path = (
            os.environ["onedrive"]
            + rf"\Trading\files_daily\{year}\{new_date}\gerencial\allocations.parquet"
        )
        if check_file_exists(allocations_path):
            allocations = (
                pl.scan_parquet(allocations_path)
                .select(COLUMNS)
                .filter(
                    pl.col("fund_nickname").str.contains("trend$"),
                    pl.col("order_percentual").abs() > 0.0025,
                )
                .group_by(["fund_nickname", "ticker"])
                .agg(pl.col("order_percentual").sum())
            ).collect()
            trades = pl.concat([trades, allocations], how="vertical_relaxed")
    trades = (
        trades.group_by(["fund_nickname", "ticker"])
        .agg(pl.col("order_percentual").sum())
        .with_columns((pl.col("order_percentual") * 100).round(2))
        .sort("fund_nickname", descending=True)
        .pivot(
            on="fund_nickname",
            index="ticker",
            values="order_percentual",
        )
        .sort("ticker")
    )
    print(f"Trades trend\n{trades}")
    return trades


def top_bottom_ibov(today):
    COLUMNS = ["fund_nickname", "ticker", "pnl_pos", "quantity"]
    year = today.year
    ibov_points = pl.DataFrame(schema=COLUMNS)
    for i in range(0, 5):
        new_date = (today - datetime.timedelta(days=i)).strftime("%Y%m%d")
        print(f"data rodando: {new_date}")
        base_path = (
            os.environ["onedrive"]
            + rf"\Trading\files_daily\{year}\{new_date}\gerencial\base.parquet"
        )
        if check_file_exists(base_path):
            ibov_base = (
                pl.scan_parquet(base_path)
                .select(COLUMNS)
                .filter(pl.col("fund_nickname").str.contains("ibov_index"))
            ).collect()

            redutor_quantity = ibov_base.filter(
                pl.col("ticker").str.contains("redutor")
            ).select(pl.col("quantity"))[0, 0]
            print(f"redutor_quantity: {redutor_quantity}")
            ibov_base = ibov_base.with_columns(
                pl.lit(redutor_quantity).alias("quantity")
            )
            ibov_points = pl.concat([ibov_points, ibov_base], how="vertical_relaxed")
    ibov_points = (
        ibov_points.with_columns(
            (pl.col("pnl_pos") / pl.col("quantity")).alias("points")
        )
        .group_by("ticker")
        .agg(pl.col("points").sum())
        .sort("points", descending=True)
    )
    ibov_points = pl.concat([ibov_points[0:5], ibov_points[-5:]])

    print(f"contribuições ibov\n{ibov_points}")
    return ibov_points


def info_bbg():
    changes = {
        "ticker": ["ibov", "small", "oil", "iron", "dolar_futuro"],
        "ticker_bbg": [
            "ibov index",
            "smllbv index",
            "cl1 comdty",
            "sco1 comdty",
            "uca curncy",
        ],
    }
    info = blp.bdp(
        tickers=changes["ticker_bbg"], flds=["PX_LAST", "CHG_PCT_5D", "CHG_PCT_1M"]
    )
    info = (
        pl.from_pandas(info.reset_index())
        .with_columns(pl.col("index").replace(changes["ticker_bbg"], changes["ticker"]))
        .rename({"index": "ticker"})
    )

    print(f"info: {info}")
    return info


def exposure_latan_trend(today):
    year = today.year
    base_path = (
        os.environ["onedrive"]
        + rf"\Trading\files_daily\{year}\{today.strftime('%Y%m%d')}\gerencial\base.parquet"
    )
    exposure = treat_exposure(base_path).with_columns(
        pl.lit("exposure_today").alias("date")
    )

    for i in range(7, 0, -1):
        new_date = (today - datetime.timedelta(days=i)).strftime("%Y%m%d")
        base_path = (
            os.environ["onedrive"]
            + rf"\Trading\files_daily\{year}\{new_date}\gerencial\base.parquet"
        )
        if check_file_exists(base_path):
            exposure = pl.concat(
                [
                    exposure,
                    treat_exposure(base_path).with_columns(
                        pl.lit("exposure_5d").alias("date")
                    ),
                ]
            )
            break

    exposure = exposure.sort("fund_nickname", descending=True).pivot(
        on="fund_nickname",
        index="date",
        values="position_current",
    )

    print(f"exposição latin/trend\n{exposure}")
    return exposure


def treat_exposure(path):
    COLUMNS = ["fund_nickname", "position_current"]
    base = (
        pl.scan_parquet(path)
        .select(COLUMNS)
        .filter(pl.col("fund_nickname").str.contains("trend"))
        .group_by("fund_nickname")
        .agg(pl.col("position_current").sum())
    ).collect()

    return base


def create_output_file(
    exposure_latan_trend, trades_latin_trend, top_bottom_ibov, info_bbg
):
    output_path = os.environ["onedrive"] + r"\Portfolio Overview\dados_semanais.txt"
    exposure_latan_trend = exposure_latan_trend.write_csv(separator="\t")
    trades_latin_trend = trades_latin_trend.write_csv(separator="\t")
    top_bottom_ibov = top_bottom_ibov.write_csv(separator="\t")
    info_bbg = info_bbg.write_csv(separator="\t")

    combined_text = f"""{EXPOSURE_TXT}\n{exposure_latan_trend}
                     {TRADES_TXT}\n{trades_latin_trend}
                     {INDEX_TXT}\n{top_bottom_ibov}
                     {INFOS_TXT}\n{info_bbg}"""

    with open(output_path, "w") as file:
        file.write(combined_text)


if __name__ == "__main__":
    today = datetime.datetime.today()
    exposure = exposure_latan_trend(today)
    trades = trades_latin_trend(today)
    index = top_bottom_ibov(today)
    infos = info_bbg()
    create_output_file(exposure, trades, index, infos)
