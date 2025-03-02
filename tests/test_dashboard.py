"""
Test Suite for Dashboard Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unit tests for dashboard functionality.
"""

import pytest
from genai_dashboard import SalesDashboard
from unittest.mock import Mock, patch

@pytest.fixture
def dashboard():
    """Create test dashboard instance."""
    return SalesDashboard(
        aws_region="us-east-1",
        data_sources=["test_data.csv"],
        output_bucket="test-bucket"
    )

def test_dashboard_initialization(dashboard):
    """Test dashboard initialization."""
    assert dashboard.aws_region == "us-east-1"
    assert len(dashboard.data_sources) == 1
    assert dashboard.output_bucket == "test-bucket"

@patch('genai_dashboard.aws.quicksight.QuickSightManager')
def test_dashboard_generation(mock_quicksight, dashboard):
    """Test dashboard generation process."""
    # Mock QuickSight response
    mock_quicksight.return_value.create_dashboard.return_value = "dashboard-123"
    
    # Generate dashboard
    result = dashboard.generate()
    
    assert result == "dashboard-123"
    mock_quicksight.return_value.create_dashboard.assert_called_once()
