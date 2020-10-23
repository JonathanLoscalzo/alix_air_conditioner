import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_summary_total_amount(df_train):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), sharex=True, sharey=True)
    df_train[df_train["Stage"] == "Closed Won"].Total_Amount.plot.hist(ax=ax1)
    ax1.legend()
    ax1.set_title("Closed Won")

    df_train[df_train["Stage"] == "Closed Lost"].Total_Amount.plot.hist(ax=ax2)
    ax2.set_title("Closed Lost")
    ax2.legend()
    plt.show()
    sns.boxplot(x="Total_Amount", y="Stage", data=df_train)

def plot_learning_curve(results):
    pd.Series(results['train']['binary_logloss'], name="Train").plot.line()
    pd.Series(results['test']['binary_logloss'], name="Test").plot.line()
    plt.legend()
    plt.xlabel('epochs')
    plt.ylabel('binary_logloss')

