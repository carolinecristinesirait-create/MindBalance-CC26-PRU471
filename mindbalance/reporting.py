"""Downloadable assessment report builders."""
from __future__ import annotations

import html
import json
from datetime import datetime

from mindbalance.schemas import PredictionResult


def result_json(result: PredictionResult) -> str:
    return json.dumps(result.to_dict(), indent=2, ensure_ascii=False)


def result_html(result: PredictionResult) -> str:
    probs = "".join(
        f"<tr><td>{html.escape(label)}</td><td>{value:.1%}</td></tr>"
        for label, value in result.probabilities.items()
    )
    strengths = "".join(
        f"<li><strong>{html.escape(item['title'])}</strong>: {html.escape(item['detail'])}</li>"
        for item in result.strengths
    ) or "<li>No specific strength was highlighted from the selected thresholds.</li>"
    focus = "".join(
        f"<li><strong>{html.escape(item['title'])}</strong>: {html.escape(item['detail'])}</li>"
        for item in result.focus_areas
    ) or "<li>No high-priority focus area was highlighted.</li>"
    actions = "".join(
        f"<li><strong>{html.escape(item['title'])}</strong>: {html.escape(item['detail'])}</li>"
        for item in result.action_plan
    )
    inputs = "".join(
        f"<tr><td>{html.escape(str(key).replace('_', ' ').title())}</td><td>{html.escape(str(value))}</td></tr>"
        for key, value in result.input_data.to_public_dict().items()
    )
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MindBalance Assessment Report</title>
<style>
body{{font-family:Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 24px;color:#172033;line-height:1.55}}
h1{{color:#0f766e;margin-bottom:4px}}h2{{margin-top:30px;border-bottom:1px solid #dbe4ea;padding-bottom:8px}}
.badge{{display:inline-block;padding:8px 14px;border-radius:999px;background:#ccfbf1;color:#115e59;font-weight:700}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.card{{border:1px solid #dbe4ea;border-radius:14px;padding:18px;background:#f8fafc}}
table{{width:100%;border-collapse:collapse}}td,th{{border-bottom:1px solid #e2e8f0;text-align:left;padding:8px}}
small{{color:#64748b}}.notice{{padding:14px;border-left:4px solid #f59e0b;background:#fffbeb}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<h1>MindBalance</h1>
<p><small>Assessment report generated {generated}</small></p>
<p class="badge">{html.escape(result.level)} screening category</p>
<p><strong>Estimated score:</strong> {result.predicted_score:.2f}/10 &nbsp; <strong>Confidence:</strong> {result.confidence:.1%}</p>
<div class="notice"><strong>Important:</strong> This output is an educational screening estimate, not a diagnosis or medical advice.</div>
<div class="grid">
<section class="card"><h2>Class probabilities</h2><table>{probs}</table></section>
<section class="card"><h2>Engineered indicators</h2>
<table><tr><td>Sleep efficiency</td><td>{result.engineered.sleep_efficiency:.1%}</td></tr>
<tr><td>Lifestyle risk</td><td>{result.engineered.lifestyle_risk:.1%}</td></tr>
<tr><td>Anxiety composite</td><td>{result.engineered.anxiety_composite:.1%}</td></tr></table></section>
</div>
<h2>Profile strengths</h2><ul>{strengths}</ul>
<h2>Focus areas</h2><ul>{focus}</ul>
<h2>Suggested next steps</h2><ol>{actions}</ol>
<h2>Submitted inputs</h2><table>{inputs}</table>
<p><small>Inference mode: {html.escape(result.model_mode)}. Data are not automatically uploaded or stored by this report.</small></p>
</body></html>"""
