# Classes

class Assignment:

    def __init__(self, id, name, type, priority, qnt_week, specific_slottime, task_time, periods):
        self.id = id
        self.name = name
        self.type = type
        self.priority = priority
        self.qnt_week = qnt_week
        self.specific_slottime = specific_slottime
        self.task_time = task_time
        self.periods = periods
        self.period_scheduled = 0

    def setPeriodScheduled(self, period_scheduled):
        self.period_scheduled = period_scheduled

    def getPeriodScheduled(self):
        return self.period_scheduled

class Periods:
    def __init__(self, id, available):
        self.ID = id
        self.available = available

    def getIDPeriod(self):
        return self.ID
    
