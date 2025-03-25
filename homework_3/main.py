import asyncio

from homework_3.manager import StudentManager


async def runner():
    student_namager = StudentManager()
    # Очищаем базу данных
    await student_namager.drop_db()

    await student_namager.init_db()

    await student_namager.load_from_csv()

    res = await student_namager.get_faculty(faculty_name="ФЛА")
    print(res)

    res = await student_namager.get_faculty(faculty_id=1)
    print(res)

    res = await student_namager.get_faculty("dsd")
    print(res)

    res = await student_namager.get_course(course_name="Мат. Анализ")
    print(res)

    res = await student_namager.get_course(course_name="Мат.sdsd Анализ")
    print(res)

    res = await student_namager.get_course(course_id=1)
    print(res)

    res = await student_namager.get_student(1)
    print(res)

    res = await student_namager.get_student(2323)
    print(res)

    res = await student_namager.get_students_by_faculty("ФПМИ")
    print(res)

    res = await student_namager.get_unique_courses()
    print(res)

    res = await student_namager.get_average_grade_by_faculty("ФПМИ")
    print(res)

    res = await student_namager.get_students_below_grade_by_course("Мат. Анализ")
    print(res)

    # last_name = 'Ягунов'
    # first_name = 'Денис'
    # faculty_name = 'МПУ'
    # course_name = 'Мат. Анализ'
    # grade = 100
    # res = await student_namager.create_student(
    #     last_name=last_name,
    #     first_name=first_name,
    #     faculty_name=faculty_name,
    #     course_name=course_name,
    #     grade=grade,
    # )
    # print(res)


if __name__ == "__main__":
    asyncio.run(runner())
