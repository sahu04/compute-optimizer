import sys
import json
import pandas as pd

# Set Pandas display options
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Get input JSON file and output CSV file from command line arguments
jsonfile = str(sys.argv[1])
csvfile = str(sys.argv[2])

# Read JSON file and load data into a dictionary
with open(jsonfile) as file:
    data = json.load(file)

# Check if the top-level structure is a list
if isinstance(data, list) and data:
    # Access the first element of the list
    data = data[0]

# Check if the key 'instanceRecommendations' is present
if 'instanceRecommendations' in data:
    # Create a DataFrame from 'instanceRecommendations' field
    df = pd.DataFrame(data['instanceRecommendations'])

    # Check if 'utilizationMetrics' and 'recommendationOptions' are present
    if 'utilizationMetrics' in df.columns and 'recommendationOptions' in df.columns:
        # Extract and flatten 'utilizationMetrics' field
        for i, item in enumerate(df['utilizationMetrics']):
            for k, metric in enumerate(item):
                metric_name = metric['name']
                metric_statistic = metric['statistic']
                metric_value = metric['value']

                # Add new columns with flattened data
                df.at[i, f'utilizationMetrics_name_{k}'] = metric_name
                df.at[i, f'utilizationMetrics_statistic_{k}'] = metric_statistic
                df.at[i, f'utilizationMetrics_value_{k}'] = metric_value

        # Extract and flatten 'recommendationOptions' field
        for i, options in enumerate(df['recommendationOptions']):
            for m, option in enumerate(options):
                instance_type = option['instanceType']
                performance_risk = option['performanceRisk']
                rank = option['rank']

                # Add new columns with flattened data
                df.at[i, f'recommendationOptions_instanceType_{m}'] = instance_type
                df.at[i, f'recommendationOptions_performanceRisk_{m}'] = performance_risk
                df.at[i, f'recommendationOptions_rank_{m}'] = rank

                # Flatten 'projectedUtilizationMetrics' within 'recommendationOptions'
                for j, projected_metric in enumerate(option.get('projectedUtilizationMetrics', [])):
                    metric_name = projected_metric.get('name', '')
                    metric_statistic = projected_metric.get('statistic', '')
                    metric_value = projected_metric.get('value', '')

                    # Add new columns with flattened data
                    df.at[i, f'reco_projectedUtilizationMetrics_{m}_{j}_name'] = metric_name
                    df.at[i, f'reco_projectedUtilizationMetrics_{m}_{j}_statistic'] = metric_statistic
                    df.at[i, f'reco_projectedUtilizationMetrics_{m}_{j}_value'] = metric_value

        # Drop original 'utilizationMetrics' and 'recommendationOptions' columns
        df = df.drop(['utilizationMetrics', 'recommendationOptions'], axis=1)

        # Write DataFrame to CSV file
        df.to_csv(csvfile, header=True, index=False)
        print(f"CSV File generated at: {csvfile}")
    else:
        print("Error: 'utilizationMetrics' or 'recommendationOptions' columns not found in the DataFrame.")
else:
    print("Error: 'instanceRecommendations' key not found in the JSON data.")





