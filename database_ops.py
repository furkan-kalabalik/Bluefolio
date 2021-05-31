TABLES = {
    'user': ''' CREATE TABLE user
                (
                  user_id INT NOT NULL AUTO_INCREMENT,
                  verified VARCHAR(1) NOT NULL DEFAULT 'N',
                  first_name VARCHAR(32) NOT NULL,
                  last_name VARCHAR(32) NOT NULL,
                  mail VARCHAR(32) NOT NULL,
                  password VARCHAR(16) NOT NULL,
                  PRIMARY KEY (user_id)
                );''',
    'coin': '''
                CREATE TABLE coin
                (
                  alias VARCHAR(16) NOT NULL,
                  volume BIGINT NOT NULL,
                  average_current_value DECIMAL(20,10) NOT NULL,
                  ath DECIMAL(20,10) NOT NULL,
                  atl DECIMAL(20,10) NOT NULL,
                  PRIMARY KEY (alias)
                ); ''',
    'platform': '''
                CREATE TABLE platform
                (
                  platform_id INT NOT NULL AUTO_INCREMENT,
                  platform_name VARCHAR(32) NOT NULL,
                  number_of_coin INT NOT NULL DEFAULT 0,
                  volume BIGINT NOT NULL,
                  PRIMARY KEY (platform_id)
                );''',
    'portfolio': '''
                CREATE TABLE portfolio
                (
                  portfolio_id INT NOT NULL AUTO_INCREMENT,
                  portfolio_name VARCHAR(32) NOT NULL,
                  start_date DATE NOT NULL,
                  start_amount DECIMAL(20,10) NOT NULL,
                  user_id INT NOT NULL,
                  PRIMARY KEY (portfolio_id),
                  FOREIGN KEY (user_id) REFERENCES user(user_id)
                );''',
    'transfer': '''
                CREATE TABLE transfer
                (
                  transfer_id INT NOT NULL AUTO_INCREMENT,
                  from_hash VARCHAR(64) NOT NULL,
                  to_hash VARCHAR(64)  NOT NULL,
                  network VARCHAR(16) NOT NULL,
                  amount DECIMAL(20,10) NOT NULL,
                  user_id INT NOT NULL,
                  PRIMARY KEY (transfer_id),
                  FOREIGN KEY (user_id) REFERENCES user(user_id)
                );''',
    'news': '''
                CREATE TABLE news
                (
                  news_id INT NOT NULL AUTO_INCREMENT,
                  link VARCHAR(255) NOT NULL,
                  importance INT NOT NULL,
                  alias VARCHAR(16) NOT NULL,
                  PRIMARY KEY (news_id),
                  FOREIGN KEY (alias) REFERENCES coin(alias)
                );''',
    'watch': '''
                CREATE TABLE watch
                (
                  user_id INT NOT NULL,
                  alias VARCHAR(16) NOT NULL,
                  PRIMARY KEY (user_id, alias),
                  FOREIGN KEY (user_id) REFERENCES user(user_id),
                  FOREIGN KEY (alias) REFERENCES coin(alias)
                );''',
    'listing': '''
                CREATE TABLE listing
                (
                  list_id INT NOT NULL AUTO_INCREMENT,
                  price DECIMAL(20,10) NOT NULL,
                  volume BIGINT NOT NULL,
                  alias VARCHAR(16) NOT NULL,
                  platform_id INT NOT NULL,
                  PRIMARY KEY (list_id),
                  FOREIGN KEY (alias) REFERENCES coin(alias),
                  FOREIGN KEY (platform_id) REFERENCES platform(platform_id)
                );''',
    'placed_order': '''
                CREATE TABLE placed_order
                (
                  order_id INT NOT NULL,
                  amount DECIMAL(20,10) NOT NULL,
                  trigger_condition VARCHAR(64) NOT NULL,
                  fee DECIMAL(20,10) NOT NULL,
                  user_id INT NOT NULL,
                  from_list_id INT NOT NULL,
                  to_list_id INT NOT NULL,
                  PRIMARY KEY (order_id),
                  FOREIGN KEY (user_id) REFERENCES user(user_id),
                  FOREIGN KEY (from_list_id) REFERENCES listing(list_id),
                  FOREIGN KEY (to_list_id) REFERENCES listing(list_id)
                );''',
    'includes': '''
                CREATE TABLE includes
                (
                  amount DECIMAL(20,10) NOT NULL,
                  buy_price DECIMAL(20,10) NOT NULL,
                  portfolio_id INT NOT NULL,
                  list_id INT NOT NULL,
                  PRIMARY KEY (portfolio_id, list_id),
                  FOREIGN KEY (portfolio_id) REFERENCES portfolio(portfolio_id),
                  FOREIGN KEY (list_id) REFERENCES listing(list_id)
                );''',
    'alarm': '''
                CREATE TABLE alarm
                (
                  alarm_id INT NOT NULL AUTO_INCREMENT,
                  trigger_condition VARCHAR(64) NOT NULL,
                  user_id INT NOT NULL,
                  list_id INT NOT NULL,
                  PRIMARY KEY (alarm_id),
                  FOREIGN KEY (user_id) REFERENCES user(user_id),
                  FOREIGN KEY (list_id) REFERENCES listing(list_id)
                );'''
}

INSERT_OPS = {
    'add_user': "INSERT INTO user(mail, password, first_name, last_name) "
                "VALUES (%s,%s,%s,%s)",
    'add_portfolio': "INSERT INTO portfolio(portfolio_name, start_date, start_amount, user_id) VALUES(%s, %s, %s, %s)",
    'add_coin': "INSERT INTO coin(alias, volume, average_current_value, ath, atl) "
                "VALUES (%s, %s, %s, %s, %s)",
    'add_platform': "INSERT INTO platform(platform_name, volume) "
                    "VALUES (%s, %s)",
    'add_listing': "INSERT INTO listing(price, volume, alias, platform_id) "
                   "VALUES (%s,%s,%s,%s)",
    'add_to_portfolio': "INSERT INTO includes(amount, buy_price, portfolio_id, list_id)"
                        "SELECT %s, listing.price, %s, listing.list_id "
                        "FROM listing WHERE listing.list_id = %s"
}

SELECT_OPS = {
    'get_users': "SELECT * FROM user",
    'get_portfolio_with_user_id': "SELECT * FROM portfolio WHERE portfolio.user_id = %s",
    'get_coins': "SELECT * FROM coin",
    'get_platforms': "SELECT * FROM platform"
}

TRIGGERS = {
    'update_coin_num': '''
        CREATE TRIGGER update_coin_num AFTER INSERT ON listing
        FOR EACH ROW BEGIN 
            SET @platform = NEW.platform_id;
            UPDATE platform SET platform.number_of_coin = platform.number_of_coin +1 
            WHERE platform.platform_id = @platform;
        END
    '''
}
