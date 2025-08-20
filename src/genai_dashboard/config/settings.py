"""
Configuration Settings
~~~~~~~~~~~~~~~~~~~~~~
Centralized, safe-by-default settings with environment overrides.

How it works
------------
1) Start with sane defaults below.
2) Override via environment variables (12-factor friendly).
3) Access merged/validated settings via `get_settings()`.

Environment variables (examples)
--------------------------------
GENAI_REGION=us-west-2
GENAI_BEDROCK_MODEL=anthropic.claude-3-haiku-20240307-v1:0
GENAI_BEDROCK_TEMPERATURE=0.4
GENAI_BEDROCK_MAX_TOKENS=800
GENAI_QUICKSIGHT_TEMPLATE=sales-template
GENAI_QUICKSIGHT_ACCOUNT_ID=123456789012
GENAI_ENABLE_BEDROCK=true
GENAI_ENABLE_QUICKSIGHT=false
GENAI_ENABLE_BENCHMARKS=true
GENAI_LOG_FORMAT=json
GENAI_PII_ALLOWED=false
GENAI_PII_HASH_SALT=change-me
GENAI_TIMEOUT_SECS=30
GENAI_MAX_RETRIES=3
"""

from __future__ import annotations

import os
from typing import Any, Dict, Literal, TypedDict


# -----------------------
# Defaults (safe values)
# -----------------------

class AWSBedrockCfg(TypedDict):
    model_id: str
    temperature: float
    max_tokens: int

class QuickSightCfg(TypedDict):
    template_name: str
    capacity_region: str
    account_id: str  # pulled from ENV, default '' (required for prod)

class AWSConfig(TypedDict):
    region: str
    bedrock: AWSBedrockCfg
    quicksight: QuickSightCfg

class ProcessingCleanOpts(TypedDict):
    remove_duplicates: bool
    fill_nulls: bool
    standardize_dates: bool

class ProcessingTransformOpts(TypedDict):
    create_date_features: bool
    normalize_numerics: bool

class ProcessingCfg(TypedDict):
    clean_options: ProcessingCleanOpts
    transform_options: ProcessingTransformOpts

class PrivacyCfg(TypedDict):
    allow_pii: bool           # hard stop if True not explicitly allowed
    hash_salt: str            # used for tokenization / hashing
    anonymize_fields: list[str]  # fields to hash/tokenize
    drop_fields: list[str]       # fields to drop at ingestion
    aggregation_only: bool       # restrict outputs to aggregates

class RuntimeCfg(TypedDict):
    enable_bedrock: bool
    enable_quicksight: bool
    enable_benchmarks: bool
    request_timeout_secs: int
    max_retries: int

class LogFormatter(TypedDict):
    format: str

class LogHandler(TypedDict):
    level: str
    formatter: str
    class_: str  # 'class' is reserved in Python

class LoggerCfg(TypedDict):
    handlers: list[str]
    level: str
    propagate: bool

class LoggingCfg(TypedDict):
    version: int
    disable_existing_loggers: bool
    formatters: Dict[str, LogFormatter]
    handlers: Dict[str, LogHandler]
    loggers: Dict[str, LoggerCfg]


# Default AWS Configuration (non-secret, overridable by ENV)
AWS_CONFIG: AWSConfig = {
    "region": "us-east-1",
    "bedrock": {
        "model_id": "anthropic.claude-v2",
        "temperature": 0.7,
        "max_tokens": 1000,
    },
    "quicksight": {
        "template_name": "sales-template",
        "capacity_region": "us-east-1",
        "account_id": "",  # must be set via ENV for production
    },
}

# Data Processing Configuration
PROCESSING_CONFIG: ProcessingCfg = {
    "clean_options": {
        "remove_duplicates": True,
        "fill_nulls": True,
        "standardize_dates": True,
    },
    "transform_options": {
        "create_date_features": True,
        "normalize_numerics": True,
    },
}

# Privacy / PII Configuration (critical for NIW credibility)
PRIVACY_CONFIG: PrivacyCfg = {
    "allow_pii": False,             # default: do not process raw PII
    "hash_salt": "change-me",       # override via ENV in any non-local env
    "anonymize_fields": ["user_id", "email", "ip_address"],
    "drop_fields": ["ssn", "passport_number"],
    "aggregation_only": True,       # export only aggregated metrics by default
}

# Runtime toggles and network hardening
RUNTIME_CONFIG: RuntimeCfg = {
    "enable_bedrock": True,
    "enable_quicksight": True,
    "enable_benchmarks": False,  # set True to generate perf artifacts
    "request_timeout_secs": 30,
    "max_retries": 3,
}

# Logging Configuration (supports 'standard' and 'json' formats)
def _build_logging_config(fmt: Literal["standard", "json"] = "standard") -> LoggingCfg:
    formatter = (
        "%(asctime)s %(levelname)s %(name)s %(message)s"
        if fmt == "standard"
        else '{"ts":"%(asctime)s","lvl":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
    )

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": formatter},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class_": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "INFO", "propagate": True}
        },
    }

LOGGING_CONFIG: LoggingCfg = _build_logging_config(
    "json" if os.getenv("GENAI_LOG_FORMAT", "").lower() == "json" else "standard"
)


# -----------------------
# Helpers / Accessors
# -----------------------

def _env_bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}

def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, "").strip() or default)
    except ValueError:
        return default

def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, "").strip() or default)
    except ValueError:
        return default


def get_settings() -> Dict[str, Any]:
    """
    Merge defaults with environment overrides and perform basic validation.
    Returns a dict with keys: aws, processing, privacy, runtime, logging.
    """
    aws: AWSConfig = {
        "region": os.getenv("GENAI_REGION", AWS_CONFIG["region"]),
        "bedrock": {
            "model_id": os.getenv("GENAI_BEDROCK_MODEL", AWS_CONFIG["bedrock"]["model_id"]),
            "temperature": _env_float("GENAI_BEDROCK_TEMPERATURE", AWS_CONFIG["bedrock"]["temperature"]),
            "max_tokens": _env_int("GENAI_BEDROCK_MAX_TOKENS", AWS_CONFIG["bedrock"]["max_tokens"]),
        },
        "quicksight": {
            "template_name": os.getenv(
                "GENAI_QUICKSIGHT_TEMPLATE", AWS_CONFIG["quicksight"]["template_name"]
            ),
            "capacity_region": os.getenv(
                "GENAI_QUICKSIGHT_CAPACITY_REGION", AWS_CONFIG["quicksight"]["capacity_region"]
            ),
            "account_id": os.getenv("GENAI_QUICKSIGHT_ACCOUNT_ID", AWS_CONFIG["quicksight"]["account_id"]),
        },
    }

    processing: ProcessingCfg = PROCESSING_CONFIG.copy()

    privacy: PrivacyCfg = {
        "allow_pii": _env_bool("GENAI_PII_ALLOWED", PRIVACY_CONFIG["allow_pii"]),
        "hash_salt": os.getenv("GENAI_PII_HASH_SALT", PRIVACY_CONFIG["hash_salt"]),
        "anonymize_fields": PRIVACY_CONFIG["anonymize_fields"],
        "drop_fields": PRIVACY_CONFIG["drop_fields"],
        "aggregation_only": _env_bool("GENAI_AGGREGATION_ONLY", PRIVACY_CONFIG["aggregation_only"]),
    }

    runtime: RuntimeCfg = {
        "enable_bedrock": _env_bool("GENAI_ENABLE_BEDROCK", RUNTIME_CONFIG["enable_bedrock"]),
        "enable_quicksight": _env_bool("GENAI_ENABLE_QUICKSIGHT", RUNTIME_CONFIG["enable_quicksight"]),
        "enable_benchmarks": _env_bool("GENAI_ENABLE_BENCHMARKS", RUNTIME_CONFIG["enable_benchmarks"]),
        "request_timeout_secs": _env_int("GENAI_TIMEOUT_SECS", RUNTIME_CONFIG["request_timeout_secs"]),
        "max_retries": _env_int("GENAI_MAX_RETRIES", RUNTIME_CONFIG["max_retries"]),
    }

    logging_cfg: LoggingCfg = LOGGING_CONFIG

    # --- Basic validation / guardrails ---
    if runtime["enable_quicksight"] and not aws["quicksight"]["account_id"]:
        # In production you might raise; here we just warn via print to avoid import-time exceptions.
        print("[WARN] QuickSight enabled but GENAI_QUICKSIGHT_ACCOUNT_ID is not set.")

    if privacy["allow_pii"] and privacy["hash_salt"] in {"", "change-me"}:
        print("[WARN] PII allowed but GENAI_PII_HASH_SALT is default. Set a strong salt.")

    if aws["bedrock"]["max_tokens"] <= 0:
        aws["bedrock"]["max_tokens"] = 1000

    return {
        "aws": aws,
        "processing": processing,
        "privacy": privacy,
        "runtime": runtime,
        "logging": logging_cfg,
    }
