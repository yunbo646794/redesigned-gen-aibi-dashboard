"""
Basic Usage Examples
~~~~~~~~~~~~~~~~~
Example implementations of dashboard generation.
"""

from genai_dashboard import SalesDashboard

def basic_dashboard_example():
    """Basic dashboard generation example."""
    # Initialize dashboard
    dashboard = SalesDashboard(
        aws_region="us-east-1",
        data_sources=["sales_data_*.csv"],
        output_bucket="my-dashboard-bucket"
    )
    
    # Generate dashboard
    dashboard_url = dashboard.generate()
    print(f"Dashboard available at: {dashboard_url}")

def custom_processing_example():
    """Example with custom data processing."""
    from genai_dashboard import DataProcessor
    
    class CustomProcessor(DataProcessor):
        def _transform_data(self, df):
            # Add custom transformations
            df['revenue'] = df['quantity'] * df['price']
            return df
    
    dashboard = SalesDashboard(
        data_processor=CustomProcessor(),
        aws_region="us-east-1"
    )
    dashboard.generate()

if __name__ == "__main__":
    basic_dashboard_example()
