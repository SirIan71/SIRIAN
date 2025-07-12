import pandas as pd
import numpy as np

# Read the merged data with low_memory=False to handle mixed types
print("Reading merged_data_1.csv...")
df = pd.read_csv('data/merged_data_1.csv', low_memory=False)

print(f"Original data shape: {df.shape}")

# Convert Date column to datetime, handling any invalid dates
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Remove rows with invalid dates
df = df.dropna(subset=['Date'])

print(f"Data shape after cleaning dates: {df.shape}")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")

# Define odds-related columns based on the documentation
odds_columns = [
    # Basic match odds (1X2 betting)
    'GBH', 'GBD', 'GBA', 'IWH', 'IWD', 'IWA', 'LBH', 'LBD', 'LBA', 
    'SBH', 'SBD', 'SBA', 'WHH', 'WHD', 'WHA', 'SYH', 'SYD', 'SYA',
    'B365H', 'B365D', 'B365A', 'SOH', 'SOD', 'SOA', 'BWH', 'BWD', 'BWA',
    'SJH', 'SJD', 'SJA', 'VCH', 'VCD', 'VCA', 'BSH', 'BSD', 'BSA',
    'PSH', 'PSD', 'PSA', 'PSCH', 'PSCD', 'PSCA',
    
    # Total goals betting odds
    'GB>2.5', 'GB<2.5', 'B365>2.5', 'B365<2.5', 'P>2.5', 'P<2.5',
    'PC>2.5', 'PC<2.5', 'B365C>2.5', 'B365C<2.5',
    
    # Asian handicap betting odds
    'GBAHH', 'GBAHA', 'GBAH', 'LBAHH', 'LBAHA', 'LBAH', 'B365AHH', 'B365AHA', 'B365AH',
    'PAHH', 'PAHA', 'B365CAHH', 'B365CAHA', 'PCAHH', 'PCAHA',
    
    # BetBrain aggregated odds
    'Bb1X2', 'BbMxH', 'BbAvH', 'BbMxD', 'BbAvD', 'BbMxA', 'BbAvA',
    'BbOU', 'BbMx>2.5', 'BbAv>2.5', 'BbMx<2.5', 'BbAv<2.5',
    'BbAH', 'BbAHh', 'BbMxAHH', 'BbAvAHH', 'BbMxAHA', 'BbAvAHA',
    
    # Market aggregated odds
    'MaxH', 'MaxD', 'MaxA', 'AvgH', 'AvgD', 'AvgA',
    'Max>2.5', 'Max<2.5', 'Avg>2.5', 'Avg<2.5',
    'MaxAHH', 'MaxAHA', 'AvgAHH', 'AvgAHA',
    'MaxCH', 'MaxCD', 'MaxCA', 'AvgCH', 'AvgCD', 'AvgCA',
    'MaxC>2.5', 'MaxC<2.5', 'AvgC>2.5', 'AvgC<2.5',
    'MaxCAHH', 'MaxCAHA', 'AvgCAHH', 'AvgCAHA',
    
    # Closing odds (with 'C' suffix)
    'B365CH', 'B365CD', 'B365CA', 'BWCH', 'BWCD', 'BWCA',
    'IWCH', 'IWCD', 'IWCA', 'WHCH', 'WHCD', 'WHCA',
    'VCCH', 'VCCD', 'VCCA', 'AHCh',
    
    # Betfair odds
    'BFH', 'BFD', 'BFA', '1XBH', '1XBD', '1XBA', 'BFEH', 'BFED', 'BFEA',
    'BFE>2.5', 'BFE<2.5', 'BFEAHH', 'BFEAHA', 'BFCH', 'BFCD', 'BFCA',
    '1XBCH', '1XBCD', '1XBCA', 'BFECH', 'BFECD', 'BFECA',
    'BFEC>2.5', 'BFEC<2.5', 'BFECAHH', 'BFECAHA'
]

# Filter columns that actually exist in the dataset
existing_odds_columns = [col for col in odds_columns if col in df.columns]
print(f"Found {len(existing_odds_columns)} odds-related columns out of {len(odds_columns)} defined")

# Create odds dataframe with Date and all odds columns
odds_data = df[['Date'] + existing_odds_columns].copy()

# Remove rows where all odds columns are NaN (no odds data available)
odds_data_clean = odds_data.dropna(subset=existing_odds_columns, how='all')

print(f"Odds data shape after removing rows with no odds: {odds_data_clean.shape}")

# Save the odds data
odds_data_clean.to_csv('data/odds_data.csv', index=False)
print("Odds data saved to data/odds_data.csv")

# Show some statistics
print(f"\nOdds data statistics:")
print(f"Date range: {odds_data_clean['Date'].min()} to {odds_data_clean['Date'].max()}")
print(f"Number of unique dates: {odds_data_clean['Date'].nunique()}")

# Show which odds columns have the most data
odds_coverage = odds_data_clean[existing_odds_columns].notna().sum().sort_values(ascending=False)
print(f"\nTop 10 odds columns by data coverage:")
print(odds_coverage.head(10)) 