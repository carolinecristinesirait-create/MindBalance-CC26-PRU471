# Security and Privacy

MindBalance is a demonstration application. It does not require accounts, external APIs, or a database. Assessment responses are held in Streamlit session state and are not intentionally persisted by the application.

## Do not commit

- `.streamlit/secrets.toml`
- API keys or access tokens
- identifiable user assessment data
- private datasets or clinical records

## Before production use

Add authentication, encryption, access controls, consent logging, retention rules, audit logging, dependency scanning, privacy review, and an incident-response process. Treat mental-health information as sensitive data.

To report a vulnerability, use a private security channel maintained by the repository owner rather than a public issue.
