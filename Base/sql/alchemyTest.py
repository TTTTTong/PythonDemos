from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'alchemyTest'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))


class clstest(Base):
    __tablename__ = 'alchemyTest2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    noname = Column(String(50), nullable=False)


# 初始化数据库连接,即使创建了Engine, 还是没有创建对数据库的连接
engine = create_engine('mysql+mysqlconnector://root:201919@localhost:3306/test')
# 如果表不存在则创建
Base.metadata.create_all(engine)
# 创建DBSession类型
sessionCls = sessionmaker(bind=engine)
# 创建session对象
session = sessionCls()

# user = User(id='12', name='Bob')
# session.add(user)
# session.commit()

user = session.query(User).filter(User.id == '11').one()
print('type: ', type(user))
print('name: ', user.name)
session.close()