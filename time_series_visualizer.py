import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
df.columns = ["views"]

# Clean data
df = df[(df["views"] <= df["views"].quantile(0.975)) & (df["views"] >= df["views"].quantile(0.025))]


def draw_line_plot():
    fig = plt.figure(figsize=(12,7))
    plt.plot(df.index, df["views"])
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")





    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["month"] = pd.to_datetime(df_bar.index, format="%B").month_name()
    df_bar["year"] = df_bar.index.year
    missing = {
        "year": [2016,2016,2016,2016],
        "month": ['January', 'February', 'March', 'April'],
        "views": [0,0,0,0]
    }
    df_bar = pd.concat((pd.DataFrame(missing), df_bar))
    df_bar = df_bar.groupby(["year", "month"])
    df_bar = df_bar["views"].mean()
    df_bar = df_bar.unstack()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    fig = df_bar.plot.bar(legend=True,label=months, use_index=True, xlabel="Years", ylabel="Average Page Views").figure
    plt.legend(months)



    # # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box["month_num"]=df_box["date"].dt.month
    df_box = df_box.sort_values("month_num")
    fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(14,4))
    axes[0] = sns.boxplot(x="year", y="views", data=df_box, ax=axes[0])
    axes[1] = sns.boxplot(x="month", y="views", data=df_box, ax=axes[1])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[0].set_ylabel("Page Views")
    axes[1].set_ylabel("Page Views")
    axes[0].set_xlabel("Year")
    axes[1].set_xlabel("Month")




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig