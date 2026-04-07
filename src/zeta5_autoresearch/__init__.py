"""Structural core for the zeta(5) autoresearch engine."""

from .baseline_family_survey import (
    load_baseline_family_survey,
    render_baseline_family_survey_report,
    run_baseline_family_survey,
    write_baseline_family_survey_report,
)
from .baseline_shift_catalog_survey import (
    enumerate_normalized_shift_supports,
    load_baseline_shift_catalog_survey,
    render_baseline_shift_catalog_survey_report,
    run_baseline_shift_catalog_survey,
    write_baseline_shift_catalog_survey_report,
)
from .baseline_q_cache import (
    get_cached_baseline_q_terms,
    get_cached_baseline_q_terms_as_fractions,
    get_cached_baseline_q_terms_mod_prime,
)
from .baseline_modular_recurrence_probe import (
    build_baseline_modular_recurrence_probe,
    render_baseline_modular_recurrence_report,
    write_baseline_modular_recurrence_report,
)
from .baseline_decay_audit import (
    build_phase2_baseline_decay_audit,
    build_phase2_dual_companion_checkpoint,
    build_phase2_pivot_decision,
    load_phase2_local_object_catalog,
    render_phase2_baseline_decay_audit_report,
    render_phase2_dual_companion_checkpoint_report,
    render_phase2_pivot_report,
    write_phase2_baseline_decay_audit_json,
    write_phase2_baseline_decay_audit_report,
    write_phase2_dual_companion_checkpoint_report,
    write_phase2_pivot_artifacts,
    write_phase2_pivot_report,
)
from .baseline_decay_bridge import (
    build_phase2_baseline_decay_bridge,
    render_phase2_baseline_decay_bridge_report,
    write_phase2_baseline_decay_bridge_json,
    write_phase2_baseline_decay_bridge_report,
)
from .baseline_recurrence_probe import build_baseline_recurrence_probe, render_baseline_recurrence_report, write_baseline_recurrence_report
from .bz_growth_probe import build_bz_baseline_growth_probe, render_bz_baseline_growth_report, write_bz_baseline_growth_report
from .bz_dual_f7 import (
    compute_f7_constant_signature_from_a,
    compute_f7_constant_term_from_a,
    compute_f7_exact_component_signature_from_a,
    compute_f7_exact_component_term_from_a,
    compute_f7_zeta3_signature_from_a,
    compute_f7_zeta3_term_from_a,
    compute_f7_zeta5_signature_from_a,
    compute_f7_zeta5_term_from_a,
    evaluate_f7,
    evaluate_f7_hyper_line,
    extract_f7_linear_form,
    extract_f7_zeta5_coefficient,
    render_exact_f7_linear_form,
)
from .bz_dual_f7_companion_probe import (
    build_bz_dual_f7_companion_probe,
    render_bz_dual_f7_companion_probe_report,
    write_bz_dual_f7_companion_probe_report,
)
from .bz_dual_f7_companion_recurrence_probe import (
    build_bz_dual_f7_companion_recurrence_probe,
    render_bz_dual_f7_companion_recurrence_report,
    write_bz_dual_f7_companion_recurrence_report,
)
from .bz_dual_f7_companion_normalization_probe import (
    build_bz_dual_f7_companion_normalization_probe,
    render_bz_dual_f7_companion_normalization_report,
    write_bz_dual_f7_companion_normalization_report,
)
from .bz_dual_f7_exact_probe import (
    build_bz_dual_f7_exact_probe,
    render_bz_dual_f7_exact_probe_report,
    write_bz_dual_f7_exact_probe_report,
)
from .bz_dual_f7_probe import build_bz_dual_f7_probe, render_bz_dual_f7_probe_report, write_bz_dual_f7_probe_report
from .bz_dual_f7_zeta5_probe import (
    build_bz_dual_f7_zeta5_probe,
    render_bz_dual_f7_zeta5_probe_report,
    write_bz_dual_f7_zeta5_probe_report,
)
from .bz_dual_f7_zeta5_growth_probe import (
    build_bz_dual_f7_zeta5_growth_probe,
    render_bz_dual_f7_zeta5_growth_report,
    write_bz_dual_f7_zeta5_growth_report,
)
from .bz_dual_f7_zeta5_modular_recurrence_probe import (
    build_bz_dual_f7_zeta5_modular_recurrence_probe,
    render_bz_dual_f7_zeta5_modular_recurrence_report,
    write_bz_dual_f7_zeta5_modular_recurrence_report,
)
from .dual_f7_zeta5_shift_catalog_survey import (
    load_dual_f7_zeta5_shift_catalog_survey,
    render_dual_f7_zeta5_shift_catalog_survey_report,
    run_dual_f7_zeta5_shift_catalog_survey,
    write_dual_f7_zeta5_shift_catalog_survey_report,
)
from .dual_f7_exact_coefficient_cache import (
    get_cached_baseline_dual_f7_companion_terms,
    get_cached_baseline_dual_f7_constant_terms,
    get_cached_baseline_dual_f7_exact_component_terms,
    get_cached_baseline_dual_f7_zeta3_terms,
    get_cached_symmetric_dual_f7_companion_terms,
    get_cached_symmetric_dual_f7_constant_terms,
    get_cached_symmetric_dual_f7_exact_component_terms,
    get_cached_symmetric_dual_f7_zeta3_terms,
)
from .bz_symmetric_linear_forms_probe import (
    build_bz_totally_symmetric_linear_forms_probe,
    render_bz_totally_symmetric_linear_forms_report,
    write_bz_totally_symmetric_linear_forms_report,
)
from .bz_symmetric_recurrence_probe import (
    build_bz_totally_symmetric_recurrence_probe,
    render_bz_totally_symmetric_recurrence_report,
    write_bz_totally_symmetric_recurrence_report,
)
from .campaigns import expand_campaign, load_campaign_spec, run_campaign_structural_dry_run
from .campaign_report import render_campaign_report, write_campaign_report
from .gate0_parse import parse_candidate_file, run_gate0
from .gate1_filter import run_gate1
from .sequence_evidence import load_sequence_evidence_by_id, resolve_candidate_sequence_evidence

__all__ = [
    "load_baseline_family_survey",
    "load_phase2_local_object_catalog",
    "render_baseline_family_survey_report",
    "render_phase2_baseline_decay_audit_report",
    "render_phase2_baseline_decay_bridge_report",
    "render_phase2_dual_companion_checkpoint_report",
    "render_phase2_pivot_report",
    "run_baseline_family_survey",
    "write_baseline_family_survey_report",
    "build_baseline_modular_recurrence_probe",
    "build_phase2_baseline_decay_audit",
    "build_phase2_baseline_decay_bridge",
    "build_phase2_dual_companion_checkpoint",
    "build_phase2_pivot_decision",
    "build_baseline_recurrence_probe",
    "build_bz_baseline_growth_probe",
    "build_bz_dual_f7_companion_normalization_probe",
    "build_bz_dual_f7_companion_probe",
    "build_bz_dual_f7_companion_recurrence_probe",
    "build_bz_dual_f7_exact_probe",
    "build_bz_dual_f7_probe",
    "build_bz_dual_f7_zeta5_growth_probe",
    "build_bz_dual_f7_zeta5_modular_recurrence_probe",
    "build_bz_dual_f7_zeta5_probe",
    "build_bz_totally_symmetric_linear_forms_probe",
    "build_bz_totally_symmetric_recurrence_probe",
    "compute_f7_constant_signature_from_a",
    "compute_f7_constant_term_from_a",
    "compute_f7_exact_component_signature_from_a",
    "compute_f7_exact_component_term_from_a",
    "compute_f7_zeta3_signature_from_a",
    "compute_f7_zeta3_term_from_a",
    "compute_f7_zeta5_signature_from_a",
    "compute_f7_zeta5_term_from_a",
    "evaluate_f7",
    "evaluate_f7_hyper_line",
    "enumerate_normalized_shift_supports",
    "expand_campaign",
    "extract_f7_linear_form",
    "extract_f7_zeta5_coefficient",
    "get_cached_baseline_dual_f7_companion_terms",
    "get_cached_baseline_dual_f7_constant_terms",
    "get_cached_baseline_dual_f7_exact_component_terms",
    "get_cached_baseline_dual_f7_zeta3_terms",
    "get_cached_baseline_q_terms",
    "get_cached_baseline_q_terms_as_fractions",
    "get_cached_baseline_q_terms_mod_prime",
    "get_cached_symmetric_dual_f7_companion_terms",
    "get_cached_symmetric_dual_f7_constant_terms",
    "get_cached_symmetric_dual_f7_exact_component_terms",
    "get_cached_symmetric_dual_f7_zeta3_terms",
    "load_dual_f7_zeta5_shift_catalog_survey",
    "load_campaign_spec",
    "load_sequence_evidence_by_id",
    "load_baseline_shift_catalog_survey",
    "parse_candidate_file",
    "render_baseline_modular_recurrence_report",
    "render_baseline_recurrence_report",
    "render_baseline_shift_catalog_survey_report",
    "render_bz_baseline_growth_report",
    "render_bz_dual_f7_companion_normalization_report",
    "render_bz_dual_f7_companion_probe_report",
    "render_bz_dual_f7_companion_recurrence_report",
    "render_bz_dual_f7_exact_probe_report",
    "render_bz_dual_f7_probe_report",
    "render_bz_dual_f7_zeta5_growth_report",
    "render_bz_dual_f7_zeta5_modular_recurrence_report",
    "render_bz_dual_f7_zeta5_probe_report",
    "render_dual_f7_zeta5_shift_catalog_survey_report",
    "render_exact_f7_linear_form",
    "render_bz_totally_symmetric_linear_forms_report",
    "render_bz_totally_symmetric_recurrence_report",
    "render_campaign_report",
    "resolve_candidate_sequence_evidence",
    "run_campaign_structural_dry_run",
    "run_baseline_shift_catalog_survey",
    "run_dual_f7_zeta5_shift_catalog_survey",
    "run_gate0",
    "run_gate1",
    "write_baseline_modular_recurrence_report",
    "write_baseline_recurrence_report",
    "write_baseline_shift_catalog_survey_report",
    "write_bz_baseline_growth_report",
    "write_bz_dual_f7_companion_normalization_report",
    "write_bz_dual_f7_companion_probe_report",
    "write_bz_dual_f7_companion_recurrence_report",
    "write_bz_dual_f7_exact_probe_report",
    "write_bz_dual_f7_probe_report",
    "write_bz_dual_f7_zeta5_growth_report",
    "write_bz_dual_f7_zeta5_modular_recurrence_report",
    "write_bz_dual_f7_zeta5_probe_report",
    "write_dual_f7_zeta5_shift_catalog_survey_report",
    "write_bz_totally_symmetric_linear_forms_report",
    "write_bz_totally_symmetric_recurrence_report",
    "write_campaign_report",
    "write_phase2_baseline_decay_audit_json",
    "write_phase2_baseline_decay_audit_report",
    "write_phase2_baseline_decay_bridge_json",
    "write_phase2_baseline_decay_bridge_report",
    "write_phase2_dual_companion_checkpoint_report",
    "write_phase2_pivot_artifacts",
    "write_phase2_pivot_report",
]
