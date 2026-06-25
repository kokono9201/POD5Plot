from app.analyzer.pod5_analyzer import Pod5Analyzer
from app.analyzer.pod5_metrics import Pod5Metrics

analyzer = Pod5Analyzer(

    r"C:\Users\ychen\Downloads\PBK49690_7a41d753_0396ad4d_28.pod5"

)

df = analyzer.load()

metrics = Pod5Metrics(df)

print(df.head())

print(df.columns)

print(metrics.summary())