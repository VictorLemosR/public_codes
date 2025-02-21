import requests
import polars as pl

class Cvm_from_folder():
    
    FILE_PATH = r"T:\Mesa Operacoes\Credito\Narizinho\Rotinas - arquivos\CVM - cadfi\cad_fi.feather"
    
    def __init__(self):
        self.read_file()
        
    def read_file(self):
        self.df_funds = pl.read_ipc(self.FILE_PATH)



class Cvm_from_internet():
    
    def __init__(self):
        print("\n\n\nBaixando o arquivo, isso pode demorar alguns segundos.")
        self.get_data()
        self.convert_to_polars()
        
    def get_data(self):
        h = {"User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
     + "Chrome/108.0.0.0 Safari/537.36", "DNT": "1", "Connection":"keep-alive", "Upgrade-Insecure-Requests": "1"}
        self.csv_file = requests.get("https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv", headers=h)
        
    def convert_to_polars(self):
        self.df_funds = pl.read_csv(self.csv_file.content, separator=";", encoding="latin-1")



class Df_operations():
    
    def __init__(self, df):
        self.df_unformatted = df
        self.filter_rows()
        self.adjust_columns()
        self.create_aum_managers()
        self.add_high_alpha()
        self.create_rank()
        self.format_aum_as_string()
        
    def filter_rows(self):
        self.df_unformatted = self.df_unformatted.filter(
                                    (~pl.col("SIT").is_in(["CANCELADA", "LIQUIDAÇÂO"]))
                                    & (pl.col("FUNDO_COTAS") != "S")
                                    & (~pl.col("DENOM_SOCIAL").str.contains("QUOTAS|COTAS|FOF|FIC|FUNDS OF FUNDS"))
                                    & (~pl.col("GESTOR").is_null())
                                    & (~pl.col("VL_PATRIM_LIQ").is_null())
                                )
        
    def adjust_columns(self):
        final_columns = ["GESTOR", "DENOM_SOCIAL", "VL_PATRIM_LIQ"]
        rename = ["gestor", "fundo", "aum"]
        
        rename_dict = {}
        for index in range(0,len(final_columns)):
            rename_dict[final_columns[index]] = rename[index]

        self.df_unformatted = (self.df_unformatted.select(pl.col(final_columns)).rename(rename_dict))
        
    def create_aum_managers(self):
        self.aum_managers = (self.df_unformatted.group_by("gestor")
                                    .agg(pl.col("aum").sum()))
        
    def add_high_alpha(self):
        high_alpha = self.df_unformatted.filter(
            pl.col("fundo").str.contains("HEDGE PLUS")
            & (pl.col("fundo").str.contains("ITA"))  
        ).drop("fundo")
        
#        if high_alpha.shape[0] > 1:
#            raise Exception("Mais de 1 fundo encontrado para o HIGH ALPHA.")
#        elif high_alpha.shape[0] < 1:
#            raise Exception("Nenhum fundo encontrado para o HIGH ALPHA.")
        
        high_alpha[0,0] = "ITAÚ HIGH ALPHA"
        self.aum_managers = pl.concat([self.aum_managers, high_alpha]).sort(by=pl.col("aum"), descending=True)

    def create_rank(self):
        self.aum_managers = self.aum_managers.with_columns(
            pl.col("gestor").str.to_uppercase(),                
            pl.lit("#").alias("rank")
            + pl.col("aum").rank("ordinal", descending=True).alias("rank").cast(pl.Utf8)
        )
    
    def format_aum_as_string(self):
        self.aum_managers = self.aum_managers.with_columns(
                                pl.when(pl.col("aum") >= 1e9)
                                .then(pl.format("{} bi", (pl.col("aum")/1e9).round(2)))
                                .otherwise(pl.format("{} mi", (pl.col("aum")/1e6).round(1)))
                                )



class Find_managers():
    
    def __init__(self, df):
        self.aum_managers = df
        self.get_manager()
    
    def get_manager(self):
        manager = input()
        while manager != "":
            manager = manager.upper()
            self.print_table(manager)
            print("\n\nDigite outra gestora para procurar ou aperte enter para finalizar.\n\n")
            manager = input()
            
    def print_table(self, manager_name):
        print_all = (manager_name in ["TODAS", "TODOS", "TODES", "T"])
        if print_all:
            managers_string = self.aum_managers[::-1].to_pandas().to_string(index=False)
            print("\n" + managers_string)
            return
        
        managers_filtered = self.aum_managers.filter(pl.col("gestor").str.contains(manager_name))
        if managers_filtered.is_empty():
            print("\n\nNENHUM gestor encontrado. Lembre-se que a pesquisa requer acentos")
        else:
            managers_filtered_string = managers_filtered.to_pandas().to_string(index=False)
            print("\n" + managers_filtered_string)



#df_cvm.df_funds.filter(pl.col("DENOM_SOCIAL").str.contains("AUGME"))

#df_cvm.df_funds.filter(pl.col("DENOM_SOCIAL").str.contains("PANA"))



if __name__ == "__main__":
    #df_cvm = Cvm_from_folder()
    df_cvm = Cvm_from_internet()
    df_mm = df_cvm.df_funds.filter(pl.col("CLASSE").is_in(["Fundo de Ações", "Fundo Multimercado"]))
    
    df_organized = Df_operations(df_cvm.df_funds)
    df_organized_mm = Df_operations(df_mm)
    
    df = df_organized.aum_managers.join(df_organized_mm.aum_managers, how='left', on='gestor', suffix="_ações", coalesce=False)
    
    len_cut = 80
    df = df.with_columns(
        pl.when(pl.col("gestor").str.len_chars() > len_cut)
        .then(pl.col("gestor").str.slice(0, length=len_cut))
        .otherwise(pl.col("gestor"))
        .alias("gestor")
    )
    print("Arquivo pronto. Por qual gestora você procura?\nLembre-se de colocar acento.\n'todas' ou 't' também é uma opção\n")
    Find_managers(df)
