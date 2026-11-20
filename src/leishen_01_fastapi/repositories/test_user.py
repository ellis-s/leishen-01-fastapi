from sqlalchemy import CursorResult, create_engine, text

url = "mysql+pymysql://felixsun:L5j5maGOylUqLsJD@mysql6.sqlpub.com:3311/shf_testdb"


engine = create_engine(url, echo=True, pool_size=5)


def print_result(result: CursorResult):
    for row in result.mappings():
        print(row)


def create_user():
    # TODO: 创建一个 user 表
    with engine.connect() as conn:
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS test_user (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT , name VARCHAR(50), age INT, gender VARCHAR(10))"
            )
        )


def init_user():
    with engine.connect() as conn:
        # TODO: 插入一些初始化数据
        conn.execute(
            text(
                "insert into test_user (name, age, gender) values (:name, :age, :gender)"
            ),
            parameters=[
                {"name": "张三", "age": 18, "gender": "男"},
                {"name": "李四", "age": 19, "gender": "男"},
                {"name": "王五", "age": 20, "gender": "女"},
            ],
        )

        # TODO: 提交事务
        conn.commit()


def query_user():

    with engine.connect() as conn:
        t = text("select * from test_user;")
        # t = text("show tables;")

        print_result(conn.execute(t))


query_user()
