

class Worker:
    def __init__(self, name, type_list, unavailable_periodes=[], preferences=None):
        self.name = name
        self.task_list = []
        self.charge = 0
        self.unavailable_periodes = unavailable_periodes

        if preferences:
            self.preferences = preferences
        else:
            avg = len(type_list) // 2
            self.preferences = dict()
            for type_task in type_list:
                self.preferences[type_task] = avg

    def addTask(self, task):
        self.charge += task.difficulty
        self.task_list.append(task.addworker())

    def canAccept(self, try_task):
        for periode in self.unavailable_periodes:
            if periode[0] <= try_task.start < periode[1] or periode[0] < try_task.end < periode[1]:
                return False

        for task in self.task_list:
            if task.start <= try_task.start < task.end or task.start < try_task.end < task.end:
                return False
        return True

    def __repr__(self):
        return str({"Worker": self.name, "task_list_size": len(self.task_list), "charge" : self.charge})
