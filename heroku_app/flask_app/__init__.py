from flask import Flask, render_template


def create_app():
    from flask_app.module.dbModule import Database
    import time

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

        database.db_close()
        
        return render_template('dashboard.html', 
                                top1_views_day=top1_views_day,
                                top10_rate=top10_rate)

    @app.route('/result/',defaults={'username':'이름도 몰라서 어떻게 코딩할래'}, methods=['GET'])
    @app.route('/result/<username>', methods=['GET'])
    def result(username):
        return render_template('result.html', username=username)

    if __name__ == '__main__':
        app.run(debug=True)

    return app