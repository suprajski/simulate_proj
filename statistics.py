import pandas as pd

files = [
    "cupy_pt1_28342235.out",  
    "cupy_pt2_28342287.out",  
    "cupy_pt3_28342359.out",   
    "cupy_pt4_28342462.out",  
]

dataframes = []
for file in files:
    header_line_num = 0
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith('building_id'):
                header_line_num = i
                break
                
    df_part = pd.read_csv(file, skiprows=header_line_num, skipinitialspace=True)
    dataframes.append(df_part)

df = pd.concat(dataframes, ignore_index=True)

cols_to_convert = ["mean_temp", "std_temp", "pct_above_18", "pct_below_15"]
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    
avg_mean_temp = df["mean_temp"].mean()
avg_std_temp = df["std_temp"].mean()
count_above_18 = (df["pct_above_18"] >= 50).sum()
count_below_15 = (df["pct_below_15"] >= 50).sum()
total_valid_buildings = df["mean_temp"].notna().sum()

print(f"Total buildings successfully parsed: {total_valid_buildings}")
print(f"Average Mean Temperature: {avg_mean_temp:.2f} C")
print(f"Average Temperature Standard Deviation: {avg_std_temp:.2f} C")
print(f"Buildings with >= 50% area above 18C: {count_above_18}")
print(f"Buildings with >= 50% area below 15C: {count_below_15}")