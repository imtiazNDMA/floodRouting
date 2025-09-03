#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import numpy as np


# In[ ]:


# Initialize the Dash app
app = dash.Dash(__name__)


# In[ ]:


# Data loading and processing functions
def load_barrage_data(file_path, sheet_name):
    """
    Load barrage data from Excel file
    
    Parameters:
    - file_path: Path to Excel file
    - sheet_name: Name of the sheet containing data
    
    Returns:
    - Cleaned pandas DataFrame
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # Clean column names
        df.columns = df.columns.str.strip().str.lower()
        expected_columns = ['date', 'inflow', 'structure']
        
        # Map columns if they have different names
        column_mapping = {}
        for col in df.columns:
            if 'date' in col:
                column_mapping[col] = 'date'
            elif 'inflow' in col:
                column_mapping[col] = 'inflow'
            elif 'structure' in col or 'barrage' in col:
                column_mapping[col] = 'structure'
        
        df = df.rename(columns=column_mapping)
        
        # Ensure we have the required columns
        for col in expected_columns:
            if col not in df.columns:
                if col == 'structure':
                    df[col] = 'Unknown'  # Default value
                else:
                    raise ValueError(f"Missing required column: {col}")
        
        # Clean and process data
        df['date'] = pd.to_datetime(df['date'])
        df['inflow'] = pd.to_numeric(df['inflow'], errors='coerce').fillna(0)
        df['structure'] = df['structure'].str.strip()
        
        # Add derived columns
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.strftime('%B')
        df['day_month'] = df['date'].dt.strftime('%d/%m')
        
        # Identify flood years and periods
        df['is_flood_year'] = df['year'].isin([2014, 2022, 2023])
        
        # Define flood periods for each year (you may need to adjust these dates)
        flood_periods = {
            2014: ('2014-09-06', '2014-09-16'),
            2022: ('2022-07-15', '2022-08-15'),  # Adjust based on actual flood dates
            2023: ('2023-07-15', '2023-08-15')   # Adjust based on actual flood dates
        }
        
        df['flood_period'] = 'Normal'
        for year, (start, end) in flood_periods.items():
            mask = (df['date'] >= start) & (df['date'] <= end) & (df['year'] == year)
            df.loc[mask, 'flood_period'] = f'{year} Flood'
        
        # Sort by structure and date
        df = df.sort_values(['structure', 'date']).reset_index(drop=True)
        
        return df
    
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return sample data for testing
        return create_sample_data()


# In[ ]:


def create_sample_data():
    """Create sample data for testing when file is not available"""
    # Create data for multiple years to test the year filter
    data = []
    for year in [2020, 2021, 2022, 2023]:
        dates = pd.date_range(f'{year}-01-01', f'{year}-12-31', freq='D')
        for date in dates:
            # Trimmu data
            data.append({
                'date': date,
                'inflow': np.random.randint(15000, 25000),
                'structure': 'Trimmu'
            })
            # Panjnad data
            data.append({
                'date': date,
                'inflow': np.random.randint(30000, 40000),
                'structure': 'Panjnad'
            })
    
    df = pd.DataFrame(data)
    # Add derived columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')
    df['day_month'] = df['date'].dt.strftime('%d/%m')
    df['is_flood_year'] = df['year'].isin([2014, 2022, 2023])
    df['flood_period'] = 'Normal'
    
    return df

# Load data from Excel file
try:
    df = load_barrage_data(
        r"C:\Users\Admin\Desktop\FFD FLood Data\Marala, Qadirabad,Sulemanki,Balloki flows (2012 -2023).xlsx",
        "Selected"
    )
except:
    print("Could not load Excel file, using sample data")
    df = create_sample_data()


# In[ ]:


# Update dropdown options to include new barrages
dropdown_options = [
{'label': 'All Barrages', 'value': 'All'},
{'label': 'Trimmu', 'value': 'Trimmu'},
{'label': 'Panjnad', 'value': 'Panjnad'},
{'label': 'Qadirabad', 'value': 'Qadirabad'},
{'label': 'Marala', 'value': 'Marala'},
{'label': 'Khanki', 'value': 'Khanki'},
{'label': 'Guddu', 'value': 'Guddu'}
]


# In[ ]:


# Calculate comprehensive statistics
def calculate_flood_statistics(df):
    """Calculate statistics for flood analysis"""
    stats = {}
    
    # Overall statistics
    stats['total_records'] = len(df)
    stats['date_range'] = f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"
    
    # Statistics by barrage
    for structure in df['structure'].unique():
        structure_data = df[df['structure'] == structure]
        stats[structure] = {
            'total_records': len(structure_data),
            'max_inflow': structure_data['inflow'].max(),
            'avg_inflow': structure_data['inflow'].mean(),
        }
        
        # Flood year analysis
        for year in [2014, 2022, 2023]:
            year_data = structure_data[structure_data['year'] == year]
            if not year_data.empty:
                flood_data = year_data[year_data['flood_period'] == f'{year} Flood']
                stats[structure][f'flood_{year}'] = {
                    'peak_inflow': year_data['inflow'].max(),
                    'peak_inflow_date': year_data.loc[year_data['inflow'].idxmax(), 'date'].strftime('%Y-%m-%d'),
                    'avg_inflow_flood': flood_data['inflow'].mean() if not flood_data.empty else 0,
                }
            else:
                # No data for this year
                stats[structure][f'flood_{year}'] = {
                    'peak_inflow': 0,
                    'peak_inflow_date': None,
                    'avg_inflow_flood': 0,
                }
    
    return stats

# Calculate statistics
stats = calculate_flood_statistics(df)


# In[ ]:


# Helper function to filter data by year
def filter_data_by_year(df, selected_year):
    """Filter dataframe by selected year"""
    if selected_year == 'All':
        return df
    else:
        return df[df['year'] == int(selected_year)]


# In[ ]:


# Chart update functions
def update_main_chart(selected_barrage, selected_year):
    # Filter data by year first
    filtered_df = filter_data_by_year(df, selected_year)

    fig = go.Figure()

    # --- Ensure selected_barrage is always a list ---
    if not isinstance(selected_barrage, list):
        selected_barrage = [selected_barrage]

    # --- Define default colors for all barrages ---
    all_colors = {
        'Trimmu': '#2563eb',
        'Panjnad': '#16a34a',
        'Qadirabad': '#f59e0b',
        'Marala': '#10b981',
        'Khanki': '#8b5cf6',
        'Guddu': '#ec4899'
    }

    # --- Determine which structures to plot ---
    if 'All' in selected_barrage:
        structures = filtered_df['structure'].unique()
    else:
        structures = selected_barrage

    colors = {s: all_colors.get(s, '#2563eb') for s in structures}

    # --- Add traces for each selected structure ---
    for structure in structures:
        structure_data = filtered_df[filtered_df['structure'] == structure].sort_values('date')

        if structure_data.empty:
            continue

        fig.add_trace(go.Scatter(
            x=structure_data['date'],
            y=structure_data['inflow'],
            mode='lines',
            name=f'{structure} Inflow',
            line=dict(color=colors.get(structure, '#2563eb'), width=2),
            hovertemplate=f'<b>{structure}</b><br>%{{x}}<br>Inflow: %{{y:,.0f}} cusecs<extra></extra>'
        ))

    # --- Highlight flood periods (if applicable) ---
    if selected_year == 'All' or int(selected_year) in [2014, 2022, 2023]:
        flood_colors = {
            2014: 'rgba(255, 0, 0, 0.2)',
            2022: 'rgba(255, 165, 0, 0.2)',
            2023: 'rgba(255, 69, 0, 0.2)'
        }

        years_to_highlight = [2014, 2022, 2023] if selected_year == 'All' else [int(selected_year)]

        for year in years_to_highlight:
            if year in [2014, 2022, 2023]:
                flood_data = filtered_df[
                    (filtered_df['year'] == year) &
                    (filtered_df['flood_period'] == f'{year} Flood')
                ]
                if not flood_data.empty:
                    fig.add_vrect(
                        x0=flood_data['date'].min(),
                        x1=flood_data['date'].max(),
                        fillcolor=flood_colors[year],
                        layer="below",
                        line_width=0,
                        annotation_text=f"{year} Flood",
                        annotation_position="top left"
                    )

    # --- Build chart title ---
    title_barrages = "All" if "All" in selected_barrage else ", ".join(selected_barrage)
    year_text = f" ({selected_year})" if selected_year != 'All' else ""

    # --- Update layout ---
    fig.update_layout(
        title=f"Flow Patterns - {title_barrages} Barrage(s){year_text}",
        xaxis_title="Date",
        yaxis_title="Flow (cusecs)",
        hovermode='x unified',
        height=600,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

    return fig


# In[ ]:


"""
def update_flood_comparison(selected_barrage, selected_year):
    # For flood comparison, we might want to show all flood years even if specific year is selected
    # But filter by year if it's one of the flood years
    if selected_year != 'All' and int(selected_year) not in [2014, 2022, 2023]:
        # If selected year is not a flood year, show empty chart with message
        fig = go.Figure()
        fig.update_layout(
            title=f"Peak Flows During Flood Years - No flood data for {selected_year}",
            xaxis_title="Flood Year & Barrage",
            yaxis_title="Peak Flow (cusecs)",
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        return fig
    
    if selected_barrage == 'All':
        structures = df['structure'].unique()
    else:
        structures = [selected_barrage]
    
    fig = go.Figure()
    
    # Colors for different years
    year_colors = {2014: '#ef4444', 2022: '#f97316', 2023: '#dc2626'}
    
    # Determine which years to show
    years_to_show = [2014, 2022, 2023] if selected_year == 'All' else [int(selected_year)]
    years_to_show = [y for y in years_to_show if y in [2014, 2022, 2023]]  # Only flood years
    
    for structure in structures:
        structure_data = df[df['structure'] == structure]
        
        peak_data = []
        for year in years_to_show:
            year_data = structure_data[structure_data['year'] == year]
            if not year_data.empty:
                peak_inflow = year_data['inflow'].max()
                peak_data.append({
                    'year': year,
                    'peak_inflow': peak_inflow,
                    'structure': structure
                })
        
        peak_df = pd.DataFrame(peak_data)
        
        if not peak_df.empty:
            # Inflow bars
            fig.add_trace(go.Bar(
                x=[f"{year} {structure}" for year in peak_df['year']],
                y=peak_df['peak_inflow'],
                name=f'{structure} Peak Inflow',
                marker_color=[year_colors[year] for year in peak_df['year']],
                hovertemplate=f'<b>{structure}</b><br>%{{x}}<br>Peak Inflow: %{{y:,.0f}} cusecs<extra></extra>',
                offsetgroup=structure,
                legendgroup=f'{structure}_inflow'
            ))
    
    year_text = f" ({selected_year})" if selected_year != 'All' else " (2014, 2022, 2023)"
    fig.update_layout(
        title=f"Peak Flows During Flood Years{year_text}",
        xaxis_title="Flood Year & Barrage",
        yaxis_title="Peak Flow (cusecs)",
        barmode='group',
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig
"""


# In[ ]:


"""
def update_yearly_peaks(selected_barrage, selected_year):
    # Filter data by year
    filtered_df = filter_data_by_year(df, selected_year)
    
    if selected_barrage == 'All':
        structures = filtered_df['structure'].unique()
    else:
        structures = [selected_barrage]
    
    fig = go.Figure()
    
    colors = {
        'Trimmu': '#2563eb',
        'Panjnad': '#16a34a',
        'Qadirabad': '#f59e0b',
        'Marala': '#10b981',
        'Khanki': '#8b5cf6',
        'Guddu': '#ec4899'
    }
    
    for structure in structures:
        structure_data = filtered_df[filtered_df['structure'] == structure]
        
        if structure_data.empty:
            continue
            
        # Calculate yearly peaks
        yearly_peaks = structure_data.groupby('year').agg({
            'inflow': 'max'
        }).reset_index()
        
        # Add traces for each structure
        fig.add_trace(go.Scatter(
            x=yearly_peaks['year'],
            y=yearly_peaks['inflow'],
            mode='lines+markers',
            name=f'{structure} Peak Inflow',
            line=dict(color=colors.get(structure, '#2563eb'), width=3),
            marker=dict(size=8),
            hovertemplate=f'<b>{structure}</b><br>Year: %{{x}}<br>Peak Inflow: %{{y:,.0f}} cusecs<extra></extra>'
        ))
    
    # Highlight flood years (only if they're in the filtered data)
    flood_years_in_data = [year for year in [2014, 2022, 2023] if year in filtered_df['year'].values]
    for year in flood_years_in_data:
        fig.add_vline(
            x=year, 
            line=dict(color="red", width=2, dash="dot"),
            annotation_text=f"{year} Flood Year",
            annotation_position="top"
        )
    
    year_text = f" ({selected_year})" if selected_year != 'All' else ""
    fig.update_layout(
        title=f"Annual Peak Flow Trends{year_text}",
        xaxis_title="Year",
        yaxis_title="Peak Flow (cusecs)",
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig
    """


# In[ ]:


"""
def update_monthly_pattern(selected_barrage, selected_year):
    # Filter data by year
    filtered_df = filter_data_by_year(df, selected_year)
    
    if selected_barrage == 'All':
        structures = filtered_df['structure'].unique()
    else:
        structures = [selected_barrage]
    
    fig = go.Figure()
    
    colors = {
        'Trimmu': '#2563eb',
        'Panjnad': '#16a34a',
        'Qadirabad': '#f59e0b',
        'Marala': '#10b981',
        'Khanki': '#8b5cf6',
        'Guddu': '#ec4899'
    }
    
    for structure in structures:
        structure_data = filtered_df[filtered_df['structure'] == structure]
        
        if structure_data.empty:
            continue
            
        # Calculate monthly averages
        monthly_avg = structure_data.groupby('month').agg({
            'inflow': 'mean'
        }).reset_index()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_avg['month_name'] = monthly_avg['month'].apply(lambda x: month_names[x-1])
        
        fig.add_trace(go.Bar(
            x=monthly_avg['month_name'],
            y=monthly_avg['inflow'],
            name=f'{structure} Avg Inflow',
            marker_color=colors.get(structure, '#2563eb'),
            hovertemplate=f'<b>{structure}</b><br>Month: %{{x}}<br>Avg Inflow: %{{y:,.0f}} cusecs<extra></extra>'
        ))
    
    year_text = f" ({selected_year})" if selected_year != 'All' else ""
    fig.update_layout(
        title=f"Average Monthly Flow Patterns{year_text}",
        xaxis_title="Month",
        yaxis_title="Average Flow (cusecs)",
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        barmode='group'
    )
    
    return fig
    """


# In[ ]:


"""
def update_flood_peaks_summary(selected_barrage, selected_year):
    # Filter by year for the summary
    if selected_year != 'All':
        year_filter = int(selected_year)
        if year_filter not in [2014, 2022, 2023]:
            return html.Div([
                html.H3("Flood Analysis", className="text-lg font-bold text-gray-800 mb-4"),
                html.P(f"No flood data available for {selected_year}", className="text-gray-600")
            ])
    
    if selected_barrage == 'All':
        structures = ['Trimmu', 'Panjnad', 'Qadirabad', 'Marala', 'Khanki', 'Guddu']
    else:
        structures = [selected_barrage]
    
    cards = []
    
    for structure in structures:
        if structure in stats:
            structure_stats = stats[structure]
            
            # Create cards for each flood year
            flood_cards = []
            years_to_show = [2014, 2022, 2023] if selected_year == 'All' else [int(selected_year)]
            
            for year in years_to_show:
                if year in [2014, 2022, 2023]:  # Only show flood years
                    flood_key = f'flood_{year}'
                    if flood_key in structure_stats:
                        flood_info = structure_stats[flood_key]
                        flood_cards.append(
                            html.Div([
                                html.H4(f"{year} Flood", className="font-semibold text-orange-800 mb-2"),
                                html.P(f"Peak Inflow: {flood_info['peak_inflow']:,.0f} cusecs", className="text-sm"),
                                html.P(f"Peak Date: {flood_info['peak_inflow_date'] or 'N/A'}", className="text-xs text-gray-600")
                            ], className="bg-orange-50 p-3 rounded border border-orange-200")
                        )
            
            if flood_cards:  # Only show structure card if there are flood cards
                # Structure summary card
                cards.append(
                    html.Div([
                        html.H3(f"{structure} Barrage", className="text-lg font-bold text-gray-800 mb-4"),
                        html.Div(flood_cards, className="grid grid-cols-1 md:grid-cols-3 gap-3")
                    ], className="mb-6")
                )
    
    return html.Div(cards)

# Get available years for dropdown
available_years = sorted(df['year'].unique())
year_options = [{'label': 'All Years', 'value': 'All'}]
year_options.extend([{'label': str(year), 'value': str(year)} for year in available_years])
"""


# In[ ]:


# Define the app layout
app.layout = html.Div([
html.Div([
html.H1("Historical Flood Flow Analysis", className="text-3xl font-bold text-center text-gray-800 mb-6"),
html.Div([
html.Div([
html.Label("Select Barrage:", className="block text-sm font-medium text-gray-700 mb-2"),
dcc.Dropdown(id='barrage-dropdown', options=dropdown_options, value='All', multi = True, className="mb-4")
], className="w-full md:w-1/2 pr-2"),
html.Div([
html.Label("Select Year:", className="block text-sm font-medium text-gray-700 mb-2"),
dcc.Dropdown(id='year-dropdown', options=[{'label': 'All Years', 'value': 'All'}] + [{'label': str(y), 'value': str(y)} for y in sorted(df['year'].unique())], value='All', className="mb-4")
], className="w-full md:w-1/2 pl-2")
], className="flex flex-wrap mb-6"),
#html.Div(id='flood-peaks-summary', className="mb-6"),
html.Div([dcc.Graph(id='main-flow-chart')], className="mb-6"),
#html.Div([dcc.Graph(id='flood-comparison-chart')], className="mb-6"),
#html.Div([dcc.Graph(id='yearly-peaks-chart')], className="mb-6"),
#html.Div([dcc.Graph(id='monthly-pattern-chart')])
], className="container mx-auto px-4 py-8")
])


# In[ ]:


# Callbacks - Updated to include year parameter
"""
@app.callback(
    Output('flood-peaks-summary', 'children'),
    [Input('barrage-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def callback_update_flood_peaks_summary(selected_barrage, selected_year):
    return update_flood_peaks_summary(selected_barrage, selected_year)
"""
@app.callback(
    Output('main-flow-chart', 'figure'),
    [Input('barrage-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def callback_update_main_chart(selected_barrage, selected_year):
    return update_main_chart(selected_barrage, selected_year)

"""
@app.callback(
    Output('flood-comparison-chart', 'figure'),
    [Input('barrage-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def callback_update_flood_comparison(selected_barrage, selected_year):
    return update_flood_comparison(selected_barrage, selected_year)

@app.callback(
    Output('yearly-peaks-chart', 'figure'),
    [Input('barrage-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def callback_update_yearly_peaks(selected_barrage, selected_year):
    return update_yearly_peaks(selected_barrage, selected_year)

@app.callback(
    Output('monthly-pattern-chart', 'figure'),
    [Input('barrage-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def callback_update_monthly_pattern(selected_barrage, selected_year):
    return update_monthly_pattern(selected_barrage, selected_year)
    """


# In[ ]:


# For standalone testing
if __name__ == '__main__':
    app.run(debug=True, port=8050)


# In[ ]:




