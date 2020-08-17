import Config
import random

global Global_vars
Global_vars = Config.Global_vars


class patient_vars:
    between_visits_time_mean = .1 * 24 * 60
    between_visits_time_sd = 3 * 24 * 60
    psa_registration_time_mean = 10
    psa_registration_time_sd = 7
    generic_waiting_time_mean = 95.7
    generic_waiting_time_sd = 7 / 10 * generic_waiting_time_mean
    physician_consultation_1_time_mean = 29
    physician_consultation_1_time_sd = 7 / 10 * physician_consultation_1_time_mean
    psa_payment_time_mean = 7.5
    psa_payment_time_sd = 7 / 10 * psa_payment_time_mean
    psa_scheduling_time_mean = 7.5
    psa_scheduling_time_sd = 7 / 10 * psa_scheduling_time_mean

    blood_test_time_mean = 30
    blood_test_time_sd = 7 / 10 * blood_test_time_mean
    blood_test_atu_time_mean = 15
    blood_test_atu_time_sd = 7 / 10 * blood_test_atu_time_mean
    blood_test_screening_time_mean = 15
    blood_test_screening_time_sd = 7 / 10 * blood_test_screening_time_mean

    physician_consultation_2_time_mean = 11.5
    physician_consultation_2_time_sd = 7 / 10 * physician_consultation_2_time_mean
    IV_start_time_mean = 1
    IV_start_time_sd = 7 / 10 * IV_start_time_mean
    IV_chemo_infusion_time_mean = 1
    IV_chemo_infusion_time_sd = 7 / 10 * IV_chemo_infusion_time_mean
    review_test_results_time_mean = 120
    review_test_results_time_sd = 7 / 10 * review_test_results_time_mean

    breast_facility_time_mean = 1
    breast_facility_time_sd = 7 / 10 * breast_facility_time_mean
    breast_atu_premed_time_mean = 1
    breast_atu_premed_time_sd = 7 / 10 * breast_atu_premed_time_mean

    breast_dox_cyclophos_time_mean = 90
    breast_dox_cyclophos_time_sd = 7 / 10 * breast_dox_cyclophos_time_mean
    breast_dox_cyclophos_adr_time_mean = 60
    breast_dox_cyclophos_adr_time_sd = 7 / 10 * breast_dox_cyclophos_adr_time_mean

    breast_paclitax_time_mean = 180
    breast_paclitax_time_sd = 7 / 10 * breast_paclitax_time_mean
    breast_paclitax_adr_time_mean = 67.8
    breast_paclitax_adr_time_sd = 7 / 10 * breast_paclitax_adr_time_mean

    post_chemo_pharmacy_time_mean = 5
    post_chemo_pharmacy_time_sd = 7 / 10 * post_chemo_pharmacy_time_mean

    post_chemo_psa_registration_time_mean = 5
    post_chemo_psa_registration_time_sd = 7 / 10 * post_chemo_psa_registration_time_mean

    # Set up probability based generators
    breast_dox_cyclophos_adr_probability = 0.009
    breast_dox_cyclophos_adr_probability_gen = (1 if random.random() < 0.009 else 0 for _ in range(1000000))
    breast_adj_blood_test1_probability = 0.7
    breast_adj_blood_test1_probability_gen = (1 if random.random() < 0.7 else 0 for _ in range(1000000))
    breast_adj_blood_test2_probability = 0.7
    breast_adj_blood_test2_probability_gen = (1 if random.random() < 0.7 else 0 for _ in range(1000000))
    breast_adj_blood_test_atu_ac_probability = 0.3
    breast_adj_blood_test_atu_ac_probability_gen = (1 if random.random() < 0.3 else 0 for _ in range(1000000))
    breast_adj_blood_test_atu_ac_review_probability = 0.3
    breast_adj_blood_test_atu_ac_review_probability_gen = (1 if random.random() < 0.3 else 0 for _ in
                                                                range(100000))
    breast_adj_blood_test_atu_t_probability = 0.3
    breast_adj_blood_test_atu_t_probability_gen = (1 if random.random() < 0.3 else 0 for _ in range(1000000))
    breast_adj_blood_test_atu_t_review_probability = 0.3
    breast_adj_blood_test_atu_t_review_probability_gen = (1 if random.random() < 0.3 else 0 for _ in range(100000))
    breast_paclitax_adr_probability = 0.027
    breast_paclitax_adr_probability_gen = (1 if random.random() < 0.027 else 0 for _ in range(1000000))

    # conditions:
    conditions_map = {1: 'Breast_Metastatic', 2: 'Breast_Adjuvant', 3: 'GI_Metastatic', 4: 'GI_Adjuvant',
                           5: 'Lung_Metastatic', 6: 'Lung_Adjuvant'}

    # treatment specific variables (costs)
    Breast_adj_ACP = {'ac_cycles': 4, 't_cycles': 12, 'clinic_costs_1': 310.03, 'fu_clinics': 8,
                           'fu_clinic_cost': 249.19, 'total_atu_cost': 14771.88, 'manpower': 87.9,
                           'time': 4988.4272, 'overall_mortality_post': .35, 'overall_mortality_pre': .4,
                           'overall_survivability_post': .863, 'overall_survivability_pre': .842,
                           'os_time_mths': 6}

    # Breast_met_Dox
    # Breast_met_Pax
    # Breast_met_Cap
    # Lung_adj_GemCis
    # Lung_met_PCP
    # Lung_met_Pemz
    # Lung_met_Osi
    # GI_adj_Capox
    # GI_met_Cap
    # GI_met_Folfox
    # GI_met_Capox





class CancerPatient:

    """The Patient class is for patient objects. Each patient is an instance of
    this class. This class also holds a static dictionary which holds all
    patient objects (a patient is removed after exiting).

    Methods are:
    __init__: constructor for new patient
    treatment_regime()
    """

    # The following static class dictionary stores all patient objects
    # This is not actually used further but shows how patients may be tracked
    all_patients = {}

    def __init__(self, env, id, hospital, condition, treatment_regime=None):
        """Constructor for new patient object.
        """

        # Increment global counts of patients

        # Set patient id and priority (random between 1 and 3)
        self.id = id
        self.priority = random.randint(1 , 1)
        self.condition = condition
        self.treatment_regime = treatment_regime
        self.treatment_regime_step = None
        self.env = env
        self.hospital = hospital
        # Set consultation time (time spent with doc) by random normal
        # distribution. If value <0 then set to 0
        #self.consulation_time = random.normalvariate(Global_vars.appointment_time_mean, Global_vars.appointment_time_sd)
        #self.consulation_time = 0 if self.consulation_time < 0 else self.consulation_time

        self.treatment_time_start = 0
        self.admin_time_start = 0
        # Set initial queuing time as zero (this will be adjusted in model if
        # patient has to waiti for doc)
        self.treatment_time = 0
        self.admin_time = 0
        self.inbetween_treatmenttime = 0

        # record simulation time patient enters simulation
        self.time_in = env.now
        self.treatment_step_in = 0
        # Set up variables to record simulation time that patients see doc and
        # exit simulation
        #self.time_see_doc = 0
        self.waiting_time = 0
        self.entire_treatment_regime_time = 0
        self.time_out = 0

    def get_treatment_regime(self):
        return None

    def undergo_regiment(self):
        for treatment_item in self.get_treatment_regime():
            t_time, t_stdev, t_desc, t_resource_depend, t_type = treatment_item
            if(t_type=='admin'):
                print('processing admin time:'+t_desc+' which takes:'+str(t_time)+' mins')
                if(t_resource_depend is not None):
                    if('pharmacist' in t_resource_depend):

                        with self.hospital.get_pharmacist_request() as pharmacists_req:
                            # Increment count of number of patients waiting. 1 is subtracted
                            # from priority to align priority (1-3) with zero indexed list.
                            # if(self.id not in Global_vars.patients_db.keys()):
                            self.hospital.print_stats('pharmacist')
                            Global_vars.admin_time += t_time
                            Global_vars.patients_waiting += 1
                            print('patient:' + str(self.id + 1) + ' waiting for pharmacists, current queue:' + str(Global_vars.patients_waiting) +' and timenow='+ str(self.env.now))
                            Global_vars.patients_waiting_for_pharmacists += 1
                            Global_vars.patients_waiting_by_priority[self.priority - 1] += 1

                            # Wait for resources to become available
                            yield pharmacists_req

                            '''
                            # Hold patient (with nurse) for treatment time required
                            yield self.env.timeout(t_time)
                            # At end of treatment add time spent to temp results
                            admin_results.append(self.env.now - self.admin_time_start)
                            # Record results in global results data if warm-up complete
                            if self.env.now >= Global_vars.warm_up:
                                Global_vars.patient_admin_queuing_results.loc[self.id + 1] = admin_results
                            # Resources now available. Record time patient starts to see doc
                            '''
                            self.admin_time_start = self.env.now
                            #admin_results = [self.priority, self.admin_time]
                            # Record patient queuing time in patient object
                            self.queuing_time = self.env.now - self.time_in
                            # Reduce count of number of patients (waiting)
                            # if(self.id not in Global_vars.patients_db.keys()):
                            Global_vars.patients_waiting_by_priority[self.priority - 1] -= 1
                            Global_vars.patients_waiting -= 1
                            print('patient:' + str(self.id + 1) + ' finished waiting for pharmacists, current queue:' + str(Global_vars.patients_waiting) +' and timenow='+ str(self.env.now))
                            Global_vars.patients_waiting_for_pharmacists -= 1
                    elif ('cashier' in t_resource_depend):
                        with self.hospital.get_cashier_request() as cashiers_req:
                            # Increment count of number of patients waiting. 1 is subtracted
                            # from priority to align priority (1-3) with zero indexed list.
                            # if(self.id not in Global_vars.patients_db.keys()):
                            self.hospital.print_stats('pharmacist')
                            Global_vars.admin_time += t_time
                            Global_vars.patients_waiting += 1
                            print('patient:' + str(self.id + 1) + ' waiting for cashier, current queue:' + str(
                                Global_vars.patients_waiting))
                            Global_vars.patients_waiting_for_cashiers += 1
                            Global_vars.patients_waiting_by_priority[self.priority - 1] += 1

                            # Wait for resources to become available
                            yield cashiers_req
                            '''
                            # Hold patient (with nurse) for treatment time required
                            yield self.env.timeout(t_time)
                            # At end of treatment add time spent to temp results
                            admin_results.append(self.env.now - self.admin_time_start)
                            # Record results in global results data if warm-up complete
                            if self.env.now >= Global_vars.warm_up:
                                Global_vars.patient_admin_queuing_results.loc[self.id + 1] = admin_results
                            '''

                            # Resources now available. Record time patient starts to see doc
                            self.admin_time_start = self.env.now
                            #admin_results = [self.priority, self.admin_time]
                            # Record patient queuing time in patient object
                            self.queuing_time = self.env.now - self.time_in
                            # Reduce count of number of patients (waiting)
                            # if(self.id not in Global_vars.patients_db.keys()):
                            Global_vars.patients_waiting_by_priority[self.priority - 1] -= 1
                            Global_vars.patients_waiting -= 1
                            print('patient:' + str(self.id + 1) + ' finished waiting for cashier, current queue:' + str(Global_vars.patients_waiting) +' and timenow='+ str(self.env.now))
                            Global_vars.patients_waiting_for_cashiers -= 1

                    elif ('nurse' in t_resource_depend):
                        with self.hospital.get_nurse_request(self.priority) as nurse_req:
                            # Increment count of number of patients waiting. 1 is subtracted
                            # from priority to align priority (1-3) with zero indexed list.
                            # if(self.id not in Global_vars.patients_db.keys()):
                            self.hospital.print_stats('nurse')
                            Global_vars.admin_time += t_time
                            Global_vars.patients_waiting += 1
                            print('patient:' + str(self.id + 1) + ' waiting for nurse, current queue:'+str(Global_vars.patients_waiting) +' and timenow='+ str(self.env.now))
                            Global_vars.patients_waiting_for_nurses += 1
                            Global_vars.patients_waiting_by_priority[self.priority - 1] += 1

                            # Wait for resources to become available
                            yield nurse_req

                            '''
                            # Hold patient (with nurse) for treatment time required
                            yield self.env.timeout(t_time)
                            # At end of treatment add time spent to temp results
                            admin_results.append(self.env.now - self.admin_time_start)
                            # Record results in global results data if warm-up complete
                            if self.env.now >= Global_vars.warm_up:
                                Global_vars.patient_admin_queuing_results.loc[self.id + 1] = admin_results
                            '''

                            # Resources now available. Record time patient starts to see doc
                            self.admin_time_start = self.env.now
                            #admin_results = [self.priority, self.admin_time]
                            # Record patient queuing time in patient object
                            self.queuing_time = self.env.now - self.time_in
                            # Reduce count of number of patients (waiting)
                            # if(self.id not in Global_vars.patients_db.keys()):
                            Global_vars.patients_waiting_by_priority[self.priority - 1] -= 1
                            Global_vars.patients_waiting -= 1
                            print('patient:' + str(self.id + 1) + ' finished waiting for nurse, current queue:' + str(Global_vars.patients_waiting) +' and timenow='+ str(self.env.now))
                            Global_vars.patients_waiting_for_nurses -= 1

                    # Create a temporary results list with patient priority and queuing
                    # time

                # Hold patient (with nurse) for treatment time required
                yield self.env.timeout(t_time)
                # At end of treatment add time spent to temp results
                #admin_results.append(self.env.now - self.admin_time_start)
                # Record results in global results data if warm-up complete

                #if self.env.now >= Global_vars.warm_up:
                #    Global_vars.patient_admin_queuing_results.loc[self.id + 1] = admin_results

            if (t_type == 'treatment'):
                print('processing treatment time:' + t_desc + ' which takes:' + str(t_time) + ' mins')
                if('ADR' in t_desc):
                    print('Adverse Drug Reaction! #consider implementing change in patient priority.')
                if (t_resource_depend is not None):
                    if ('chair' in t_resource_depend):
                        with self.hospital.get_chair_request(self.priority) as chair_req:
                            # print(Global_vars)
                            print('patient:' + str(self.id+1) + ' waiting for chair')
                            Global_vars.patients_waiting_for_chairs += 1
                            yield chair_req
                            if ('nurse' in t_resource_depend):
                                with self.hospital.get_nurse_request(self.priority) as nurse_req:
                                    # Increment count of number of patients waiting. 1 is subtracted
                                    # from priority to align priority (1-3) with zero indexed list.
                                    # if(self.id not in Global_vars.patients_db.keys()):
                                    Global_vars.treatment_time += t_time
                                    Global_vars.patients_waiting += 1
                                    print('patient:' + str(self.id + 1) + ' waiting for nurse and chair, current queue:' + str(Global_vars.patients_waiting) +' and timenow='+ str(self.env.now))
                                    Global_vars.patients_waiting_for_nurses += 1
                                    Global_vars.patients_waiting_by_priority[self.priority - 1] += 1

                                    # Wait for resources to become available
                                    yield nurse_req

                                    '''
                                    # Hold patient (with nurse) for treatment time required
                                    yield self.env.timeout(t_time)
                                    # At end of treatment add time spent to temp results
                                    _results.append(self.env.now - self.treatment_time_start)
                                    # Record results in global results data if warm-up complete
                                    if self.env.now >= Global_vars.warm_up:
                                        Global_vars.patient_queuing_results.loc[self.id+1] = _results
                                    '''

                                    # Resources now available. Record time patient starts to see doc
                                    self.treatment_time_start = self.env.now
                                    # Record patient queuing time in patient object
                                    self.queuing_time = self.env.now - self.time_in
                                    _results = [self.priority, self.queuing_time]
                                    # Reduce count of number of patients (waiting)
                                    # if(self.id not in Global_vars.patients_db.keys()):
                                    Global_vars.patients_waiting_by_priority[self.priority - 1] -= 1
                                    Global_vars.patients_waiting -= 1
                                    print('patient:' + str(self.id + 1) + ' finished waiting for nurse, current queue:' + str(Global_vars.patients_waiting)+' and timenow='+ str(self.env.now))
                                    Global_vars.patients_waiting_for_nurses -= 1
                            Global_vars.patients_waiting_for_chairs -= 1


                    elif ('dmo' in t_resource_depend):
                        with self.hospital.get_doc_request(self.priority) as doc_req:
                            if (len(t_resource_depend) == 1):
                                # Increment count of number of patients waiting. 1 is subtracted
                                # from priority to align priority (1-3) with zero indexed list.
                                # if(self.id not in Global_vars.patients_db.keys()):
                                Global_vars.treatment_time += t_time
                                Global_vars.patients_waiting += 1
                                print('patient:' + str(self.id + 1) + ' waiting for DMO, current queue:' + str(
                                    Global_vars.patients_waiting))
                                Global_vars.patients_waiting_for_docs += 1
                                Global_vars.patients_waiting_by_priority[self.priority - 1] += 1
                                #print('inputs: desc=' + t_desc + ' time_Input:' + str(t_time) + ' counter:' + str(
                                #    Global_vars.patients_waiting) + ' total treatment time:' + str(
                                #    Global_vars.treatment_time))

                                # Wait for resources to become available
                                yield doc_req


                                '''
                                # Hold patient (with nurse) for treatment time required
                                yield self.env.timeout(t_time)
                                # At end of treatment add time spent to temp results
                                _results.append(self.env.now - self.treatment_time_start)
                                # Record results in global results data if warm-up complete
                                if self.env.now >= Global_vars.warm_up:
                                    Global_vars.patient_queuing_results.loc[self.id+1] = _results
                                '''

                                # Resources now available. Record time patient starts to see doc
                                self.treatment_time_start = self.env.now
                                # Record patient queuing time in patient object
                                self.queuing_time = self.env.now - self.time_in
                                _results = [self.priority, self.queuing_time]
                                # Reduce count of number of patients (waiting)
                                # if(self.id not in Global_vars.patients_db.keys()):
                                Global_vars.patients_waiting_by_priority[self.priority - 1] -= 1
                                Global_vars.patients_waiting -= 1
                                Global_vars.patients_waiting_for_docs -= 1
                            elif ('nurse' in t_resource_depend):
                                with self.hospital.get_nurse_request(self.priority) as nurse_req:
                                    # Increment count of number of patients waiting. 1 is subtracted
                                    # from priority to align priority (1-3) with zero indexed list.
                                    # if(self.id not in Global_vars.patients_db.keys()):
                                    Global_vars.treatment_time += t_time
                                    Global_vars.patients_waiting += 1
                                    print('patient:' + str(self.id + 1) + ' waiting for nurse, current queue:' + str(Global_vars.patients_waiting) +' and timenow='+ str(self.env.now))
                                    Global_vars.patients_waiting_for_docs += 1
                                    Global_vars.patients_waiting_for_nurses += 1
                                    Global_vars.patients_waiting_by_priority[self.priority - 1] += 1
                                    #print('inputs: desc=' + t_desc + ' time_Input:' + str(t_time) + ' counter:' + str(
                                    #    Global_vars.patients_waiting) + ' total treatment time:' + str(
                                    #    Global_vars.treatment_time))

                                    # Wait for resources to become available
                                    yield nurse_req

                                    '''
                                    # Hold patient (with nurse) for treatment time required
                                    yield self.env.timeout(t_time)
                                    # At end of treatment add time spent to temp results
                                    _results.append(self.env.now - self.treatment_time_start)
                                    # Record results in global results data if warm-up complete
                                    if self.env.now >= Global_vars.warm_up:
                                        Global_vars.patient_queuing_results.loc[self.id+1] = _results
                                    '''

                                    # Resources now available. Record time patient starts to see doc
                                    self.treatment_time_start = self.env.now
                                    # Record patient queuing time in patient object
                                    self.queuing_time = self.env.now - self.time_in
                                    _results = [self.priority, self.queuing_time]
                                    # Reduce count of number of patients (waiting)
                                    # if(self.id not in Global_vars.patients_db.keys()):
                                    Global_vars.patients_waiting_by_priority[self.priority - 1] -= 1
                                    Global_vars.patients_waiting -= 1
                                    print('patient:' + str(self.id + 1) + ' finished waiting for nurse, current queue:' + str(Global_vars.patients_waiting))
                                    Global_vars.patients_waiting_for_nurses -= 1
                                    Global_vars.patients_waiting_for_docs -= 1

                    elif ('nurse' in t_resource_depend):
                        with self.hospital.get_nurse_request(self.priority) as nurse_req:
                            # Increment count of number of patients waiting. 1 is subtracted
                            # from priority to align priority (1-3) with zero indexed list.
                            # if(self.id not in Global_vars.patients_db.keys()):
                            Global_vars.treatment_time += t_time
                            Global_vars.patients_waiting += 1
                            print('patient:' + str(self.id + 1) + ' waiting for nurse, current queue:' + str(
                                Global_vars.patients_waiting))
                            Global_vars.patients_waiting_for_nurses += 1
                            Global_vars.patients_waiting_by_priority[self.priority - 1] += 1

                            # Wait for resources to become available
                            yield nurse_req
                            # Create a temporary results list with patient priority and queuing
                            # time

                            # Resources now available. Record time patient starts to see doc
                            self.treatment_time_start = self.env.now
                            # Record patient queuing time in patient object
                            self.queuing_time = self.env.now - self.time_in
                            _results = [self.priority, self.queuing_time]
                            # Reduce count of number of patients (waiting)
                            # if(self.id not in Global_vars.patients_db.keys()):
                            Global_vars.patients_waiting_by_priority[self.priority - 1] -= 1
                            Global_vars.patients_waiting -= 1
                            print('patient:' + str(self.id + 1) + ' finished waiting for nurse, current queue:' + str(
                                Global_vars.patients_waiting))
                            Global_vars.patients_waiting_for_nurses -= 1
                else:
                    _results = None
                # Hold patient (with nurse) for treatment time required
                yield self.env.timeout(t_time)
                # At end of treatment add time spent to temp results
                if(_results is not None):
                    _results.append(self.env.now - self.treatment_time_start)
                    # Record results in global results data if warm-up complete
                    print(_results)
                    #print(Global_vars.patient_queuing_results.loc[self.id+1])
                    if self.env.now >= Global_vars.warm_up:
                        Global_vars.patient_queuing_results.loc[self.id] = _results

                # Delete patient (removal from patient dictionary removes only
                # reference to patient and Python then automatically cleans up)
                # del Patient.all_patients[self.id+1]
            if (t_type == 'time_between_visits'):
                print('patient:' + str(self.id+1) + ' waiting for in between visits for time='+str(t_time)+' mins')
                yield self.env.timeout(t_time)

        return



class BreastAdjuvant_Patient(CancerPatient):
    """extends from Patient - this specifies a patient with specific condition and treatment regime (for now).
    Methods are:
    __init__: constructor for new patient
    treatment_regime()
    """

    def __init__(self, env, id, hospital, treatment_regime):
        CancerPatient.__init__(self,env,id,hospital,condition=2,treatment_regime=treatment_regime)
        #
        #probability of ADR
        self.breast_dox_cyclophos_adr = next(patient_vars.breast_dox_cyclophos_adr_probability_gen)
        self.breast_adj_blood_test1 = next(patient_vars.breast_adj_blood_test1_probability_gen)
        self.breast_adj_blood_test2 = next(patient_vars.breast_adj_blood_test2_probability_gen)
        self.breast_adj_blood_test_atu_ac = next(patient_vars.breast_adj_blood_test_atu_ac_probability_gen)
        self.breast_adj_blood_test_atu_ac_review = self.breast_adj_blood_test_atu_ac
        self.breast_adj_blood_test_atu_t = next(patient_vars.breast_adj_blood_test_atu_t_probability_gen)
        self.breast_adj_blood_test_atu_t_review = self.breast_adj_blood_test_atu_t
        self.breast_paclitax_adr = next(patient_vars.breast_paclitax_adr_probability_gen)
        #self.Global_vars = Global_vars
        #self.metastatic_regiment = random.randint(1, 3)


    def get_treatment_regime(self):
        regime = [
                    (patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, '1st psa registration time',['nurse'], 'admin'),
                    (patient_vars.generic_waiting_time_mean,patient_vars.generic_waiting_time_sd, 'generic waiting',None,'admin'),
                    (patient_vars.physician_consultation_1_time_mean,patient_vars.physician_consultation_1_time_sd, 'dmo 1st consultation',['dmo'],'admin'),
                    (patient_vars.psa_payment_time_sd,patient_vars.psa_payment_time_sd, 'psa payment',['cashier'],'admin'),
                    (patient_vars.psa_scheduling_time_mean, patient_vars.psa_scheduling_time_sd, 'psa scheduling',['nurse'],'admin'),
                ]
        if (self.breast_adj_blood_test1):
            regime.append((patient_vars.blood_test_time_mean, patient_vars.blood_test_time_sd, '1st blood test',['nurse'],'admin'))

        regime.append((patient_vars.between_visits_time_mean, patient_vars.between_visits_time_sd, 'time between visit',None,'time_between_visits'))

        regime.append((patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, '2nd psa registration',['nurse'],'admin'))
        if (self.breast_adj_blood_test2):
            regime.append((patient_vars.blood_test_time_mean, patient_vars.blood_test_time_sd, '2nd blood test',['nurse'],'admin'))
        regime.append((patient_vars.generic_waiting_time_mean, patient_vars.generic_waiting_time_sd, 'generic waiting time', None,'admin'))
        regime.append((patient_vars.physician_consultation_2_time_mean, patient_vars.physician_consultation_2_time_sd,'dmo 2nd consultation',['dmo'],'admin'))
        regime.append((patient_vars.psa_payment_time_sd, patient_vars.psa_payment_time_sd, 'psa payment',['cashier'],'admin'))
        regime.append((patient_vars.psa_scheduling_time_mean, patient_vars.psa_scheduling_time_sd, 'psa scheduling',['nurse'],'admin'))

        regime.append((patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, '3rd psa registration',['nurse'],'admin'))
        regime.append((patient_vars.IV_start_time_mean, patient_vars.IV_start_time_sd,'IV start - ATU (AC)',['chair','nurse'],'treatment'))
        regime.append((patient_vars.IV_chemo_infusion_time_mean, patient_vars.IV_chemo_infusion_time_sd, 'IV Chemo Infusion - ATU (AC)',['chair','nurse'],'treatment'))
        regime.append((patient_vars.breast_facility_time_mean, patient_vars.breast_facility_time_sd, '', None,'treatment'))

        if (self.breast_adj_blood_test_atu_ac):
            regime.append((patient_vars.blood_test_time_mean, patient_vars.blood_test_atu_time_sd, 'ATU (AC) blood test',['nurse'],'treatment'))
            regime.append((patient_vars.review_test_results_time_mean, patient_vars.review_test_results_time_sd, 'ATU (AC) blood test review',['dmo'],'treatment'))
        regime.append((patient_vars.blood_test_screening_time_mean, patient_vars.blood_test_screening_time_sd, 'ATU (AC) blood test screening',['dmo'],'treatment'))
        regime.append((patient_vars.breast_atu_premed_time_mean, patient_vars.breast_atu_premed_time_sd, 'ATU (AC) premedication',['nurse'],'treatment'))
        regime.append((patient_vars.breast_dox_cyclophos_time_mean, patient_vars.breast_dox_cyclophos_time_sd, 'ATU (AC) Doxorubicin, Cyclophosphamide',['chair','nurse'],'treatment'))
        if(self.breast_dox_cyclophos_adr):
            regime.append((patient_vars.breast_dox_cyclophos_adr_time_mean, patient_vars.breast_dox_cyclophos_adr_time_sd, 'ATU (AC) Doxorubicin, Cyclophosphamide ADR',['chair','nurse'],'treatment'))
        regime.append((patient_vars.post_chemo_pharmacy_time_mean, patient_vars.post_chemo_pharmacy_time_sd, 'ATU (AC) post chemo pharmacy',['pharmacist'],'admin'))

        regime.append((patient_vars.between_visits_time_mean, patient_vars.between_visits_time_sd, 'time between visit',None,'time_between_visits'))

        regime.append((patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, '4th psa registration',['nurse'],'admin'))
        regime.append((patient_vars.IV_start_time_mean,patient_vars.IV_start_time_sd,'IV start - ATU (T)',['chair','nurse'],'treatment'))
        regime.append((patient_vars.IV_chemo_infusion_time_mean, patient_vars.IV_chemo_infusion_time_sd, 'IV Chemo Infusion - ATU (T)',['chair','nurse'],'treatment'))
        regime.append((patient_vars.breast_facility_time_mean, patient_vars.breast_facility_time_sd, '', None,'treatment'))

        if (self.breast_adj_blood_test_atu_t):
            regime.append((patient_vars.blood_test_time_mean, patient_vars.blood_test_atu_time_sd, 'ATU (T) blood test',['nurse'],'treatment'))
            regime.append((patient_vars.review_test_results_time_mean, patient_vars.review_test_results_time_sd, 'ATU (T) blood test review',['nurse'],'treatment'))
        regime.append((patient_vars.blood_test_screening_time_mean, patient_vars.blood_test_screening_time_sd, 'ATU (T) blood test screening',['dmo'],'treatment'))
        regime.append((patient_vars.breast_atu_premed_time_mean, patient_vars.breast_atu_premed_time_sd, 'ATU (T) premedication',['nurse'],'treatment'))
        regime.append((patient_vars.breast_paclitax_time_mean, patient_vars.breast_paclitax_time_sd, 'ATU (T) paclitaxel',['chair','nurse'],'treatment'))
        if(self.breast_paclitax_adr):
            regime.append((patient_vars.breast_paclitax_adr_time_mean, patient_vars.breast_paclitax_adr_time_sd, 'ATU (T) paclitaxel ADR',['chair','nurse'],'treatment'))
        regime.append((patient_vars.post_chemo_pharmacy_time_mean, patient_vars.post_chemo_pharmacy_time_sd, 'ATU (T) post chemo pharmacy',['chair','nurse'],'admin'))
        return regime





class BreastMetatstatic_Patient(CancerPatient):
    """extends from Patient - this specifies a patient with specific condition and treatment regime (for now).
    Methods are:
    __init__: constructor for new patient
    treatment_regime()
    """

    def __init__(self, env, id, hospital, treatment_regime):
        CancerPatient.__init__(self,env,id,hospital,condition=1,treatment_regime=treatment_regime)

    def get_treatment_regime(self):
        regime = [
                    (5, patient_vars.psa_registration_time_sd, '1st psa registration time',['cashier'], 'admin'),
                    (5, patient_vars.psa_scheduling_time_sd, 'psa scheduling',['cashier'],'admin'),
                    (5, patient_vars.psa_scheduling_time_sd, 'psa scheduling2', ['cashier'], 'admin'),
                 ]
        return regime
