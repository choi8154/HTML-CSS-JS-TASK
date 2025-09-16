# 사용안함. SQLALCHEMY로 다 만들기 가능...
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    passwd="dain8154",
    db="WorkOutDB",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

def create_DB():
    with conn.cursor() as cur:
        sql = f"CREATE DATABASE IF NOT EXISTS WorkOutDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
        cur.execute(sql)
        conn.commit()
        cur.close()

def create_Table():
    with conn.cursor() as cur:
        sql = f"""CREATE TABLE IF NOT EXISTS Users(
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                height INT,
                weight INT,
                created_at DATETIME
                )"""
        cur.execute(sql)
        conn.commit()
        cur.close()

def create_Table2():
    with conn.cursor() as cur:
        sql = f"""CREATE TABLE IF NOT EXISTS Exercise_logs(
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                exercise_id INT,
                sets INT,
                reps INT,
                weight INT,
                log_date DATE,
                created_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (exercise_id) REFERENCES Exercises(exercise_id)
                )"""
        cur.execute(sql)
        conn.commit()
        cur.close()

def create_Table1():
    with conn.cursor() as cur:
        sql = f"""CREATE TABLE IF NOT EXISTS Exercises(
                exercise_id int PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50)
                )"""
        cur.execute(sql)
        conn.commit()
        cur.close()
create_Table2()
