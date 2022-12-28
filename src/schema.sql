CREATE table messages(id integer auto_increment primary key, content text, activate integer);
CREATE table followers(id integer auto_increment primary key, uid text, screen_name text);
