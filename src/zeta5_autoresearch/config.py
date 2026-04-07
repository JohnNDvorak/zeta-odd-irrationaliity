from __future__ import annotations

from pathlib import Path

SUPPORTED_CERTIFICATE_TEMPLATES = frozenset({"BZ_standard", "BZ_extended", "new_template"})
CERTIFICATION_STATUSES = (
    "certified_true",
    "certified_safe_bound",
    "uncertified_numeric",
    "invalidated",
)
KNOWN_CONFIGURATION_SUPPORT = {
    "8pi8": {
        "family_label": "8pi_odd",
        "support_class": "odd_only_zeta3_zeta5",
    },
    "8pi8v": {
        "family_label": "dual_of_8pi_odd",
        "support_class": "dual_zeta5_with_parasitic_zeta2",
    },
}
KNOWN_EXCLUDED_ROUTING_HASHES = frozenset()
DEFAULT_CONVERGENCE_START_N = 1
DEFAULT_CONVERGENCE_SCAN_LIMIT = 8

RESULT_COLUMNS = (
    "id",
    "timestamp",
    "configuration_label",
    "family_label",
    "routing_hash",
    "sequence_hash",
    "certificate_hash",
    "mode",
    "representation",
    "certificate_template",
    "certification_status",
    "u",
    "v",
    "C0_est",
    "C0_lo",
    "C0_hi",
    "C1_est",
    "C1_lo",
    "C1_hi",
    "C2_est",
    "C2_lo",
    "C2_hi",
    "gamma_est",
    "gamma_lo",
    "gamma_hi",
    "M_proof_est",
    "gate_reached",
    "improvement_source",
    "equality_witness",
    "notes",
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
RESULTS_PATH = DATA_DIR / "results.tsv"
CANDIDATES_DIR = DATA_DIR / "candidates"
