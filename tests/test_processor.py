"""
Test Suite for Data Processor
~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit tests for data processing functionality.
"""

import pytest
import pandas as pd
from genai_dashboard import DataProcessor

@pytest.fixture
def processor():
    """Create test processor instance."""
    return DataProcessor()

@pytest.fixture
def sample_data():
    """Create sample test data."""
    return pd.DataFrame({
        'date': ['2024-01-01', '2024-01-02'],
        'sales': [1000, 2000],
        'region': ['NA', 'EU']
    })

def test_data_cleaning(processor, sample_data):
    """Test data cleaning functionality."""
    # Add some duplicates
    dirty_data = pd.concat([sample_data, sample_data])
    
    # Clean data
    clean_data = processor._clean_data(dirty_data)
    
    assert len(clean_data) == len(sample_data)
    assert not clean_data.duplicated().any()
