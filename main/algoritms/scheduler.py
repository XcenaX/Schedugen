import random
from operator import itemgetter
from utils import load_data, show_timetable, set_up, show_statistics, write_solution_to_file, show_timetable_for_groups, get_schedule_for_groups
from costs import check_hard_constraints, hard_constraints_cost, empty_space_groups_cost, empty_space_teachers_cost, \
    free_hour, WORK_HOURS, WORK_DAYS
import copy
import math


def initial_population(data, matrix, free, filled, groups_empty_space, teachers_empty_space, subjects_order):
    """
    Настраивает начальное расписание для заданных классов,
    вставляя в свободные поля таким образом,
    чтобы каждый урок находился в соответствующем классе.
    """
    classes = data.classes

    for index, classs in classes.items():
        ind = 0
        # ind = random.randrange(len(free) - int(classs.duration))
        while True:
            start_field = free[ind]

            # проверяем не начинаются ли занятия в один день а закончиваются на следующий день
            start_time = start_field[0]
            end_time = start_time + int(classs.duration) - 1
            if start_time % WORK_HOURS > end_time % WORK_HOURS:
                ind += 1
                continue

            found = True
            # проверяем свободен ли весь блок для класса
            for i in range(1, int(classs.duration)):
                field = (i + start_time, start_field[1])
                if field not in free:
                    found = False
                    ind += 1
                    break

            # подходит ли кабинет 
            if start_field[1] not in classs.classrooms:
                ind += 1
                continue

            if found:
                for group_index in classs.groups:
                    # добавляем порядок предметов для групп
                    insert_order(subjects_order, classs.subject, group_index, classs.type, start_time)                    
                    # добавялем время занятий для группы
                    for i in range(int(classs.duration)):
                        groups_empty_space[group_index].append(i + start_time)

                for i in range(int(classs.duration)):
                    filled.setdefault(index, []).append((i + start_time, start_field[1]))         
                    free.remove((i + start_time, start_field[1]))                                
                    # добавялем время занятий для учителей
                    teachers_empty_space[classs.teacher].append(i + start_time)
                break

    # заполняем матрицу
    for index, fields_list in filled.items():
        for field in fields_list:
            matrix[field[0]][field[1]] = index


def insert_order(subjects_order, subject, group, type, start_time):
    """
    Вставляет время начала занятия для данного предмета, группы и типа занятия.
    """
    times = subjects_order[(subject, group)]
    if type == 'P':
        times[0] = start_time
    elif type == 'V':
        times[1] = start_time
    else:
        times[2] = start_time
    subjects_order[(subject, group)] = times


def exchange_two(matrix, filled, ind1, ind2):
    """    
    Меняет местами два занятия одинаковой продолжительности в матрице расписания.
    """
    fields1 = filled[ind1]
    filled.pop(ind1, None)
    fields2 = filled[ind2]
    filled.pop(ind2, None)

    for i in range(len(fields1)):
        t = matrix[fields1[i][0]][fields1[i][1]]
        matrix[fields1[i][0]][fields1[i][1]] = matrix[fields2[i][0]][fields2[i][1]]
        matrix[fields2[i][0]][fields2[i][1]] = t

    filled[ind1] = fields2
    filled[ind2] = fields1

    return matrix


def valid_teacher_group_row(matrix, data, index_class, row):
    """    
    Возвращает, может ли находиться класс в этой строке из-за возможного перекрытия учителей или групп.
    """
    c1 = data.classes[index_class]
    for j in range(len(matrix[row])):
        if matrix[row][j] is not None:
            c2 = data.classes[matrix[row][j]]
            # check teacher
            if c1.teacher == c2.teacher:
                return False
            # check groups
            for g in c2.groups:
                if g in c1.groups:
                    return False
    return True


def mutate_ideal_spot(matrix, data, ind_class, free, filled, groups_empty_space, teachers_empty_space, subjects_order):
    """    
    Функция, которая пытается найти новые поля в матрице для индекса класса, где стоимость класса равна 0 (учитываются
    только жесткие ограничения). Если найдено оптимальное место, поля в матрице заменяются.
    """

    # найдим строки и поля, в которых в данный момент находится класс
    rows = []
    fields = filled[ind_class]
    for f in fields:
        rows.append(f[0])

    classs = data.classes[ind_class]
    ind = 0
    while True:        
        # идеальное место не найдено, делаем return
        if ind >= len(free):
            return
        start_field = free[ind]
        
        # проверяем не начнутся ли занятия в один день а закончатся на следующий день
        start_time = start_field[0]
        end_time = start_time + int(classs.duration) - 1
        if start_time % WORK_HOURS > end_time % WORK_HOURS:
            ind += 1
            continue
        
        # проверяем подходит ли новый класс
        if start_field[1] not in classs.classrooms:
            ind += 1
            continue

        # проверяем можно ли использовать весь блок для нового класса и возможных совпадений с учителями и группами
        found = True
        for i in range(int(classs.duration)):
            field = (i + start_time, start_field[1])
            if field not in free or not valid_teacher_group_row(matrix, data, ind_class, field[0]):
                found = False
                ind += 1
                break

        if found:            
            # удаляем текущий класс из заполненного dict и добавьте его в свободный dict
            filled.pop(ind_class, None)
            for f in fields:
                free.append((f[0], f[1]))
                matrix[f[0]][f[1]] = None
                # remove empty space of the group from old place of the class
                for group_index in classs.groups:
                    groups_empty_space[group_index].remove(f[0])
                # remove teacher's empty space from old place of the class
                teachers_empty_space[classs.teacher].remove(f[0])

            # update order of the subjects and add empty space for each group
            for group_index in classs.groups:
                insert_order(subjects_order, classs.subject, group_index, classs.type, start_time)
                for i in range(int(classs.duration)):
                    groups_empty_space[group_index].append(i + start_time)

            # add new term of the class to filled, remove those fields from free dict and insert new block in matrix
            for i in range(int(classs.duration)):
                filled.setdefault(ind_class, []).append((i + start_time, start_field[1]))
                free.remove((i + start_time, start_field[1]))
                matrix[i + start_time][start_field[1]] = ind_class
                # add new empty space for teacher
                teachers_empty_space[classs.teacher].append(i+start_time)
            break


def evolutionary_algorithm(matrix, data, free, filled, groups_empty_space, teachers_empty_space, subjects_order):
    """
    Evolutionary algorithm that tires to find schedule such that hard constraints are satisfied.
    It uses (1+1) evolutionary strategy with Stifel's notation.
    """
    n = 3
    sigma = 2
    run_times = 5
    max_stagnation = 200

    for run in range(run_times):
        print('Run {} | sigma = {}'.format(run + 1, sigma))

        t = 0
        stagnation = 0
        cost_stats = 0
        while stagnation < max_stagnation:

            # check if optimal solution is found
            loss_before, cost_classes, cost_teachers, cost_classrooms, cost_groups = hard_constraints_cost(matrix, data)
            if loss_before == 0 and check_hard_constraints(matrix, data) == 0:
                print('Found optimal solution: \n')
                show_timetable(matrix)
                break

            # sort classes by their loss, [(loss, class index)]
            costs_list = sorted(cost_classes.items(), key=itemgetter(1), reverse=True)

            # 10*n
            for i in range(len(costs_list) // 4):
                # mutate one to its ideal spot
                if random.uniform(0, 1) < sigma and costs_list[i][1] != 0:
                    mutate_ideal_spot(matrix, data, costs_list[i][0], free, filled, groups_empty_space,
                                      teachers_empty_space, subjects_order)
                # else:
                #     # exchange two who have the same duration
                #     r = random.randrange(len(costs_list))
                #     c1 = data.classes[costs_list[i][0]]
                #     c2 = data.classes[costs_list[r][0]]
                #     if r != i and costs_list[r][1] != 0 and costs_list[i][1] != 0 and c1.duration == c2.duration:
                #         exchange_two(matrix, filled, costs_list[i][0], costs_list[r][0])

            loss_after, _, _, _, _ = hard_constraints_cost(matrix, data)
            if loss_after < loss_before:
                stagnation = 0
                cost_stats += 1
            else:
                stagnation += 1

            t += 1
            # Stifel for (1+1)-ES
            if t >= 10*n and t % n == 0:
                s = cost_stats
                if s < 2*n:
                    sigma *= 0.85
                else:
                    sigma /= 0.85
                cost_stats = 0

        print('Number of iterations: {} \nCost: {} \nTeachers cost: {} | Groups cost: {} | Classrooms cost:'
              ' {}'.format(t, loss_after, cost_teachers, cost_groups, cost_classrooms))


def simulated_hardening(matrix, data, free, filled, groups_empty_space, teachers_empty_space, subjects_order, file):
    """
    Algorithm that uses simulated hardening with geometric decrease of temperature to optimize timetable by satisfying
    soft constraints as much as possible (empty space for groups and existence of an hour in which there is no classes).
    """
    # number of iterations
    iter_count = 2500
    # temperature
    t = 0.5
    _, _, curr_cost_group = empty_space_groups_cost(groups_empty_space)
    _, _, curr_cost_teachers = empty_space_teachers_cost(teachers_empty_space)
    curr_cost = curr_cost_group  # + curr_cost_teachers
    if free_hour(matrix) == -1:
        curr_cost += 1

    for i in range(iter_count):
        rt = random.uniform(0, 1)
        t *= 0.99                   # geometric decrease of temperature

        # save current results
        old_matrix = copy.deepcopy(matrix)
        old_free = copy.deepcopy(free)
        old_filled = copy.deepcopy(filled)
        old_groups_empty_space = copy.deepcopy(groups_empty_space)
        old_teachers_empty_space = copy.deepcopy(teachers_empty_space)
        old_subjects_order = copy.deepcopy(subjects_order)

        # try to mutate 1/4 of all classes
        for j in range(len(data.classes) // 4):
            index_class = random.randrange(len(data.classes))
            mutate_ideal_spot(matrix, data, index_class, free, filled, groups_empty_space, teachers_empty_space,
                              subjects_order)
        _, _, new_cost_groups = empty_space_groups_cost(groups_empty_space)
        _, _, new_cost_teachers = empty_space_teachers_cost(teachers_empty_space)
        new_cost = new_cost_groups  # + new_cost_teachers
        if free_hour(matrix) == -1:
            new_cost += 1

        if new_cost < curr_cost or rt <= math.exp((curr_cost - new_cost) / t):
            # take new cost and continue with new data
            curr_cost = new_cost
        else:
            # return to previously saved data
            matrix = copy.deepcopy(old_matrix)
            free = copy.deepcopy(old_free)
            filled = copy.deepcopy(old_filled)
            groups_empty_space = copy.deepcopy(old_groups_empty_space)
            teachers_empty_space = copy.deepcopy(old_teachers_empty_space)
            subjects_order = copy.deepcopy(old_subjects_order)
        if i % 100 == 0:
            print('Iteration: {:4d} | Average cost: {:0.8f}'.format(i, curr_cost))

    print('TIMETABLE AFTER HARDENING')
    show_timetable(matrix)
    print('STATISTICS AFTER HARDENING')
    show_statistics(matrix, data, subjects_order, groups_empty_space, teachers_empty_space)
    write_solution_to_file(matrix, data, filled, file, groups_empty_space, teachers_empty_space, subjects_order)


def make_schedule(data):
    """
    main method but with current db
    """
    filled = {}
    subjects_order = {}
    groups_empty_space = {}
    teachers_empty_space = {}
    
    data = load_data('test_files/' + file, teachers_empty_space, groups_empty_space, subjects_order)
        
    matrix, free = set_up(len(data.classrooms))
    initial_population(data, matrix, free, filled, groups_empty_space, teachers_empty_space, subjects_order)

    total, _, _, _, _ = hard_constraints_cost(matrix, data)
    print('Initial cost of hard constraints: {}'.format(total))

    evolutionary_algorithm(matrix, data, free, filled, groups_empty_space, teachers_empty_space, subjects_order)
    print('STATISTICS')
    show_statistics(matrix, data, subjects_order, groups_empty_space, teachers_empty_space)
        
    simulated_hardening(matrix, data, free, filled, groups_empty_space, teachers_empty_space, subjects_order, file)

    print("TIMETABLE FOR GROUPS OY DA:\n") # ВОТ ТУТ ВСЕ ВЫВОДИТСЯ

    groups_matrix = get_schedule_for_groups(data, matrix)
    show_timetable_for_groups(data, groups_matrix)



def main():
    """
    free = [(row, column)...] - list of free fields (row, column) in matrix
    filled: dictionary where key = index of the class, value = list of fields in matrix

    subjects_order: dictionary where key = (name of the subject, index of the group), value = [int, int, int]
    where ints represent start times (row in matrix) for types of classes P, V and L respectively
    groups_empty_space: dictionary where key = group index, values = list of rows where it is in
    teachers_empty_space: dictionary where key = name of the teacher, values = list of rows where it is in

    matrix = columns are classrooms, rows are times, each field has index of the class or it is empty
    data = input data, contains classes, classrooms, teachers and groups
    """
    filled = {}
    subjects_order = {}
    groups_empty_space = {}
    teachers_empty_space = {}
    file = 'ulaz1.txt'

    
    data = load_data('test_files/' + file, teachers_empty_space, groups_empty_space, subjects_order)
        
    matrix, free = set_up(len(data.classrooms))
    initial_population(data, matrix, free, filled, groups_empty_space, teachers_empty_space, subjects_order)

    total, _, _, _, _ = hard_constraints_cost(matrix, data)
    print('Initial cost of hard constraints: {}'.format(total))

    evolutionary_algorithm(matrix, data, free, filled, groups_empty_space, teachers_empty_space, subjects_order)
    print('STATISTICS')
    show_statistics(matrix, data, subjects_order, groups_empty_space, teachers_empty_space)
        
    simulated_hardening(matrix, data, free, filled, groups_empty_space, teachers_empty_space, subjects_order, file)

    print("TIMETABLE FOR GROUPS OY DA:\n") # ВОТ ТУТ ВСЕ ВЫВОДИТСЯ

    groups_matrix = get_schedule_for_groups(data, matrix)
    show_timetable_for_groups(data, groups_matrix)


if __name__ == '__main__':
    main()
