# MindBalance

**AI-assisted anxiety risk screening and wellness intelligence**  
Coding Camp 2026 powered by DBS Foundation · Team **CC26-PRU471**

MindBalance is a polished, GitHub-ready Streamlit dashboard built from the supplied dataset, TensorFlow/Keras models, and training notebook. It combines a structured self-reflection, model inference, explainable wellness guidance, interactive exploratory analysis, a wellness toolkit, and a transparent model card.

> **Important:** MindBalance is an educational data-science project. It is not a diagnostic device, medical advice, treatment guidance, or a replacement for a qualified mental health professional.

## Highlights

- Six-page Streamlit application with a responsive dark glass interface
- 3-step private assessment covering lifestyle, physiological signals, and context
- TensorFlow multi-output inference using the included `.keras` deployment model
- Low, Medium, and High class probabilities
- Estimated anxiety score on a 1–10 scale
- Confidence interpretation and training-range warnings
- Explainable strengths, focus areas, and deterministic next-step guidance
- Wellness radar and engineered-feature gauges
- Downloadable HTML assessment report and JSON data
- Interactive dataset filters, Plotly charts, correlations, and CSV export
- Guided breathing and pulse-counting component
- Grounding exercise, quick emotional check-in, and 24-hour plan builder
- Model card, reported performance, feature order, data dictionary, and limitations
- Graceful fallback inference when TensorFlow cannot load
- Dockerfile, Streamlit configuration, tests, GitHub Actions, security notes, and MIT license

## Repository structure

```text
MindBalance-GitHub/
├── app.py
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── Dockerfile
├── Procfile
├── .python-version
├── .streamlit/
│   └── config.toml
├── .github/
│   └── workflows/quality.yml
├── data/
│   └── cleaned_anxiety_data.csv
├── models/
│   ├── mindbalance_model_preprocess.keras
│   ├── mindbalance_model_new.keras
│   └── MODEL_CARD.md
├── notebooks/
│   └── MindBalance_training_notebook.ipynb
├── examples/
│   └── sample_profile.json
├── mindbalance/
│   ├── config.py
│   ├── schemas.py
│   ├── features.py
│   ├── model_engine.py
│   ├── recommendations.py
│   ├── resources.py
│   ├── reporting.py
│   ├── charts.py
│   ├── state.py
│   ├── theme.py
│   ├── suite.py
│   ├── ui.py
│   └── pages/
│       ├── home.py
│       ├── assessment.py
│       ├── insights.py
│       ├── toolkit.py
│       ├── transparency.py
│       └── about.py
└── tests/
```

## Run locally

### 1. Install Python

Use **Python 3.11**. It is supported by the pinned TensorFlow 2.21.0 package and is the recommended version for this repository.

### 2. Create an environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS or Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

TensorFlow is a large dependency. The initial installation can consume substantial disk space.

### 3. Start the dashboard

```bash
streamlit run app.py
```

Open the local address shown in the terminal, usually `http://localhost:8501`.

## Upload to GitHub

1. Create an empty GitHub repository.
2. Extract this ZIP.
3. Upload **the contents inside the extracted folder**, not another nested ZIP.
4. Confirm that `app.py`, `requirements.txt`, `data/`, `models/`, and `mindbalance/` appear at the repository root.
5. Commit the files to the default branch.

Command-line alternative:

```bash
git init
git add .
git commit -m "Add MindBalance Streamlit dashboard"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

## Deploy to Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud with GitHub.
2. Choose **Create app** or **New app**.
3. Select the GitHub repository and branch.
4. Set the entrypoint to `app.py`.
5. Select Python **3.11** in the advanced settings.
6. Deploy.

The application requires no API keys. The dataset and Keras models are included directly in the repository.

### Deployment notes

- The first cold start may be slower because TensorFlow is imported and the model is loaded.
- The deployment model is only about 1 MB, but the TensorFlow runtime is much larger.
- If TensorFlow fails to install, verify the selected Python version and inspect the build log.
- When the model cannot load, the app remains usable in a clearly labelled transparent fallback mode.
- Keep `app.py` and `requirements.txt` in the repository root.

## Model contract

The model receives 21 ordered numeric features:

- 18 encoded source variables
- `SleepEfficiencyScore`
- `LifestyleRiskIndex`
- `AnxietyCompositeScore`

The preferred model, `mindbalance_model_preprocess.keras`, includes the fitted RobustScaler in the model graph. The app therefore sends raw encoded values in the same feature order used during training.

The outputs are:

1. Softmax class probabilities for `Low`, `Medium`, and `High`
2. A normalized regression value converted to the original 1–10 scale

## Reported held-out test metrics

| Metric | Value |
|---|---:|
| Classification accuracy | 0.7570 |
| Weighted F1 | 0.7573 |
| Regression MAE | 0.8780 |
| Regression RMSE | 1.1081 |
| Regression R² | 0.7249 |

Per-class performance reported in the notebook:

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Low | 0.88 | 0.89 | 0.88 | 171 |
| Medium | 0.82 | 0.69 | 0.75 | 780 |
| High | 0.68 | 0.80 | 0.74 | 699 |

These metrics describe the notebook's held-out test split. They do not establish clinical validity.

## Privacy behavior

- No login is required.
- No database is configured.
- Assessment values are kept in Streamlit session state.
- Data are not automatically sent to an external AI service.
- Users can deliberately download an HTML or JSON report.
- Streamlit hosting infrastructure may still generate ordinary technical logs. Review platform policies before handling sensitive data.

## Tests

Install the lightweight development requirements:

```bash
pip install -r requirements-dev.txt
pytest -q
python -m compileall -q app.py mindbalance tests
```

The tests verify the 21-feature model contract, feature-engineering bounds, fallback inference, dataset integrity, and report serialization. TensorFlow is intentionally not required for the lightweight unit-test workflow.

## Docker

```bash
docker build -t mindbalance .
docker run --rm -p 8501:8501 mindbalance
```

Then open `http://localhost:8501`.

## Limitations and responsible use

- Inputs are self-reported and can be inaccurate.
- The dataset does not represent every population or clinical context.
- The model can produce errors and uncertain classifications.
- The Medium class has weaker recall than the other reported classes.
- Model probabilities are not the probability that a person has a disorder.
- Suggestions are deterministic wellness prompts, not treatment recommendations.
- External validation, calibration, fairness analysis, privacy review, accessibility testing, and professional governance are required before any production or high-stakes use.

## Team

- Vincentius Tanujaya
- Caroline Cristine Sirait
- Nabillah Indah Tsuraya

## License

MIT License. See `LICENSE`.
