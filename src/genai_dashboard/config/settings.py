"""
Configuration Settings
~~~~~~~~~~~~~~~~~~~
Default configuration and settings management.
"""

from typing import Dict, Any

# Default AWS Configuration
AWS_CONFIG: Dict[str, Any] = {
    'region': 'us-east-1',
    'bedrock': {
        'model_id': 'anthropic.claude-v2',
        'temperature': 0.7,
        'max_tokens': 1000
    },
    'quicksight': {
        'template_name': 'sales-template',
        'capacity_region': 'us-east-1'
    }
}

# Data Processing Configuration
PROCESSING_CONFIG: Dict[str, Any] = {
    'clean_options': {
        'remove_duplicates': True,
        'fill_nulls': True,
        'standardize_dates': True
    },
    'transform_options': {
        'create_date_features': True,
        'normalize_numerics': True
    }
}

# Logging Configuration
LOGGING_CONFIG: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
