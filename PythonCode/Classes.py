# Classes

class Assignments:
    def __init__(self, id, name, type, priority, qnt_week, specific_slottime, task_time, periods):
        self.id = id
        self.name = name
        self.type = type
        self.priority = priority
        self.qnt_week = qnt_week
        self.specific_slottime = specific_slottime
        self.task_time = task_time
        self.periods = periods

class Periods:
    def __init__(self, id, day, time):
        self.id = id
        self.day = day
        self.time = time