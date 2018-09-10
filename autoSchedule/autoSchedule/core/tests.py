import unittest
import datetime
from scheduling import Worker, Solver, Task
import sys

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

    

class Senarios(unittest.TestCase):
    def setUp(self):
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
        self.workers = workers
        self.tasks = tasks

    def test_base(self):
        workers, tasks = simple_setup()
        answer = Solver(tasks, 1, workers).solve()
        good_answer = "({'Toto': [Vaisselle_Task_0, Vaisselle_Task_3, Vaisselle_Task_6], 'Tata': [Vaisselle_Task_1, Vaisselle_Task_4], 'Titi': [Vaisselle_Task_2, Vaisselle_Task_5]}, [])"
        self.assertEqual(str(answer), good_answer) 
        self.assertEqual(answer[-1],  [])        
    
    def test_types(self):
        answer = Solver(self.tasks, 2, self.workers).solve()
        good_answer = "({'Toto': [Vaisselle_Task_0, Vaisselle_Task_2, Vaisselle_Task_4, Vaisselle_Task_6], 'Tata': [Menage_Task_1, Menage_Task_3, Menage_Task_5], 'Titi': [Menage_Task_1, Menage_Task_3, Menage_Task_5]}, [])"
        self.assertEqual(str(answer), good_answer)  
        self.assertEqual(answer[-1],  [])       
    
    def test_preferences(self):
        preference1 = {"Vaisselle":0, "Menage": 2}
        self.workers[1].preferences = preference1
        answer = Solver(self.tasks, 2, self.workers).solve()
        good_answer = "({'Toto': [Vaisselle_Task_0, Vaisselle_Task_2, Vaisselle_Task_4, Vaisselle_Task_6], 'Tata': [Menage_Task_1, Menage_Task_3, Menage_Task_5], 'Titi': [Menage_Task_1, Menage_Task_3, Menage_Task_5]}, [])"      
        self.assertEqual(str(answer), good_answer)   
        self.assertEqual(answer[-1],  [])  

    def test_unavailable(self):
        preference1 = {"Vaisselle":0, "Menage": 2}
        self.workers[1].preferences = preference1
        unavailable= [[now,now  + datetime.timedelta(days=1)], [now + datetime.timedelta(days=4), now + datetime.timedelta(days=6)]]
        self.workers[2].unavailable_periodes = unavailable
        answer = Solver(self.tasks, 2, self.workers).solve()
        good_answer = "({'Toto': [Vaisselle_Task_0, Vaisselle_Task_2, Menage_Task_3], 'Tata': [Menage_Task_1, Menage_Task_3, Vaisselle_Task_4, Menage_Task_5], 'Titi': [Menage_Task_1, Menage_Task_5, Vaisselle_Task_6]}, [])"      
        self.assertEqual(str(answer), good_answer)  
        self.assertEqual(answer[-1],  [])   

def setUpPerf():
    tasks = []
    types = ["Vaisselle"]
    workers = [Worker("Worker_" + str(i), types) for i in range(1000)]
    offset = datetime.timedelta(days=1)
    for i in range(1000):
        current_start = now + offset
        current_end = current_start + datetime.timedelta(days=1)
        offset += datetime.timedelta(days=1)
        tasks.append(Task("Task_" + str(i), types[0], current_start, current_end, 1))
    return workers, tasks




class Perf(unittest.TestCase):
    def setUp(self):
        tasks = []
        types = ["Vaisselle", "Menage", "Repas"]
        workers = [Worker("Worker_" + str(i), types) for i in range(1000)]
        offset = datetime.timedelta(days=1)
        for i in range(1000):
            current_start = now + offset
            current_end = current_start + datetime.timedelta(days=1)
            offset += datetime.timedelta(days=1)
            if i % 3 == 0:
                tasks.append(Task("Task_" + str(i), types[0], current_start, current_end, 1))
            elif i % 3 == 1:
                tasks.append(Task("Task_" + str(i), types[1], current_start, current_end, 2))
            elif i % 3 == 2:
                tasks.append(Task("Task_" + str(i), types[2], current_start, current_end, 3))
        self.workers = workers
        self.tasks = tasks
   
    def test_1000workers__1000taches_1types(self):
        workers, tasks = setUpPerf()
        answer = Solver(tasks, 1, workers).solve()
        repartion = [len(v.task_list) for v in answer[0].values()]
        charge = [v.charge for v in answer[0].values()]
        self.assertEqual(answer[-1],  []) 
        self.assertEqual(repartion,  [1]*1000) 
        self.assertEqual(charge,  [1]*1000) 

    def test_1000workers__1000taches_3types(self):
        answer = Solver(self.tasks, 3, self.workers).solve()
        repartion = [len(v.task_list) for v in answer[0].values()]
        charge = [v.charge for v in answer[0].values()]
        self.assertEqual(answer[-1],  []) 
        self.assertEqual(repartion,  [2]*999 + [1]) 
        self.assertEqual(charge,  [2]*999 + [1]) 

if __name__ == '__main__':
    #unittest.main() 
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )