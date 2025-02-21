import datetime
import os
import time

import polars as pl

from Modules.portfolio_position import obtain_position
from Modules.warning_message import show_warning
from Modules.workbook_functions import obtain_wb
from Trading.Bbg.fills_bbg_excel import obtain_fills_bbg
from Trading.Solutions.fills_solutions import obtain_fills_solutions

pl.Config.set_tbl_cols(30)
pl.Config.set_tbl_rows(30)


class Main:
    def __init__(self) -> None:
        Loop()


class Loop:
    def __init__(self) -> None:
        self.execute_before_loop()
        self.handle_loop()

    def execute_before_loop(self):
        self.now = datetime.datetime.now()
        self.wb_class = Workbook()
        self.weights_class = Weights()

    def handle_loop(self):
        print("Enter the time to wait between checks (in seconds):")
        self.wait_time = input()
        if self.wait_time == "":
            loop_time = 5
            self.loop_handler(loop_time)
        else:
            try:
                loop_time = int(self.wait_time)
                self.loop_handler(loop_time)
            except ValueError:
                self.loop_functions()

    def loop_handler(self, loop_time):
        while True:
            self.loop_functions()
            print(f"Last check: {self.now.strftime('%H:%M:%S')}")
            self.now = datetime.datetime.now()
            time.sleep(loop_time)

    def loop_functions(self):
        fills = Fills().fills

        if not fills.is_empty():
            weights = self.wb_class.obtain_weights()
            self.weights_class.update_weights(weights)
            allocations = Allocations(
                fills,
                self.weights_class.weights,
                self.wb_class,
                self.weights_class.position_class.security_info,
            ).allocations
            if allocations.is_empty():
                return

            allocations = Excel_output_info(allocations).allocations
            allocations = allocations.with_columns(
                pl.lit(self.now.strftime("%H:%M")).alias("allocation_time")
            )

            Outputs(allocations, self.wb_class, fills)


class Fills:
    COLUMNS_FILLS = [
        "side",
        "ticker",
        "broker",
        "filled",
        "average_price",
        "last_fill",
        "platform",
        "azimut",
    ]

    def __init__(self) -> None:
        self.obtain_fills()

    def obtain_fills(self):
        fills_solutions = obtain_fills_solutions()
        fills_bbg = obtain_fills_bbg()
        self.concat_fills(fills_solutions, fills_bbg)

    def concat_fills(self, fills_solutions, fills_bbg):
        fills_possibities = 0
        if not fills_solutions.is_empty():
            fills_solutions = fills_solutions.with_columns(
                pl.lit("solutions").alias("platform")
            ).select(pl.col(self.COLUMNS_FILLS))
            fills_possibities += 1
        if not fills_bbg.is_empty():
            fills_bbg = fills_bbg.with_columns(pl.lit("bbg").alias("platform")).select(
                pl.col(self.COLUMNS_FILLS)
            )
            fills_possibities += 2

        no_fills = fills_possibities == 0
        only_solutions = fills_possibities == 1
        only_bbg = fills_possibities == 2
        both_fills = fills_possibities == 3
        if no_fills:
            self.fills = pl.DataFrame()
        if only_solutions:
            self.fills = self.treat_fills(fills_solutions)
        if only_bbg:
            self.fills = self.treat_fills(fills_bbg)
        if both_fills:
            self.fills = self.treat_fills(pl.concat([fills_solutions, fills_bbg]))

    def treat_fills(self, fills):
        fills = (
            fills.with_columns(
                pl.col("last_fill").dt.strftime("%H:%M:%S"),
                pl.concat_str(["ticker", "side"], separator="_").alias(
                    "match_ticker_side"
                ),
            )
            .group_by(["side", "ticker", "broker", "azimut"])
            .agg(
                pl.col("filled").sum(),
                (
                    (pl.col("filled") * pl.col("average_price")).sum()
                    / pl.col("filled").sum()
                ).alias("average_price"),
                pl.col("last_fill").last(),
                pl.col("platform").str.concat(delimiter=", ").alias("platform"),
            )
            .sort(
                by=[
                    "side",
                    "ticker",
                ]
            )
        )

        return fills


class Workbook:
    WB_PATH = (
        os.environ["onedrive"] + r"\Trading\trading.xlsm"
    )
    FILLS_SHEET = "Fills"
    FILLS_PRINT = "A1"
    FILLS_CLEAR_RANGE = "A1:T1000"

    WEIGHTS_SHEET = "Allocations"
    WEIGHTS_RANGE = "Z4:AP1000"

    ALLOCATIONS_SHEET = "Allocations"
    ALLOCATIONS_RANGE = "A4"
    ALLOCATIONS_CLEAR_RANGE = "A4:X10000"

    MISSING_FILLS_PRINT = "AS4"
    MISSING_FILLS_CLEAR_RANGE = "AS4:AX1000"

    def __init__(self) -> None:
        self.get_workbook()

    def get_workbook(self):
        self.wb = obtain_wb(self.WB_PATH)

    def obtain_weights(self):
        weights = self.wb.obtain_range(self.WEIGHTS_SHEET, self.WEIGHTS_RANGE)

        return weights

    def paste_fills(self, df):
        self.wb.display(df, self.FILLS_SHEET, self.FILLS_PRINT, self.FILLS_CLEAR_RANGE)

    def paste_allocations(self, df):
        self.wb.display(
            df,
            self.ALLOCATIONS_SHEET,
            self.ALLOCATIONS_RANGE,
            self.ALLOCATIONS_CLEAR_RANGE,
        )

    def paste_missing_fills(self, df):
        self.wb.display(
            df,
            self.ALLOCATIONS_SHEET,
            self.MISSING_FILLS_PRINT,
            self.MISSING_FILLS_CLEAR_RANGE,
        )


class Weights:
    FUNDS = [
        "tr",
        "top",
        "top prev",
        "small",
        "grumari",
        "itupava",
        "small prev",
        "itau small",
        "fia",
        "itau fia",
        "latam",
        "trend",
    ]

    WEIGHTS_COLUMNS = [
        "bool_quantity",
        "broker",
        "ticker",
        "order",
        "fund_nickname",
        "aum",
        "side",
        "position_initial",
        "azimut",
        "quantity",
        "fund_strategy",
    ]

    COLUMNS_POSITION = [
        "ticker",
        "position_initial",
        "fund_nickname",
        "quantity",
    ]

    COLUMNS_FUNDS_AUM = [
        "fund_nickname",
        "fund_strategy",
        "id_sgi",
        "aum_current",
    ]

    def __init__(self):
        self.position_class = obtain_position()

    def update_weights(self, weights):
        self._update_position()
        self._obtain_weights(weights)
        self._add_aum_weights()
        self._add_position_weights()

    def _update_position(self):
        self.position_class.refresh_current_position()

    def _obtain_weights(self, weights: pl.DataFrame):
        self.weights = (
            weights.with_columns(pl.col(pl.Utf8).str.to_lowercase())
            .unpivot(
                index=["bool_quantity", "broker_quest", "broker_azimut", "ticker"],
                variable_name="fund_nickname",
                value_name="order",
                on=self.FUNDS,
            )
            .with_columns(pl.col("order").cast(pl.Float64).alias("order"))
            .filter(pl.col("order").is_not_null())
        )

    def _add_aum_weights(self):
        self.weights = (
            self.weights.join(
                self.position_class.funds_aum.select(pl.col(self.COLUMNS_FUNDS_AUM)),
                on="fund_nickname",
                how="left",
                coalesce=True,
            )
            .with_columns(
                pl.when(pl.col("fund_nickname").str.contains("trend|latam"))
                .then(pl.col("broker_azimut"))
                .otherwise(pl.col("broker_quest"))
                .alias("broker"),
                pl.when(pl.col("ticker").str.contains(" "))
                .then(pl.col("aum_current"))
                .otherwise(pl.col("aum_current"))
                .alias("aum"),
                pl.when(pl.col("order") > 0)
                .then(pl.lit("buy"))
                .otherwise(pl.lit("sell"))
                .alias("side"),
                pl.when(
                    (pl.col("bool_quantity").is_not_null())
                    | (pl.col("order").abs() > 15)
                    | (pl.col("fund_nickname").str.contains("trend|latam"))
                )
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias("bool_quantity"),
                pl.when(pl.col("fund_nickname").str.contains("trend|latam"))
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias("azimut"),
            )
            .filter(pl.col("aum").is_not_null())
            .with_columns(
                pl.when(pl.col("bool_quantity"))
                .then(pl.col("order") / pl.col("aum"))
                .otherwise(pl.col("order") / 100)
                .alias("order_percentual"),
                pl.when(pl.col("bool_quantity"))
                .then(pl.col("order"))
                .otherwise((pl.col("order") / 100) * pl.col("aum"))
                .alias("order_quantity"),
            )
        )

    def _add_position_weights(self):
        # Group_by necessario para o caso de swap, em que o ticker tem o mesmo nome e aparenta ser repetido
        self.position_class.position = self.position_class.position.select(pl.col(self.COLUMNS_POSITION)).group_by(
            ["ticker", "fund_nickname"]
        ).agg(
            pl.col("position_initial").sum().alias("position_initial"),
            pl.col("quantity").sum().alias("quantity"),
        )
        self.weights = self.weights.join(
            self.position_class.position.select(pl.col(self.COLUMNS_POSITION)),
            on=["fund_nickname", "ticker"],
            how="left",
            coalesce=True,
        ).select(pl.col(self.WEIGHTS_COLUMNS))


class Allocations:
    def __init__(self, fills, weights, wb, security_info):
        self.wb = wb
        self.join_broker_weights(fills, weights)
        self.join_no_broker_weights(weights, fills.columns)
        self.check_missing_fills()
        if self.allocations.is_empty():
            return
        self.merge_security_info(security_info)
        self.create_orders_columns()
        self.create_financial_orders()
        self.create_percentual_order()
        self.check_allocations()
        self.treat_allocations()
        self.check_change_side()
        self.check_total_fill(fills)

    def join_broker_weights(self, fills, weights):
        weights_broker = weights.filter(pl.col("broker").is_not_null())
        self.allocations_broker = fills.join(
            weights_broker,
            on=["ticker", "side", "broker", "azimut"],
            how="left",
            coalesce=True,
        )

    def join_no_broker_weights(self, weights, fills_columns):
        self.allocations_no_broker = self.allocations_broker.filter(
            pl.col("order").is_null()
        )
        repeated_order = (
            self.allocations_no_broker.group_by(["ticker", "side", "azimut"])
            .agg(
                pl.col("ticker").count().alias("count"),
                pl.col("broker"),
                pl.col("platform").str.concat(delimiter=", ").alias("platform"),
            )
            .filter(pl.col("count") > 1)
        )

        exist_repeated_order = not repeated_order.is_empty()
        if exist_repeated_order:
            repeated_order = repeated_order.explode("broker").select(
                pl.col(["broker", "ticker", "side", "azimut", "platform"]),
            )
            self.exist_missing_fills(repeated_order)
            return

        weights_no_broker = weights.filter(pl.col("broker").is_null())
        self.allocations_no_broker = self.allocations_no_broker.select(
            pl.col(fills_columns)
        ).join(
            weights_no_broker.drop("broker", strict=False),
            on=["ticker", "side", "azimut"],
            how="left",
            coalesce=True,
        )

    def check_missing_fills(self):
        missing_fills = self.allocations_no_broker.filter(pl.col("order").is_null())
        exist_missing_fills_df = not missing_fills.is_empty()
        if exist_missing_fills_df:
            self.exist_missing_fills(missing_fills)
            self.allocations = pl.DataFrame()
            return

        self.allocations = pl.concat(
            [self.allocations_broker, self.allocations_no_broker]
        )
        self.allocations = self.allocations.with_columns(
                pl.when(pl.col("fund_nickname").str.contains("grumari"))
                .then(pl.lit(10000000))
                .otherwise(pl.col("aum"))
                .alias("aum"),
                )

    def exist_missing_fills(self, missing_fills):
        dataframe = (
            missing_fills.with_columns(
                pl.lit(True).alias("keep_line"),
                pl.lit(True).alias("bool_quantity"),
                pl.when(pl.col("azimut"))
                .then(pl.col("broker"))
                .otherwise(pl.lit(None))
                .alias("broker_azimut"),
                pl.when(pl.col("azimut"))
                .then(pl.lit(None))
                .otherwise(pl.col("broker"))
                .alias("broker_quest"),
            )
            .select(
                pl.col(
                    [
                        "keep_line",
                        "bool_quantity",
                        "broker_quest",
                        "broker_azimut",
                        "ticker",
                        "side",
                    ]
                )
            )
            .sort(by=["side", "ticker"])
        )

        self.wb.paste_missing_fills(dataframe)
        show_warning(
            dataframe=missing_fills.sort(by="ticker"),
            columns=["ticker", "broker", "side", "platform"],
            title="Missing Fills",
            stop=False,
        )

    def merge_security_info(self, security_info):
        self.allocations = self.allocations.join(
            security_info, on="ticker", how="left", coalesce=True
        )

    def create_orders_columns(self):
        self.allocations = self.allocations.with_columns(
            pl.when(pl.col("bool_quantity"))
            .then(pl.col("order") * pl.col("price_current_brl") / pl.col("aum"))
            .otherwise(pl.col("order") / 100)
            .alias("order_percentual"),
            pl.when(pl.col("bool_quantity"))
            .then(pl.col("order"))
            .otherwise(
                (pl.col("order") / 100) * pl.col("aum") / pl.col("price_current_brl")
            )
            .alias("order_quantity"),
        )

    def create_financial_orders(self):
        self.allocations = self.allocations.with_columns(
            pl.when(pl.col("ticker").str.contains("wd1|wi1"))
            .then(pl.col("order") * pl.col("average_price"))
            .otherwise((pl.col("order_percentual") * pl.col("aum")))
            .alias("order_financial")
        ).filter(pl.col("order_financial") != 0)

    def create_percentual_order(self):
        self.allocations = self.allocations.with_columns(
            (
                pl.col("order_financial")
                .sum()
                .over(["side", "ticker", "broker", "azimut"])
            ).alias("order_financial_total")
        ).with_columns(
            (
                pl.col("order_financial")
                / pl.col("order_financial_total")
                * pl.col("filled")
            )
            .round(0)
            .alias("fill")
        )

    def check_allocations(self):
        """Checa se a alocação total é igual ao total preenchido, se não for,
        aloca a diferença na maior ordem percentual, ou seja, no maior fundo em que a ordem foi passada
        """
        self.allocations = self.allocations.with_columns(
            pl.col("fill")
            .sum()
            .over(["side", "ticker", "broker", "azimut"])
            .alias("total_allocation"),
            pl.col("order_financial")
            .max()
            .over(["side", "ticker", "broker", "azimut"])
            .alias("order_biggest_financial"),
        ).with_columns(
            pl.when(pl.col("total_allocation") == pl.col("filled"))
            .then(pl.col("fill"))
            .when(pl.col("order_biggest_financial") != pl.col("order_financial"))
            .then(pl.col("fill"))
            .otherwise(pl.col("fill") + pl.col("filled") - pl.col("total_allocation"))
            .alias("fill")
        )

    def treat_allocations(self):
        self.allocations = (
            self.allocations.with_columns(
                (
                    pl.when(pl.col("side") == "buy")
                    .then(pl.col("fill"))
                    .otherwise(-pl.col("fill"))
                ).alias("fill"),
                pl.col("quantity").fill_null(0),
            )
            .with_columns(
                (
                    pl.col("fill").sum().over(["ticker", "fund_nickname"])
                    + pl.col("quantity")
                ).alias("quantity_final")
            )
            .with_columns(
                (
                    pl.col("quantity_final")
                    * pl.col("price_current_brl")
                    * pl.col("size")
                    / pl.col("aum")
                ).alias("position_final"),
            )
            .rename({"quantity": "quantity_initial"})
            .sort(by=["ticker", "side", "broker"])
        )

    def check_change_side(self):
        change_side = self.allocations.filter(
            pl.col("quantity_final") * pl.col("quantity_initial") < 0
        )
        if not change_side.is_empty():
            show_warning(
                dataframe=change_side.sort(by="ticker"),
                columns=["ticker", "broker", "side", "fund_nickname"],
                title="Tem mudança de lado!",
                start_text="Esses tickers mudaram buy <-> sell:",
                stop=False,
            )

    def check_total_fill(self, fills):
        total_fill_allocations = self.allocations.select(
                pl.col("fill").abs().sum())[ 0, 0 ]
        total_fill_fills = fills.select(pl.col("filled").sum())[0, 0]

        if total_fill_allocations != total_fill_fills:
            allocations = self.allocations.group_by(
                ["side", "ticker", "broker", "azimut"]
            ).agg(pl.col("fill").sum().abs())
            wrong_allocations = allocations.join(
                fills.select(["side", "ticker", "broker", "azimut", "filled"]),
                on=["side", "ticker", "broker", "azimut"],
                how="left",
                coalesce=True,
            ).filter(pl.col("fill") != pl.col("filled"))
            if not wrong_allocations.is_empty():
                show_warning(
                    dataframe=wrong_allocations.sort(by="ticker"),
                    title="Alocação errada",
                    start_text="Rever alocação para esses ativos:",
                    stop=False,
                )


class Excel_output_info:
    def __init__(self, allocations: pl.DataFrame) -> None:
        self.allocations = allocations

        self.create_tags()
        self.aggregate_orders_and_fills()
        self.create_pnl_columns()
        self.create_info_resumo_table()
        self.format_floats()

    def create_tags(self):
        self.allocations = self.allocations.with_columns(
            pl.concat_str(["ticker", "side", "fund_nickname"], separator="_").alias(
                "tag_ticker_side_fund"
            ),
            (pl.col("ticker") + "_" + pl.col("side") + "_" + pl.col("azimut")).alias(
                "tag_ticker_side_azimut"
            ),
            (pl.col("ticker") + "_" + pl.col("fund_nickname")).alias("tag_ticker_fund"),
        )

    def aggregate_orders_and_fills(self):
        self.allocations = self.allocations.with_columns(
            (
                (pl.col("order_financial").sum().over(["ticker", "side", "azimut"]))
                / pl.col("price_current_brl")
            ).alias("order_ticker_side_azimut"),
            pl.col("fill")
            .sum()
            .over(["ticker", "side", "azimut"])
            .alias("fill_ticker_side_azimut"),
            (
                (
                    pl.col("order_financial")
                    .sum()
                    .over(["ticker", "side", "fund_nickname"])
                )
                / pl.col("size")
                / pl.col("price_current_brl")
            ).alias("order_ticker_side_fund"),
            pl.col("fill")
            .sum()
            .over(["ticker", "side", "fund_nickname"])
            .alias("fill_ticker_side_fund"),
        ).with_columns(
            (pl.col("fill_ticker_side_fund") / pl.col("order_ticker_side_fund")).alias(
                "percentual_executed_fund"
            )
        )

    def create_pnl_columns(self):
        self.allocations = self.allocations.with_columns(
            (pl.col(["fund_nickname"]).count().over(["fund_nickname", "ticker"])).alias(
                "count_fund_ticker"
            )
        ).with_columns(
            (
                (pl.col("average_price") * pl.col("fill"))
                .sum()
                .over(["ticker", "side", "fund_nickname"])
                / pl.col("aum")
                * 10000
            ).alias("pnl_bips_fund_executado"),
            (
                (pl.col("price_current_brl") * pl.col("fill"))
                .sum()
                .over(["ticker", "side", "fund_nickname"])
                / pl.col("aum")
                * 10000
            ).alias("pnl_bips_fund_position"),
            (
                (
                    pl.when(
                        (pl.col("ticker").str.contains("wdo|win"))
                        | (
                            (pl.col("ticker").str.contains(" us"))
                            & (pl.col("fund_nickname").str.contains("top$|tr$"))
                        )
                    )
                    .then(0)
                    .otherwise(
                        (pl.col("position_initial") - pl.col("position_final"))
                        / pl.col("count_fund_ticker")
                    )
                )
                .sum()
                .over(pl.col(["fund_nickname"]))
            ).alias("caixa_difference"),
            (
                (
                    (pl.col("position_initial") - pl.col("position_final"))
                    / pl.col("count_fund_ticker")
                )
                .sum()
                .over(pl.col(["fund_nickname"]))
            ).alias("position_difference"),
        )

    def create_info_resumo_table(self):
        self.allocations = self.allocations.with_columns(
            (
                pl.col("fill").sum().over(["ticker", "side"])
                * pl.col("price_current_brl")
                * pl.col("size")
                / pl.col("order_financial").sum().over(["ticker", "side"])
            ).alias("order_total_percentual_executed"),
            pl.col("order_percentual")
            .sum()
            .over(["ticker", "fund_nickname"])
            .alias("order_percentual_summed"),
        )

    def format_floats(self):
        self.allocations = self.allocations.with_columns(
            pl.when(pl.col("bool_quantity") | pl.col("azimut"))
            .then(pl.format("{}", pl.col("order").round(2)))
            .otherwise(pl.format("{}%", (pl.col("order")).round(3)))
            .alias("order"),
            (
                pl.format(
                    "{}",
                    (
                        pl.when(
                            (pl.col("percentual_executed_fund") > 0.96)
                            & (pl.col("percentual_executed_fund") < 1.04)
                        )
                        .then(pl.col("order_percentual_summed"))
                        .otherwise(
                            pl.col("percentual_executed_fund")
                            * pl.col("order_percentual_summed")
                        )
                        * 100
                    ).round(2),
                )
                + "/"
                + pl.format("{}", (pl.col("order_percentual_summed") * 100).round(2))
            ).alias("text_resumo"),
            pl.when(
                (pl.col("percentual_executed_fund") > 0.96)
                & (pl.col("percentual_executed_fund") < 1.04)
            )
            .then(1)
            .otherwise(
                pl.format(
                    "{}%", (pl.col("order_total_percentual_executed") * 100).round(2)
                )
            )
            .alias("order_total_percentual_executed"),
            pl.col("order_percentual")
            .sum()
            .over(["fund_nickname"])
            .alias("position_difference_expected"),
        )


class Outputs:
    today = datetime.datetime.today()
    year = today.year
    date_string = today.strftime("%Y%m%d")

    PATH_PARQUET_FILES = (
        os.environ["onedrive"] + r"\Trading\files_daily"
    )
    PATH_FUNDS_INFO = (
        os.environ["onedrive"] + r"\Trading\files_static\dictionaries\funds_info.parquet"
    )
    PATH_PARQUET_ALLOCATIONS_V2 = (
        PATH_PARQUET_FILES
        + rf"\{year}\{date_string}\gerencial\allocations_portfolio.parquet"
    )
    PATH_PARQUET_ALLOCATIONS = (
        PATH_PARQUET_FILES + rf"\{year}\{date_string}\gerencial\allocations.parquet"
    )
    PATH_TXT_ALLOCATIONS_RISCO = (
        r"O:\Shared\_Importacoes\ImportacaoTradesBolsa\allocations.txt"
    )

    COLUMNS_V2 = [
        "ticker",
        "fund_nickname",
        "fill",
        "average_price",
        "trade_financial",
    ]
    COLUMNS_RISCO = ["date", "ticker", "name_risk", "side", "fill", "average_price"]

    ALLOCATIONS_COLUMNS = [
        "fund_nickname",
        "ticker",
        "side",
        "broker",
        "fill",
        "average_price",
        "order",
        "position_initial",
        "position_final",
        "quantity_final",
        "tag_ticker_side_fund",
        "order_ticker_side_azimut",
        "fill_ticker_side_azimut",
        "tag_ticker_side_azimut",
        "pnl_bips_fund_executado",
        "pnl_bips_fund_position",
        "caixa_difference",
        "order_total_percentual_executed",
        "text_resumo",
        "percentual_executed_fund",
        "allocation_time",
        "tag_ticker_fund",
    ]

    def __init__(self, allocations: pl.DataFrame, wb_class, fills) -> None:
        self.allocations = allocations
        self.create_allocations_parquet()
        self.merge_funds_info()
        self.create_txt_risco()
        self.paste_fills_excel(wb_class, fills)
        self.paste_allocations_excel(wb_class, allocations)

    def create_allocations_parquet(self):
        self.allocations.write_parquet(self.PATH_PARQUET_ALLOCATIONS)

    def merge_funds_info(self):
        funds_info = pl.read_parquet(self.PATH_FUNDS_INFO)
        self.allocations = self.allocations.join(
            funds_info, on="fund_nickname", how="left", coalesce=True
        )

    def create_txt_risco(self):
        df_risco = self.allocations.with_columns(
            pl.when(
                (pl.col("ticker").str.contains(" "))
                & (pl.col("fund_nickname").is_in(["top", "tr"]))
            )
            .then("quest " + pl.col("fund_nickname") + " cl")
            .otherwise(pl.col("name_risk"))
            .alias("name_risk")
        )
        df_risco = (
            df_risco.with_columns(
                pl.col("ticker").str.replace(r" (.)+", ""),
                pl.lit(self.date_string).alias("date"),
            )
            .select(pl.col(self.COLUMNS_RISCO))
            .write_csv(
                self.PATH_TXT_ALLOCATIONS_RISCO,
            )
        )

    def paste_fills_excel(self, wb_class, fills):
        wb_class.paste_fills(fills)

    def paste_allocations_excel(self, wb_class, allocations):
        global a
        a = allocations
        df_allocations = allocations.select(self.ALLOCATIONS_COLUMNS)
        df_allocations = df_allocations.sort(["fund_nickname", "ticker"])
        wb_class.paste_allocations(df_allocations)


main = Main()

# ERROS:
# 1. Se o order_biggest_financial for repetido (pode acontecer quando se for utilizado
# quantidade no lugar de financeiro) e o round do fill for errado, a aloca'cao vai ficar incorreta

# Consertar caso em que h'a ordem duplicada
