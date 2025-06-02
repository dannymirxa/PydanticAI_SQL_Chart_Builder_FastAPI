import plotly.express as px
from app.dataframe import create_dataframe_pd
from sqlalchemy import create_engine
# df is assumed to be pre-loaded with the data
db_engine = create_engine('postgresql+psycopg2://chinook:chinook@localhost:5433/chinook_auto_increment')
    

df = create_dataframe_pd(db_engine, "SELECT artist.name AS artist_name, COUNT(album.album_id) AS album_count FROM artist LEFT JOIN album ON artist.artist_id = album.artist_id GROUP BY artist.name ORDER BY album_count DESC")


# Creating the bar graph
fig = px.bar(df, x='artist_name', y='album_count', title='Album Counts by Artist')
fig.write_html('chart.html')
# fig.show()