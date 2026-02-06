# 📊 Poverty Dashboard

A comprehensive, deployment-ready Streamlit application for visualizing and analyzing global and India-specific poverty data. Features interactive visualizations, statistical analysis, machine learning predictions, and PDF report generation.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.1-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 📈 Interactive Visualizations
- **Line Charts**: Trend analysis over time
- **Bar Charts**: Comparative analysis across regions
- **Scatter Plots**: Correlation exploration
- **Box Plots**: Distribution analysis
- **Pie Charts**: Categorical breakdowns
- **Choropleth Maps**: Geographic visualization

### 🌍 Global Trends Analysis
- World Bank poverty indicators
- Country-wise comparisons
- Regional analysis
- Time series trends
- International poverty lines ($2.15, $3.65, $6.85 PPP)

### 🇮🇳 India-Specific Analysis
- State-wise poverty data
- Rural vs Urban comparison
- Multi-dimensional poverty indicators
- Demographic correlations

### 📊 Statistical Analysis
- Summary statistics
- Correlation analysis (Pearson, Spearman, Kendall)
- Regression models
- Hypothesis testing
- Confidence intervals

### 🤖 Machine Learning
- Linear Regression
- Random Forest
- Gradient Boosting
- Future poverty predictions
- Model performance metrics

### 📄 Reports & Downloads
- CSV export
- Excel export (multiple sheets)
- PDF report generation
- Customizable report templates

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Poverty_dashboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Poverty_dashboard/
│
├── app.py                         # Main Streamlit entry point
├── config.py                       # App configuration and constants
├── requirements.txt                # Python dependencies
│
├── data/                           # Data module
│   ├── __init__.py
│   ├── wb_api.py                   # World Bank API integration
│   ├── india_poverty_api.py        # India poverty data API
│   ├── data_loader.py              # Unified data fetching & caching
│   └── preprocess.py               # Data cleaning & transformations
│
├── pages/                          # Application pages
│   ├── __init__.py
│   ├── dashboard.py                # Overview with KPIs
│   ├── global_trends.py            # Global poverty visualization
│   ├── rural_vs_urban.py           # Rural vs Urban comparison
│   ├── analysis.py                 # Statistical analysis
│   ├── visualization.py            # Interactive charts
│   ├── reports.py                  # Downloads & PDF generation
│   └── learn_more.py               # Documentation & info
│
├── components/                     # Reusable UI components
│   ├── __init__.py
│   ├── sidebar.py                  # Navigation & filters
│   ├── filters.py                  # Filter controls
│   ├── metrics.py                  # KPI cards
│   └── tables.py                   # Styled data tables
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── visualization.py            # Chart creation functions
│   ├── stats.py                    # Statistical calculations
│   ├── ml.py                       # ML models & predictions
│   └── pdf_generator.py            # PDF report generation
│
├── assets/                         # Static assets
│   ├── css/style.css               # Custom styling
│   ├── images/logo.png.txt         # Logo placeholder
│   └── geojson/india_states.geojson.txt  # Map data placeholder
│
├── reports/                        # Generated reports
│   ├── generated/                  # Auto-generated PDFs
│   └── exports/                    # CSV/Excel downloads
│
└── README.md                       # This file
```

## 🔧 Configuration

### API Integration

The dashboard includes placeholder API functions in:
- `data/wb_api.py` - World Bank API
- `data/india_poverty_api.py` - India poverty data API

**To integrate real APIs:**

1. Open the respective API file
2. Replace the placeholder `TODO` sections with actual API calls
3. Update the API base URLs in `config.py`
4. Add your API keys to environment variables

Example for World Bank API:
```python
import requests

def fetch_wb_poverty_data(indicator_code, start_year, end_year):
    url = f"{config.WB_API_BASE_URL}/country/all/indicator/{indicator_code}"
    params = {
        'date': f'{start_year}:{end_year}',
        'format': 'json',
        'per_page': 10000
    }
    response = requests.get(url, params=params)
    data = response.json()
    # Process and return data
    return processed_data
```

### Customization

Edit [`config.py`](config.py:1) to customize:
- Data year ranges
- Color schemes
- Indicator lists
- Cache settings
- ML model parameters

## 📊 Usage Guide

### Navigation

1. **Dashboard**: Overview with key metrics and highlights
2. **Global Trends**: Worldwide poverty analysis
3. **Rural vs Urban**: Compare poverty across area types
4. **Statistical Analysis**: Advanced statistical methods
5. **Visualization**: Create custom charts
6. **Reports**: Export data and generate PDFs
7. **Learn More**: Documentation and methodology

### Filtering Data

Use the sidebar filters to:
- Select year range
- Choose specific states (for India data)
- Filter by area type (Rural/Urban/All)

### Generating Reports

1. Navigate to the **Reports** page
2. Select report type and configuration
3. Click "Generate PDF Report"
4. Download the generated file

### Exporting Data

1. Go to **Reports** → **Data Export**
2. Select data source
3. Choose format (CSV or Excel)
4. Click download button

## 🧪 Testing

Run the application locally to test:

```bash
# Start the app
streamlit run app.py

# Test different pages and features
# Verify filters work correctly
# Test data export and PDF generation
```

## 🚢 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t poverty-dashboard .
docker run -p 8501:8501 poverty-dashboard
```

### Heroku

1. Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 📦 Dependencies

All dependencies are pinned in [`requirements.txt`](requirements.txt:1):

- **streamlit** (1.31.1) - Web framework
- **pandas** (2.2.0) - Data manipulation
- **numpy** (1.26.4) - Numerical computing
- **plotly** (5.19.0) - Interactive charts
- **scikit-learn** (1.4.1.post1) - Machine learning
- **reportlab** (4.1.0) - PDF generation
- And more...

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Data Sources

- **World Bank Open Data**: https://data.worldbank.org
- **Government of India**: https://data.gov.in
- **Census of India**: https://censusindia.gov.in

## 🐛 Known Issues

- GeoJSON map requires actual India states GeoJSON file (placeholder provided)
- Logo image is a placeholder (add your own PNG)
- API functions return synthetic data (integrate real APIs)

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Email: poverty.dashboard@example.com
- Documentation: See **Learn More** page in the app

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- World Bank for open data access
- Streamlit team for the amazing framework
- Open source community for libraries and tools

## 🔄 Version History

- **v1.0.0** (2024) - Initial release
  - Core dashboard functionality
  - Global and India data analysis
  - Statistical analysis and ML predictions
  - PDF report generation
  - Data export features

---

**Made with ❤️ using Streamlit**

For more information, visit the **Learn More** page in the application.
