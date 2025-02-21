import os
import polars as pl
import btgsolutions_tradeservices as api_solutions
from Trading.Solutions.solutions_info import Info
import datetime


class _Main:
    def __init__(self) -> None:
        self.controller = _Solutions().controller
        self.today = datetime.datetime.today()
        self.brokers = _Broker().df


class _Solutions:
    def __init__(self):
        self.create_controller()

    def create_controller(self):
        self.controller = api_solutions.OrderController(
            token=Info.token,
            entity=Info.entity,
            order_api_host=Info.host,
        )


class _Broker:
    BROKERS_PATH = (
        os.environ["onedrive"] + r"\Trading\files_static\dictionaries\broker_codes.parquet"
    )
    COLUMNS = ["code_b3", "broker"]

    def __init__(self) -> None:
        self.obtain_broker_info()
        self.filter_brokers()

    def obtain_broker_info(self):
        self.brokers_df = pl.read_parquet(self.BROKERS_PATH)

    def filter_brokers(self):
        self.df = self.brokers_df.select(pl.col(self.COLUMNS))


class _Fills:
    COLUMNS = {
        "symbol": "ticker",
        "side": "side",
        "cumQty": "filled",
        "avgPx": "average_price",
        "brokerExchangeCode": "code_b3",
        "transactTime": "last_fill_time",
        "price": "limited_price",
        "qty": "sent_quantity",
        # cum, descobrir se eh util
        # forexReq, descobrir se eh util
    }

    def __init__(self, controller, today, brokers) -> None:
        self.controller = controller
        if self.exist_order():
            self.filter_fills(today)
            self.merge_brokers(brokers)
            self.treat_fills()

    def exist_order(self):
        answer_controller = self.controller.get_orders()
        if answer_controller == 204:
            print("No solutions")
            self.df = pl.DataFrame()
            return False
        else:
            try:
                self.df = pl.DataFrame(answer_controller)
            except Exception as e:
                print(f"answer_controller: {answer_controller}")
                raise Exception(f"Erro na resposta do solutions: {e}")
            return True

    def filter_fills(self, today):
        self.df = (
            self.df.select(self.COLUMNS.keys())
            .rename(self.COLUMNS)
            .with_columns(
                pl.col("last_fill_time").str.strptime(pl.Datetime, "%FT%H:%M:%S.%Z")
            )
            .with_columns(pl.col("last_fill_time").dt.day().alias("day"))
            # .filter(pl.col("last_fill_time") == today)
            .with_columns(pl.col(pl.Utf8).str.to_lowercase())
        )

    def merge_brokers(self, brokers):
        self.df = (
            self.df.with_columns(pl.col("code_b3").cast(pl.Int16))
            .join(brokers, on="code_b3", how="left", coalesce=False)
            .select(pl.exclude("code_b3"))
        )

    def treat_fills(self):
        self.df = (
            self.df.with_columns(
                pl.col("average_price").cast(pl.Float64),
                pl.col("filled").cast(pl.Int64),
                pl.when(
                    (
                        (pl.col("ticker").str.len_chars() == 6)
                        | (pl.col("ticker").str.len_chars() == 7)
                    )
                    & (pl.col("ticker").str.ends_with("f"))
                )
                .then(pl.col("ticker").str.replace(".$", ""))
                .otherwise(pl.col("ticker"))
                .alias("ticker"),
            )
            .filter(pl.col("filled") > 0)
            .group_by(["ticker", "side", "broker"])
            .agg(
                pl.col("filled").sum(),
                ((pl.col("average_price") * pl.col("filled")).sum()).alias(
                    "financeiro"
                ),
                pl.col("last_fill_time").max().alias("last_fill"),
            )
            .with_columns(
                ((pl.col("financeiro") / pl.col("filled")).round(4)).alias(
                    "average_price"
                ),
                pl.lit(False).alias("azimut"),
            )
            .select(pl.exclude(("financeiro")))
            .sort(by=["side", "ticker", "broker"])
        )


def obtain_fills_solutions():
    """Para ser chamado a cada x segundos, basta colocar o _Fills() no while"""
    m = _Main()
    fills = _Fills(m.controller, m.today, m.brokers)
    global a
    a = fills
    return fills.df


if __name__ == "__main__":
    print(obtain_fills_solutions())


#COLUMNS = [
#    "symbol",
#    'account',
#    'execBroker',
#    "side",
#    "transactTime",
#    "price",
#    "qty",
#]
#pl.DataFrame(a.controller.get_trades()).select(pl.col(COLUMNS)).filter(pl.col("symbol") == "BBAS3")
