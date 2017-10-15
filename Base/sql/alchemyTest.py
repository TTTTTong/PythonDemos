from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'alchemyTest'

    # 表结构
    id = Column(String(20), primary_key=True)
    name = Column(String(20))


# 初始化数据库连接
engine = create_engine('mysql+mysqlconnector://root:201919@localhost:3306/test')
# 创建DBSession类型
DBSession = sessionmaker(bind=engine)
# 创建session对象
session = DBSession()

# user = User(id='5', name='Bob')
# session.add(user)
# session.commit()

user = session.query(User).filter(User.id == '111').one()
print('type: ', type(user))
print('name: ', user.name)
session.close()