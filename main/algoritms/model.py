class Workload:
    def __init__(self, points, groups, subject,  max_lessons):
        self.points = points # Нагрузка предмета в баллах для текущего класса
        self.groups = groups
        self.subject = subject        
        self.max_lessons = max_lessons

    def __str__(self):
        return "Subject {} | Points '{}' | Groups '{}'\n"\
            .format(self.subject, self.points, self.groups)

    def __repr__(self):
        return str(self)

class Class:

    def __init__(self, groups, teacher, subject, type, duration, classrooms, max_lessons, points):
        self.groups = groups
        self.teacher = teacher
        self.subject = subject
        self.type = type
        self.duration = duration
        self.classrooms = classrooms
        self.max_lessons = max_lessons
        self.points = points

    def __str__(self):
        return "Groups {} | Teacher '{}' | Subject '{}' | Type {} | {} hours | Classrooms {} \n"\
            .format(self.groups, self.teacher, self.subject, self.type, self.duration, self.classrooms)

    def __repr__(self):
        return str(self)


class Classroom:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return "{} - {} \n".format(self.name, self.type)

    def __repr__(self):
        return str(self)


class Data:

    def __init__(self, groups, teachers, classes, classrooms):
        self.groups = groups
        self.teachers = teachers
        self.classes = classes
        self.classrooms = classrooms
