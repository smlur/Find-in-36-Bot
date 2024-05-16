import sqlalchemy as db


#создаем соединение с нашей базой данных
engine = db.create_engine('sqlite:///events.db')
conn = engine.connect()
#создаем объект метаданных
metadata = db.MetaData()
#создаем саму таблицу, ее столбцы
events = db.Table('events', metadata,
  db.Column('event_id', db.Integer, primary_key=True, autoincrement=True),
  db.Column('event_name', db.Text),
  db.Column('event_place', db.Text),
  db.Column('description', db.Text),
  db.Column('date', db.Date)
)
metadata.create_all(engine)