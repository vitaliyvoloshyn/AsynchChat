from time import sleep

from main import ServerDB, ClientDB

d = ServerDB()
c = ClientDB()
sleep(30)
user_s = d.User(login='alex', password=123)
d.session.add(user_s)
d.session.commit()

user_c = c.User(login='bob', password=123)
c.session.add(user_c)
c.session.commit()
print(d.session.query(d.User).all())
print(c.session.query(c.User).all())
# print(d.session.query(d.User).filter(d.User.login=='alex').first().id)
# print([i for i in d.session.execute('Select * from users')])
