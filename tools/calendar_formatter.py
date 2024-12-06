import pandas as pd

# 读取输入文件
input_file = "test_calendar.csv"
output_file = "google_calendar.csv"

df = pd.read_csv(input_file)

# 定义转换函数
def format_date_time(row):
    if row["All Day Event"] == "TRUE":
        # 当 All Day Event 为 TRUE，使用 YYYY/MM/DD 格式
        start_date = pd.to_datetime(row["Event start time"]).strftime("%Y/%m/%d")
        end_date = pd.to_datetime(row["Event end time"]).strftime("%Y/%m/%d")
        start_time = ""
        end_time = ""
    else:
        # 当 All Day Event 为 FALSE，使用 MM/DD/YYYY 和 12小时制时间格式
        start_date = pd.to_datetime(row["Event start time"]).strftime("%m/%d/%Y")
        end_date = pd.to_datetime(row["Event end time"]).strftime("%m/%d/%Y")
        start_time = pd.to_datetime(row["Event start time"]).strftime("%I:%M %p")
        end_time = pd.to_datetime(row["Event end time"]).strftime("%I:%M %p")
    return pd.Series([start_date, start_time, end_date, end_time])

# 动态设置 All Day Event 列
df["All Day Event"] = df["Whether recurring"].apply(lambda x: "TRUE" if x == "1-Day Time Off" else "FALSE")

# 应用日期和时间格式化函数
df[["Start Date", "Start Time", "End Date", "End Time"]] = df.apply(format_date_time, axis=1)

# 构造最终的输出 DataFrame
output = pd.DataFrame({
    "Subject": df["Subject"],  # 保留事件标题
    "Start Date": df["Start Date"],
    "Start Time": df["Start Time"],
    "End Date": df["End Date"],
    "End Time": df["End Time"],
    "All Day Event": df["All Day Event"],
    "Description": df["Description"].replace("None", ""),
    "Location": df["Location"].replace("None", ""),
    "Private": "FALSE",  # 默认设置为非私密事件
})

# 保存为新的 CSV 文件
output.to_csv(output_file, index=False)

print(f"output: {output_file}")