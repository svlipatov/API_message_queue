import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import time

# Путь к файлу лога
log_path = Path("/usr/src/app/logs/metric_log.csv")

def create_histogram(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    df['absolute_error'].hist(ax=ax, bins=20)
    ax.set_xlabel('Absolute Error')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Absolute Errors')
    plt.savefig('/usr/src/app/logs/error_distribution.png')  # Сохраним график в ту же папку

while True:
    if log_path.exists():
        df = pd.read_csv(log_path)
        create_histogram(df)
    time.sleep(60)  # Проверять каждые 60 секунд