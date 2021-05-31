from flask import Flask, redirect, url_for, render_template, request
import mysql.connector as db_conn

from database_ops import TABLES, INSERT_OPS, SELECT_OPS, TRIGGERS

app = Flask(__name__)

my_db = db_conn.connect(
    host='localhost',
    user='root',
    password='Ye110w.1997',
    database='coin_portfolio'
)

my_cursor = my_db.cursor()

for create_table in reversed(TABLES.keys()):
    my_cursor.execute("DROP TABLE IF EXISTS " + create_table, ";")
for create_table in TABLES.values():
    my_cursor.execute(create_table)

my_cursor.execute(TRIGGERS['update_coin_num'])

my_cursor.execute(INSERT_OPS['add_user'], ("furkankalabalik34@gmail.com", "demo", "Furkan", "Kalabalık"))
my_cursor.execute(INSERT_OPS['add_user'], ("alicewonder@gmail.com", "demo", "Alice", "Wonderlan"))
my_cursor.execute(INSERT_OPS['add_user'], ("terryjohn@gmail.com", "demo", "John", "Terry"))
my_cursor.execute(INSERT_OPS['add_user'], ("carter1970@gmail.com", "demo", "Josh", "Carter"))
my_cursor.execute(INSERT_OPS['add_user'], ("stanleyrulez@gmail.com", "demo", "Bob", "Stanley"))
my_cursor.execute(INSERT_OPS['add_user'], ("monicalover@gmail.com", "demo", "Monica", "Schwartz"))

my_cursor.execute(INSERT_OPS['add_coin'], ("BTC", "672697296515", "35941.89", "64863.10", "8975.53"))
my_cursor.execute(INSERT_OPS['add_coin'], ("ETH", "284037393904", "2436.84", "4362.35", "219.47"))
my_cursor.execute(INSERT_OPS['add_coin'], ("BNB", "50464681499", "328.90", "690.93", "15.02"))
my_cursor.execute(INSERT_OPS['add_coin'], ("SHIB", "3128075307", "0.000007943", "0.0000388", "0.00"))
my_cursor.execute(INSERT_OPS['add_coin'], ("CAKE", "2634710107", "16.03", "44.18", "0.198"))
my_cursor.execute(INSERT_OPS['add_coin'], ("BTT", "2406474443", "0.003646", "0.01426", "0.0002714"))
my_cursor.execute(INSERT_OPS['add_coin'], ("CHZ", "1601543202", "0.2731", "0.8915", "0.008867"))
my_cursor.execute(INSERT_OPS['add_coin'], ("ENJ", "1205253660", "1.44", "4.00", "0.1115"))

my_cursor.execute(INSERT_OPS['add_portfolio'], ("Altcoins", "2021-02-14", "53.65", "1"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("Shitcoins", "2020-08-25", "64.53", "3"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("Altcoins", "2021-02-11", "20.65", "2"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("Shitcoins", "2020-11-25", "45.53", "4"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("demo", "2021-02-14", "53.65", "5"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("lambo", "2020-08-25", "64.53", "6"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("gateio", "2021-02-11", "20.65", "2"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("binance", "2020-11-25", "45.53", "4"))

my_cursor.execute(INSERT_OPS['add_platform'], ("Binance", "31483086126"))
my_cursor.execute(INSERT_OPS['add_platform'], ("Gate.io", "1115835289"))
my_cursor.execute(INSERT_OPS['add_platform'], ("Huobi", "8913185754"))

my_cursor.execute(INSERT_OPS['add_listing'], ("35785.34", "4104984874", "BTC", "1"))
my_cursor.execute(INSERT_OPS['add_listing'], ("35872.85", "1383190231", "BTC", "3"))
my_cursor.execute(INSERT_OPS['add_listing'], ("331.20", "15878431", "BNB", "2"))
my_cursor.execute(INSERT_OPS['add_listing'], ("331.42", "1444364453", "BNB", "1"))

# amount, portfolio_id, listing_id
my_cursor.execute(INSERT_OPS['add_to_portfolio'], ("3", "2", "2"))
my_cursor.execute(INSERT_OPS['add_to_portfolio'], ("0.25", "1", "3"))
my_cursor.execute(INSERT_OPS['add_to_portfolio'], ("1.25", "4", "4"))
my_db.commit()


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "GET":
        my_cursor.execute(SELECT_OPS['get_users'])

        user_list = my_cursor.fetchall()
        return render_template("index.html", content=user_list)
    else:
        user = request.form['user_id']
        return redirect(url_for("user_page", usr_id=user))


@app.route('/users/<usr_id>', methods=["POST", "GET"])
def user_page(usr_id):
    if request.method == "GET":
        my_cursor.execute(SELECT_OPS['get_portfolio_with_user_id'] % usr_id)
        portfolio = my_cursor.fetchall()
        return render_template("user_page.html", content=portfolio)
    else:
        portfolio_id = request.form['portfolio_id']
        return redirect(url_for("user_portfolio", usr_id=usr_id, portfolio_id=portfolio_id))


@app.route('/users/<usr_id>/<portfolio_id>')
def user_portfolio(usr_id, portfolio_id):
    my_cursor.execute('''SELECT listing.alias, platform.platform_name, includes.amount
                         FROM includes
                         INNER JOIN listing
                         ON includes.list_id = listing.list_id
                         INNER JOIN platform
                         ON listing.platform_id = platform.platform_id
                         WHERE includes.portfolio_id = ''' + portfolio_id)
    portfolio = my_cursor.fetchall()
    return render_template("portfolio.html", content=portfolio)


@app.route('/coins')
def coin_list():
    my_cursor.execute(SELECT_OPS['get_coins'])
    coins = my_cursor.fetchall()
    return render_template("coins.html", content=coins)


@app.route('/platforms', methods=["POST", "GET"])
def platform_list():
    if request.method == "GET":
        my_cursor.execute(SELECT_OPS['get_platforms'])
        platforms = my_cursor.fetchall()
        return render_template("platforms.html", content=platforms)
    else:
        platform_id = request.form['platform_id']
        return redirect(url_for("platform_coins", platform_id=platform_id))


@app.route('/platforms/<platform_id>')
def platform_coins(platform_id):
    my_cursor.execute('''SELECT listing.alias, listing.price,listing.volume 
                         FROM listing 
                         WHERE listing.platform_id = ''' + platform_id)
    platform_listing = my_cursor.fetchall()
    return render_template("platform_listing.html", content=platform_listing)


@app.route('/coins/with_listing')
def coins_with_listing():
    my_cursor.execute('''SELECT coin.alias, listing.price, platform.platform_name FROM coin
                         LEFT JOIN listing
                         ON coin.alias = listing.alias
                         LEFT JOIN platform
                         ON platform.platform_id = listing.platform_id''')
    coin_listing = my_cursor.fetchall()
    return render_template("coins_with_listing.html", content=coin_listing)


if __name__ == '__main__':
    app.run()
