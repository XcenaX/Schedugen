import json
import random
import datetime
from .costs import check_hard_constraints, subjects_order_cost, empty_space_groups_cost, empty_space_teachers_cost, \
    free_hour, WORK_HOURS, WORK_DAYS
from ..models import Class, Classroom
from .model import Data
from .model import Class as Class2


# ММММ
def load_data(file_path, teachers_empty_space, groups_empty_space, subjects_order):
    """
    Loads and processes input data, initialises helper structures.
    :param file_path: path to file with input data
    :param teachers_empty_space: dictionary where key = name of the teacher, values = list of rows where it is in
    :param groups_empty_space: dictionary where key = group index, values = list of rows where it is in
    :param subjects_order: dictionary where key = (name of the subject, index of the group), value = [int, int, int]
    where ints represent start times (row in matrix) for types of classes P, V and L respectively. If start time is -1
    it means that that subject does not have that type of class.
    :return: Data(groups, teachers, classes, classrooms)
    """
    with open(file_path) as file:
        data = json.load(file)

    # classes: dictionary where key = index of a class, value = class
    classes = {}
    # classrooms: dictionary where key = index, value = classroom name
    classrooms = {}
    # teachers: dictionary where key = teachers' name, value = index
    teachers = {}
    # groups: dictionary where key = name of the group, value = index
    groups = {}
    class_list = [] 

    # every class is assigned a list of classrooms he can be in as indexes (later columns of matrix)
    for type in data['Classrooms']:
        for name in data['Classrooms'][type]:
            new = Classroom(name, type)
            classrooms[len(classrooms)] = new    


    for cl in data['Classes']:
        new_group = cl['Group']
        new_teacher = cl['Teacher']
        max_lessons = cl['MaxLessons']

        # initialise for empty space of teachers
        if new_teacher not in teachers_empty_space:
            teachers_empty_space[new_teacher] = []

        # new = Class(new_group, new_teacher, cl['Subject'], cl['Type'], cl['Duration'], cl['Classroom'],  workloads[int(cl["Workload"])])
        
        # add groups
        for group in new_group:
            if group not in groups:
                groups[group] = len(groups)
                # initialise for empty space of groups
                groups_empty_space[groups[group]] = []
            
        # add teacher
        if new_teacher not in teachers:
            teachers[new_teacher] = len(teachers)
        
        for group in new_group:
            for i in range(max_lessons):
                new = Class2(group, new_teacher, cl['Subject'], cl['Type'], cl['Duration'], cl['Classroom'], cl["MaxLessons"], cl["Points"])
                class_list.append(new)

    # shuffle mostly because of teachers
    random.shuffle(class_list)
    # add classrooms
    for cl in class_list:
        classes[len(classes)] = cl

    

    # every class has a list of groups marked by its index, same for classrooms
    for i in classes:
        cl = classes[i]

        classroom = cl.classrooms
        index_classrooms = []
        # add classrooms
        for index, c in classrooms.items():
            if c.type == classroom:
                index_classrooms.append(index)
        cl.classrooms = index_classrooms

        class_groups = cl.groups
        index_groups = []
        for name, index in groups.items():
            if name in class_groups:
                # initialise order of subjects
                if (cl.subject, index) not in subjects_order:
                    subjects_order[(cl.subject, index)] = [-1, -1, -1]
                index_groups.append(index)
        cl.groups = index_groups

    return Data(groups, teachers, classes, classrooms)


def load_data2(teachers_empty_space, groups_empty_space):
    data_classes = Class.objects.all()
    data_classrooms = Classroom.objects.all()

    # classes: dictionary where key = index of a class, value = class
    classes = {}
    # classrooms: dictionary where key = index, value = classroom name
    classrooms = {}
    # teachers: dictionary where key = teachers' name, value = index
    teachers = {}
    # groups: dictionary where key = name of the group, value = index
    groups = {}
    class_list = [] 

    # every class is assigned a list of classrooms he can be in as indexes (later columns of matrix)
    for name in data_classrooms:
        classrooms[len(classrooms)] = name


    for cl in data_classes:
        new_group = cl.groups.all()
        new_teacher = cl.teacher.name
        max_lessons = cl.max_lessons

        # initialise for empty space of teachers
        if new_teacher not in teachers_empty_space:
            teachers_empty_space[new_teacher] = []

        # new = Class(new_group, new_teacher, cl['Subject'], cl['Type'], cl['Duration'], cl['Classroom'],  workloads[int(cl["Workload"])])
        
        # add groups
        for group in new_group:
            if group.name not in groups:
                groups[group.name] = len(groups)
                # initialise for empty space of groups
                groups_empty_space[groups[group.name]] = []
            
        # add teacher
        if new_teacher not in teachers:
            teachers[new_teacher] = len(teachers)
        
        for group in new_group:
            for i in range(max_lessons):
                classrooms_ids = []
                for clroom in cl.classrooms.all():
                    classrooms_ids.append(clroom.id)
                new = Class2(group.name, new_teacher, cl.subject.name, cl.duration, classrooms_ids, cl.max_lessons, cl.points)
                class_list.append(new)

    # shuffle mostly because of teachers
    random.shuffle(class_list)
    # add classrooms
    for cl in class_list:
        classes[len(classes)] = cl

    

    # every class has a list of groups marked by its index, same for classrooms
    for i in classes:
        cl = classes[i]

        classroom = cl.classrooms
        index_classrooms = []
        # add classrooms
        for index, c in classrooms.items():
            #if c.type == classroom:
            index_classrooms.append(index)
        cl.classrooms = index_classrooms

        class_groups = cl.groups
        index_groups = []
        for name, index in groups.items():
            if name in class_groups:                
                index_groups.append(index)
        cl.groups = index_groups

    return Data(groups, teachers, classes, classrooms), groups_empty_space, teachers_empty_space


def set_up(num_of_columns):
    """
    Sets up the timetable matrix and dictionary that stores free fields from matrix.
    :param num_of_columns: number of classrooms
    :return: matrix, free
    """
    w, h = num_of_columns, WORK_DAYS*WORK_HOURS # 5 (workdays) * 12 (work hours) = 60
    matrix = [[None for x in range(w)] for y in range(h)]
    free = []

    # initialise free dict as all the fields from matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            free.append((i, j))
    return matrix, free


def show_timetable(matrix):
    """
    Prints timetable matrix.
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    hours = get_time_of_lessons(WORK_HOURS)

    # print heading for classrooms
    for i in range(len(matrix[0])):
        if i == 0:
            print('{:17s} C{:6s}'.format('', '0'), end='')
        else:
            print('C{:6s}'.format(str(i)), end='')
    print()

    d_cnt = 0
    h_cnt = 0
    for i in range(len(matrix)):
        day = days[d_cnt]
        hour = hours[h_cnt]
        print('{:10s} {:13s} ->  '.format(day, "{0} - {1}".format(hour[0].strftime("%H:%M"), hour[1].strftime("%H:%M"))), end='')
        for j in range(len(matrix[i])):
            print('{:6s} '.format(str(matrix[i][j])), end='')
        print()
        h_cnt += 1
        if h_cnt == WORK_HOURS:
            h_cnt = 0
            d_cnt += 1
            print()

def get_group_by_index(groups, index):
    for key, value in groups.items():
        if index == value:
            return key

def get_schedule_for_group(data, matrix, group: str):
    group_schedule = {}
    for i in range(len(matrix)):                       
        if not group_schedule.get(i // WORK_HOURS):
            group_schedule[i // WORK_HOURS] = []

        founded = False

        for j in range(len(matrix[i])):
            if matrix[i][j] is not None:
                if get_group_by_index(data.groups, data.classes[matrix[i][j]].groups[0]) == group:
                    class_info = data.classes[matrix[i][j]].__to_dict__()
                    class_info["classroom"] = data.classrooms[j].name
                    class_info["group"] = group
                    group_schedule[i // WORK_HOURS].append(class_info)
                    founded = True
        if not founded:
            group_schedule[i // WORK_HOURS].append(None)
    return group_schedule


def get_schedule_for_groups(data, matrix):
    schedule = {}
    for group_name, group_index in data.groups.items():
        schedule[group_name] = get_schedule_for_group(data, matrix, group_name)
    return schedule


def show_timetable_for_groups(data, groups_matrix: dict):
    """
    Prints timetable matrix for all groups.
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    # hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    hours = get_time_of_lessons(WORK_HOURS)

    # print heading for groups
    count = 0
    for group_name, _ in groups_matrix.items():
        if count == 0:
            print('{:28s} {:6s}'.format('', group_name), end='')
        else:
            print('C{:6s}'.format(group_name), end='')
        count+=1
    print()

    d_cnt = 0
    h_cnt = 0
    matrix_len = WORK_DAYS*WORK_HOURS
    for i in range(matrix_len):
        day = days[d_cnt]
        day_index = days.index(day)
        hour = hours[h_cnt]
        hour_index = hours.index(hour)
        
        print('{:10s} {:13s} ->  '
            .format(day, "{0} - {1}"
            .format(hour[0].strftime("%H:%M"), hour[1].strftime("%H:%M"))), end='')
        
        for group_name, group_index in data.groups.items():
            if groups_matrix[group_name][day_index][hour_index] is not None:                
                print('{:6s} '.format("{:.{}s}".format(groups_matrix[group_name][day_index][hour_index].subject, 6)), end='')
            else:
                print('{:6s} '.format("None"), end='')
        
        print()
        h_cnt += 1
        if h_cnt == WORK_HOURS:
            h_cnt = 0
            d_cnt += 1
            print()


def get_time_of_lessons(count_of_lessons=6, hour=8, minute=0, hour2=14, minute2=0):
    """
        count_lessons = количество уроков для которых нужно получить время
        hour, minute = время начала первой смены
        hour2, minute2 = время начала второй смены
    """
    _break = 10 # перемена
    big_break = 15 # большая перемена
    big_break_lesson = [3, 9] # после этих уроков большая перемена
    lesson_duration = 40 
    start_time = datetime.datetime(year=2000, month=1, day=1, hour=hour, minute=minute)
    start_time2 = datetime.datetime(year=2000, month=1, day=1, hour=hour2, minute=minute2)
    time = []
    
    generated = False
    for i in range(count_of_lessons):
    
        if start_time.hour >= hour2 and generated is False:
            start_time = start_time2
            generated = True
        
        temp = start_time        
        start_time += datetime.timedelta(minutes=lesson_duration)
        time.append((temp, start_time))

        if i in big_break_lesson:
            start_time += datetime.timedelta(minutes=big_break)
        else:
            start_time += datetime.timedelta(minutes=_break)
        
    return time
        


def write_solution_to_file(matrix, data, filled, filepath, groups_empty_space, teachers_empty_space, subjects_order):
    """
    Writes statistics and schedule to file.
    """
    f = open('solution_files/sol_' + filepath, 'w')

    f.write('-------------------------- STATISTICS --------------------------\n')
    cost_hard = check_hard_constraints(matrix, data)
    if cost_hard == 0:
        f.write('\nHard constraints satisfied: 100.00 %\n')
    else:
        f.write('Hard constraints NOT satisfied, cost: {}\n'.format(cost_hard))
    f.write('Soft constraints satisfied: {:.02f} %\n\n'.format(subjects_order_cost(subjects_order)))

    empty_groups, max_empty_group, average_empty_groups = empty_space_groups_cost(groups_empty_space)
    f.write('TOTAL empty space for all GROUPS and all days: {}\n'.format(empty_groups))
    f.write('MAX empty space for GROUP in day: {}\n'.format(max_empty_group))
    f.write('AVERAGE empty space for GROUPS per week: {:.02f}\n\n'.format(average_empty_groups))

    empty_teachers, max_empty_teacher, average_empty_teachers = empty_space_teachers_cost(teachers_empty_space)
    f.write('TOTAL empty space for all TEACHERS and all days: {}\n'.format(empty_teachers))
    f.write('MAX empty space for TEACHER in day: {}\n'.format(max_empty_teacher))
    f.write('AVERAGE empty space for TEACHERS per week: {:.02f}\n\n'.format(average_empty_teachers))

    f_hour = free_hour(matrix)
    if f_hour != -1:
        f.write('Free term -> {}\n'.format(f_hour))
    else:
        f.write('NO hours without classes.\n')

    groups_dict = {}
    for group_name, group_index in data.groups.items():
        if group_index not in groups_dict:
            groups_dict[group_index] = group_name
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    hours = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    hours = get_time_of_lessons(WORK_HOURS) # 12 уроков в день

    f.write('\n--------------------------- SCHEDULE ---------------------------')
    for class_index, times in filled.items():
        c = data.classes[class_index]
        groups = ' '
        for g in c.groups:
            groups += groups_dict[g] + ', '
        f.write('\n\nClass {}\n'.format(class_index))
        f.write('Teacher: {} \nSubject: {} \nGroups:{} \nType: {} \nDuration: {} hour(s)'
                .format(c.teacher, c.subject, groups[:len(groups) - 2], c.type, c.duration))
        room = str(data.classrooms[times[0][1]])
        f.write('\nClassroom: {:2s}\nTime: {}'.format(room[:room.rfind('-')], days[times[0][0] // WORK_HOURS]))
        for time in times:
            current_hour = hours[time[0] % WORK_HOURS]
            f.write(' {}'.format("{0} - {1}".format(current_hour[0].strftime("%H:%M"), current_hour[1].strftime("%H:%M"))))
    f.close()


def show_statistics(matrix, data, groups_empty_space, teachers_empty_space):
    """
    Prints statistics.
    """
    cost_hard = check_hard_constraints(matrix, data)
    if cost_hard == 0:
        print('Hard constraints satisfied: 100.00 %')
    else:
        print('Hard constraints NOT satisfied, cost: {}'.format(cost_hard))
    # print('Soft constraints satisfied: {:.02f} %\n'.format(subjects_order_cost(subjects_order)))

    empty_groups, max_empty_group, average_empty_groups = empty_space_groups_cost(groups_empty_space)
    print('TOTAL empty space for all GROUPS and all days: ', empty_groups)
    print('MAX empty space for GROUP in day: ', max_empty_group)
    print('AVERAGE empty space for GROUPS per week: {:.02f}\n'.format(average_empty_groups))

    empty_teachers, max_empty_teacher, average_empty_teachers = empty_space_teachers_cost(teachers_empty_space)
    print('TOTAL empty space for all TEACHERS and all days: ', empty_teachers)
    print('MAX empty space for TEACHER in day: ', max_empty_teacher)
    print('AVERAGE empty space for TEACHERS per week: {:.02f}\n'.format(average_empty_teachers))

    f_hour = free_hour(matrix)
    if f_hour != -1:
        print('Free term ->', f_hour)
    else:
        print('NO hours without classes.')
