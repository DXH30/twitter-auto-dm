CREATE table messages(id integer primary key not null, content text, activate integer default 1);
CREATE table followers(id integer primary key not null, uid text, screen_name text, sent integer default 0);
