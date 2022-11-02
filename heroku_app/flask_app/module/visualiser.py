import plotly
# import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# from bs4 import BeautifulSoup
from flask_app.module.dbModule import Database
# from dbModule import Database

class Visualiser:
    def __init__(self):
        pass

    def pie(self, data=None, title=""):
        
        # database = Database()
        # query_count_gnere = f"""SELECT genre, COUNT(*) 
        # FROM webtoons 
        # GROUP BY genre 
        # ORDER BY COUNT(*) 
        # DESC LIMIT 5"""
        # count_gnere = database.execute_all(query_count_gnere)    
        df = pd.DataFrame(data=data,columns=['장르','작품수']).set_index("장르")
        # print(df.head())
        # df = px.data.gapminder().query("year == 2007").query("continent == 'Europe'")
        # df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
        # df = pd.DataFrame(data)
        # fig = px.pie(df, values='pop', names='country', title='Population of European continent')
        # fig = px.pie(df, title='Population of European continent')

        fig = go.Figure(data=[go.Pie(labels=df.index, values=df["작품수"], hole=.5, title=title)])
        # json_source = fig.to_json()
        fig.write_html("./flask_app/static/charts/piechart.html")
        # soup = BeautifulSoup(fig.to_html(),'html.parser')
        # html_source = soup.select_one("div")
        # parser = HTMLParser()
        # parser.feed(str(html_source))
        # print(parser.get_starttag_text())
        # file = open("test2.html",'w')
        # file.write(str(html_source))
        # file.close()
        # fig = go.Figure(data=df)
        # fig.show()
        # return json_source
    
    def hbar(self, data=None, title=""):

        df = pd.DataFrame(data=data,columns=['장르','작품수']).set_index("장르")
        df = df.sort_values(by="작품수",ascending=True)
        fig = go.Figure(data=[go.Bar(
            x=df["작품수"],
            y=df.index,
            orientation='h')])
        fig.update_layout(title_text=title)
        fig.write_html("./flask_app/static/charts/hbarchart.html")


# vis = Visualiser()
# vis.piechart()