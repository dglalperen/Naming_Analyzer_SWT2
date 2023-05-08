import pandas as pd
from sonar_analyzer import analyze_naming_conventions



if __name__ == '__main__':
    df = pd.read_csv('repositories.csv')
    analyze_naming_conventions(df, "javascript")



