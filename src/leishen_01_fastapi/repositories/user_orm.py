"""
使用 sqlalchemy 的 ORM 模式对表进行 CRUD
"""

from sqlalchemy import Integer, Select, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

url = "mysql+pymysql://felixsun:L5j5maGOylUqLsJD@mysql6.sqlpub.com:3311/shf_testdb"
engine = create_engine(
    url,
    echo=True,
    pool_size=5,
)


TABLE_NAME = "user_orm"


# TODO 定义表结构 user_orm
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = TABLE_NAME

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str | None] = mapped_column(String(10))

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, age={self.age}, gender={self.gender})"


# TODO 创建表
def creat_user():
    Base.metadata.create_all(engine)


# creat_user()


# TODO: 新增数据
def add_user(user: User | list[User]):
    with Session(engine) as session:
        if type(user) == User:
            session.add(user)
        elif type(user) == list:
            session.add_all(user)
        session.commit()


# add_user(
#     User(name="张三", age=18, gender="男"),
# )

# add_user(
#     User(name="李四", age=19, gender="男"),
# )

# add_user(
#     [
#         User(name="王五", age=20, gender="女"),
#         User(name="赵六", age=20, gender="女"),
#     ]
# )


# TODO 查询，2 种方法，一个是 session api, 另外一个是 sql api
def query_user_session():
    with Session(engine) as session:
        result = session.query(User).filter(User.gender == "女")

        print("=" * 20, "query")
        for row in result:
            print(row)

        res = session.get(User, 2)
        print("使用 get 查询一个数据", res)


# query_user_session()


def query_user_sql():
    with Session(engine) as session:
        # NOTE stmt 是一个 sql 语句， 最终还是需要调用 session.scalar 调用，类似 engine.connct().execute(stmt)
        stmt = Select(User).where(User.gender == "男").where(User.age == 18)

        result = session.execute(stmt)

        print(result)
        for row in session.execute(stmt).scalars():
            print(row)


# query_user_sql()


# TODO 修改数据。 也有 2 种方式
# 1. 先查询  2. 修改  3. 重新赋值
def update_user_session():
    with Session(engine) as session:
        user = session.get(User, 2)
        if user:
            user.gender = "女"
            session.add(user)
        else:
            print("用户不存在")

        session.commit()


# update_user_session()


def update_user_sql(id, gender="男"):
    with Session(engine) as session:
        # stmt 是一个 sql 语句， 最终还是需要调用 session.scalar 调用，类似 engine.connct().execute(stmt)
        stmt = Select(User).where(User.id == id)
        print(f"stmt==={stmt}")
        user = session.scalar(stmt)
        user.gender = gender
        session.commit()


# update_user_sql(2, "男")


# TODO 删除
def del_user():

    # TODO session api 写法
    # with Session(engine) as session:
    #     # user = session.query(User).filter(User.id == 3).one_or_none()
    #     user = session.get(User, 3)
    #     if user:
    #         session.delete(user)
    #         session.commit()
    #     else:
    #         print("无此用户!!")

    # TODO sql api 写法
    with Session(engine) as session:
        stmt = Select(User).where(User.id > 4)
        users = session.scalars(stmt)
        session.delete_all(users)
        session.commit()


# del_user()


# ======== 测试 sessionmaker =======

SessionFromMaker = sessionmaker(engine)

"""
使用 SessionFromMaker.begin()的好处是: 成功后会默认 COMMIT , 失败会默认 ROLLBACK

如果是 SessionFromMaker() 的话，需要手动 COMMIT
"""


def change_user():

    # 第一种写法：
    # with SessionFromMaker.begin() as session:
    #     user = session.get(User, 2)
    #     if user:
    #         user.age = 21

    # 第二种写法
    with SessionFromMaker() as session:
        user = session.get(User, 2)
        if user:
            user.age = 21
            session.commit()


change_user()
