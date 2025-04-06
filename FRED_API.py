import requests
import pandas as pd

def fetch_fred_data(start_date="2000-01-01", end_date="2025-01-01", api_key_path="fred_api_key.txt"):
    """Fetch economic indicators from the FRED API with minimal processing."""

    print("🚀 Fetching data from FRED API...")

    # Define economic indicators
    series_ids = {
        "GDP": ("GDPC1", "Q"),
        'Real Consumer Exp': ('PCEC96','Q'),
        'Business Inv': ('W790RC1Q027SBEA','Q'),
        'Govt Expenditure': ('W068RCQ027SBEA', 'Q'),
        'Net Exports': ('NETEXC', 'Q'),
        'Imports': ('IMPGSCA', 'Q'),
        'Exports': ('EXPGSC1', 'Q'),
        'CPI': ('CPIAUCSL', 'M'),
        "US Grocery Sales": ("RSGCS", "M"),  
        "US Food Service and Drinking Places": ("RSFSDP", "M"),
        "CPI (Food at Home)": ("CUSR0000SAF11", "M"),
        "Real Disposable Income": ("DSPIC96", "M"),
        "Unemployment Rate": ("UNRATE", "M"),
        "Initial Jobless Claims": ("ICSA", "W"),
        "Continued Jobless Claims": ("CCSA", "W"),
        "GDP": ("GDPC1", "Q"),
        "Personal Savings": ("PMSAVE", "M"),
        "Consumer Debt % DI": ("CDSP", "Q"),
        "Credit Card Delinquency": ("DRCCLACBS", "Q"),
        "Mortgage Delinquency": ("DRSFRMACBS", "Q"),
        "Oil Prices": ("DCOILWTICO", "D"),
        "US Grocery Sales": ("RSGCS", "M"),          
        "CPI (Food at Home)": ("CUSR0000SAF11", "M"),
        "Restaurant Sales": ('MRTSSM7225USN', "M"),
        "Avg Home Price": ("CSUSHPINSA", "M"),
        "Consumer Sentiment": ("UMCSENT", "M"),
        "Avg Home Price": ("CSUSHPINSA", "M"),
        "Consumer Sentiment": ("UMCSENT", "M"),
        "PPI Farm Products": ("WPU01", "M"),
        "PPI Final Food": ("PPIDFS", "M"),
        "PPI Food and Feed": ("WPU02", "M"),
        "PPI Finished Consumer Goods": ("WPSFD4111", "M"),
        "PPI Food Manufacture": ("PCU311311", "M"),
        "PPI Grocery": ("PCU445110445110", "M"),
        "Retail Wages": ("CES4200000003", "M")
    }


    # Read API key
    try:
        with open(api_key_path, "r") as file:
            API_KEY = file.read().strip()
    except FileNotFoundError:
        print("❌ ERROR: API Key file not found!")
        return pd.DataFrame()  

    df_list = []

    for name, (series_id, frequency) in series_ids.items():
        print(f"🔄 Fetching {name} ({series_id})...")

        url = (f"https://api.stlouisfed.org/fred/series/observations?"
               f"series_id={series_id}&api_key={API_KEY}&file_type=json&"
               f"observation_start={start_date}&observation_end={end_date}")
        
        response = requests.get(url)
        data = response.json()

        if "observations" not in data or not data["observations"]:
            print(f"❌ No data retrieved for {name}")
            continue  

        df = pd.DataFrame(data["observations"])
        df["date"] = pd.to_datetime(df["date"])
        df[name] = pd.to_numeric(df["value"], errors="coerce")
        df = df[["date", name]]

        df.set_index("date", inplace=True)

        # Handle different frequencies
        if frequency == "Q":  # Convert quarterly to monthly
            df = df.resample("M").ffill()
            df.index = df.index.to_period("M").to_timestamp()

        elif frequency == "D":  # Convert daily to monthly (average)
            df = df.resample("M").mean()
            df.index = df.index.to_period("M").to_timestamp()

        elif frequency == "W":  # Convert weekly to monthly (sum)
            df = df.resample("M").sum()
            df.index = df.index.to_period("M").to_timestamp()

        df_list.append(df)

    if not df_list:
        print("❌ No valid data retrieved. Returning an empty DataFrame.")
        return pd.DataFrame(columns=["date"] + list(series_ids.keys()))

    # ✅ Merge all datasets
    final_df = df_list[0]
    for df in df_list[1:]:
        final_df = final_df.merge(df, on="date", how="outer")

    print("\n📊 Final Merged Data Preview:")
    print(final_df.head())  # Display first rows for debugging
    return final_df

if __name__ == "__main__":
    print("🚀 Running FRED API Test...")
    df = fetch_fred_data()

    print("📌 Final DataFrame Info:")
    print(df.info())  
    print("📊 First Few Rows of Data:")
    print(df.head())  

    # Save the DataFrame to CSV
    output_path = "fred_data.csv"
    df.to_csv(output_path)
    print(f"✅ Data saved to {output_path}")

