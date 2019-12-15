import pandas as pd
import lightgbm as lgb
import pickle
import shap
import numpy as np

TARGET_COL = "arrears_target"

INPUT_PATH = "bin/market-invoice-data.csv"

OUTPUT_CLASSIFIER_BIN_PATH = "bin/market-invoice-lgb.pkl"

DROP_COLS = [
    "Trade ID",
    "Seller ID",
    "Trade Type",
    "Expected Payment Date",
    "Settlement Date",
    "In Arrears",
    "In Arrears on Date",
    "Crystallised Loss Date",
    "Payment State",
    "Crystallised Loss",
    "Advance Date",
]

TEST_DICT = {
    "Price Grade": 6.0,
    "Face Value": 18318.0,
    "Advance": 16486.2,
    "Advance %": 90.0,
    "Discount %": 1.0,
    "Outstanding Principal": 0.0,
    "Face Value (GBP)": 18318.0,
    "Advance (GBP)": 16486.2,
    "Outstanding Principal (GBP)": 0.0,
    "Annualised Gross Yield %": 14.164038846995776,
    "expected_duration": 31,
    "prev_settles": 0,
    "Currency_EUR": 0,
    "Currency_GBP": 1,
    "Currency_USD": 0,
    "Discount On (Advance or Face Value)_Advance": 0,
    "Discount On (Advance or Face Value)_Facevalue": 1,
}


def main():
    raw = pd.read_csv(INPUT_PATH).drop(columns=DROP_COLS)
    y = raw[TARGET_COL]
    X = raw.drop(columns=[TARGET_COL])
    X_dum = pd.get_dummies(X)
    model = lgb.LGBMClassifier()
    model.fit(X_dum, y)
    pickle.dump(model, open(OUTPUT_CLASSIFIER_BIN_PATH, "wb"))

    print("example record")
    print("----------------------")
    print(X_dum.head(1).to_dict(orient="records"))


if __name__ == "__main__":
    main()
