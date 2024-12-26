import pandas as pd
from typing import List
import sys

result_columns = [
    "COD_EMPRESA",
    "COD_TIPO_CONTABIL",
    "NUM_GUIA",
    "COD_SIS",
    "COD_FILIAL",
    "COD_CONTA_CONTABIL",
    "ID_CENTRO_CUSTO",
    "COD_PROJETO",
    "DT_LANC_CONTABIL",
    "TIPO_LANC",
    "COD_HIST_PADRAO",
    "REFERENCIA",
    "DT_CONVERSAO",
    "VLR",
    "COMPLEMENTO",
    "HIST",
    "COD_CONTA_CONTRA",
    "ID_CCUSTO_CONTRA",
    "COD_CENTRO_CUSTO",
    "COD_CENTRO_CUSTO_CONTRA",
    "COD_CONTA_REDUZIDA",
    "COD_CONTA_REDUZIDA_CONTRA",
    "GRUPO_LANC",
    "CONTRAPARTE",
    "DT_LANC_EXTEMPORANEO",
    "RATEIOS",
]

def tweak_accounts(df: pd.DataFrame) -> pd.DataFrame:
    """Tweak the accounts DataFrame to standardize column names and types."""
    accounts_columns = ["Cód Conta", "PLANO2025"]

    df = df.loc[:, accounts_columns].copy()
    df[accounts_columns] = df[accounts_columns].astype("Int64")

    df = df.rename(
        columns={
            "Cód Conta": "conta_sinqia",
            "PLANO2025": "conta_matera",
        }
    ).sort_values("conta_sinqia")

    return df


def transform_movements(mov_df: pd.DataFrame, accounts_df: pd.DataFrame) -> pd.DataFrame:
    """Transform movements DataFrame by merging with accounts DataFrame."""
    transformed_df = (
        mov_df.merge(accounts_df, left_on="Cta. débito", right_on="conta_sinqia", how="left")
        .rename(columns={"conta_matera": "Cta. Débito Matera"})
        .drop(columns="conta_sinqia")
        .merge(accounts_df, left_on="Cta. crédito", right_on="conta_sinqia", how="left")
        .rename(columns={"conta_matera": "Cta. Crédito Matera"})
        .drop(columns="conta_sinqia")
        .loc[:, ["Cta. Débito Matera", "Cta. Crédito Matera", "Data  de movimento", "Vlr. lança."]]
    )

    return transformed_df


def prepare_transaction_dataframe(mov_df: pd.DataFrame) -> pd.DataFrame:
    """Prepare a DataFrame for transactions by separating debits and credits."""
    debit_df = mov_df[["Cta. Débito Matera", "Data  de movimento", "Vlr. lança."]].rename(
        columns={"Cta. Débito Matera": "cta"}
    )

    debit_df["lcto"] = "D"

    credit_df = mov_df[["Cta. Crédito Matera", "Data  de movimento", "Vlr. lança."]].rename(
        columns={"Cta. Crédito Matera": "cta"}
    )

    credit_df["lcto"] = "C"

    result_df = pd.concat([debit_df, credit_df], ignore_index=True).sort_values(
        by=["Vlr. lança.", "lcto"], ascending=[True, False], ignore_index=True
    )

    return result_df


def add_and_populate_columns(df: pd.DataFrame, column_names: List[str]) -> pd.DataFrame:
    """Add and populate specified columns in the DataFrame."""

    column_mapping = {
        "COD_CONTA_CONTABIL": "cta",
        "DT_LANC_CONTABIL": "Data  de movimento",
        "TIPO_LANC": "lcto",
        "VLR": "Vlr. lança.",
    }

    for column in column_names:
        if column in column_mapping:
            source_column = column_mapping[column]
            df[column] = df[source_column] if source_column in df.columns else pd.NA
        else:
            df[column] = pd.NA

    ordered_df = df.loc[:, column_names].copy()

    return ordered_df

def main(file_path: str) -> None:
    """Main function to execute the data processing pipeline."""

    accounts = pd.read_csv("input/accounts_sinqia_matera.csv")

    # Uncomment if you want to tweak accounts
    # accounts = tweak_accounts(accounts)

    initial_df = pd.read_excel(f"input/{file_path}")

    transformed_df = transform_movements(initial_df, accounts)

    transformed_df = prepare_transaction_dataframe(transformed_df)

    result_df = add_and_populate_columns(transformed_df, result_columns)

    result_df.to_csv("output/resultado_esperado.csv", index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_excel_file>")
        sys.exit(1)

    excel_file_path = sys.argv[1]

    main(excel_file_path)
