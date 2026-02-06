"""
Learn More Page - Project information, methodology, and data sources
"""

import streamlit as st
import config


def render():
    """Render the learn more page"""
    
    st.title("📚 Learn More")
    st.markdown("Information about the Poverty Dashboard project, methodology, and data sources")
    st.markdown("---")
    
    # Create tabs for different sections
    tabs = st.tabs([
        "About",
        "Methodology",
        "Data Sources",
        "Indicators",
        "FAQ",
        "Contact"
    ])
    
    with tabs[0]:
        render_about()
    
    with tabs[1]:
        render_methodology()
    
    with tabs[2]:
        render_data_sources()
    
    with tabs[3]:
        render_indicators()
    
    with tabs[4]:
        render_faq()
    
    with tabs[5]:
        render_contact()


def render_about():
    """Render about section"""
    
    st.subheader("📊 About the Poverty Dashboard")
    
    st.markdown("""
    The **Poverty Dashboard** is a comprehensive data visualization and analysis platform designed to provide
    insights into poverty trends across the globe with a special focus on India.
    
    ### 🎯 Purpose
    
    This dashboard aims to:
    - **Visualize** poverty data through interactive charts and maps
    - **Analyze** trends and patterns in poverty rates over time
    - **Compare** rural and urban poverty dynamics
    - **Predict** future poverty trends using machine learning
    - **Provide** actionable insights for policymakers and researchers
    
    ### ✨ Key Features
    
    - **Interactive Visualizations**: Line charts, bar charts, scatter plots, box plots, and geographic maps
    - **Statistical Analysis**: Correlation analysis, regression models, and summary statistics
    - **Machine Learning**: Predictive models for forecasting poverty trends
    - **Data Export**: Download data in CSV and Excel formats
    - **PDF Reports**: Generate comprehensive reports with charts and analysis
    - **Real-time Filtering**: Filter data by year range, states, countries, and area types
    
    ### 📈 Version Information
    
    - **Version**: {version}
    - **Last Updated**: 2024
    - **Data Coverage**: {start_year} - {end_year}
    """.format(
        version=config.APP_VERSION,
        start_year=config.DATA_START_YEAR,
        end_year=config.DATA_END_YEAR
    ))


def render_methodology():
    """Render methodology section"""
    
    st.subheader("🔬 Methodology")
    
    st.markdown("""
    ### Data Collection
    
    The dashboard integrates data from multiple authoritative sources:
    
    1. **World Bank Open Data**: Global poverty indicators using standardized international poverty lines
    2. **Government of India Statistical Databases**: State-wise poverty estimates and demographic data
    3. **Census Data**: Population distribution and socioeconomic indicators
    
    ### Poverty Measurement
    
    #### International Poverty Lines
    
    The World Bank uses three international poverty lines:
    
    - **$2.15 per day (2017 PPP)**: Extreme poverty line for low-income countries
    - **$3.65 per day (2017 PPP)**: Lower middle-income class poverty line
    - **$6.85 per day (2017 PPP)**: Upper middle-income class poverty line
    
    #### India-Specific Measures
    
    For India, we track:
    
    - **Multidimensional Poverty Index (MPI)**: Considers health, education, and living standards
    - **Per Capita Income**: Economic indicator at state level
    - **Rural vs Urban**: Separate tracking for rural and urban areas
    
    ### Statistical Methods
    
    #### Correlation Analysis
    
    We use multiple correlation methods:
    - **Pearson**: Linear relationships
    - **Spearman**: Monotonic relationships
    - **Kendall**: Rank correlations
    
    #### Regression Analysis
    
    Our regression models include:
    - **Linear Regression**: For linear relationships
    - **Multiple Regression**: Multiple independent variables
    - **Polynomial Regression**: Non-linear patterns
    
    #### Machine Learning Models
    
    Predictive models available:
    - **Linear Regression**: Baseline model
    - **Random Forest**: Ensemble method for complex patterns
    - **Gradient Boosting**: Advanced ensemble technique
    
    ### Data Quality
    
    #### Cleaning Process
    
    1. **Duplicate Removal**: Eliminate duplicate records
    2. **Missing Value Handling**: Imputation using median/mode
    3. **Outlier Detection**: IQR method for identifying outliers
    4. **Standardization**: Consistent units and formats
    
    #### Validation
    
    - Cross-validation of statistical models
    - Comparison with published reports
    - Regular data updates and verification
    """)


def render_data_sources():
    """Render data sources section"""
    
    st.subheader("📚 Data Sources")
    
    st.markdown("""
    ### Primary Data Sources
    
    #### 1. World Bank Open Data
    
    - **Website**: [data.worldbank.org](https://data.worldbank.org)
    - **Coverage**: Global poverty indicators for 200+ countries
    - **Update Frequency**: Annual
    - **Data Quality**: High - peer-reviewed and internationally recognized
    
    **Key Indicators**:
    - Poverty headcount ratio at various poverty lines
    - GDP per capita (PPP)
    - Gini index
    - Income distribution metrics
    
    #### 2. Government of India - Data.gov.in
    
    - **Website**: [data.gov.in](https://data.gov.in)
    - **Coverage**: State-wise poverty and demographic data
    - **Update Frequency**: Varies by dataset (annual to quinquennial)
    - **Data Quality**: Official government statistics
    
    **Key Datasets**:
    - State-wise poverty estimates
    - Rural and urban poverty statistics
    - Multidimensional Poverty Index
    
    #### 3. Census of India
    
    - **Website**: [censusindia.gov.in](https://censusindia.gov.in)
    - **Coverage**: Comprehensive demographic data
    - **Update Frequency**: Decennial (every 10 years)
    - **Data Quality**: High - official census data
    
    #### 4. National Sample Survey Office (NSSO)
    
    - **Coverage**: Household consumption and poverty surveys
    - **Update Frequency**: Periodic surveys
    - **Data Quality**: Representative national samples
    
    ### Data Attribution
    
    All data used in this dashboard is properly attributed to its original source. We comply with:
    - Creative Commons licenses where applicable
    - Open data policies
    - Citation requirements
    
    ### Data Limitations
    
    Users should be aware of:
    - **Time Lag**: Official poverty data often has a 2-3 year lag
    - **Coverage Gaps**: Some regions/years may have missing data
    - **Methodology Changes**: Poverty measurement methodologies evolve over time
    - **Estimation**: Some values are estimates based on surveys
    
    ### API Integration
    
    This dashboard includes placeholder API integration points for:
    - World Bank API: `{wb_api}`
    - India government APIs: Ready for integration
    
    Replace the placeholder functions in `data/wb_api.py` and `data/india_poverty_api.py` with actual API calls.
    """.format(wb_api=config.WB_API_BASE_URL))


def render_indicators():
    """Render indicators section"""
    
    st.subheader("📊 Poverty Indicators")
    
    st.markdown("### World Bank Indicators")
    
    # Display WB indicators
    for indicator in config.WB_POVERTY_INDICATORS:
        with st.expander(f"📌 {indicator['name']}"):
            st.markdown(f"""
            **Indicator Code**: `{indicator['code']}`
            
            **Description**: This indicator measures {indicator['name'].lower()}.
            
            **Interpretation**:
            - Higher values indicate higher poverty rates
            - Used for international comparisons
            - Adjusted for purchasing power parity (PPP)
            """)
    
    st.markdown("---")
    st.markdown("### India Poverty Indicators")
    
    # Display India indicators
    for indicator in config.INDIA_POVERTY_INDICATORS:
        with st.expander(f"📌 {indicator}"):
            description = get_indicator_description(indicator)
            st.markdown(description)


def get_indicator_description(indicator):
    """Get description for India indicators"""
    
    descriptions = {
        "Poverty Rate (%)": """
        **Description**: Percentage of population living below the poverty line
        
        **Measurement**: Based on consumption expenditure surveys
        
        **Categories**:
        - Rural poverty rate
        - Urban poverty rate
        - Combined poverty rate
        """,
        
        "Multidimensional Poverty Index (MPI)": """
        **Description**: Measures poverty across multiple dimensions beyond income
        
        **Dimensions**:
        - Health (nutrition, child mortality)
        - Education (years of schooling, school attendance)
        - Living Standards (cooking fuel, sanitation, drinking water, electricity, housing, assets)
        
        **Range**: 0 to 1 (higher values indicate higher poverty)
        """,
        
        "Per Capita Income (₹)": """
        **Description**: Average income per person in Indian Rupees
        
        **Use**: Economic indicator of prosperity
        
        **Note**: Adjusted for inflation in constant prices
        """,
        
        "Unemployment Rate (%)": """
        **Description**: Percentage of labor force that is unemployed
        
        **Measurement**: Based on labor force surveys
        
        **Significance**: Linked to poverty and economic wellbeing
        """,
        
        "Literacy Rate (%)": """
        **Description**: Percentage of population (age 7+) who can read and write
        
        **Significance**: Education is strongly correlated with poverty reduction
        
        **Trend**: Generally improving across India
        """
    }
    
    return descriptions.get(indicator, f"**{indicator}**\n\nDetailed description coming soon.")


def render_faq():
    """Render FAQ section"""
    
    st.subheader("❓ Frequently Asked Questions")
    
    faqs = [
        {
            "question": "What is the poverty line?",
            "answer": """
            The poverty line is a threshold income level below which a person or household is considered poor.
            Different countries and organizations use different poverty lines. The World Bank uses international
            poverty lines of $2.15, $3.65, and $6.85 per day (2017 PPP), while India uses its own national
            poverty line based on consumption expenditure.
            """
        },
        {
            "question": "How often is the data updated?",
            "answer": """
            Data update frequency varies by source:
            - World Bank indicators: Annual updates
            - India state-wise data: Updated based on NSSO surveys (periodic)
            - The dashboard cache is refreshed hourly
            
            Note: Official poverty data typically has a 2-3 year lag due to data collection and processing time.
            """
        },
        {
            "question": "Why is rural poverty higher than urban poverty?",
            "answer": """
            Rural poverty is generally higher due to:
            - Limited access to economic opportunities
            - Lower wages in agricultural sector
            - Limited access to education and healthcare
            - Infrastructure challenges
            - Seasonal employment patterns
            
            However, the gap is narrowing in many regions due to rural development programs and migration.
            """
        },
        {
            "question": "How accurate are the ML predictions?",
            "answer": """
            Machine learning predictions should be interpreted with caution:
            - Models are trained on historical data
            - Accuracy metrics (R², RMSE) are shown for each model
            - Predictions assume historical trends continue
            - External shocks (pandemics, policy changes) can affect actual outcomes
            
            Use predictions as indicative trends, not absolute forecasts.
            """
        },
        {
            "question": "Can I use this data for research?",
            "answer": """
            Yes, with proper attribution:
            - Cite the original data sources (World Bank, Government of India)
            - Cite this dashboard if using processed/analyzed data
            - Follow open data licenses for each dataset
            - Verify data accuracy for critical research
            """
        },
        {
            "question": "How do I report data issues?",
            "answer": """
            If you notice any data inconsistencies:
            1. Check the data source documentation
            2. Verify filters and selections
            3. Contact us through the Contact section
            4. Provide specific details (indicator, year, location)
            """
        }
    ]
    
    for i, faq in enumerate(faqs, 1):
        with st.expander(f"**{i}. {faq['question']}**"):
            st.markdown(faq['answer'])


def render_contact():
    """Render contact section"""
    
    st.subheader("📧 Contact & Support")
    
    st.markdown("""
    ### Get in Touch
    
    We welcome your feedback, questions, and suggestions!
    
    #### 📬 Contact Information
    
    - **Email**: poverty.dashboard@example.com
    - **GitHub**: [github.com/poverty-dashboard](https://github.com/poverty-dashboard)
    - **Documentation**: [docs.poverty-dashboard.org](https://docs.poverty-dashboard.org)
    
    #### 🐛 Report Issues
    
    Found a bug or data issue?
    - Open an issue on our [GitHub repository](https://github.com/poverty-dashboard/issues)
    - Include steps to reproduce the problem
    - Attach screenshots if applicable
    
    #### 💡 Feature Requests
    
    Have ideas for new features?
    - Submit feature requests on GitHub
    - Join community discussions
    - Contribute to the project
    
    #### 🤝 Contributing
    
    This is an open-source project. Contributions are welcome!
    
    **Ways to contribute**:
    - Code contributions (features, bug fixes)
    - Documentation improvements
    - Data quality checks
    - Translations
    
    See our [Contributing Guide](https://github.com/poverty-dashboard/CONTRIBUTING.md) for details.
    
    #### 📄 License
    
    This dashboard is released under the MIT License.
    Data is subject to original source licenses.
    
    #### 🙏 Acknowledgments
    
    Thanks to:
    - World Bank for providing open data access
    - Government of India for official statistics
    - Open source community for tools and libraries
    - All contributors to this project
    """)
    
    # Feedback form
    st.markdown("---")
    st.markdown("### 📝 Quick Feedback")
    
    with st.form("feedback_form"):
        name = st.text_input("Name (optional)")
        email = st.text_input("Email (optional)")
        feedback = st.text_area("Your feedback or questions")
        
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            if feedback:
                st.success("Thank you for your feedback! We'll review it soon.")
                # In production, this would send feedback to a database or email
            else:
                st.warning("Please enter your feedback before submitting.")
