import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_rating_distribution():
    # Load the dataset
    df = pd.read_csv('recommender/dataset/resort_data.csv')  # Ensure correct path

    # Create the plot
    plt.figure(figsize=(8, 5))
    sns.histplot(df['rating'], bins=5, kde=True)
    plt.title('Resort Rating Distribution')
    plt.xlabel('Ratings')
    plt.ylabel('Count')

    # Show the plot
    plt.show()
