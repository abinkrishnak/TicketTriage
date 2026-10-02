# Local classifier artifact

This small scikit-learn Pipeline was trained on the project's cleaned synthetic Bitext classification split. Its SHA-256 is checked against `data/demo/runtime_manifest.json` before loading. Only load the trusted supplied file; joblib is not a safe format for arbitrary untrusted input. The classifier predicts one of six known categories and is not an OOD detector. See the third-party notices for data attribution.
