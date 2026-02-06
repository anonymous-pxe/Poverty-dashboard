"""
Configuration file for Poverty Dashboard
Contains constants, settings, and indicator lists
"""

# Application metadata
APP_TITLE = "Poverty Dashboard"
APP_ICON = "📊"
APP_VERSION = "1.0.0"

# Data settings
CACHE_TTL = 3600  # Cache time-to-live in seconds (1 hour)
DATA_START_YEAR = 2000
DATA_END_YEAR = 2024

# World Bank API settings (placeholders)
WB_API_BASE_URL = "https://api.worldbank.org/v2"
WB_POVERTY_INDICATORS = [
    {"code": "SI.POV.DDAY", "name": "Poverty headcount ratio at $2.15 a day (2017 PPP)"},
    {"code": "SI.POV.LMIC", "name": "Poverty headcount ratio at $3.65 a day (2017 PPP)"},
    {"code": "SI.POV.UMIC", "name": "Poverty headcount ratio at $6.85 a day (2017 PPP)"},
    {"code": "SI.POV.GINI", "name": "Gini index"},
    {"code": "NY.GDP.PCAP.PP.CD", "name": "GDP per capita, PPP (current international $)"},
]

# India poverty indicators
INDIA_POVERTY_INDICATORS = [
    "Poverty Rate (%)",
    "Multidimensional Poverty Index (MPI)",
    "Per Capita Income (₹)",
    "Unemployment Rate (%)",
    "Literacy Rate (%)",
]

# Indian states
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Jammu & Kashmir",
    "Ladakh", "Puducherry", "Chandigarh", "Dadra & Nagar Haveli and Daman & Diu",
    "Lakshadweep", "Andaman & Nicobar Islands"
]

# Area types
AREA_TYPES = ["All", "Rural", "Urban"]

# Chart color schemes
COLOR_SCHEME = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff9800",
    "info": "#17a2b8",
    "rural": "#2ecc71",
    "urban": "#e74c3c",
}

# Map settings
MAP_CENTER_LAT = 20.5937
MAP_CENTER_LON = 78.9629
MAP_ZOOM = 4

# Export settings
EXPORT_DIR = "reports/exports"
GENERATED_DIR = "reports/generated"

# Machine Learning settings
ML_MODELS = ["Linear Regression", "Random Forest", "Gradient Boosting"]
ML_TEST_SIZE = 0.2
ML_RANDOM_STATE = 42

# Statistical analysis settings
CORRELATION_METHODS = ["pearson", "spearman", "kendall"]
CONFIDENCE_LEVEL = 0.95
