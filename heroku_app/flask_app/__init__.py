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
        time.sleep(5)
        # res=query_list_all
        return render_template('search.html', kw=kw, res=res)
    
    @app.route('/result/',defaults={'username':'이름도 몰라서 어떻게 코딩할래'}, methods=['GET'])
    @app.route('/result/<username>', methods=['GET'])
    def result(username):
        return render_template('result.html', username=username)

    if __name__ == '__main__':
        app.run(debug=True)

    return app