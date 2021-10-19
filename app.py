from flask import Flask, redirect, url_for, render_template, request
import mysql.connector as db_conn
import random

from database_ops import TABLES, INSERT_OPS, SELECT_OPS, TRIGGERS, VIEWS, PROCEDURES

app = Flask(__name__)

my_db = db_conn.connect(
    host='localhost',
    user='root',
    password='Ye110w.1997',
    database='coin_portfolio'
)
my_db.start_transaction(isolation_level='READ COMMITTED')
my_cursor = my_db.cursor()

for create_table in reversed(TABLES.keys()):
    my_cursor.execute("DROP TABLE IF EXISTS " + create_table)
for create_table in TABLES.values():
    my_cursor.execute(create_table)

for trigger in TRIGGERS.keys():
    my_cursor.execute("DROP TRIGGER IF EXISTS " + trigger)
for trigger in TRIGGERS.values():
    my_cursor.execute(trigger)

for view in VIEWS.keys():
    my_cursor.execute("DROP VIEW IF EXISTS " + view)
for view in VIEWS.values():
    my_cursor.execute(view)

for procedure in PROCEDURES.keys():
    my_cursor.execute("DROP PROCEDURE IF EXISTS " + procedure)
for procedure in PROCEDURES.values():
    my_cursor.execute(procedure)

my_db.commit()

# email, passwor, first_name, last_name
my_cursor.execute(INSERT_OPS['add_user'], ("furkankalabalik34@gmail.com", "demo", "Furkan", "Kalabalık"))
my_cursor.execute(INSERT_OPS['add_user'], ("alicewonder@gmail.com", "demo", "Alice", "Wonderlan"))
my_cursor.execute(INSERT_OPS['add_user'], ("terryjohn@gmail.com", "demo", "John", "Terry"))
my_cursor.execute(INSERT_OPS['add_user'], ("carter1970@gmail.com", "demo", "Josh", "Carter"))
my_cursor.execute(INSERT_OPS['add_user'], ("stanleyrulez@gmail.com", "demo", "Bob", "Stanley"))
my_cursor.execute(INSERT_OPS['add_user'], ("monicalover@gmail.com", "demo", "Monica", "Schwartz"))
my_cursor.execute(INSERT_OPS['add_user'], ("deneme@gmail.com", "demo", "Melike", "Kalabalık"))
my_cursor.execute(INSERT_OPS['add_user'], ("david@gmail.com", "demo", "David", "Marshall"))
my_cursor.execute(INSERT_OPS['add_user'], ("james@gmail.com", "demo", "James", "Lewis"))
my_cursor.execute(INSERT_OPS['add_user'], ("luke1970@gmail.com", "demo", "Luke", "Show"))
my_cursor.execute(INSERT_OPS['add_user'], ("rice@gmail.com", "demo", "Declan", "Rice"))
my_cursor.execute(INSERT_OPS['add_user'], ("stones@gmail.com", "demo", "John", "Stones"))

# Alias, volume, average current value, ath, atl
my_cursor.execute(INSERT_OPS['add_coin'], ("BTC", "672697296515", "35941.89", "64863.10", "8975.53"))
my_cursor.execute(INSERT_OPS['add_coin'], ("ETH", "284037393904", "2436.84", "4362.35", "219.47"))
my_cursor.execute(INSERT_OPS['add_coin'], ("BNB", "50464681499", "328.90", "690.93", "15.02"))
my_cursor.execute(INSERT_OPS['add_coin'], ("SHIB", "3128075307", "0.000007943", "0.0000388", "0.00"))
my_cursor.execute(INSERT_OPS['add_coin'], ("CAKE", "2634710107", "16.03", "44.18", "0.198"))
my_cursor.execute(INSERT_OPS['add_coin'], ("BTT", "2406474443", "0.003646", "0.01426", "0.0002714"))
my_cursor.execute(INSERT_OPS['add_coin'], ("CHZ", "1601543202", "0.2731", "0.8915", "0.008867"))
my_cursor.execute(INSERT_OPS['add_coin'], ("ENJ", "1205253660", "1.44", "4.00", "0.1115"))
my_cursor.execute(INSERT_OPS['add_coin'], ("THETA", "377551565", "9.04", "8.53", "9.83"))
my_cursor.execute(INSERT_OPS['add_coin'], ("MATIC", "1406098525", "1.41", "1.48", "1.31"))
my_cursor.execute(INSERT_OPS['add_coin'], ("XLM", "519745635", "0.3021", "0.7965", "0.06125"))
my_cursor.execute(INSERT_OPS['add_coin'], ("DAI", "374995086", "1.00", "1.14", "0.8935"))
my_cursor.execute(INSERT_OPS['add_coin'], ("TRX", "951773619", "0.07006", "0.1799", "0.01496"))
my_cursor.execute(INSERT_OPS['add_coin'], ("ALGO", "123513201", "0.9819", "1.82", "0.1984"))
my_cursor.execute(INSERT_OPS['add_coin'], ("MKR", "101136571", "2689.58", "6339.02", "422.42"))
my_cursor.execute(INSERT_OPS['add_coin'], ("XEM", "56414818", "0.1512", "0.8652", "0.04036"))

# Portfolio_name, start-date, total amount, user_id
my_cursor.execute(INSERT_OPS['add_portfolio'], ("Altcoins", "2021-02-14", "1"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("Shitcoins", "2020-08-25", "3"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("Altcoins", "2021-02-11", "2"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("Shitcoins", "2020-11-25", "4"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("demo", "2021-02-14", "5"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("lambo", "2020-08-25", "6"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("gateio", "2021-02-11", "2"))
my_cursor.execute(INSERT_OPS['add_portfolio'], ("binance", "2020-11-25", "4"))

# Platform name, volume
my_cursor.execute(INSERT_OPS['add_platform'], ("Binance", "31483086126"))
my_cursor.execute(INSERT_OPS['add_platform'], ("Gate.io", "1115835289"))
my_cursor.execute(INSERT_OPS['add_platform'], ("Huobi", "8913185754"))
my_cursor.execute(INSERT_OPS['add_platform'], ("Coinlist", "21483086126"))
my_cursor.execute(INSERT_OPS['add_platform'], ("Crypto.com", "125835289"))
my_cursor.execute(INSERT_OPS['add_platform'], ("BTCTurk", "953185754"))

# current value, volume, alias, platform_id
my_cursor.execute(INSERT_OPS['add_listing'], ("35785.34", "4104984874", "BTC", "1"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2436.95", "2840373", "ETH", "1"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.000007980", "26155361", "SHIB", "1"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.003650", "261652647", "BTT", "1"))
my_cursor.execute(INSERT_OPS['add_listing'], ("1.45", "36516774", "MATIC", "1"))
my_cursor.execute(INSERT_OPS['add_listing'], ("1.032", "725167351", "DAI", "1"))

my_cursor.execute(INSERT_OPS['add_listing'], ("35785.60", "2104984874", "BTC", "2"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2436.56", "23840373", "ETH", "2"))
my_cursor.execute(INSERT_OPS['add_listing'], ("16.077", "3161531", "CAKE", "2"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.32", "3615531", "XLM", "2"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.071", "7362713", "TRX", "2"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.16", "725167351", "XEM", "2"))

my_cursor.execute(INSERT_OPS['add_listing'], ("35785.90", "2148277861", "BTC", "3"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2436.76", "275613", "ETH", "3"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.28", "37617565", "CHZ", "3"))
my_cursor.execute(INSERT_OPS['add_listing'], ("1.45", "32767619", "ENJ", "3"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.99", "38767556", "ALGO", "3"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2689.99", "86785767899", "MKR", "3"))

my_cursor.execute(INSERT_OPS['add_listing'], ("35785.44", "124676123", "BTC", "4"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2436.98", "317613", "ETH", "4"))
my_cursor.execute(INSERT_OPS['add_listing'], ("9.0486", "37617565", "THETA", "4"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.1588", "37687812", "XEM", "4"))
my_cursor.execute(INSERT_OPS['add_listing'], ("16.099", "37856713", "CAKE", "4"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2690.00", "38787571", "MKR", "4"))

my_cursor.execute(INSERT_OPS['add_listing'], ("35785.88", "21667671", "BTC", "5"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2436.55", "162652", "ETH", "5"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.29", "36675161", "CHZ", "5"))
my_cursor.execute(INSERT_OPS['add_listing'], ("9.04999", "21671628", "THETA", "5"))
my_cursor.execute(INSERT_OPS['add_listing'], ("1", "97898761", "ALGO", "5"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.0000081", "12756123", "SHIB", "5"))

my_cursor.execute(INSERT_OPS['add_listing'], ("35785.88", "21667671", "BTC", "6"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2436.55", "162652", "ETH", "6"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.161117", "378167261", "XEM", "6"))
my_cursor.execute(INSERT_OPS['add_listing'], ("2690.000001", "376785671", "MKR", "6"))
my_cursor.execute(INSERT_OPS['add_listing'], ("16.1", "3177671", "CAKE", "6"))
my_cursor.execute(INSERT_OPS['add_listing'], ("0.0000082663", "1736671", "SHIB", "6"))

# amount, portfolio_id, listing_id
my_cursor.execute("SELECT portfolio_id FROM portfolio")
portfolio_id_list = my_cursor.fetchall()
my_cursor.execute("SELECT list_id FROM listing")
listing_list = my_cursor.fetchall()
for portfolio in portfolio_id_list:
    for number in range(6):
        try:
            my_cursor.execute(INSERT_OPS['add_to_portfolio'],
                              (
                                  str(round(random.uniform(0, 10), 5)), str(portfolio[0]),
                                  str(random.choice(listing_list)[0])))
        except:
            print("Key error")

        my_db.commit()

# add coin news
my_cursor.execute(INSERT_OPS['add_news_coin'], (
    "https://seekingalpha.com/news/3703512-bitcoins-trillion-dollar-issue-esg-takes-stage-at-bitcoin-2021-conference?utm_source=coinmarketcap.com&utm_medium=referral",
    5, "BTC"))
my_cursor.execute(INSERT_OPS['add_news'], ("https://uzmancoin.com/anonymous-elon-muski-hedef-aldi-bekle-bizi/", 3))
my_cursor.execute(INSERT_OPS['add_news_coin'], (
    "https://seekingalpha.com/news/3703512-bitcoins-trillion-dollar-issue-esg-takes-stage-at-bitcoin-2021-conference?utm_source=coinmarketcap.com&utm_medium=referral",
    5, "ALGO"))
my_cursor.execute(INSERT_OPS['add_news'], ("https://uzmancoin.com/anonymous-elon-muski-hedef-aldi-bekle-bizi/", 3))
my_cursor.execute(INSERT_OPS['add_news_coin'], (
    "https://seekingalpha.com/news/3703512-bitcoins-trillion-dollar-issue-esg-takes-stage-at-bitcoin-2021-conference?utm_source=coinmarketcap.com&utm_medium=referral",
    5, "BTT"))
my_cursor.execute(INSERT_OPS['add_news'], ("https://uzmancoin.com/anonymous-elon-muski-hedef-aldi-bekle-bizi/", 3))
my_cursor.execute(INSERT_OPS['add_news_coin'], (
    "https://seekingalpha.com/news/3703512-bitcoins-trillion-dollar-issue-esg-takes-stage-at-bitcoin-2021-conference?utm_source=coinmarketcap.com&utm_medium=referral",
    5, "ETH"))
my_cursor.execute(INSERT_OPS['add_news'], ("https://uzmancoin.com/anonymous-elon-muski-hedef-aldi-bekle-bizi/", 3))
my_cursor.execute(INSERT_OPS['add_news_coin'], (
    "https://seekingalpha.com/news/3703512-bitcoins-trillion-dollar-issue-esg-takes-stage-at-bitcoin-2021-conference?utm_source=coinmarketcap.com&utm_medium=referral",
    5, "TRX"))
my_cursor.execute(INSERT_OPS['add_news'], ("https://uzmancoin.com/anonymous-elon-muski-hedef-aldi-bekle-bizi/", 3))
my_cursor.execute(INSERT_OPS['add_news_coin'], (
    "https://seekingalpha.com/news/3703512-bitcoins-trillion-dollar-issue-esg-takes-stage-at-bitcoin-2021-conference?utm_source=coinmarketcap.com&utm_medium=referral",
    5, "SHIB"))
my_cursor.execute(INSERT_OPS['add_news'], ("https://uzmancoin.com/anonymous-elon-muski-hedef-aldi-bekle-bizi/", 3))
my_cursor.execute(INSERT_OPS['add_news_coin'], (
    "https://seekingalpha.com/news/3703512-bitcoins-trillion-dollar-issue-esg-takes-stage-at-bitcoin-2021-conference?utm_source=coinmarketcap.com&utm_medium=referral",
    5, "CHZ"))
my_cursor.execute(INSERT_OPS['add_news'], ("https://uzmancoin.com/anonymous-elon-muski-hedef-aldi-bekle-bizi/", 3))
my_db.commit()


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "GET":
        my_cursor.execute(SELECT_OPS['get_users'])

        user_list = my_cursor.fetchall()
        return render_template("index.html", content=user_list)
    else:
        if request.form['post_req'] == "get_portfolio":
            user = request.form['user_id']
            return redirect(url_for("user_page", usr_id=user))
        elif request.form['post_req'] == "add_user":
            mail = request.form['mail']
            password = request.form['password']
            first = request.form['first']
            last = request.form['last']

            my_cursor.execute(INSERT_OPS['add_user'], (mail, password, first, last))
            my_db.commit()

            return redirect(url_for("home"))


@app.route('/users/<usr_id>', methods=["POST", "GET"])
def user_page(usr_id):
    if request.method == "GET":
        my_cursor.execute(SELECT_OPS['get_portfolio_with_user_id'] % usr_id)
        portfolio = my_cursor.fetchall()
        return render_template("user_page.html", content=portfolio)
    else:
        if request.form['req'] == 'get_coins':
            portfolio_id = request.form['portfolio_id']
            return redirect(url_for("user_portfolio", usr_id=usr_id, portfolio_id=portfolio_id))
        elif request.form['req'] == 'delete_portfolio':
            my_cursor.execute("DELETE FROM portfolio WHERE portfolio_id=%s" % (request.form['portfolio_id']))
            my_db.commit()
            return redirect(url_for("user_page", usr_id=usr_id))


@app.route('/users/<usr_id>/<portfolio_id>')
def user_portfolio(usr_id, portfolio_id):
    my_cursor.execute('''SELECT listing.list_id, listing.alias, platform.platform_name, includes.amount
                         FROM includes
                         INNER JOIN listing
                         ON includes.list_id = listing.list_id
                         INNER JOIN platform
                         ON listing.platform_id = platform.platform_id
                         WHERE includes.portfolio_id = ''' + portfolio_id)
    portfolio = my_cursor.fetchall()
    return render_template("portfolio.html", content=portfolio)


@app.route('/coins', methods=["POST", "GET"])
def coin_list():
    if request.method == "GET":
        my_cursor.execute(SELECT_OPS['get_coins'])
        coins = my_cursor.fetchall()
        return render_template("coins.html", content=coins)
    else:
        print(request.form['post_req'])
        if request.form['post_req'] == "1":
            alias = request.form['coin_alias']
            return redirect(url_for("coin_news", alias=alias))
        elif request.form['post_req'] == "2":
            alias = request.form['coin_alias']
            return redirect(url_for("coin_listings", alias=alias))
        elif request.form['post_req'] == "3":
            alias = request.form['alias']
            volume = request.form['volume']
            price = request.form['price']
            ath = request.form['ath']
            atl = request.form['atl']

            my_cursor.execute(INSERT_OPS['add_coin'], (alias, volume, price, ath, atl))
            my_db.commit()
            return redirect(url_for("coin_list"))


@app.route('/portfolio/dump_all')
def dump_all_portfolios():
    my_cursor.execute("""
                        SELECT portfolio.user_id, portfolio.portfolio_name, includes.amount, listing.alias
                        FROM portfolio
                        LEFT OUTER JOIN includes
                        ON portfolio.portfolio_id = includes.portfolio_id
                        LEFT OUTER JOIN listing
                        ON includes.list_id = listing.list_id
                        UNION
                        SELECT portfolio.user_id, portfolio.portfolio_name, includes.amount, listing.alias
                        FROM portfolio
                        RIGHT OUTER JOIN includes
                        ON portfolio.portfolio_id = includes.portfolio_id
                        LEFT OUTER JOIN listing
                        ON includes.list_id = listing.list_id;               
    """)
    dump = my_cursor.fetchall()
    return render_template("all_portfolios.html", content=dump)


@app.route('/coins/<alias>')
def coin_listings(alias):
    my_cursor.execute("""SELECT platform.platform_name, listing.price FROM listing
                      INNER JOIN platform
                      WHERE platform.platform_id = listing.platform_id AND listing.alias = \"%s\"""" % alias)

    all_listings = my_cursor.fetchall()
    return render_template("coin_markets.html", content=all_listings)


@app.route("/coins/news/<alias>")
def coin_news(alias):
    my_cursor.execute(SELECT_OPS['get_news_about_coin'] % alias)
    news_link = my_cursor.fetchall()
    return render_template("coin_news.html", content=news_link)


@app.route("/news")
def news():
    my_cursor.execute('''SELECT news.link, news.importance, coin.alias FROM coin
                             RIGHT JOIN news
                             ON coin.alias = news.alias
                        ''')
    news_link = my_cursor.fetchall()
    return render_template("news.html", content=news_link)


@app.route('/platforms', methods=["POST", "GET"])
def platform_list():
    if request.method == "GET":
        my_cursor.execute(SELECT_OPS['get_platforms'])
        platforms = my_cursor.fetchall()
        return render_template("platforms.html", content=platforms)
    else:
        platform_id = request.form['platform_id']
        return redirect(url_for("platform_coins", platform_id=platform_id))


@app.route('/platforms/<platform_id>', methods=["POST", "GET"])
def platform_coins(platform_id):
    if request.method == "GET":
        my_cursor.execute('''SELECT listing.alias, listing.price,listing.volume 
                             FROM listing 
                             WHERE listing.platform_id = ''' + platform_id)
        platform_listing = my_cursor.fetchall()
        return render_template("platform_listing.html", content=platform_listing)
    else:
        req = request.form['post_req']
        if req == 'change_price':
            my_cursor.execute("UPDATE listing SET price = %s WHERE alias =\"%s\" AND platform_id = %s" %
                              (request.form['new_price'].replace(',', ''), request.form['coin_alias'], platform_id))
            my_db.commit()

            my_cursor.execute("SELECT order_id, amount, fee, user_id, from_list_id, to_list_id FROM placed_order WHERE "
                              "status='DONE'")
            done_orders = my_cursor.fetchall()
            print(done_orders)
            for done in done_orders:
                my_cursor.execute("CALL exchange(%s, %s,%s,%s,%s, %s)", (str(done[0]), str(done[1]), str(done[2]),
                                                                         str(done[3]), str(done[4]), str(done[5])))
            my_db.commit()
            return redirect(url_for("platform_coins", platform_id=platform_id))
        elif req == 'delist':
            my_cursor.execute("DELETE FROM listing WHERE alias = \"%s\" AND platform_id = %s" %
                              (request.form['coin_alias'], platform_id))
            my_db.commit()
            return redirect(url_for("platform_coins", platform_id=platform_id))
        elif req == 'add_listing':
            alias = request.form['alias']
            volume = request.form['volume']
            price = request.form['price']
            print(alias, price, volume, platform_id)
            my_cursor.execute(INSERT_OPS['add_listing'], (price, volume, alias, platform_id))
            my_db.commit()

            return redirect(url_for("platform_coins", platform_id=platform_id))


@app.route('/coins/with_listing')
def coins_with_listing():
    my_cursor.execute('''SELECT coin.alias, listing.price, platform.platform_name FROM coin
                         LEFT JOIN listing
                         ON coin.alias = listing.alias
                         LEFT JOIN platform
                         ON platform.platform_id = listing.platform_id''')
    coin_listing = my_cursor.fetchall()
    return render_template("coins_with_listing.html", content=coin_listing)


@app.route('/users/total_amounts')
def show_all_user_amounts():
    my_cursor.execute("SELECT * FROM show_total_amount_of_users")
    total_amounts = my_cursor.fetchall()

    return render_template("total_user_amounts.html", content=total_amounts)


@app.route('/platforms/usage_stats')
def list_platform_usage():
    my_cursor.execute('''
        SELECT platform.platform_name , COUNT(show_user_platform_usage.platform_name)
        FROM show_user_platform_usage
        RIGHT OUTER JOIN platform
        ON show_user_platform_usage.platform_name = platform.platform_name
        GROUP BY platform.platform_name''')
    usage_stats = my_cursor.fetchall()

    return render_template("platform_usage_stats.html", content=usage_stats)


@app.route('/orders', methods=["POST", "GET"])
def list_all_orders():
    if request.method == "GET":
        my_cursor.execute("SELECT * FROM orders_with_coin_names")
        orders = my_cursor.fetchall()
        return render_template("orders.html", content=orders)
    else:
        amount = request.form['amount']
        trigger_cond = request.form['trigger_condition']
        trigger_value = 0.0
        user_id = request.form['user_id']
        buy_or_sell = request.form['buy_or_sell']
        from_list = request.form['from']
        to_list = request.form['to']

        if trigger_cond[0] == '<':
            trigger_value = (-1) * float(trigger_cond.split('<')[1])
        elif trigger_cond[0] == '>':
            trigger_value = float(trigger_cond.split('>')[1])
        my_cursor.execute("CALL place_a_order(%s,%s,'%s',%s,%s,%s)" % (
            amount, str(trigger_value), buy_or_sell, user_id, from_list, to_list))
        my_db.commit()
        return redirect(url_for("list_all_orders"))


@app.route('/alarms', methods=["POST", "GET"])
def show_all_alarms():
    if request.method == "GET":
        my_cursor.execute("SELECT * FROM show_alarm_with_coin")
        alarms = my_cursor.fetchall()

        return render_template("alarms.html", content=alarms)
    else:
        user_id = request.form['user_id']
        list_id = request.form['list_id']
        trigger_cond = request.form['trigger_condition']
        trigger_value = 0

        if trigger_cond[0] == '<':
            trigger_value = (-1) * float(trigger_cond.split('<')[1])
        elif trigger_cond[0] == '>':
            trigger_value = float(trigger_cond.split('>')[1])

        my_cursor.execute(INSERT_OPS['add_alarm'], (str(trigger_value), user_id, list_id))
        my_db.commit()
        return redirect(url_for("show_all_alarms"))


@app.route('/transfers', methods=["POST", "GET"])
def show_all_transfers():
    if request.method == "GET":
        my_cursor.execute("SELECT transfer_id, from_hash, to_hash, network, alias, amount, user_id FROM transfer")
        transfers = my_cursor.fetchall()

        return render_template("transfers.html", content=transfers)
    else:
        from_hash = request.form['from']
        to_hash = request.form['to']
        network = request.form['network']
        alias = request.form['alias']
        amount = request.form['amount']
        user_id = request.form['user_id']

        my_cursor.execute("CALL create_a_transfer(\"%s\",\"%s\",\"%s\",\"%s\",%s,%s)" % (
            from_hash, to_hash, network, alias, amount, user_id))
        my_db.commit()

        return redirect(url_for("show_all_transfers"))


@app.route('/coins/stats')
def show_coin_usage():
    my_cursor.execute("SELECT * FROM show_portfolio_coin_usage")
    stats = my_cursor.fetchall()

    return render_template("coin_usage_stats.html", content=stats)


if __name__ == '__main__':
    app.run()
