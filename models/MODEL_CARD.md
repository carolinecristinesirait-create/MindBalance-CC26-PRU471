# MindBalance Model Card

## Purpose

Educational screening of anxiety-related patterns from self-reported lifestyle, physiological, and contextual inputs. The model is not a diagnostic device.

## Inputs

21 numeric features: 18 encoded source variables and 3 engineered composites. The deployment model embeds the RobustScaler used during training.

## Outputs

- Classification probabilities for Low, Medium, and High categories.
- A normalized regression output converted to a 1–10 estimated score.

## Reported held-out test results

- Accuracy: 0.7570
- Weighted F1: 0.7573
- Regression MAE: 0.8780
- Regression RMSE: 1.1081
- Regression R²: 0.7249

## Important limitations

The dataset uses structured self-reports. The results do not establish clinical validity, causal relationships, or generalization to populations outside the training data. The Medium class has lower recall than the Low and High classes. External validation and professional governance are required before any high-stakes use.
