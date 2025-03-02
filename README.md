# Redesigned GenAI BI Dashboard

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An AWS-powered solution that combines business intelligence with generative AI to create dynamic sales analytics dashboards. This project integrates data from multiple sources, processes it using AWS services, and generates AI-enhanced insights through interactive dashboards.

## 🎯 Project Overview

This solution combines:
- Data processing from 13 different tables
- GenAI-powered analytics
- Interactive BI dashboards
- Real-time monitoring and insights

## 🚀 Key Features

- **Data Integration**
  - Multi-table data combination
  - Automated data cleaning
  - Intelligent transformation pipeline

- **AWS Integration**
  - AWS Glue for ETL
  - Amazon Bedrock for GenAI
  - Amazon QuickSight for visualization
  - CloudWatch for monitoring

- **AI Analytics**
  - Automated insight generation
  - Pattern recognition
  - Trend analysis

## 📋 Prerequisites

- AWS Account with configured services:
  - AWS Glue
  - Amazon Bedrock
  - Amazon QuickSight
  - Amazon S3
- Python 3.8+
- Required AWS permissions

## 🔧 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yunbo646794/redesigned-gen-aibi-dashboard.git
cd redesigned-gen-aibi-dashboard

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

    

    
💻 Usage
Basic Implementation
    
from genai_dashboard import SalesDashboard

# Initialize dashboard
dashboard = SalesDashboard(
    aws_region="us-east-1",
    data_sources=["sales_*.csv"]
)

# Generate dashboard
dashboard.generate()

    

    
Data Processing Configuration
    
# Configure data processing
dashboard = SalesDashboard(
    data_config={
        "combine_tables": True,
        "clean_data": True,
        "transform": True
    }
)

    

    
📊 Project Structure
    
redesigned-gen-aibi-dashboard/
├── src/
│   ├── etl/                 # Data processing
│   ├── analysis/            # AI analysis
│   └── dashboard/           # Dashboard generation
├── infrastructure/          # AWS infrastructure
├── tests/                   # Test suite
└── docs/                    # Documentation

    

    
⚙️ Configuration
Key configuration options:

Data source settings
AWS service parameters
AI model configurations
Dashboard customization
🛠️ Development
Configure AWS credentials
Set up required services
Run test suite
Deploy infrastructure
🤝 Contributing
Contributions are welcome! Please feel free to:

Fork the repository
Create your feature branch
Submit a Pull Request
📫 Support
Create Issues in the [GitHub repository](https://github.com/yunbo646794/redesigned-gen-aibi-dashboard/issues)
Submit Pull Requests for improvements
Contact repository owner for major changes
📝 License
This project is licensed under the MIT License - see the [LICENSE](https://console.harmony.a2z.com/LICENSE) file for details.
