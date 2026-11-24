"""Lightweight API smoke tests for the documented M-Tools scientific stack.

These are compatibility checks, not scientific validation on production data.
Run: python tests/scientific_stack_smoke.py <core|forecast|causal|bayesian|optimization|analytics|ml|nlp>
"""
from __future__ import annotations

import sys


def core() -> None:
    import numpy as np
    import pandas as pd
    from scipy.optimize import Bounds, LinearConstraint, milp
    from sklearn.cluster import HDBSCAN, KMeans
    from statsmodels.stats.proportion import confint_proportions_2indep

    assert np.__version__ == "2.3.5"
    assert pd.__version__ == "2.3.3"

    result = milp(
        c=np.array([-3.0, -2.0]),
        integrality=np.ones(2),
        bounds=Bounds([0, 0], [np.inf, np.inf]),
        constraints=LinearConstraint([[1, 1], [1, 0]], [-np.inf, -np.inf], [4, 2]),
    )
    assert result.success and round(-result.fun) == 10
    assert np.allclose(result.x, [2, 2])

    X = np.array([[0.0, 0.0], [0.1, 0.0], [10.0, 10.0], [10.1, 10.0]])
    labels = KMeans(n_clusters=2, random_state=7, n_init=10).fit_predict(X)
    assert labels[0] == labels[1] and labels[2] == labels[3] and labels[0] != labels[2]
    density_labels = HDBSCAN(min_cluster_size=2, min_samples=1, copy=True).fit_predict(X)
    assert len(set(density_labels)) >= 2

    low, high = confint_proportions_2indep(30, 100, 20, 100, method="newcomb")
    assert np.isfinite([low, high]).all() and low < 0.10 < high


def forecast() -> None:
    import numpy as np
    import pandas as pd
    from statsforecast import StatsForecast
    from statsforecast.models import AutoETS, Naive

    dates = pd.date_range("2023-01-01", periods=36, freq="MS")
    t = np.arange(36, dtype=float)
    values = 50 + 0.7 * t + 5 * np.sin(2 * np.pi * t / 12)
    frame = pd.DataFrame({"unique_id": "shop-1", "ds": dates, "y": values})
    engine = StatsForecast(
        models=[Naive(), AutoETS(season_length=12)],
        freq="MS",
        n_jobs=1,
    )
    forecast_frame = engine.forecast(df=frame, h=3)
    assert len(forecast_frame) == 3
    assert np.isfinite(forecast_frame[["Naive", "AutoETS"]].to_numpy()).all()


def causal() -> None:
    import numpy as np
    import pandas as pd
    from dowhy import CausalModel
    from econml.dml import LinearDML
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

    rng = np.random.default_rng(13)
    n = 500
    x = rng.normal(size=n)
    propensity = 1 / (1 + np.exp(-x))
    treatment = rng.binomial(1, propensity)
    outcome = 2.0 * treatment + 1.5 * x + rng.normal(scale=0.5, size=n)
    frame = pd.DataFrame({"x": x, "t": treatment, "y": outcome})

    causal_model = CausalModel(
        data=frame,
        treatment="t",
        outcome="y",
        common_causes=["x"],
    )
    estimand = causal_model.identify_effect()
    estimate = causal_model.estimate_effect(
        estimand,
        method_name="backdoor.linear_regression",
    )
    assert np.isfinite(float(estimate.value))
    refutation = causal_model.refute_estimate(
        estimand,
        estimate,
        method_name="random_common_cause",
        random_seed=13,
    )
    assert refutation is not None

    X = rng.normal(size=(n, 2))
    W = rng.normal(size=(n, 1))
    T = rng.binomial(1, 1 / (1 + np.exp(-W[:, 0])))
    Y = 1.25 * T + 0.5 * X[:, 0] + W[:, 0] + rng.normal(scale=0.5, size=n)
    dml = LinearDML(
        model_y=RandomForestRegressor(n_estimators=12, min_samples_leaf=5, random_state=13),
        model_t=RandomForestClassifier(n_estimators=12, min_samples_leaf=5, random_state=13),
        discrete_treatment=True,
        cv=2,
        random_state=13,
    )
    dml.fit(Y, T, X=X, W=W)
    assert dml.effect(X[:5]).shape == (5,)


def bayesian() -> None:
    from pymc_marketing import clv
    from pymc_marketing.mmm import GeometricAdstock, LogisticSaturation, MMM

    assert MMM is not None
    assert GeometricAdstock is not None
    assert LogisticSaturation is not None
    assert hasattr(clv, "BetaGeoModel")


def optimization() -> None:
    import numpy as np
    from ortools.sat.python import cp_model
    from SALib.analyze import sobol as sobol_analyze
    from SALib.sample import sobol
    from SALib.test_functions import Ishigami

    problem = {
        "num_vars": 3,
        "names": ["x1", "x2", "x3"],
        "bounds": [[-np.pi, np.pi], [-np.pi, np.pi], [-np.pi, np.pi]],
    }
    samples = sobol.sample(problem, 128, calc_second_order=False, seed=17)
    outputs = Ishigami.evaluate(samples)
    indices = sobol_analyze.analyze(
        problem,
        outputs,
        calc_second_order=False,
        print_to_console=False,
    )
    assert np.isfinite(indices["S1"]).all()

    model = cp_model.CpModel()
    x = model.new_int_var(0, 4, "x")
    y = model.new_int_var(0, 4, "y")
    model.add(x + y <= 4)
    model.add(x <= 2)
    model.maximize(3 * x + 2 * y)
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    assert status == cp_model.OPTIMAL
    assert (solver.value(x), solver.value(y)) == (2, 2)


def analytics() -> None:
    import duckdb
    import polars as pl

    assert duckdb.sql("SELECT 6 * 7").fetchall()[0][0] == 42
    total = pl.DataFrame({"amount": [10, 20, 30]}).select(pl.col("amount").sum()).item()
    assert total == 60


def ml() -> None:
    import numpy as np
    import optuna
    import shap
    from catboost import CatBoostClassifier

    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0, 2], [2, 0], [2, 2], [2, 1]], dtype=float)
    y = np.array([0, 0, 0, 1, 0, 1, 1, 1])
    model = CatBoostClassifier(iterations=6, depth=2, verbose=False, thread_count=1, allow_writing_files=False)
    model.fit(X, y)
    values = shap.TreeExplainer(model).shap_values(X)
    assert values is not None

    study = optuna.create_study(direction="minimize")
    study.optimize(lambda trial: (trial.suggest_float("x", -1, 1)) ** 2, n_trials=2)
    assert study.best_value >= 0


def nlp() -> None:
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer

    assert BERTopic is not None
    assert SentenceTransformer is not None
    # Package import only; the separate nlp_model suite downloads Qwen3 weights.
    # Persian semantic quality still requires a human-labelled benchmark.



def nlp_model() -> None:
    import numpy as np
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B", device="cpu")
    texts = [
        "مشتریان از تأخیر در تحویل سفارش ناراضی هستند.",
        "مشتریان از دیر رسیدن سفارش‌ها شکایت دارند.",
        "کیفیت بسته‌بندی محصول پایین است.",
    ]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    assert embeddings.shape[0] == len(texts)
    assert embeddings.ndim == 2 and embeddings.shape[1] > 0
    assert np.isfinite(embeddings).all()
    print(f"Loaded Qwen3-Embedding-0.6B; Persian embedding shape={embeddings.shape}")



def meridian() -> None:
    import meridian
    from meridian import constants
    from meridian.analysis import analyzer, optimizer, summarizer
    from meridian.model import model, spec

    assert getattr(meridian, "__version__", None)
    assert constants is not None
    assert analyzer is not None and optimizer is not None and summarizer is not None
    assert model is not None and spec is not None
    print(f"Meridian import/API smoke test; version={meridian.__version__}")


def combined() -> None:
    # Run all selected library suites in one shared environment to catch cross-stack conflicts.
    for suite in (core, forecast, causal, bayesian, optimization, analytics, ml, nlp):
        suite()


if __name__ == "__main__":
    suites = {
        "core": core,
        "forecast": forecast,
        "causal": causal,
        "bayesian": bayesian,
        "optimization": optimization,
        "analytics": analytics,
        "ml": ml,
        "nlp": nlp,
        "nlp_model": nlp_model,
        "meridian": meridian,
        "combined": combined,
    }
    selected = sys.argv[1] if len(sys.argv) > 1 else "core"
    if selected not in suites:
        raise SystemExit(f"Unknown suite: {selected}; choose from {', '.join(suites)}")
    suites[selected]()
    print(f"PASS: {selected} import/API smoke test")
