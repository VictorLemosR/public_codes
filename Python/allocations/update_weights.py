import os

import polars as pl

# b
from Modules.portfolio_position import obtain_position
from Modules.warning_message import show_warning
from Modules.workbook_functions import obtain_wb as obtain_wb_module

FUNDS = ["tr", "top", "small", "fia", "trend", "latam"]

pl.Config.set_tbl_cols(30)
pl.Config.set_tbl_rows(80)


class Main:
    def __init__(self) -> None:
        self.wb_class = Workbook()
        self.position_class = obtain_position()
        self.weights_class = Weights(
            self.wb_class.orders,
            self.position_class.position,
            self.position_class.funds_aum,
            self.wb_class.old_weights,
            self.position_class.security_info,
        )
        self.wb_class.display_weights(self.weights_class.weights)

        if self.wb_class.update_caixa:
            from Portfolio.Routines.caixa_sql import Main as caixa_sql

            df_caixa = caixa_sql().df
            self.wb_class.display_caixa(df_caixa)

        if self.wb_class.update_subred:
            from Portfolio.Routines.subred_quest import Main as subred_quest

            subred_quest = subred_quest().df
            self.wb_class.display_subred(subred_quest)

class Workbook:
    WORKBOOK_PATH = (
        os.environ["onedrive"] + r"\Trading\Trading.xlsm"
    )

    ORDERS_SHEET_NAME = "Ordens"
    ORDERS_RANGE = "A3:P103"
    ORDERS_COLUMNS = (
        [
            "broker",
            "plataforma",
            "ticker",
        ]
        + FUNDS
        + ["preço local"]
    )

    WEIGHTS_SHEET_NAME = "Allocations"
    WEIGHTS_INPUT_RANGE = "Z4:AP1000"
    WEIGHTS_OUTPUT_RANGE = "Z4:AP1000"

    TRADES_SHEET_NAME = "Trades"

    CAIXA_SHEET_NAME = "Caixa"
    CAIXA_INPUT_RANGE = "H2:H3"
    CAIXA_OUTPUT_RANGE = "B2:H11"
    SUBRED_INPUT_RANGE = "C18:C19"
    SUBRED_OUTPUT_RANGE ="A18" 
    SUBRED_CLEAR_RANGE ="A19:C29" 

    def __init__(self):
        self.obtain_wb()
        self.obtain_orders()
        self.check_order_empty()
        self.obtain_old_weights()
        self.obtain_caixa_date()
        self.obtain_subred_updated()

    def obtain_wb(self):
        self.wb = obtain_wb_module(self.WORKBOOK_PATH)

    def obtain_orders(self):
        self.orders = (
            self.wb.obtain_range(self.ORDERS_SHEET_NAME, self.ORDERS_RANGE)
            .select(pl.col(self.ORDERS_COLUMNS))
            .with_columns(pl.col(pl.Utf8).str.to_lowercase())
        )
        #Copiar valores na trading
        #self.wb.wb.sheets[self.ORDERS_SHEET_NAME].range("D4:I33").value = (
        #    self.wb.wb.sheets[self.ORDERS_SHEET_NAME].range("D4:I33").value
        #)

    def obtain_old_weights(self):
        self.old_weights = self.wb.obtain_range(
            self.WEIGHTS_SHEET_NAME, self.WEIGHTS_INPUT_RANGE
        )

    def obtain_caixa_date(self):
        self.caixa_date = self.wb.obtain_range(
            self.CAIXA_SHEET_NAME, self.CAIXA_INPUT_RANGE
        )
        self.update_caixa = False
        if self.caixa_date.shape[0] == 0:
            self.update_caixa = True

    def obtain_subred_updated(self):
        self.subred = self.wb.obtain_range(
            self.CAIXA_SHEET_NAME, self.SUBRED_INPUT_RANGE
        )
        self.update_subred = False
        if self.subred.shape[0] == 0:
            self.update_subred = True

    def check_order_empty(self):
        not_null_columns = (pl.col("ticker").is_not_null()) & (
            pl.any_horizontal(pl.col(FUNDS).is_not_null())
        )
        broker_is_empty = self.orders.filter(not_null_columns).is_empty()
        if broker_is_empty:
            message = "\n\nNão há ordem para ser alocada"
            show_warning(stop=True, title="Ordem vazia", start_text=message)

    def obtain_allocation_sheet(self):
        self.allocation_sheet = self.wb.wb.sheets[self.WEIGHTS_SHEET_NAME]

    def display_weights(self, df):
        self.wb.display(
            df,
            sheet_name=self.WEIGHTS_SHEET_NAME,
            cell_to_print=self.WEIGHTS_OUTPUT_RANGE[:2],
            range_to_clear=self.WEIGHTS_OUTPUT_RANGE,
        )
        weight_sheet = self.wb.wb.sheets[self.WEIGHTS_SHEET_NAME]
        weight_sheet.select()
        weight_sheet.range("al5").select()

    def display_subred(self, df):
        self.wb.display(
            df,
            sheet_name=self.CAIXA_SHEET_NAME,
            cell_to_print=self.SUBRED_OUTPUT_RANGE,
            range_to_clear=self.SUBRED_CLEAR_RANGE,
        )

    def display_caixa(self, df):
        self.wb.display(
            df,
            sheet_name=self.CAIXA_SHEET_NAME,
            cell_to_print=self.CAIXA_OUTPUT_RANGE[:2],
        )


class Weights:
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
        "aum_onshore_strategy_financial",
        "aum_offshore_strategy_financial",
    ]

    COLUMNS_WEIGHTS = [
        "broker",
        "plataforma",
        "ticker",
        "fund_nickname",
        "order",
        "aum",
        "position_initial",
        "fund_strategy",
        "quantity",
        "price_current_brl",
        "side",
    ]
    QUEST_STRATEGIES = ["tr", "top", "small", "fia"]
    AZIMUT_STRATEGIES = ["trend", "latam"]
    STRATEGIES = QUEST_STRATEGIES + AZIMUT_STRATEGIES
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
        "trend",
        "latam",
    ]
    COLUMNS_PRINT = [
        "keep_line",
        "bool_quantity",
        "broker_quest",
        "broker_azimut",
        "ticker",
    ] + FUNDS

    def __init__(self, orders, position, funds_aum, old_weights, prices) -> None:
        self.check_class = Weights_checks()
        self.check_class

        self.select_columns_start(orders)
        self.check_duplicated_order()
        self.check_keep_line(old_weights)
        if self.orders.is_empty():
            self.weights = self.keep_line.sort(
                by=[
                    "ticker",
                    "keep_line",
                    "bool_quantity",
                    "broker_azimut",
                    "broker_quest",
                ]
            )

            return
        self.add_prices(prices)
        self.treat_orders()
        self.join_orders_aum_position(position, funds_aum)
        self.treat_onshore_offshore()
        self.check_price_exists()
        self.create_targets()
        self.align_orders()
        self.check_big_differences()
        self.create_weights()
        self.add_keep_line()

    def select_columns_start(self, orders: pl.DataFrame):
        self.orders = orders.rename({"preço local": "price_current_excel"})

    def check_duplicated_order(self):
        self.orders = (
            self.orders.filter(
                ((pl.col("plataforma") != "xxxxx") | (pl.col("plataforma").is_null()))
                & (pl.any_horizontal(pl.col(self.STRATEGIES).is_not_null()))
                & (pl.col("ticker").is_not_null())
            )
            .with_columns(pl.col(self.STRATEGIES).cast(pl.Float64))
            .with_columns(
                pl.when(pl.sum_horizontal(pl.col(self.STRATEGIES)) > 0)
                .then(pl.lit("buy"))
                .otherwise(pl.lit("sell"))
                .alias("side"),
                pl.when(pl.sum_horizontal(pl.col(self.QUEST_STRATEGIES)) != 0)
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias("quest"),
                pl.when(pl.sum_horizontal(pl.col(self.AZIMUT_STRATEGIES)) != 0)
                .then(pl.lit(True))
                .otherwise(pl.lit(False))
                .alias("azimut"),
                pl.col("broker").replace(None, "").alias("broker"),
            )
        )

        duplicated_order_quest = self.orders.filter(
            pl.col("quest").is_not_null()
        ).filter(
            (
                self.orders.select(
                    pl.col(["broker", "ticker", "side", "quest"])
                ).is_duplicated()
            )
        )
        duplicated_order_azimut = self.orders.filter(
            pl.col("azimut").is_not_null()
        ).filter(
            (
                self.orders.select(
                    pl.col(["broker", "ticker", "side", "azimut"])
                ).is_duplicated()
            )
        )
        duplicated_order = pl.concat([duplicated_order_quest, duplicated_order_azimut])
        exist_duplicated_order = not duplicated_order.is_empty()
        if exist_duplicated_order:
            duplicated_order_print = duplicated_order.select(
                pl.col(["broker", "ticker", "side"])
            ).sort(by="ticker")
            show_warning(
                dataframe=duplicated_order_print,
                title="Ordens duplicadas",
                start_text="Colocar broker\n",
                stop=True,
            )

    def check_keep_line(self, old_weights) -> None:
        self.keep_line = old_weights.filter(
            pl.col("keep_line").is_not_null()
        ).with_columns(
            pl.col(self.FUNDS).cast(pl.Float64),
            pl.lit(True).alias("keep_line").cast(pl.Boolean),
            pl.when(pl.col("bool_quantity").is_null())
            .then(pl.lit(None))
            .otherwise(True)
            .cast(pl.Boolean)
            .alias("bool_quantity")
            .cast(pl.Boolean),
            pl.col("broker_quest").replace(None, "").alias("broker_quest"),
        )
        delete_from_orders = self.keep_line.with_columns(
            pl.when(pl.sum_horizontal(pl.col(self.FUNDS)) > 0)
            .then(pl.lit("buy"))
            .otherwise(pl.lit("sell"))
            .alias("side"),
            pl.lit(True).alias("delete_from_orders"),
        ).select(pl.col(["broker_quest", "ticker", "side", "delete_from_orders"]))
        self.orders = self.orders.join(
            delete_from_orders,
            left_on=["broker", "ticker", "side"],
            right_on=["broker_quest", "ticker", "side"],
            how="left",
            coalesce=False,
        ).filter(pl.col("delete_from_orders").is_null())

    def add_prices(self, prices):
        try:
            self.orders = self.orders.with_columns(
                pl.col("price_current_excel").cast(pl.Float64)
            )
        except pl.ComputeError:
            self.orders = self.orders.with_columns(
                pl.when(pl.col("price_current_excel") == "n/a")
                .then(pl.lit(None))
                .otherwise(pl.col("price_current_excel"))
                .cast(pl.Float64)
                .alias("price_current_excel")
            )

        self.orders = (
            self.orders.join(prices, on="ticker", how="left", coalesce=True)
            .with_columns(
                pl.when(pl.col("price_current_brl").is_null())
                .then(pl.col("price_current_excel"))
                .otherwise(pl.col("price_current_brl"))
                .alias("price_current_brl"),
            )
            .with_columns(
                pl.when(pl.col("ticker").str.contains("wdo|dol"))
                .then(pl.col("price_current_brl") * 10)
                .when(pl.col("ticker").str.contains("win|ind"))
                .then(pl.col("price_current_brl") * 0.2)
                .otherwise(pl.col("price_current_brl"))
                .alias("price_current_brl")
            )
        )

    def treat_orders(self):
        self.orders = self.orders.unpivot(
            index=["broker", "plataforma", "ticker", "side", "price_current_brl"],
            variable_name="fund_strategy",
            value_name="order",
            on=FUNDS,
        ).with_columns(pl.col("order").cast(pl.Float64))

    def join_orders_aum_position(self, position, funds_aum):
        self.orders = (
            self.orders.join(
                funds_aum.select(pl.col(self.COLUMNS_FUNDS_AUM)),
                on="fund_strategy",
                how="left",
                coalesce=False,
            )
            .join(
                position.select(pl.col(self.COLUMNS_POSITION)),
                on=["ticker", "fund_nickname"],
                how="left",
                coalesce=False,
            )
            .with_columns(
                pl.col("quantity").fill_null(0),
                pl.col("position_initial").fill_null(0) * 100,
            )
        )

    def treat_onshore_offshore(self):
        self.orders = self.orders.with_columns(
            pl.when(pl.col("ticker").str.contains(" "))
            .then(
                pl.when(pl.col("aum_offshore_strategy_financial") != 0)
                .then(pl.col("aum_current"))
                .otherwise(0)
            )
            .otherwise(pl.col("aum_current"))
            .alias("aum"),
            pl.col(pl.Utf8).fill_null(""),
        ).select(pl.col(self.COLUMNS_WEIGHTS))

    def check_price_exists(self):
        price_is_null = self.orders.filter((pl.col("price_current_brl").is_null()))
        if not price_is_null.is_empty():
            show_warning(
                dataframe=price_is_null.unique("ticker"),
                columns=["ticker"],
                title="Preço não encontrado",
                stop=True,
                start_text="Preço não encontrado\n(possivelmente não existe na base)",
            )

        self.orders = self.orders.with_columns(
            pl.col("price_current_brl").cast(pl.Float64)
        )

    def create_targets(self):
        self.targets = (
            self.orders.filter((pl.col("order").is_not_null()) & (pl.col("order") != 0))
            .with_columns(
                pl.when(pl.col("fund_nickname") == pl.col("fund_strategy"))
                .then(
                    pl.col("order")
                    + pl.col("quantity")
                    * pl.col("price_current_brl")
                    / pl.col("aum")
                    * 100
                )
                .otherwise(None)
                .alias("target")
            )
            .with_columns(
                pl.col("target")
                .max()
                .over(["broker", "ticker", "fund_strategy", "side"])
            )
            .filter((pl.col("fund_nickname") == pl.col("fund_strategy")))
            .select(
                pl.col(
                    [
                        "position_initial",
                        "broker",
                        "ticker",
                        "fund_strategy",
                        "target",
                        "side",
                    ]
                )
            )
        )

    def align_orders(self):
        self.orders = (
            self.orders.join(
                self.targets,
                on=["broker", "ticker", "fund_strategy", "side"],
                how="left",
                coalesce=False,
            )
            # Ajustar o target para a situação em que ele ficou muito próximo de 0, indicando que é uma zeragem
            .with_columns(
                pl.when(pl.col("order").is_null())
                .then(None)
                .otherwise(pl.col("target"))
                .alias("target"),
                pl.when(pl.col("target").abs() < 0.05)
                .then(True)
                .otherwise(False)
                .alias("bool_quantity"),
            )
            .with_columns(
                pl.when(pl.col("bool_quantity"))
                .then(-pl.col("quantity"))
                .otherwise(pl.col("target") - pl.col("position_initial"))
                .alias("order_aligned")
            )
            .with_columns(
                pl.when(
                    (pl.col("fund_nickname").str.contains("trend|latam"))
                    & (~pl.col("bool_quantity"))
                )
                .then(
                    (
                        pl.col("order_aligned")
                        * pl.col("aum")
                        / 10000
                        / pl.col("price_current_brl")
                    ).round(2)
                    * 100
                )
                .otherwise(pl.col("order_aligned"))
                .alias("order_aligned"),
            )
            .with_columns(
                pl.when(
                    (
                        (pl.col("fund_nickname").str.contains("trend|latam"))
                        & (pl.col("ticker").str.contains(" "))
                    )
                    | (~pl.col("fund_nickname").str.contains("trend|latam"))
                )
                .then(pl.col("order_aligned"))
                .otherwise((pl.col("order_aligned") / 100).round(0) * 100)
                .alias("order_aligned")
            )
        )

    def check_big_differences(self):
        big_differences = self.orders.filter(
            (
                (~pl.col("bool_quantity"))
                & (~pl.col("fund_nickname").str.contains("trend|latam"))
            )
            & ((pl.col("order_aligned") - pl.col("order")).abs() > 0.15)
        )

        if big_differences.is_empty():
            return

        big_differences = big_differences.with_columns(
            pl.col("position_initial").round(2)
        )
        show_warning(
            dataframe=big_differences,
            columns=["fund_nickname", "ticker", "position_initial"],
            title="Existem diferenças grandes",
        )
        self.orders = self.orders.with_columns(
            pl.when(
                (
                    (~pl.col("bool_quantity"))
                    & (~pl.col("fund_nickname").str.contains("trend|latam"))
                )
                & ((pl.col("order_aligned") - pl.col("order")).abs() > 0.15)
            )
            .then(pl.lit(None))
            .otherwise(pl.col("order_aligned"))
            .alias("order_aligned"),
        )
        self.orders = self.orders.with_columns(
            pl.when(
                (pl.col("fund_nickname") == "top prev")
                & (pl.col("ticker").str.contains(" "))
            )
            .then(pl.lit(None))
            .otherwise(pl.col("order_aligned"))
            .alias("order_aligned"),
        )

    def create_weights(self):
        self.weights = (
            self.orders.pivot(
                index=["broker", "ticker", "bool_quantity", "side"],
                on="fund_nickname",
                values=["order_aligned"],
                aggregate_function="sum",
            )
            .filter(pl.sum_horizontal(self.FUNDS) != 0)
            .with_columns(
                pl.col(pl.Float64).replace(0, None),
                pl.col("broker").alias("broker_quest"),
                pl.lit("").alias("broker_azimut"),
                pl.lit(None).alias("keep_line").cast(pl.Boolean),
                pl.col("bool_quantity").replace(False, None),
            )
            .select(self.COLUMNS_PRINT)
        )

    def add_keep_line(self):
        self.weights = pl.concat([self.weights, self.keep_line]).sort(
            by=["ticker", "keep_line", "bool_quantity", "broker_azimut", "broker_quest"]
        )


class Weights_checks:
    def check_keep_line(self):
        pass


m = Main()
# Montar latam e  trend via um parquet possivelmente, mas so quando eu conseguir enviar ordem via api
