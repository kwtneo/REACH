import simpy

class HostpitalATUResources:
    """Resources class for simpy. resources are nurses and chairs"""
    def __init__(self, env, number_of_docs, number_of_nurses, number_of_chairs, number_of_pharmacists, number_of_cashiers):
        self.docs = simpy.PriorityResource(env, capacity=number_of_docs)
        self.chairs = simpy.PriorityResource(env, capacity=number_of_chairs)
        self.nurses = simpy.PriorityResource(env, capacity=number_of_nurses)
        self.pharmacists = simpy.Resource(env, capacity=number_of_pharmacists)
        self.cashiers = simpy.Resource(env, capacity=number_of_cashiers)

    def get_nurse_request(self,priority = 1):
        return self.nurses.request(priority=priority)
    def get_doc_request(self,priority = 1):
        return self.docs.request(priority=priority)
    def get_chair_request(self,priority = 1):
        return self.chairs.request(priority=priority)
    def get_cashier_request(self):
        return self.cashiers.request()
    def get_pharmacist_request(self):
        return self.pharmacists.request()

    def print_stats(self,res='nurse'):
        if(res=='nurse'):
            ptr = self.nurses
        if(res=='cashier'):
            ptr = self.cashiers
        if(res=='pharmacist'):
            ptr = self.pharmacists

        print(f'{ptr.count} of {ptr.capacity} slots are allocated.')
        print(f'  Users: {ptr.users}')
        print(f'  Queued events: {ptr.queue}')