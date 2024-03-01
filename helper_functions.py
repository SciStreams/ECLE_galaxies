import streamlit as st

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import os

@st.cache_data
def load_data(directory):
    data_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            # Extract the key from the filename
            key = filename.split('_Processed')[0]
            # Load the CSV file
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            # Store the DataFrame in the dictionary with the key
            data_dict[key] = df
    return data_dict


def filter_data(data_dict, variability):
    if variability == "All":
        filtered_data_dict = data_dict
        return filtered_data_dict
    
    elif variability == "Variable":
        selected_keys = ["SDSS_J0748", "SDSS_J0952", "SDSS_J1342", "SDSS_J1350", "SDSS_J1241"]
        
        filtered_data_dict = {key: data_dict[key] for key in data_dict.keys() if any(key.startswith(prefix) for prefix in selected_keys)}
        return filtered_data_dict

    elif variability == "Non Variable":
        selected_keys = ["SDSS_J0938", "SDSS_J1055"]

        filtered_data_dict = {key: data_dict[key] for key in data_dict.keys() if any(key.startswith(prefix) for prefix in selected_keys)}
        return filtered_data_dict


def get_galaxy_names(data_dict):
    galaxy_names = [key[:10] for key in data_dict.keys()]
    return galaxy_names


def spectral_lines():
    lines_with_wavelengths = {
        '[FeVII]': [3662.5, 5145.8, 6087.0],
        'Hδ': 4101.7,
        'HeI': 4471.5,
        'HeII': 4685.7,
        'Hβ': 4861.3,
        '[OIII]': [4958.9, 5006.8],
        '[FeXIV]': 5236.1,
        '[FeX]': 6374.5,
        'Hα': 6562.8,
        '[FeXI]': 7891.8
    }

    return lines_with_wavelengths

def extract_lines_and_wavelengths(lines_with_wavelengths):
    lines = []
    wavelengths = []
    for line, value in lines_with_wavelengths.items():
        if isinstance(value, list):
            lines.extend([line] * len(value))
            wavelengths.extend(value)
        else:
            lines.append(line)
            wavelengths.append(value)
    return lines, wavelengths


def get_line_color(line_name):
    if line_name.startswith('SDSS'):
        return 'black'
    elif line_name.startswith('MMT'):
        return '#92c5de'
    elif line_name.startswith('DESI'):
        return '#a6611a'
    elif line_name.startswith('Kast'):
        return '#018571'
    elif line_name.startswith('NTT'):
        return '#d7301f'
    else:
        return 'grey'

def plot_data_subplots(data_dict, scale, galaxy=None, lines=None, wavelengths=None):
    fig = go.Figure()
    for key, df in data_dict.items():
        # Create a trace for each key
        #st.dataframe(df)
        max_y_value = max(df['f$_\lambda$'].max() for df in data_dict.values())
        max_y_axis_limit = max_y_value * 1.05

        line_color = get_line_color(key[11:])
        
        trace = go.Scatter(x=df['#RestWavelength(Angs)'], 
                           y=df['f$_\lambda$'], 
                           mode='lines', 
                           name=key,
                           line=dict(width=1, color=line_color),
                           
                           )

        fig.add_trace(trace)

    

    # Add vertical lines for wavelengths if provided
    if lines and wavelengths:
        for line, wavelength in zip(lines, wavelengths):
            fig.add_shape(type="line",
                          x0=wavelength, y0=0, x1=wavelength, y1=max_y_axis_limit,
                          line=dict(color="black", width=1, dash="dash"),
                          name=line
                         )
            # Add annotation for line name
            fig.add_annotation(x=wavelength, y=max_y_axis_limit, text=line,
                               showarrow=False, yshift=15, xshift=-3, textangle=270)


    if scale == "All":
        h = 10000
        w = 800
        y_legend = 0.956
    elif scale == "Individual":
        h=4000
        w=800
        y_legend = 0.89


    elif scale == "Single":
        h=2000
        w=800
        #y_legend = 0.72
        # Calculate the position of y_legend dynamically
        y_legend_percentage = 0.37  # 20% below the 0 of the y-axis
        y_legend = max_y_axis_limit * y_legend_percentage

        if galaxy == "SDSS_J1342":
            y_legend = 0.72
        if galaxy == "SDSS_J1055":
            y_legend = 0.65
        if galaxy == "SDSS_J0938":
            y_legend = 0.72
        if galaxy == "SDSS_J1241":
            y_legend = 0.65
        if galaxy == "SDSS_J1241":
            y_legend = 0.65


        if galaxy == "Variable":
            h=8000
            w=800
            y_legend = 0.94

        if galaxy == "Non Variable":
            h=4000
            w=800
            y_legend = 0.85

    else:
        h=1000
        w=800
        y_legend = 0.6


    # Update layout to display subplots
    fig.update_layout(title='The spectroscopic sequences of the ECLE sample',
                      xaxis_title=r'Rest Wavelength [Å]',
                      yaxis_title='log<sub>10</sub> (Scaled f<sub>λ</sub>)',
                      showlegend=True,
                      height=h,
                      #width=w,
                      xaxis=dict(range=[3490, 8000]),
                      yaxis=dict(range=[0, max_y_axis_limit]),
                      grid=dict(rows=len(data_dict), columns=1),
                      legend=dict(orientation='h', y=y_legend),
                      #colorway=px.colors.sequential.Viridis,
                      )
    return fig



def plot_data_subplots_split(data_dict, scale, lines=None, wavelengths=None):
    galaxy_names = get_galaxy_names(data_dict)
    unique_galaxy_names = list(set(galaxy_names))

    num_rows = len(unique_galaxy_names)
    num_cols = 1
    h_factor = 300

    if scale == "Variable":
        num_rows = 5
        y_legend = 0.89
        h_factor = 500

    if scale == "Non Variable":
        num_rows = 2
        y_legend = 0.89
        h_factor = 750


    fig = make_subplots(rows=num_rows, cols=num_cols, shared_xaxes=True,
                        subplot_titles=unique_galaxy_names)

    for i, (key, df) in enumerate(data_dict.items(), start=1):
        galaxy_name = key[:10]
        row_index = unique_galaxy_names.index(galaxy_name) + 1

        max_y_value = max(df['f$_\lambda$'].max() for df in data_dict.values())
        max_y_axis_limit = max_y_value * 1.05

        line_color = get_line_color(key[11:])

        # Create a trace for each key
        trace = go.Scatter(x=df['#RestWavelength(Angs)'], 
                           y=df['f$_\lambda$'], 
                           mode='lines', 
                           name=key[11:],
                           line=dict(width=1, color=line_color),
                           )

        fig.add_trace(trace, row=row_index, col=1)

    # Add vertical lines for wavelengths if provided (outside the loop)
    if lines and wavelengths:
        for line, wavelength in zip(lines, wavelengths):
            for i, (galaxy_name, row_index) in enumerate(zip(unique_galaxy_names, range(1, num_rows+1)), start=1):
                fig.add_shape(type="line",
                              x0=wavelength, y0=0, x1=wavelength, y1=2,
                              line=dict(color="black", width=1, dash="dash"),
                              name=line,
                              row=row_index, col=1
                             )
                # Add annotation for line name
                fig.add_annotation(x=wavelength, y=0, text=line,
                                   showarrow=False, yshift=-20, xshift=-3, textangle=270, row=row_index, col=1)

    # Update layout
    fig.update_layout(title='The spectroscopic sequences of the ECLE sample',
                      xaxis_title=r'Rest Wavelength [Å]',
                      yaxis_title='log<sub>10</sub> (Scaled f<sub>λ</sub>)',
                      #showlegend=True,
                      height=h_factor*num_rows,
                      xaxis=dict(range=[3490, 8000], title=dict(text="Rest Wavelength [Å]", standoff=1222)),
                      #colorway=px.colors.sequential.Viridis,
                      )

    # Apply CSS styling to reduce spacing between rows
    fig.update_layout(
        margin=dict(l=0, r=0, t=80, b=0, pad=0),
    )

    # Update yaxis range for all rows
    for row_index in range(1, num_rows + 1):
        fig.update_yaxes(range=[0, 2], row=row_index, col=1)


    return fig
