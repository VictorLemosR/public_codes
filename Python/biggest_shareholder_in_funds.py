import polars as pl


class Main:
    def __init__(self) -> None:
        self.w = Workbooks()
        self.d = Dataframe_operations(self.w.df)


class Workbooks:
    """Utilizo dois arquivos que podem ser baixados via links abaixo. Procurar o mais
    recente para o link 2 e extrair o arquivo 'cda_fi_BLC_2.csv', que é o csv que possui
    os fundos de investimento em outros fundos:
        1. https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv
        2. https://dados.cvm.gov.br/dados/FI/DOC/CDA/DADOS/"""

    #
    PATH_INPUTS = r"M:\BOLSA\Victor\Codes\Shareholder_funds\Inputs"
    FUNDS_INFO = "cad_fi.csv"
    FUNDS_ALLOCATIONS = "cda_fi_BLC_2_202403.csv"
    COLUMNS_INFO = {
        "CNPJ_FUNDO": "fund_cnpj",
        "DENOM_SOCIAL": "fund_name",
        "SIT": "sit",
        "VL_PATRIM_LIQ": "aum",
        "RENTAB_FUNDO": "benchmark",
        "GESTOR": "manager",
        "CLASSE_ANBIMA": "class",
        "CLASSE": "class2",
    }
    COLUMNS_ALLOCATIONS = {
        "CNPJ_FUNDO": "investing_fund_cnpj",
        "DENOM_SOCIAL": "investing_fund_name",
        "VL_MERC_POS_FINAL": "allocated_aum",
        "CNPJ_FUNDO_COTA": "invested_fund_cnpj",
        "NM_FUNDO_COTA": "invested_fund_name",
    }
    REARRANGED_COLUMNS = [
        "investing_fund_name",
        "allocated_aum",
        "investing_manager",
        "invested_fund_name",
        "invested_manager",
        "invested_class",
        "invested_aum",
        "invested_class2",
        "invested_benchmark",
    ]

    def __init__(self) -> None:
        self.open_workbooks()
        self.curate_info()
        self.merge_info()
        self.rearrange_columns()

    def open_workbooks(self):
        self.df_info = pl.read_csv(
            self.PATH_INPUTS + "\\" + self.FUNDS_INFO,
            separator=";",
            encoding="latin-1",
            quote_char=None,
        )
        self.df_allocations = pl.read_csv(
            self.PATH_INPUTS + "\\" + self.FUNDS_ALLOCATIONS,
            separator=";",
            encoding="latin-1",
        )

    def curate_info(self):
        self.df_info = (
            self.df_info.select(self.COLUMNS_INFO.keys())
            .rename(self.COLUMNS_INFO)
            .filter(~pl.col("sit").str.contains("CANCELADA"))
        )
        self.df_allocations = self.df_allocations.select(
            self.COLUMNS_ALLOCATIONS.keys()
        ).rename(self.COLUMNS_ALLOCATIONS)

    def merge_info(self):
        self.df = self.df_allocations.join(
            self.df_info.select(pl.col(["fund_cnpj", "class", "aum", "manager"])),
            how="left",coalesce=False,
            left_on="investing_fund_cnpj",
            right_on="fund_cnpj",
        )
        dict_rename = {}
        for column in ["class", "aum", "manager"]:
            dict_rename[column] = "investing_" + column

        self.df = self.df.rename(dict_rename)

        self.df = self.df.join(
            self.df_info.select(
                pl.col(["fund_cnpj", "class", "aum", "manager", "class2", "benchmark"])
            ),
            how="left",coalesce=False,
            left_on="invested_fund_cnpj",
            right_on="fund_cnpj",
        )
        dict_rename = {}
        for column in ["class", "aum", "manager", "class2", "benchmark"]:
            dict_rename[column] = "invested_" + column

        self.df = self.df.rename(dict_rename)

    def rearrange_columns(self):
        self.df = self.df.select(self.REARRANGED_COLUMNS)


class Dataframe_operations:
    CHOSEN_CLASS = "^$|Ações|Ação|Multimercados Livre|Multimercados L/S|Multimercado"
    COLUMNS_ORDER = [
        "investing_manager",
        "invested_manager",
        "allocated_aum",
        "invested_fund_name",
        "invested_aum",
        "invested_class",
        "invested_benchmark",
    ]

    def __init__(self, df) -> None:
        self.df = df
        self.filter_relevant_allocations()
        self.aggregate_investors()
        self.print_info()

    def filter_relevant_allocations(self):
        self.df = self.df.filter(
            pl.col("invested_class").str.contains(self.CHOSEN_CLASS),
            ~pl.col("invested_fund_name").str.contains("[cC][rR][eEéÉ][dD][iI][tT]"),
            pl.col("invested_benchmark").str.contains(
                "OUTROS|Não se aplica|Ibovespa|IBrX|DI de um"
            ),
            pl.col("investing_manager").str.split(" ").list.get(0)
            != pl.col("invested_fund_name").str.split(" ").list.get(0),
            #pl.col("allocated_aum") > 1e7,
        ).filter(~pl.col("invested_class").str.contains("Exterior|Sustentab|Mono"))

        filter_by_allocated_aum = (
            self.df.group_by("invested_fund_name")
            .agg(pl.col("allocated_aum").sum())
            #.filter(pl.col("allocated_aum") > 1e7)
            .select(pl.col("invested_fund_name"))
        )
        self.df = self.df.join(
            filter_by_allocated_aum, how="inner", on="invested_fund_name"
        )

    def aggregate_investors(self):
        self.df_aggregated_managers = (
            (
                self.df.group_by(["investing_manager", "invested_fund_name"])
                .agg(
                    pl.col("invested_manager").first(),
                    pl.col("allocated_aum").sum(),
                    pl.col("invested_aum").first(),
                    pl.col("invested_class").first(),
                    pl.col("invested_benchmark").first(),
                )
                .sort(by="allocated_aum", descending=True)
            )
            .select(self.COLUMNS_ORDER)
            .sort(by=["invested_manager", "allocated_aum"], descending=[False,True])
        )

    def print_info(self):
        self.df.write_excel(r"M:\BOLSA\Victor\Codes\Shareholder_funds\dados.xlsx")
        self.df_aggregated_managers.write_excel(
            r"M:\BOLSA\Victor\Codes\Shareholder_funds\Alocadores de fundos.xlsx"
        )


m = Main()
