import os

user= os.environ['POSTGRES_USER']
password= os.environ['POSTGRES_PASSWORD']
host=os.environ['POSTGRES_HOST']
database=os.environ['POSTGRES_DB']
port=os.environ['POSTGRES_PORT']
secret_key=os.environ['SECRET_KEY']

#local machine debug
#user = 'postgres'
#password ='postgres' 
#host ='localhost'
#database ='GymDB' 
#port = '5432'
#secret-key='Not_The_Best_password'
DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'