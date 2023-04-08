from random import shuffle

def assign_teachers_to_classes(teachers, classes):
    # Сортируем учителей по специализации и случайным образом перемешиваем
    sorted_teachers = sorted(teachers, key=lambda x: x.specialization)
    shuffle(sorted_teachers)

    # Создаем словарь для хранения учителей и классов, которые им назначены
    teacher_assignments = {teacher: [] for teacher in sorted_teachers}

    # Назначаем учителей на классы с учетом их предпочтений
    for school_class in classes:
        # Сортируем учителей по количеству уроков, которые они уже имеют в день
        available_teachers = sorted(
            sorted_teachers,
            key=lambda x: len(teacher_assignments[x]),
            reverse=True
        )

        # Находим первого доступного учителя с соответствующей специализацией и назначаем его на класс
        for teacher in available_teachers:
            if teacher.specialization == school_class.specialization:
                teacher_assignments[teacher].append(school_class)
                break

    return teacher_assignments


def divide_classes_into_groups(classes):
    # Создаем словарь для хранения классов и их предметов
    classes_by_subject = {}

    # Сортируем классы по названию и группируем их по предметам
    sorted_classes = sorted(classes, key=lambda x: x.class_name)
    for school_class in sorted_classes:
        if school_class.teacher.specialization not in classes_by_subject:
            classes_by_subject[school_class.teacher.specialization] = []
        classes_by_subject[school_class.teacher.specialization].append(school_class)

    # Назначаем количество уроков для каждого класса
    for subject, classes in classes_by_subject.items():
        classes_per_day = len(classes) // 6  # 6 - количество учебных дней в неделю
        classes_per_week = len(classes)

        for school_class in classes:
            school_class.max_lessons_per_day = classes_per_day
            school_class.max_lessons_per_week = classes_per_week // classes_per_day
            school_class.save()


