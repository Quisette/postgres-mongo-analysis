from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random, string
from datetime import datetime
from random import randint
from sys import argv
DB_USERNAME = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_NAME = 'sql-test-database'

if argv[1] == '-h':
    print("app, model, field,record")


if len(argv) <= 4:
    raise Error("Insufficient arguments.")

map(int, argv)
BENCHMARK_APP_COUNT = int(argv[1])
BENCHMARK_MODELS_PER_APP =  int(argv[2])
BENCHMARK_RECORDS_PER_MODEL =  int(argv[3])
BENCHMARK_FIELDS_PER_MODEL =  int(argv[4])

print(BENCHMARK_APP_COUNT, BENCHMARK_MODELS_PER_APP, BENCHMARK_RECORDS_PER_MODEL, BENCHMARK_FIELDS_PER_MODEL)

MODEL_KEY_LENGTH = 10
FIELD_KEY_LENGTH = 10


def drop(engine):
    try:
        Data.__table__.drop(engine)
        Record.__table__.drop(engine)
        Field.__table__.drop(engine)
        Model.__table__.drop(engine)
        App.__table__.drop(engine)
    except:
        pass


# create a connection to the database
engine = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

drop(engine)


# create a declarative base
Base = declarative_base()


# define a table class
class App(Base):
    __tablename__ = 'apps'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    models = relationship('Model', back_populates='app')


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey('apps.id'))
    app = relationship('App', back_populates='models')

    name = Column(String)
    fields = relationship('Field', back_populates='model')
    records = relationship('Record', back_populates='model')


class Field(Base):
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship('Model', back_populates='fields')

    name = Column(String)
    type = Column(String)
    default_value = Column(String)


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship('Model', back_populates='records')

    data = relationship('Data', back_populates='record')


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey('records.id'))
    record = relationship('Record', back_populates='data')

    key = Column(String)
    value = Column(String)



# create the table in the database
Base.metadata.create_all(engine)

# Define session maker
Session = sessionmaker(bind=engine, expire_on_commit=False)

def create_app(app_name):
    session = Session()
    new_app = App(name=app_name)
    session.add(new_app)
    session.commit()

def create_model(app_name, model_name):
    session = Session()
    app = session.query(App).filter_by(name=app_name).first()
    new_model = Model(name=model_name, app_id=app.id)
    session.add(new_model)
    session.commit()

def create_field(app_name, model_name, field_name):
    session = Session()
    app = session.query(App).filter_by(name=app_name).first()
    model = session.query(Model).filter_by(name=model_name, app_id=app.id).first()
    new_field = Field(name=field_name, model_id=model.id)
    session.add(new_field)
    session.commit()

def create_record(app_name, model_name, record_payload):
    session = Session()
    app = session.query(App).filter_by(name=app_name).first()
    model = session.query(Model).filter_by(name=model_name, app_id=app.id).first()
    # field = session.query(Field).filter_by(name=field_name, model_name=model.id).first()
    new_record = Record()
    session.add(new_record)
    session.commit()


# Clear all the tables
def flush():
    session = Session()
    session.query(Data).delete()
    session.query(Record).delete()
    session.query(Field).delete()
    session.query(Model).delete()
    session.query(App).delete()
    session.commit()


print('Dropping existing data...')
#flush()
# drop(engine)
#create_app('app_0')
#create_model('Test App', 'Test Model')
#create_field('Test App', 'Test Model', 'Test Field')
#create_record('Test App', 'Test Model', {})



FIELD_TYPES     = ['int', 'str', 'bool', 'datetime', 'int']
DEFAULT_VALUES  = [1586479000, 'Lorem ipsum dolor sit amet, consectetur adipisicing elit', True, datetime.now().timestamp(), 1]


# Random name generator
def generate_name(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


# Generate a model with a random name
# then randomly generate 4 to 10
def generate_model(app_name, model_name):
    model = Model()
    model.name = model_name
    for i in range(BENCHMARK_FIELDS_PER_MODEL):
        model.fields.append(
            Field(
                type=FIELD_TYPES[i%len(FIELD_TYPES)],
                # name=generate_name(FIELD_KEY_LENGTH),
                name=f"field_{i}",
                default_value=DEFAULT_VALUES[i%len(FIELD_TYPES)],
            )
        )
    session = Session()
    app = session.query(App).filter_by(name=app_name).first()
    model.app_id = app.id
    session.add(model)
    session.commit()
    return model



def generate_records(app_name, model_name, count=BENCHMARK_RECORDS_PER_MODEL):
    session = Session()
    app = session.query(App).filter_by(name=app_name).first()
    model = session.query(Model).filter_by(name=model_name, app_id=app.id).first()

    for _ in range(count):
        record = Record()
        record.model_id = model.id
        for field in model.fields:
            data = Data(key=field.name, value=field.default_value)
            session.add(data)
            record.data.append(data)
        session.add(record)
        session.commit()

    session.add(model)
    session.commit()


# Pre-generate model names
# MODEL_NAMES = [generate_name(MODEL_KEY_LENGTH) for _ in range(BENCHMARK_MODELS_PER_APP)]

print('Starting generating...')
start = datetime.now().timestamp()
for a in range(BENCHMARK_APP_COUNT):
    create_app(f'app_{a}')
    for i in range(BENCHMARK_MODELS_PER_APP):
        model = generate_model(f'app_{a}', f'model_{i}')
        generate_records(f'app_{a}', model.name, BENCHMARK_RECORDS_PER_MODEL)
end = datetime.now().timestamp()

print(f'Time used: {int(end-start)} s ({int((end-start)*1000)} ms)')
