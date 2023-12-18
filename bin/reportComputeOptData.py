
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
                df.at[i, 'utilizationMetrics_name_{}'.format(k)] = metric_name
                df.at[i, 'utilizationMetrics_statistic_{}'.format(k)] = metric_statistic
                df.at[i, 'utilizationMetrics_value_{}'.format(k)] = metric_value

        # Extract and flatten 'recommendationOptions' field
        for i, options in enumerate(df['recommendationOptions']):
            for m, option in enumerate(options):
                instance_type = option['instanceType']
                performance_risk = option['performanceRisk']
                rank = option['rank']

                # Add new columns with flattened data
                df.at[i, 'recommendationOptions_instanceType_{}'.format(m)] = instance_type
                df.at[i, 'recommendationOptions_performanceRisk_{}'.format(m)] = performance_risk
                df.at[i, 'recommendationOptions_rank_{}'.format(m)] = rank

                # Flatten 'projectedUtilizationMetrics' within 'recommendationOptions'
                for j, projected_metric in enumerate(option.get('projectedUtilizationMetrics', [])):
                    metric_name = projected_metric.get('name', '')
                    metric_statistic = projected_metric.get('statistic', '')
                    metric_value = projected_metric.get('value', '')

                    # Add new columns with flattened data
                    df.at[i, 'reco_projectedUtilizationMetrics_{}_{}_name'.format(m, j)] = metric_name
                    df.at[i, 'reco_projectedUtilizationMetrics_{}_{}_statistic'.format(m, j)] = metric_statistic
                    df.at[i, 'reco_projectedUtilizationMetrics_{}_{}_value'.format(m, j)] = metric_value

        # Drop original 'utilizationMetrics' and 'recommendationOptions' columns
        df = df.drop(['utilizationMetrics', 'recommendationOptions'], axis=1)

        # Write DataFrame to CSV file
        df.to_csv(csvfile, header=True, index=False)
       print("CSV File generated at: {}".format(csvfile))
    else:
        print("Error: 'utilizationMetrics' or 'recommendationOptions' columns not found in the DataFrame.")
else:
    print("Error: 'instanceRecommendations' key not found in the JSON data.")




