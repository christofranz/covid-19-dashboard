import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def load_dataset():
    df = pd.read_csv("data/covid_19.csv")
    cumulative_df = df.groupby(["countryterritoryCode"]).sum()["cases"].reset_index()
    country_df = df[["countriesAndTerritories", "countryterritoryCode"]].drop_duplicates().reset_index()
    df_merged = pd.merge(cumulative_df, country_df, on="countryterritoryCode")
    return df_merged

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    df = pd.read_csv("data/covid_19.csv")
    cumulative_df = df.groupby(["countryterritoryCode"]).sum()[["cases", "deaths"]].reset_index()
    country_df = df[["countriesAndTerritories", "countryterritoryCode"]].drop_duplicates().reset_index()
    df_merged = pd.merge(cumulative_df, country_df, on="countryterritoryCode")
  
    graph_one = []
    df["time"] = pd.to_datetime(df[["day", "month", "year"]])
    country_of_interest = ["United_States_of_America", "China", "Taiwan", "Italy", "Spain", "France", "Germany", "Iran", "Japan", "South_Corea"]
    for country in country_of_interest:
        df_country = df[df["countriesAndTerritories"] == country]
        df_country_sorted = df_country.sort_values(by='time')
        graph_one.append(
          go.Scatter(
          x = df_country_sorted["time"],
          y = df_country_sorted["cases"],
          mode = 'lines+markers',
          name = country
          )
    )

    layout_one = dict(title = 'Confirmed Cases per Day and Country',
                xaxis = dict(title = 'time'),
                yaxis = dict(title = 'Cases per day'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    df_merged["ratio"] = df_merged["deaths"] / df_merged["cases"]
    df_ratio = df_merged.sort_values(by="ratio", ascending=False)
    df_ratio = df_ratio[df_ratio["cases"] > 1000]
    df_ratio["ratio"] = df_ratio["ratio"] * 100
    countries_high = df_ratio["countriesAndTerritories"][:10].tolist()

    graph_two.append(
        go.Bar(
            x = countries_high,
            y = df_ratio.iloc[:10].ratio.tolist(),
            name = "death ratio"
        )
    )
    layout_two = dict(title = 'Death Ratio Per Country',
                barmode = "group",
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Death Ratio [%]')
                )
    
    # world map
    
    graph_five = []
    graph_five.append(go.Choropleth(
        locations = df_merged['countryterritoryCode'],
        z = df_merged['cases'],
        text = df_merged['countriesAndTerritories'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=False))

    layout_five = dict(title = 'Confirmed COVID-19 cases 20/04/08',
                title_x=0.5,
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                ),
                marker_line_color='darkgray',
                marker_line_width=0.5,
                colorbar_tickprefix = '',
                colorbar_title = 'Confirmed Cases',
                annotations = [dict(
                    x=0.55,
                    y=0.1,
                    xref='paper',
                    yref='paper',
                    text='Source: <a href="https://data.europa.eu/euodp/de/data/dataset/covid-19-coronavirus-data">data.europe</a>',
                    showarrow = False)]
                )
    
    
    
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_five, layout=layout_five))                               
    
   
    return figures
