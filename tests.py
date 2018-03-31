import unittest
import datetime
from scheduling import Worker, Solver, Task

now = datetime.datetime.now()

def simple_setup():
    now = datetime.datetime.now()
    tasks = []
    names = ["Toto", "Tata", "Titi"]
    types = ["Vaisselle"]
    workers = [Worker(name, types) for name in names]
    offset = datetime.timedelta(days=1)
    for i in range(7):
        current_start = now + offset
        current_end = current_start + datetime.timedelta(days=1)
        offset += datetime.timedelta(days=1)
        name = "Task_" + str(i)
        tasks.append(Task(name, types[0], current_start, current_end, 1))
    return workers, tasks
    
types = ["Vaisselle", "Menage"]
def setup():
    
    tasks = []
    names = ["Toto", "Tata", "Titi"]
    types = ["Vaisselle", "Menage"]
    workers = [Worker(name, types) for name in names]
    offset = datetime.timedelta(days=1)
    for i in range(7):
        current_start = now + offset
        current_end = current_start + datetime.timedelta(days=1)
        offset += datetime.timedelta(days=1)
        name = "Task_" + str(i)
        if i % 2 == 0:
            tasks.append(Task(name, types[0], current_start, current_end, 1))
        else:        
            tasks.append(Task(name, types[1], current_start, current_end, 2))
    return workers, tasks


class Senario1(unittest.TestCase):
    def test_base(self):
        workers, tasks = simple_setup()
        answer = Solver(tasks, 1, workers).solve()
        good_answer = "({'Toto': [], 'Tata': [], 'Titi': [Vaisselle_Task_0, Vaisselle_Task_1, Vaisselle_Task_2, Vaisselle_Task_3, Vaisselle_Task_4, Vaisselle_Task_5, Vaisselle_Task_6]}, [])"
        self.assertEqual(str(answer), good_answer)        
    
    def test_types(self):
        workers, tasks = setup()
        answer = Solver(tasks, 2, workers).solve()
        good_answer = "({'Toto': [], 'Tata': [Menage_Task_1, Menage_Task_3, Menage_Task_5], 'Titi': [Vaisselle_Task_0, Menage_Task_1, Vaisselle_Task_2, Menage_Task_3, Vaisselle_Task_4, Menage_Task_5, Vaisselle_Task_6]}, [])"
        self.assertEqual(str(answer), good_answer)        
    
    def test_preferences(self):
        workers, tasks = setup()
        preference1 = {"Vaisselle":0, "Menage": 2}
        workers[1].preferences = preference1
        answer = Solver(tasks, 2, workers).solve()
        good_answer = "({'Toto': [], 'Tata': [Menage_Task_1, Menage_Task_3, Menage_Task_5], 'Titi': [Vaisselle_Task_0, Menage_Task_1, Vaisselle_Task_2, Menage_Task_3, Vaisselle_Task_4, Menage_Task_5, Vaisselle_Task_6]}, [])"      
        self.assertEqual(str(answer), good_answer)    

    def test_unavailable(self):
        workers, tasks = setup()
        preference1 = {"Vaisselle":0, "Menage": 2}
        workers[1].preferences = preference1
        unavailable= [[now,now  + datetime.timedelta(days=1)], [now + datetime.timedelta(days=4), now + datetime.timedelta(days=6)]]
        workers[2].unavailable_periodes = unavailable
        answer = Solver(tasks, 2, workers).solve()
        good_answer = "({'Toto': [Menage_Task_3, Vaisselle_Task_4], 'Tata': [Menage_Task_1, Menage_Task_3, Menage_Task_5], 'Titi': [Vaisselle_Task_0, Menage_Task_1, Vaisselle_Task_2, Menage_Task_5, Vaisselle_Task_6]}, [])"      
        self.assertEqual(str(answer), good_answer)    

if __name__ == '__main__':
    unittest.main() 