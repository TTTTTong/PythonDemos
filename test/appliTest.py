from sqlalchemy import create_engine

engine = create_engine('mysql://root：201919@localhost/scrapy001', echo=True)
