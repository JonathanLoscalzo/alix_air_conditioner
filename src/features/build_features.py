import warnings
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import log_loss
from sklearn.model_selection import train_test_split
import numpy as np


def add_has_contract(df):
    warnings.warn("Sales_Contract_No: data-leakage feature")
    df.loc[:, "has_contract"] = (~df.Sales_Contract_No.isna()).astype("int")
    return df.drop(columns="Sales_Contract_No")


def __calc_asp_imputer(df):
    asp_imputer = (
        df[(df.ASP > 0)]
        .groupby(
            [
                df["Last_Modified_Date"].dt.year * 100
                + df["Last_Modified_Date"].dt.month,
                "ASP_Currency",
            ]
        )
        .agg({"ASP_(converted)": ["mean"], "ASP": ["mean"]})
    )
    asp_imputer.loc[:, "rate"] = asp_imputer.iloc[:, 1] / asp_imputer.iloc[:, 0]
    return asp_imputer


def impute_rate(df, imputer=None):
    asp_imputer = __calc_asp_imputer(df) if imputer is None else imputer
    df.loc[:, "LMP"] = (
        df["Last_Modified_Date"].dt.year * 100 + df["Last_Modified_Date"].dt.month
    )
    df = df.merge(
        asp_imputer["rate"],
        left_on=["LMP", "ASP_Currency"],
        right_index=True,
        how="left",
    )

    df.loc[df.rate.isna(), "rate"] = (
        df.loc[df.rate.isna(), "Total_Amount_Currency"] == "USD"
    ).astype("int")
    df["ASP_was_converted"] = (
        df["rate"] != 1
    )  # todos los no convertidos son dolares # df["ASP"] != df["ASP_(converted)"]

    return (
        df.drop(
            columns=[
                "LMP",
                "ASP",
                "ASP_Currency",
                "ASP_(converted)",
                "ASP_(converted)_Currency",
            ]
        ),
        asp_imputer,
    )


def filter_stages(df, isin=["Closed Lost", "Closed Won", "None"]):
    return df[df.Stage.isin(isin)]


def impute_total_amount(df):
    df["Total_Amount_Imputed"] = -1  # posibles valores; -1, 0, 1.
    df = __impute_total_amount_by_near_date(df)
    df = __impute_total_amount_by_currency_and_product(df)
    return df


def __impute_total_amount_by_currency_and_product(df_train):
    mask = df_train.Total_Amount.isna()  # | (df_train.Total_Amount == 0)

    df_with_total = df_train[~mask]

    for_impute_total_amount = (
        df_with_total.groupby(["Total_Amount_Currency", "Product_Name"])
        .agg({"Total_Amount": ["mean", "std"]})
        .reset_index()
    )

    to_impute = (
        df_train.loc[mask, ["Total_Amount_Currency", "Product_Name"]]
        .merge(
            for_impute_total_amount,
            on=["Total_Amount_Currency", "Product_Name"],
            how="left",
        )
        .iloc[:, 2]
    )

    df_train.loc[mask, "Total_Amount_Imputed"] = (
        pd.Series(to_impute.values).notna().astype("int").values
    )
    df_train.loc[mask, "Total_Amount"] = to_impute.values

    return df_train


def __impute_total_amount_by_near_date(df_train):

    mask = df_train.Total_Amount.isna()  # | (df_train.Total_Amount == 0)

    df_with_total = df_train[~mask]

    for_impute_total_amount = (
        df_with_total.groupby(
            [
                "Total_Amount_Currency",
                "Product_Name",
                df_with_total.Last_Modified_Date.dt.year * 100
                + df_with_total.Last_Modified_Date.dt.month,
            ]
        )
        .agg({"Total_Amount": ["mean", "std"]})
        .reset_index()
        .sort_values(by="Last_Modified_Date")
    )

    to_impute = df_train.loc[
        mask, ["Total_Amount_Currency", "Product_Name", "Last_Modified_Date"]
    ]
    to_impute["Last_Modified_Date"] = (
        to_impute.Last_Modified_Date.dt.year * 100
        + to_impute.Last_Modified_Date.dt.month
    )
    to_impute = to_impute.sort_values(by="Last_Modified_Date")

    to_impute = pd.merge_asof(
        to_impute,
        for_impute_total_amount,
        on=["Last_Modified_Date"],
        by=["Total_Amount_Currency", "Product_Name"],
    ).iloc[:, 3]

    df_train.loc[mask, "Total_Amount_Imputed"] = (
        pd.Series(to_impute.values).notna().astype("int").values
    )
    df_train.loc[mask, "Total_Amount"] = to_impute.values

    return df_train


def impute_japan_territory(df):
    # Imputo territorio Japan con los que tienen region Japan
    df.loc[(df.Territory.isna()) & (df.Region == "Japan"), "Territory"] = "Japan"
    return df


def impute_americas_region(df):
    americas_territory = [
        "SW America",
        "South America",
        "SE America",
        "Central America",
    ]
    df.loc[df.Territory.isin(americas_territory), "Region"] = "Americas"
    return df


def impute_dubai_region(df):
    dubai_territory = ["UAE (Dubai)"]
    df.loc[df.Territory.isin(dubai_territory), "Region"] = "Middle East"
    return df


def impute_planned_end_date(df, impute_planned_days):
    mask = df.Planned_Delivery_End_Date.isna()
    df.loc[mask, "Planned_Delivery_End_Date"] = df.loc[
        df.Planned_Delivery_End_Date.isna(), "Planned_Delivery_Start_Date"
    ] + pd.DateOffset(days=impute_planned_days)

    df.loc[:, "Planned_Delivery_End_Date_Imputed"] = False
    df.loc[mask, "Planned_Delivery_End_Date_Imputed"] = True
    return df


def impute_quote_Expiry_Date(df, value):
    mask = df.Quote_Expiry_Date.isna()
    df.loc[mask, "Quote_Expiry_Date"] = df["Opportunity_Created_Date"] + pd.DateOffset(
        days=value
    )

    df.loc[:, "Quote_Expiry_Date_Imputed"] = False
    df.loc[mask, "Quote_Expiry_Date_Imputed"] = True

    return df


def impute_billing_country(df, impute_billing_by_territory):
    """
    imputamos billing_country con el más frecuente según territorio
    """
    # buscamos territorios que tengan billing_country en na y no sean na
    territory_valid = df[(df.Billing_Country.isna()) & ~(df.Territory.isna())].Territory
    mask = (df.Territory.isin(territory_valid)) & (df.Billing_Country.isna())
    # imputamos con el valor más frecuente ya calculado
    df.loc[mask, "Billing_Country"] = df.loc[mask, "Territory"].apply(
        lambda d: impute_billing_by_territory[d]
    )

    if "Billing_Country_Imputed" not in df.columns:
        df.loc[:, "Billing_Country_Imputed"] = False

    df.loc[mask, "Billing_Country_Imputed"] = True
    return df


def impute_territory_nan(df_train):

    # ======= Preprocessing ===========
    mask = df_train.Territory.isna()

    fx = df_train[~mask][
        [
            "Region",
            "Billing_Country",
            "Bureaucratic_Code",
            "Delivery_Terms",
            "Account_Owner",
            "Account_Name",
        ]
    ]
    fy = df_train[~mask][["Territory"]]

    fx = fx.fillna("None")

    oh = OneHotEncoder(handle_unknown="ignore").fit(fx)

    fx = oh.transform(fx)

    # ======= Train ===========
    fm = RandomForestClassifier(random_state=42).fit(fx, fy)

    y_pred = fm.predict_proba(fx)
    print("Métrica logLoss: {}".format(log_loss(fy, y_pred)))

    # ======= Predict ===========
    s = df_train[mask][
        [
            "Region",
            "Billing_Country",
            "Bureaucratic_Code",
            "Delivery_Terms",
            "Account_Owner",
            "Account_Name",
        ]
    ].fillna("None")
    fxs = oh.transform(s)
    fys = fm.predict(fxs)
    probas = fm.predict_proba(fxs)

    df_train.loc[mask, "Territory"] = fys

    if "Territory_Imputed" not in df_train.columns:
        df_train.loc[:, "Territory_Imputed"] = -1

    df_train.loc[mask, "Territory_Imputed"] = probas.max(axis=1)
    return df_train

def get_prod_cols(df):
    return df.columns[
        df.columns.str.contains("Product_Name|Product_Family")
    ]

def product_agg(df_train):
    prod_cols = get_prod_cols(df_train)
    group = df_train.groupby("Opportunity_ID")
    prods = group.agg({p: "sum" for p in prod_cols})
    prods = (
        prods.merge(
            group.agg(
                {
                    #         "Total_Amount": 'sum',
                    #         "Total_Amount_Converted":"sum",
                    #         "Diff_Amount":"sum",
                    #         "Diff_Amount_converted":"sum",
                    "TRF": "sum",
                    "Planned_Range_days": ["mean", "std"],
                    "Planned_Delivery_Start_Date_Period": ["mean", "std"],
                    "Planned_Delivery_Start_Date_Year": ["mean", "std"],
                    "Planned_Delivery_Start_Date_Month": ["mean", "std"],
                    "Planned_Delivery_End_Date_Period": ["mean", "std"],
                    "Planned_Delivery_End_Date_Year": ["mean", "std"],
                    "Planned_Delivery_End_Date_Month": ["mean", "std"],
                    "Planned_Delivery_Start_Date_Q1_Quarter": "sum",
                    "Planned_Delivery_Start_Date_Q2_Quarter": "sum",
                    "Planned_Delivery_Start_Date_Q3_Quarter": "sum",
                    "Planned_Delivery_Start_Date_Q4_Quarter": "sum",
                    "Planned_Delivery_End_Date_Q1_Quarter": "sum",
                    "Planned_Delivery_End_Date_Q2_Quarter": "sum",
                    "Planned_Delivery_End_Date_Q3_Quarter": "sum",
                    "Planned_Delivery_End_Date_Q4_Quarter": "sum",
                    "Planned_Delivery_End_Date_Imputed":'sum'
                }
            ),
            left_index=True,
            right_index=True,
        )
        .fillna(0)
        .reset_index("Opportunity_ID")
    )

    cols_rename = [isinstance(v, tuple) for v in prods.columns.values]
    cols_new_name = [
        k + ("_" + v if v != "sum" else "")
        for k, v in prods.columns[cols_rename].values
    ]
    return prods.rename(
        columns={k: v for k, v in zip(prods.columns[cols_rename].values, cols_new_name)}
    )


def join_aggregates(df, agg):
    # removemos las columnas que se agregaron en agg
    prod_cols = get_prod_cols(df)
    agg_cols = [
        "TRF",
        #     "Total_Amount",
        #     "Total_Amount_Converted",
        "Planned_Range_days",
        "Planned_Delivery_Start_Date_Period",
        "Planned_Delivery_Start_Date_Year",
        "Planned_Delivery_Start_Date_Month",
        "Planned_Delivery_Start_Date_Q1_Quarter",
        "Planned_Delivery_Start_Date_Q2_Quarter",
        "Planned_Delivery_Start_Date_Q3_Quarter",
        "Planned_Delivery_Start_Date_Q4_Quarter",
        "Planned_Delivery_End_Date_Period",
        "Planned_Delivery_End_Date_Year",
        "Planned_Delivery_End_Date_Month",
        "Planned_Delivery_End_Date_Q1_Quarter",
        "Planned_Delivery_End_Date_Q2_Quarter",
        "Planned_Delivery_End_Date_Q3_Quarter",
        "Planned_Delivery_End_Date_Q4_Quarter",
        "Planned_Delivery_End_Date_Imputed"
    ]
    
    df_int = df.loc[
        :, ~df.columns.isin(np.append(prod_cols, agg_cols))
    ].drop_duplicates()

    # === Validate Agg columns
    oc = df_int.columns[~df_int.columns.isin(["Opportunity_ID"])].to_numpy() 
    for c in oc:
        if (df_int[['Opportunity_ID', c]].drop_duplicates().shape[0] != df_int.Opportunity_ID.nunique()): 
            print(f"Falta agrupar por: {c}") # debería ser un warn?

    return df_int.merge(agg, on="Opportunity_ID", validate="one_to_one")

