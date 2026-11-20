"""
多对多关联

1. students
2. courses
3. student_course
"""

from sqlalchemy import BigInteger, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

engine = create_engine(
    url="mysql+pymysql://felixsun:L5j5maGOylUqLsJD@mysql6.sqlpub.com:3311/shf_testdb",
    echo=True,
    pool_size=10,
)


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "student"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))

    # 所有课程
    courses: Mapped[list["Course"]] = relationship(
        back_populates="students", secondary="student_course"
    )

    # 所有课程-等分
    student_courses: Mapped[list["StudentCourse"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id}, name={self.name})"


class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))

    # 所有学生
    students: Mapped[list["Student"]] = relationship(
        back_populates="courses", secondary="student_course"
    )

    # 所有学生-等分
    student_courses: Mapped[list["StudentCourse"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Course(id={self.id}, title={self.title})"


class StudentCourse(Base):
    __tablename__ = "student_course"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    score: Mapped[int] = mapped_column(Integer)

    student_id: Mapped[int] = mapped_column(ForeignKey("student.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))

    student: Mapped["Student"] = relationship(back_populates="student_courses")
    course: Mapped["Course"] = relationship(back_populates="student_courses")

    def __repr__(self) -> str:
        return f"StudentCourse(id={self.id}, score={self.score})"


# 创建所有表
Base.metadata.create_all(engine)


Session = sessionmaker(engine)


# TODO 插入一些数据
def insert_data():
    with Session() as session:
        st1 = Student(name="张三")
        st2 = Student(name="李四")
        st3 = Student(name="王五")

        course1 = Course(title="语文")
        course2 = Course(title="数学")
        course3 = Course(title="英语")

        session.add_all(
            [
                StudentCourse(student=st1, course=course1, score=90),
                StudentCourse(student=st1, course=course2, score=91),
                StudentCourse(student=st1, course=course3, score=93),
                StudentCourse(student=st2, course=course1, score=80),
                StudentCourse(student=st2, course=course2, score=81),
                StudentCourse(student=st2, course=course3, score=83),
                StudentCourse(student=st3, course=course1, score=70),
                StudentCourse(student=st3, course=course2, score=71),
                StudentCourse(student=st3, course=course3, score=73),
            ]
        )

        session.commit()


# insert_data()


# TODO 查询张三都有哪些课程
def read_courses(user_id):
    with Session() as session:
        student = session.query(Student).filter(Student.id == user_id).first()
        if student:
            for index, course in enumerate(student.courses, start=1):
                print(f"{student.name}的第{index}个课程是：{course.title}")


# read_courses(1)


# TODO 查询李四所有分数
def read_scores(user_id):
    with Session() as session:
        student = session.get(Student, user_id)
        if student:
            for index, student_course in enumerate(student.student_courses, start=1):
                print(
                    f"{student.name}的第{index}个课程是：{student_course.course.title}，分数是：{student_course.score}"
                )


# read_scores(2)


# TODO 更新王五的英语成绩为100分
def update_score(user_id, course_name, score):
    with Session.begin() as session:
        student = session.get(Student, user_id)
        if student:
            for s_c in student.student_courses:
                if s_c.course.title == course_name:
                    s_c.score = score
                    print("更新成功！")


# update_score(3, "英语", 100)


def read_all_students(session: Session):

    if session:
        students = session.query(Student).all()
        for student in students:
            print(student)
        return

    with Session() as new_session:
        students = new_session.query(Student).all()
        for student in students:
            print(student)


def read_all_sc(user_id, session):

    def __read(session: Session):
        sc_list = (
            session.query(StudentCourse)
            .filter(StudentCourse.student_id == user_id)
            .all()
        )

        if not len(sc_list):
            print("该用户无得分数据！")
            return

        for sc in sc_list:
            print(sc)

    if session:
        __read(session)
        return

    with Session() as new_session:
        __read(new_session)


# TODO 删除张三这个用户
def delete_user(user_id: int):
    with Session() as session:
        student = session.get(Student, user_id)
        if student:
            session.delete(student)
            print("删除成功！")
            read_all_students(session)
            read_all_sc(user_id, session)
            # session.commit() # 该事务暂时不提交, 用于测试。 默认会自动 rollback


delete_user(1)
