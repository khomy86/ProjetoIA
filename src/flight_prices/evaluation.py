import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def fit_and_predict(models, X_train, y_train, X_test):
    """Treina cada modelo e devolve {nome: previsões no conjunto de teste}."""
    predictions = {}
    for name, model in models.items():
        start = time.perf_counter()
        model.fit(X_train, y_train)
        print(f"{name}: treinado em {time.perf_counter() - start:.2f}s")
        predictions[name] = model.predict(X_test)
    return predictions


def metrics_table(y_test, predictions, unit):
    return pd.DataFrame(
        {
            name: {
                f"MAE ({unit})": mean_absolute_error(y_test, y_pred),
                f"RMSE ({unit})": np.sqrt(mean_squared_error(y_test, y_pred)),
                "R²": r2_score(y_test, y_pred),
            }
            for name, y_pred in predictions.items()
        }
    ).T


def plot_predictions_vs_actual(name, y_test, y_pred, unit, max_points=None):
    y_test, y_pred = np.asarray(y_test), np.asarray(y_pred)
    if max_points and len(y_test) > max_points:
        idx = np.random.default_rng(42).choice(len(y_test), max_points, replace=False)
        y_test, y_pred = y_test[idx], y_pred[idx]

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
    plt.xlabel(f"Valores Reais ({unit})")
    plt.ylabel(f"Previsões ({unit})")
    plt.title(f"Previsões vs Valores Reais - {name}")
    plt.show()


def plot_residuals(name, y_test, y_pred, unit):
    plt.figure(figsize=(10, 6))
    plt.hist(y_test - y_pred, bins=50)
    plt.xlabel(f"Resíduos ({unit})")
    plt.ylabel("Frequência")
    plt.title(f"Distribuição dos Resíduos - {name}")
    plt.show()


def plot_error_comparison(metrics, unit):
    metrics[[f"MAE ({unit})", f"RMSE ({unit})"]].plot(kind="bar")
    plt.title("Comparação de MAE e RMSE entre modelos")
    plt.ylabel(f"Valor ({unit})")
    plt.xticks(rotation=45)
    plt.show()


def plot_feature_importance(name, model, feature_names):
    importances = pd.Series(model.feature_importances_, index=feature_names)
    plt.figure(figsize=(10, 6))
    importances.sort_values().plot(kind="barh")
    plt.title(f"Importância das Features - {name}")
    plt.show()
