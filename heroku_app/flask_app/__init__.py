from flask import Flask, render_template


def create_app():
    from flask_app.module.dbModule import Database
    from flask_app.module.visualiser import Visualiser


    app = Flask(__name__)

    @app.route('/')
    def index():
        database = Database()
        query_list_all = f"""SELECT * FROM webtoons WHERE day='tue' ORDER BY rate DESC"""
        res = database.execute_all(query_list_all)
        database.db_close()

        return render_template("index.html", res=res), 200
    
    # @app.route('/search/',defaults={'input':'추천 웹툰'}, methods=['GET'])
    @app.route('/search/<kw>',methods=['GET'])
    def search(kw):
        database = Database()
        query_list_all = f"""SELECT * FROM webtoons WHERE title LIKE '%%{kw}%%' ORDER BY rate DESC"""
        res = database.execute_all(query_list_all)
        database.db_close()
        # res=query_list_all
        return render_template('search.html', kw=kw, res=res)
    
    @app.route('/dashboard/',methods=['GET'])
    def dashboard():
        database = Database()
        query_top1_views_day = f"""SELECT * FROM webtoons WHERE views_rank=1"""
        top1_views_day = database.execute_all(query_top1_views_day)

        query_top10_rate = f"""SELECT * FROM webtoons ORDER BY rate DESC LIMIT 10"""
        top10_rate = database.execute_all(query_top10_rate)

        query_count_genre = f"""SELECT genre, COUNT(*) 
        FROM webtoons 
        GROUP BY genre 
        ORDER BY COUNT(*) 
        DESC LIMIT 5"""
        count_genre = database.execute_all(query_count_genre)

        query_rank_genre = f"""SELECT sub.genre, COUNT(*)
        FROM (SELECT title, genre FROM webtoons WHERE views_rank < 20) AS sub
        GROUP BY sub.genre
        ORDER BY COUNT(*) DESC
        LIMIT 5"""
        rank_genre = database.execute_all(query_rank_genre)
    
        database.db_close()

        visual = Visualiser()
        visual.pie(count_genre,"장르별 작품 수")
        visual.hbar(rank_genre,"장르별 인기도")
        
        return render_template('dashboard.html', 
                                top1_views_day=top1_views_day,
                                top10_rate=top10_rate,
                                )

    # @app.route('/result/',defaults={'username':'이름도 몰라서 어떻게 코딩할래'}, methods=['GET'])
    # @app.route('/result/<username>', methods=['GET'])
    # def result(username):
    #     return render_template('result.html', username=username)

    if __name__ == '__main__':
        app.run(debug=True)

    return app