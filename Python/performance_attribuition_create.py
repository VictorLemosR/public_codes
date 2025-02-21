# Implementar read_only aossalvar
import os

import datetime
import polars as pl
import xlsxwriter


class Main:
    def __init__(self, year=datetime.datetime.now().year) -> None:
        self.dataframes = Parquet_reader(year).dataframes
        Printer(self.dataframes, year)


class Parquet_reader:
    GROUP_FUNDS = {"tr cl": "tr", "top cl": "top"}

    def __init__(self, year) -> None:
        self.obtain_folders(year)
        self.obtain_parquets()
        # self.update_security_info()

    def obtain_folders(self, year):
        BACKUP_FOLDER = (
            os.environ["onedrive"] + rf"\Trading\files_daily\backup\{year}"
        )
        self.FOLDER_BASE = BACKUP_FOLDER + r"\base"
        self.FOLDER_FUNDS = BACKUP_FOLDER + r"\data_funds"

    def obtain_parquets(self):
        queries_base = []
        entries = os.scandir(self.FOLDER_BASE)
        for entry in entries:
            date = entry.name[5:13]
            print(entry.name)
            path_base = self.FOLDER_BASE + "\\base_" + date + ".parquet"
            path_funds = self.FOLDER_FUNDS + "\\funds_" + date + ".parquet"

            query_base = Base(path_base, date).query_base
            query_funds = Funds().treat_funds(path_funds, date)

            query_base = (
                query_base.join(
                    query_funds,
                    on=["fund", "date"],
                    how="left",  # coalesce=False
                ).with_columns(
                    pl.col("fund_nickname")
                    .replace(self.GROUP_FUNDS)
                    .alias("fund_nickname")
                )
                # .collect()
            )
            queries_base.append(query_base)
        # self.dataframes = pl.concat(queries_base)
        collected_bases = pl.collect_all(queries_base)
        self.dataframes = pl.concat(collected_bases)

    def update_security_info(self):
        self.dataframes = self.dataframes.sort(by="date", descending=True).with_columns(
            pl.col(["country", "sector", "strategy", "ticker", "size"])
            .first()
            .over(pl.col("ticker_old"))
        )


class Base:
    COLUMNS_BASE = [
        # initial parameters
        "fund",
        "ticker",
        "quantity",
        "strategy_book",
        "f_global",
        # fixed parameters
        "size",
        "country",
        "sector",
        "strategy",
        "ticker_old",
        "fund_strategy",
        "fx",
        # variables
        "price_current_brl",
        "price_close_yesterday_brl",
        "dividend",
        "1d_change",
        "position_current",
        "position_initial",
        "weight_index_cur",
        "weight_index_ini",
        "1d_bench",
        "alpha",
        "selection",
        "return",
        "return_trade",
    ]

    def __init__(self, path, date) -> None:
        self.path = path
        self.date = date
        self.treat_base()

    def treat_base(self):
        query_base = pl.scan_parquet(self.path)
        self.query_base = (
            query_base.select(pl.col(self.COLUMNS_BASE))
            .filter(~pl.col("strategy_book").str.contains("CORE_RATES_CASH"))
            .with_columns(
                pl.lit(self.date).str.strptime(pl.Date, "%Y%m%d").alias("date"),
                pl.col(pl.Utf8).str.to_lowercase(),
            )
        )

    def join_all_bases(self):
        pass


class Funds:
    COLUMNS_FUNDS = [
        "fund",
        "fund_nickname",
        "portfolio_return_ytd",
        "pnl_cash",
        "portfolio_return",
        "pnl_trades",
        "aum_initial",
        "aum_current",
    ]

    def __init__(self) -> None:
        pass

    def treat_funds(self, path, date):
        query_funds = pl.scan_parquet(path)

        query_funds = query_funds.select(pl.col(self.COLUMNS_FUNDS)).with_columns(
            pl.lit(date).str.strptime(pl.Date, "%Y%m%d").alias("date"),
            pl.col("pnl_trades").cast(pl.Float64),
        )
        if query_funds.select(pl.col("portfolio_return")).dtypes[0] == pl.String:
            query_funds = query_funds.with_columns(
                pl.col("portfolio_return").str.replace("#DIV/0!", "0").cast(pl.Float64),
            )
        else:
            query_funds = query_funds.with_columns(
                pl.col("portfolio_return").cast(pl.Float64),
                pl.col(pl.Utf8).str.to_lowercase(),
            )

        return query_funds


class Printer:
    FUNDS = ["tr", "top", "small", "fia", "trend"]
    MONHTS_RENAME = {
        "1": "Jan",
        "2": "Feb",
        "3": "Mar",
        "4": "Apr",
        "5": "May",
        "6": "Jun",
        "7": "Jul",
        "8": "Aug",
        "9": "Sep",
        "10": "Oct",
        "11": "Nov",
        "12": "Dec",
    }

    def __init__(self, df: pl.DataFrame, year) -> None:
        self.year = year
        self.df = df
        self.treat_base()
        global a
        a = self.df
        self.print_base()
        print("Base printado")
        self.print_returns()
        self.print_alpha()
        self.print_selection()

    def treat_base(self):
        self.df = (
            self.df.filter(pl.col("ticker") != "cdi index")
            .sort(by="date")
            .with_columns(
                pl.col("date").dt.strftime("%m").cast(pl.Int32).alias("month"),
            )
        )

    def print_base(self):
        self.highest_month = self.df.select(pl.col("month").max())[0, 0]
        keys_to_remove = []
        for key in self.MONHTS_RENAME.keys():
            if int(key) > self.highest_month:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            self.MONHTS_RENAME.pop(key)

        explanation_df = self.build_explanation()
        returns_df, returns_sector = self.build_performance_item("return")
        returns_lines = returns_sector.shape[0] + 3
        alpha_df, alpha_sector = self.build_performance_item("alpha")
        alpha_lines = alpha_sector.shape[0] + 3
        selection_df, selection_sector = self.build_performance_item("selection")
        selection_lines = selection_sector.shape[0] + 3

        with xlsxwriter.Workbook(
            os.environ["onedrive"] + r"\Portfolio Overview\Performance attribution\Perfomance_attribution.xlsx"
        ) as workbook:
            print("Printando primeira parte lenta")
            self.df.write_excel(workbook=workbook, worksheet="base", autofit=True)
            explanation_df.write_excel(
                workbook=workbook, worksheet="explanation", autofit=True
            )
            print("Printando segunda parte lenta")
            returns_sector.write_excel(
                workbook=workbook, worksheet="returns", autofit=True
            )
            returns_df.write_excel(
                workbook=workbook,
                worksheet="returns",
                autofit=True,
                position=(returns_lines, 0),
            )

            alpha_sector.write_excel(workbook=workbook, worksheet="alpha", autofit=True)
            alpha_df.write_excel(
                workbook=workbook,
                worksheet="alpha",
                autofit=True,
                position=(alpha_lines, 0),
            )

            selection_sector.write_excel(
                workbook=workbook, worksheet="selection", autofit=True
            )
            selection_df.write_excel(
                workbook=workbook,
                worksheet="selection",
                autofit=True,
                position=(selection_lines, 0),
            )

            workbook.read_only_recommended()

    def build_explanation(self):
        explanation = pl.DataFrame(
            {
                "attribute": ["return", "alpha", "selection"],
                "formula": [
                    "peso_ticker*1d_change",
                    "under_over*1d_change",
                    "1d_change_ticker(pos_i_fundo - exposition_fundo*pos_i_bench)",
                ],
                "description": [
                    "Retorno do papel - Para o top e o tr, ativos us e bdr são mostrados o retorno com hedge. Para o latam e o trend, não há hedge (variação cambial tem efeito)",
                    "Performance do papel. Da mesma forma acima, efeito cambial igual ao retorno, sem efeito no top e tr e efeito no latam e trend",
                    ".",
                ],
            }
        )

        return explanation

    def build_performance_item(self, column):
        item_df = self.df.group_by(["fund_nickname", "ticker", "month"]).agg(
            pl.col(column).sum().alias("summed_value"),
            pl.col("sector").last().alias("sector"),
        )

        total_columns = []
        for column in range(1, self.highest_month + 1):
            total_columns.append(str(column))
        if self.highest_month < 6:
            total_operations = pl.sum_horizontal(pl.col(total_columns)).alias("total")
            columns_select = ["fund_nickname", "sector", "total"]
        else:
            semester_columns = []
            for column in range(7, self.highest_month + 1):
                semester_columns.append(str(column))
            total_operations = (
                pl.sum_horizontal(pl.col(total_columns)).alias("total"),
                pl.sum_horizontal(pl.col(semester_columns)).alias("semester"),
            )
            columns_select = ["fund_nickname", "sector", "total", "semester"]

        sector_df = (
            item_df.group_by(["fund_nickname", "sector", "month"])
            .agg(
                pl.col("summed_value").sum().alias("summed_value"),
            )
            .sort(by="month", descending=True)
            .pivot(
                on="month",
                index=["fund_nickname", "sector"],
                values="summed_value",
            )
            .with_columns(total_operations)
            .select(
                pl.col(columns_select),
                pl.exclude(columns_select),
            )
            .filter(pl.col("total") != 0)
            .sort(
                by=["fund_nickname", "sector", "total"], descending=[False, False, True]
            )
            .rename(self.MONHTS_RENAME)
        )
        columns_select.insert(2, "ticker")

        item_df = (
            item_df.sort(by="month", descending=True)
            .pivot(
                on="month",
                index=["fund_nickname", "sector", "ticker"],
                values="summed_value",
            )
            .with_columns(total_operations)
            .select(
                pl.col(columns_select),
                pl.exclude(columns_select),
            )
            .filter(pl.col("total") != 0)
            .sort(
                by=["fund_nickname", "sector", "total"], descending=[False, False, True]
            )
            .rename(self.MONHTS_RENAME)
        )

        return item_df, sector_df

    def attribute_per_fund(self, column_agg):
        COLUMNS_SELECT = ["country", "sector", "ticker", "total"]
        fund_returns = (
            self.df.filter(pl.col(column_agg) != 0)
            .sort(by="date", descending=True)
            .group_by(["country", "sector", "ticker", "month", "fund_nickname"])
            .agg(pl.col(column_agg).sum().alias("summed_value"))
        )
        total_columns = []
        for column in range(1, self.highest_month + 1):
            total_columns.append(str(column))
        if self.highest_month < 6:
            total_operations = pl.sum_horizontal(pl.col(total_columns)).alias("total")
        else:
            semester_columns = []
            for column in range(7, self.highest_month + 1):
                semester_columns.append(str(column))
            total_operations = (
                pl.sum_horizontal(pl.col(total_columns)).alias("total"),
                pl.sum_horizontal(pl.col(semester_columns)).alias("semester"),
            )
            COLUMNS_SELECT.append("semester")

        returns_list = []
        for fund in self.FUNDS:
            fund = fund_returns.filter(pl.col("fund_nickname") == fund)
            fund = (
                fund.sort(by="month", descending=True)
                .pivot(
                    on="month",
                    index=["country", "sector", "ticker"],
                    values="summed_value",
                )
                .with_columns(total_operations)
                .sort(by="total", descending=True)
                .select(
                    pl.col(COLUMNS_SELECT),
                    pl.exclude(COLUMNS_SELECT),
                )
                .rename(self.MONHTS_RENAME)
            )
            returns_list.append(fund)

        return returns_list

    def print_returns(self):
        funds_returns = self.attribute_per_fund("return")
        with xlsxwriter.Workbook(
            os.environ["onedrive"] + rf"\Portfolio Overview\Performance attribution\Retorno_por_fundo_{self.year}.xlsx"
        ) as workbook:
            for index in range(0, len(self.FUNDS)):
                fund_df = funds_returns[index]
                fund_name = self.FUNDS[index]
                fund_df.write_excel(
                    workbook=workbook, worksheet=fund_name, autofit=True
                )

    def print_alpha(self):
        funds_alpha = self.attribute_per_fund("alpha")
        with xlsxwriter.Workbook(
            os.environ["onedrive"] + rf"\Portfolio Overview\Performance attribution\Alpha_por_fundo_{self.year}.xlsx"
        ) as workbook:
            for index in range(0, len(self.FUNDS)):
                fund_df = funds_alpha[index]
                fund_name = self.FUNDS[index]
                fund_df.write_excel(
                    workbook=workbook, worksheet=fund_name, autofit=True
                )

    def print_selection(self):
        funds_selection = self.attribute_per_fund("selection")
        with xlsxwriter.Workbook(
            os.environ["onedrive"] + rf"\Portfolio Overview\Performance attribution\Selection_por_fundo_{self.year}.xlsx"
        ) as workbook:
            for index in range(0, len(self.FUNDS)):
                fund_df = funds_selection[index]
                fund_name = self.FUNDS[index]
                fund_df.write_excel(
                    workbook=workbook, worksheet=fund_name, autofit=True
                )


if __name__ == "__main__":
    year = datetime.datetime.now().year
    m = Main(year)
    # m = Main(2024)

# m.dataframes.write_excel(r"C:\Users\victor.reial\OneDrive - QUEST INVESTIMENTOS LTDA\Trading\Gestão\Performance_attribution.xlsx")
# pl.read_parquet(r'C:\Users\bloomberg1\OneDrive - QUEST INVESTIMENTOS LTDA\Trading\files_daily\2024\Base\base_20240104.parquet').select(pl.col('parent_strategy'))

##Analisar inconsistências entre portfolio_return e soma dos returns
# a.columns
# b = (
#   a.with_columns(
#       pl.when(pl.col("fund").str.contains(" CL"))
#       .then(999999)
#       .otherwise(pl.col("portfolio_return"))
#       .alias("portfolio_return")
#   )
#   .group_by(pl.col(["date", "fund_nickname"]))
#   .agg(pl.col("return").sum(), pl.col("portfolio_return").min() * 10000)
#   .with_columns(
#       (pl.col("return") - pl.col("portfolio_return")).alias("diff"),
#       (pl.col("return") / pl.col("portfolio_return")).alias("ratio"),
#   )
#   .filter(
#       (pl.col("diff").abs() > 2)
#       & ~(pl.col("fund_nickname").str.contains("_INDEX"))
#       & (pl.col("fund_nickname").str.contains("TOP$"))
#   )
#   .sort(pl.col("diff"))
# )
# b

# Calcular a diferença se tudo tivesse sido convertido para DOL


def adicionar_efeito_hedge_azimut():
    from xbbg import blp

    moedas_pandas = blp.bdh(
        ["usdmxn curncy", "usdclp curncy", "usdcop curncy"],
        "chg_pct_1d",
        "20240102",
        "20241212",
    )

    moedas = pl.from_pandas(moedas_pandas.reset_index(names="date"))
    moedas = moedas.rename(
        {
            "('date', '')": "date",
            "('usdcop curncy', 'chg_pct_1d')": "cop",
            "('usdclp curncy', 'chg_pct_1d')": "clp",
            "('usdmxn curncy', 'chg_pct_1d')": "mxn",
        }
    )
    moedas = moedas.unpivot(
        index="date", variable_name="fx", value_name="1d_change_fx"
    ).with_columns(pl.col("1d_change_fx") / 100)
    moedas

    change_dol = (
        a.filter(
            (
                (pl.col("ticker").str.contains("WDO"))
                | (pl.col("ticker").str.contains("DOL"))
            )
            & (pl.col("fund_nickname").str.contains("^TOP$"))
        )
        .select(
            pl.col("date"),
            pl.lit("brl").alias("fx"),
            (
                (pl.col("price_current_brl") / pl.col("price_close_yesterday_brl")) - 1
            ).alias("1d_change_fx"),
        )
        .unique("date")
    )
    moedas = pl.concat([moedas, change_dol])

    b = (
        a.select(
            pl.col(
                [
                    "date",
                    "ticker",
                    "1d_change",
                    "fx",
                    "fund_nickname",
                    "position_initial",
                    "return",
                    "return_trade",
                    "month",
                ]
            )
        )
        .filter(pl.col("fund_nickname").str.contains("^LATAM$|^TREND$"))
        .with_columns(
            pl.col("fx").replace(
                ["CLPBRL", "BRL", "USD", "MXNBRL", "COPBRL"],
                ["clp", "brl", "usd", "mxn", "cop"],
            )
        )
        .join(moedas, on=["fx", "date"], how="left")
    )

    print(
        "Moedas que nao possuem valor em algum dia",
        b.filter(pl.col("1d_change_fx").is_null()).select(pl.col("fx")).unique(),
    )

    b = (
        b.with_columns(pl.col("1d_change_fx").fill_null(0))
        .with_columns(
            ((1 + pl.col("1d_change")) / (1 + pl.col("1d_change_fx")) - 1).alias(
                "1d_change_dolarizado"
            )
        )
        .with_columns(
            (
                pl.col("1d_change") * pl.col("position_initial")
                + pl.col("return_trade")
            ).alias("return_com_hedge"),
            (
                pl.col("1d_change_dolarizado") * pl.col("position_initial")
                + pl.col("return_trade")
            ).alias("return_dolarizado"),
        )
    )
    c = (
        b.group_by(["fund_nickname", "month"])
        .agg(
            pl.col("return_com_hedge").sum() * 10000,
            pl.col("return_dolarizado").sum() * 10000,
        )
        .sort(by=["fund_nickname", "month"])
        .with_columns(
            (pl.col("return_com_hedge") - pl.col("return_dolarizado")).alias(
                "dif_hedge"
            )
        )
    )
    print(c)

    c = (
        b.group_by(["fund_nickname", "fx"])
        .agg(
            pl.col("return_com_hedge").sum() * 10000,
            pl.col("return_dolarizado").sum() * 10000,
        )
        .filter(pl.col("fx").str.contains("brl|mxn|clp|usd"))
        .sort(by=["fund_nickname", "fx"])
        .with_columns(
            (pl.col("return_com_hedge") - pl.col("return_dolarizado")).alias(
                "dif_hedge"
            )
        )
        .with_columns(
            pl.when(pl.col("dif_hedge").abs() < 0.0001)
            .then(0)
            .otherwise(pl.col("dif_hedge"))
            .alias("dif_hedge")
        )
    )
    print(c)

    c = (
        b.group_by(["fund_nickname"])
        .agg(
            pl.col("return_com_hedge").sum() * 10000,
            pl.col("return_dolarizado").sum() * 10000,
        )
        .with_columns(
            (pl.col("return_com_hedge") - pl.col("return_dolarizado")).alias(
                "dif_hedge"
            )
        )
    )
    print(c)
