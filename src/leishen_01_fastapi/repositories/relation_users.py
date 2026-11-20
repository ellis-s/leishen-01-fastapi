from sqlalchemy import BigInteger, ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

url = "mysql+pymysql://felixsun:L5j5maGOylUqLsJD@mysql6.sqlpub.com:3311/shf_testdb"
engine = create_engine(url, echo=True, pool_size=5)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))

    profile: Mapped["UserProfile"] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name})"


class UserProfile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    bio: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"UserProfile(id={self.id}, name={self.bio})"


def create_tables():
    Base.metadata.create_all(engine)


create_tables()


LocalSession = sessionmaker(engine)


def add_data(name, bio):
    with LocalSession.begin() as session:
        user = User(name=name, profile=UserProfile(bio=bio))
        session.add(user)
        print("数据新增成功！")


# add_data(name="李四", bio="我是李四，哈哈哈")


def get_user(id):
    with LocalSession.begin() as session:
        user = session.get(User, id)
        if user:
            print(user.name)
            print(user.profile.bio)


# get_user(2)


def get_profile():
    with LocalSession.begin() as session:
        profile = session.query(UserProfile).first()
        if profile:
            print(profile.bio)
            print(profile.user.name)


# get_profile()


def update_user(user_id: int, name: str, bio: str):
    with LocalSession.begin() as session:
        user = session.get(User, user_id)
        user.name = name
        user.profile.bio = bio
        print("修改成功")


# update_user(1, "张三丰", bio="我真的是张三丰")

# 级联删除
"""

1. 要设置： cascade="all, delete-orphan", passive_deletes=True
profile: Mapped["UserProfile"] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )

cascade="all, delete-orphan" => 属于是 ORM 层面的删除设置。SQLAlchemy 会根据代码和设置生成对应的 sql 语句。语句虽然生成了，但是能否真的执行，是需要依赖数据库层面的设置。



2. 要设置： ondelete="CASCADE"  => 属于是 数据层面 的级联删除设置，只在创建表的时候生效。  但是如果这个表之前已经创建了，那后面再添加这个设置，对于数据库是不生效的。所以我手动的在数据库中删除外键，并重新添加外键，同时设置 on delete casecade 。

user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )

"""


def delete_user(user_id: int):
    with LocalSession.begin() as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)


delete_user(2)
