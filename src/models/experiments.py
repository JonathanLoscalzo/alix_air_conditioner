import pandas as pd
from joblib import dump, load


def save_experiment(
    model,
    now,
    prediction_file,
    train_logloss,
    val_logloss,
    competition_score,
    observations,
):
    raise Exception("Aún no implementado")
    model_file = f"../models/rf-{now}.joblib"
    dump(model, model_file)

    experiment = {
        "model": model.__class__.__name__,  # set full uri
        "model_file": model_file,
        "prediction_file": prediction_file,
        "train_logloss": train_logloss,
        "val_logloss": val_logloss,
        "competition_score": competition_score,
        "observations": observations,
        "created_at": now,
    }
    experiments = pd.read_csv("../reports/experiments.csv")
    experiments.append(experiment, ignore_index=True).to_csv(
        "../reports/experiments.csv", index=False
    )

