import psycopg2 as driver

con = driver.connect(database='postgres', user='postgres', host='localhost', password='mIdIa490')
cur = con.cursor()

cur.execute("""INSERT INTO users VALUES (0, '{"(twitter,mkbhd,0)"}');""");
cur.execute("select feeds[1] from users where user_id=0;")

con.commit()

cur.fetchone()