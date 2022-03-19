import pandas as pd

filepath = "song_data/A/B/C/TRABCEI128F424C983.json"
df = pd.read_json(filepath, lines=True)
df = pd.read_json("data/log_data/2018/11/2018-11-01-events.json", lines=True)
