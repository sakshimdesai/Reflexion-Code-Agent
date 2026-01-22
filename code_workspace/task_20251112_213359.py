import subprocess
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Check if matplotlib is installed
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print("Matplotlib is not installed. Trying to install it...")
    
    # Install matplotlib using pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    
    # Try importing matplotlib again
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        print("Failed to install matplotlib. Please install it manually.")
        exit(1)

def plot_average_sales_per_region(csv_file):
    """
    Reads a CSV file and plots a bar chart of average sales per region.
    
    Args:
    csv_file (str): Path to the CSV file containing sales data.
    """
    try:
        # Read the CSV file
        sales_data = pd.read_csv(csv_file)
        
        # Ensure necessary columns exist in the CSV file
        required_columns = ['Region', 'Sales']
        if not all(column in sales_data.columns for column in required_columns):
            raise ValueError("The CSV file must contain 'Region' and 'Sales' columns.")
        
        # Group sales data by region and calculate the average sales
        average_sales_per_region = sales_data.groupby('Region')['Sales'].mean().reset_index()
        
        # Create a bar chart of average sales per region
        plt.figure(figsize=(10, 6))
        plt.bar(average_sales_per_region['Region'], average_sales_per_region['Sales'])
        plt.xlabel('Region')
        plt.ylabel('Average Sales')
        plt.title('Average Sales per Region')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        print("The CSV file was not found. Please ensure the file exists and is in the correct location.")
    except pd.errors.EmptyDataError:
        print("The CSV file is empty. Please ensure the file contains data.")
    except pd.errors.ParserError:
        print("An error occurred while parsing the CSV file. Please ensure the file is in a valid format.")
    except Exception as e:
        print("An error occurred: ", str(e))

def main():
    csv_file = 'sales_data.csv'  # replace with your CSV file
    plot_average_sales_per_region(csv_file)

if __name__ == "__main__":
    main()
