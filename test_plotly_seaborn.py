import pandas as pd
from dataframe import create_dataframe_pd
from sqlalchemy import create_engine

db_engine = create_engine('postgresql+psycopg2://chinook:chinook@localhost:5433/chinook_auto_increment')
    

df = create_dataframe_pd(db_engine, "SELECT g.name AS genre_name, COUNT(t.track_id) AS total_tracks, AVG(t.milliseconds) AS avg_track_duration \
FROM genre g \
JOIN track t ON g.genre_id = t.genre_id \
GROUP BY g.name \
HAVING COUNT(t.track_id) > 100 \
ORDER BY total_tracks DESC")

import matplotlib.pyplot as plt
import seaborn as sns
# df is assumed to be pre-loaded with the data

plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='total_tracks', y='genre_name')
plt.title('Total Tracks by Genre')
plt.xlabel('Total Tracks')
plt.ylabel('Genre')
# plt.savefig('chart.png')
plt.show()