import simpy

class HostpitalATUResources:
    """Resources class for simpy. resources are nurses and chairs"""
    def __init__(self, env, number_of_docs, number_of_nurses, number_of_chairs, number_of_pharmacists, number_of_cashiers):
        self.docs = simpy.PriorityResource(env, capacity=number_of_docs)
        self.chairs = simpy.PriorityResource(env, capacity=number_of_chairs)
        self.nurses = simpy.PriorityResource(env, capacity=number_of_nurses)
        self.pharmacists = simpy.PriorityResource(env, capacity=number_of_pharmacists)
        self.cashiers = simpy.PriorityResource(env, capacity=number_of_cashiers)