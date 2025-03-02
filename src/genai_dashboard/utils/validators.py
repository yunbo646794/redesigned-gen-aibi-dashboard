"""
Validation Utilities
~~~~~~~~~~~~~~~~~~
Data and configuration validation functions.
"""

from typing import List, Any
import os

def validate_data_source(sources: List[str]) -> bool:
    """
    Validate data sources exist and are accessible.
    
    Args:
        sources: List of data source paths
        
    Raises:
        ValueError: If sources are invalid
    """
    if not sources:
        raise ValueError("No data sources provided")
        
    for source in sources:
        if not os.path.exists(source):
            raise ValueError(f"Data source not found: {source}")
            
    return True

def validate_aws_config(config: dict) -> bool:
    """
    Validate AWS configuration.
    
    Example:
        config = {'region': 'us-east-1', 'bucket': 'my-bucket'}
        is_valid = validate_aws_config(config)
    """
    required_keys = ['region', 'bucket']
    
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config: {key}")
            
    return True
