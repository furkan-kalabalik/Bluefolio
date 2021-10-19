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
                  start_amount DECIMAL(20,10) NOT NULL DEFAULT 0.0,
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
                  alias VARCHAR(16) NOT NULL,
                  amount DECIMAL(20,10) NOT NULL,
                  user_id INT NOT NULL,
                  PRIMARY KEY (transfer_id),
                  FOREIGN KEY (user_id) REFERENCES user(user_id),
                  FOREIGN KEY (alias) REFERENCES coin(alias)
                );''',
    'news': '''
                CREATE TABLE news
                (
                  news_id INT NOT NULL AUTO_INCREMENT,
                  link VARCHAR(255) NOT NULL,
                  importance INT NOT NULL,
                  alias VARCHAR(16),
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
                  order_id INT NOT NULL AUTO_INCREMENT,
                  amount DECIMAL(20,10) NOT NULL,
                  trigger_condition DECIMAL(20,10) NOT NULL,
                  buy_or_sell VARCHAR(1) NOT NULL,
                  status VARCHAR(10) NOT NULL DEFAULT 'PENDING',
                  fee DECIMAL(20,10) NOT NULL DEFAULT (amount*0.0001),
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
                  trigger_condition DECIMAL(20,10) NOT NULL,
                  user_id INT NOT NULL,
                  list_id INT NOT NULL,
                  status VARCHAR(10) NOT NULL DEFAULT 'PENDING',
                  PRIMARY KEY (alarm_id),
                  FOREIGN KEY (user_id) REFERENCES user(user_id),
                  FOREIGN KEY (list_id) REFERENCES listing(list_id)
                );'''
}

INSERT_OPS = {
    'add_user': "INSERT INTO user(mail, password, first_name, last_name) "
                "VALUES (%s,%s,%s,%s)",
    'add_portfolio': "INSERT INTO portfolio(portfolio_name, start_date, user_id) VALUES(%s, %s, %s)",
    'add_coin': "INSERT INTO coin(alias, volume, average_current_value, ath, atl) "
                "VALUES (%s, %s, %s, %s, %s)",
    'add_platform': "INSERT INTO platform(platform_name, volume) "
                    "VALUES (%s, %s)",
    'add_listing': "INSERT INTO listing(price, volume, alias, platform_id) "
                   "VALUES (%s,%s,%s,%s)",
    'add_to_portfolio': "INSERT INTO includes(amount, buy_price, portfolio_id, list_id)"
                        "SELECT %s, listing.price, %s, listing.list_id "
                        "FROM listing WHERE listing.list_id = %s",
    'add_news_coin': "INSERT INTO news(link, importance, alias) VALUES (%s,%s,%s)",
    'add_news': "INSERT INTO news(link, importance) VALUES (%s,%s)",
    'place_a_order': "INSERT INTO placed_order(amount, trigger_condition, buy_or_sell, user_id, from_list_id, "
                     "to_list_id) "
                     "VALUES (%s,%s,'%s',%s,%s,%s)",
    'add_alarm': "INSERT INTO alarm(trigger_condition, user_id, list_id) VALUES (%s,%s,%s)",
}

SELECT_OPS = {
    'get_users': "SELECT * FROM user",
    'get_portfolio_with_user_id': "SELECT * FROM portfolio WHERE portfolio.user_id = %s",
    'get_coins': "SELECT * FROM coin",
    'get_platforms': "SELECT * FROM platform",
    'get_all_news': "SELECT * FROM news",
    'get_news_about_coin': "SELECT news.link, news.importance FROM news WHERE news.alias = \"%s\"",
}

TRIGGERS = {
    # CHECK
    'update_coin_num': '''
        CREATE TRIGGER update_coin_num AFTER INSERT ON listing
        FOR EACH ROW BEGIN 
            SET @platform = NEW.platform_id;
            UPDATE platform SET platform.number_of_coin = platform.number_of_coin +1 
            WHERE platform.platform_id = @platform;
        END
    ''',
    # CHECK
    'update_alarm_status': '''
        CREATE TRIGGER check_alarm AFTER UPDATE ON listing
        FOR EACH ROW BEGIN
        IF(OLD.price > NEW.price) THEN
            UPDATE alarm SET status="DONE" WHERE alarm.trigger_condition < 0 AND alarm.trigger_condition <= (-1)*NEW.price AND NEW.list_id = alarm.list_id;
        ELSEIF(OLD.price < NEW.price) THEN
            UPDATE alarm SET status="DONE" WHERE alarm.trigger_condition > 0 AND alarm.trigger_condition <= NEW.price AND NEW.list_id = alarm.list_id;
        END IF;
        END
    ''',
    # CHECK
    'update_order_status': '''
        CREATE TRIGGER check_order AFTER UPDATE ON listing
        FOR EACH ROW BEGIN
        IF(OLD.price > NEW.price) THEN
            UPDATE placed_order SET placed_order.status="DONE" WHERE placed_order.trigger_condition < 0 AND placed_order.trigger_condition <= (-1)*NEW.price AND NEW.list_id = placed_order.from_list_id;
        ELSEIF(OLD.price < NEW.price) THEN
            UPDATE placed_order SET placed_order.status="DONE" WHERE placed_order.trigger_condition > 0 AND placed_order.trigger_condition <= NEW.price AND NEW.list_id = placed_order.from_list_id;
        END IF;
        END
    ''',
    # CHECK
    'delete_portfolio': '''
        CREATE TRIGGER delete_portfolio_includes BEFORE DELETE ON portfolio
        FOR EACH ROW BEGIN
            DELETE FROM includes WHERE includes.portfolio_id = OLD.portfolio_id;
        END
    ''',
    # CHECK
    'delist_coin': '''
        CREATE TRIGGER delist_coin BEFORE DELETE ON listing
        FOR EACH ROW BEGIN
            DELETE FROM includes WHERE includes.list_id = OLD.list_id;
            DELETE FROM alarm WHERE alarm.list_id = OLD.list_id;
            DELETE FROM placed_order WHERE placed_order.from_list_id = OLD.list_id OR placed_order.to_list_id = OLD.list_id;
            UPDATE platform SET number_of_coin = number_of_coin-1 WHERE OLD.platform_id = platform.platform_id;
        END
    ''',
    # CHECK
    'create_default_portfolio': '''
        CREATE TRIGGER create_default_portfolio AFTER INSERT ON user
        FOR EACH ROW BEGIN 
            SET @new_user = NEW.user_id;
            INSERT INTO portfolio(portfolio_name, start_date, start_amount, user_id)
            VALUES ('Default', now(), 0, @new_user);
        END
    ''',
}

VIEWS = {
    # CHECK
    'listing_with_platforms': '''
        CREATE VIEW listing_with_platforms AS
        SELECT listing.alias, listing.price, platform.platform_name, listing.volume
        FROM listing
        INNER JOIN platform
        ON platform.platform_id = listing.platform_id
    ''',
    # CHECK
    'orders_with_coin_names': '''
        CREATE VIEW orders_with_coin_names AS
        SELECT placed_order.amount, placed_order.trigger_condition, placed_order.buy_or_sell, placed_order.status,
        placed_order.user_id, list1.alias AS 'From coin', list2.alias AS 'To coin'
        FROM placed_order
        INNER JOIN listing AS list1 ON list1.list_id = placed_order.from_list_id
        INNER JOIN listing AS list2 ON list2.list_id = placed_order.to_list_id
    ''',
    # CHECK
    'show_alarm_with_coin': '''
        CREATE VIEW show_alarm_with_coin AS
        SELECT alarm.alarm_id, alarm.user_id, platform.platform_name, listing.alias, alarm.trigger_condition, alarm.status
        FROM alarm
        INNER JOIN listing
        ON alarm.list_id = listing.list_id
        INNER JOIN platform
        ON listing.platform_id = platform.platform_id;
    ''',
    # CHECK
    'show_user_platform_usage': '''
        CREATE VIEW show_user_platform_usage AS
        SELECT DISTINCT portfolio.user_id, platform.platform_name
        FROM portfolio
        INNER JOIN includes ON includes.portfolio_id = portfolio.portfolio_id
        INNER JOIN listing ON listing.list_id = includes.list_id
        INNER JOIN platform ON listing.platform_id = platform.platform_id
    ''',
    # CHECK
    'show_total_amount_of_users': '''
        CREATE VIEW show_total_amount_of_users AS
        SELECT portfolio.user_id, SUM(includes.amount*listing.price) AS total_amount
        FROM portfolio
        LEFT JOIN includes ON includes.portfolio_id = portfolio.portfolio_id
        LEFT JOIN listing ON listing.list_id = includes.list_id
        GROUP BY user_id
    ''',
    # CHECK
    'show_portfolio_coin_usage': '''
        CREATE VIEW show_portfolio_coin_usage AS
        SELECT listing.alias, COUNT(listing.alias)
        FROM includes
        INNER JOIN listing
        ON listing.list_id = includes.list_id
        GROUP BY listing.alias
    '''
}

PROCEDURES = {
    'place_a_order': '''
        CREATE PROCEDURE place_a_order(
            IN amount_i DECIMAL(20,10),
            IN trigger_cond_i DECIMAL(20,10),
            IN b_s VARCHAR(1),
            IN user_id_i INT,
            IN from_i INT,
            IN to_i INT
        )
        BEGIN 
            DECLARE having_amount DEC(20,10) DEFAULT 0.0;
            DECLARE platform_from INT;
            DECLARE platform_to INT;
            DECLARE error INT DEFAULT 0;
            START TRANSACTION;
                SET @error = (SELECT 0);
                SET @having_amount = (SELECT SUM(includes.amount) 
                                    FROM includes 
                                    INNER JOIN portfolio 
                                    ON portfolio.portfolio_id = includes.portfolio_id
                                    WHERE includes.list_id = from_i AND portfolio.user_id = user_id_i
                                    );
                IF(@having_amount < amount_i) THEN
                    SET @error = (SELECT 1);
                END IF;
                
                SET @platform_from = (SELECT listing.platform_id
                                    FROM listing
                                    WHERE listing.list_id = from_i);
                SET @platform_to = (SELECT listing.platform_id
                                    FROM listing
                                    WHERE listing.list_id = to_i);
                                    
                IF(@platform_from != @platform_to) THEN
                    SET @error = (SELECT 1);
                END IF;   
                
                INSERT INTO placed_order(amount, trigger_condition, buy_or_sell,user_id, from_list_id, to_list_id) 
                VALUES (amount_i, trigger_cond_i, b_s, user_id_i, from_i, to_i);
                            
                IF (@error != 1) THEN
                    COMMIT ;
                ELSE
                    ROLLBACK ;
                END IF;
        END
    ''',
    'create_a_transfer': '''
        CREATE PROCEDURE create_a_transfer(
            IN from_hash_i VARCHAR(64),
            IN to_hash_i VARCHAR(64),
            IN network_i VARCHAR(16),
            IN alias_i VARCHAR(16),
            IN amount_i DECIMAL(20, 10),
            IN user_id_i INT
        )
        BEGIN 
            DECLARE having_amount DEC(20,10) DEFAULT 0.0;
            DECLARE error INT DEFAULT 0;
            START TRANSACTION;
                SET @error = (SELECT 0);
                SET @having_amount = (  SELECT SUM(includes.amount)
                                        FROM includes
                                        INNER JOIN portfolio
                                        ON includes.portfolio_id = portfolio.portfolio_id
                                        INNER JOIN listing
                                        ON listing.list_id = includes.list_id
                                        WHERE portfolio.portfolio_id IN (
                                            SELECT portfolio_id FROM portfolio WHERE portfolio.user_id=user_id_i) 
                                        AND listing.alias = alias_i
                                    );
                
                IF(@having_amount < amount_i) THEN
                    SET @error = (SELECT 1);
                END IF;
                                    
                INSERT INTO transfer(from_hash, to_hash, network,alias, amount, user_id) 
                VALUES (from_hash_i, to_hash_i, network_i, alias_i, amount_i, user_id_i);
                            
                IF (@error != 1) THEN
                    COMMIT ;
                ELSE
                    ROLLBACK ;
                END IF;
        END
    ''',
    'exchange': '''
        CREATE PROCEDURE exchange(
            IN order_id_i INT,
            IN amount_i DECIMAL(20,10),
            IN fee_i DECIMAL(20,10),
            IN user_id_i INT,
            IN from_list_id_i INT,
            IN to_list_id_i INT
        )
        BEGIN 
            DECLARE from_amount_usd DEC(20,10) DEFAULT 0.0;
            DECLARE to_price_usd DEC(20,10) DEFAULT 0.0;
            DECLARE to_coin_amount DEC(20,10) DEFAULT 0.0;
            START TRANSACTION;
            
                UPDATE placed_order 
                SET status = 'COMPLETED'
                WHERE status = 'DONE' AND order_id = order_id_i;
                
                SET @from_amount_usd = (SELECT SUM(includes.amount*listing.price)
                                        FROM includes
                                        INNER JOIN portfolio
                                        ON includes.portfolio_id = portfolio.portfolio_id
                                        INNER JOIN listing
                                        ON listing.list_id = includes.list_id
                                        WHERE portfolio.portfolio_id IN (
                                            SELECT portfolio_id FROM portfolio WHERE portfolio.user_id=user_id_i) 
                                        AND listing.list_id = from_list_id_i
                                        GROUP BY listing.list_id
                                        );
                SET @to_price_usd = (SELECT price FROM listing WHERE listing.list_id = to_list_id_i);
                SET @to_coin_amount = (SELECT ((@from_amount_usd)/(@to_price_usd))); 
                
                
                INSERT INTO includes(amount, buy_price, portfolio_id, list_id)
                SELECT @to_coin_amount, listing.price, (SELECT portfolio_id FROM portfolio WHERE portfolio.user_id=user_id_i LIMIT 1), listing.list_id 
                FROM listing WHERE listing.list_id = to_list_id_i
                ON DUPLICATE KEY UPDATE 
                amount = @to_coin_amount;
                COMMIT;
        END
    '''
}