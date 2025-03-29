import asyncio

from homework_3.manager import StudentManager
from homework_4.services.course import course_service
from homework_4.services.faculty import faculty_service
from homework_4.services.student import student_service


async def runner():
    # Очищаем базу данных
    await student_service.drop_db()

    await student_service.init_db()

    await student_service.load_from_csv()

    res = await faculty_service.get_faculty(faculty_name="ФЛА")
    print(res)

    res = await faculty_service.get_faculty(faculty_id=1)
    print(res)

    res = await faculty_service.get_faculty(faculty_name="dsd")
    print(res)

    res = await course_service.get_course(course_name="Мат. Анализ")
    print(res)

    res = await course_service.get_course(course_name="Мат.sdsd Анализ")
    print(res)

    res = await course_service.get_course(course_id=1)
    print(res)

    res = await student_service.get_student(1)
    print(res)

    res = await course_service.create_course('Мой курс')
    print(res)

    res = await course_service.get_course(course_name='Мой курс')
    print(res)

    res = await faculty_service.create_faculty('Мой факультет')
    print(res)

    res = await faculty_service.get_faculty(faculty_name='Мой факультет')
    print(res)


    res = await student_service.get_student(2323)
    print(res)

    res = await student_service.get_students_by_faculty("ФПМИ")
    print(res)

    res = await course_service.get_unique_courses()
    print(res)

    res = await student_service.get_average_students_grade_by_faculty("ФПМИ")
    print(res)

    res = await student_service.get_students_below_grade_by_course("Мат. Анализ")
    print(res)

    last_name = 'Ягунов'
    first_name = 'Денис'
    faculty_name = 'МПУ'
    course_name = 'Мат. Анализ'
    grade = 100
    res = await student_service.create_student(
        last_name=last_name,
        first_name=first_name,
        faculty_name=faculty_name,
        course_name=course_name,
        grade=grade,
    )
    print(res)


if __name__ == "__main__":
    asyncio.run(runner())
