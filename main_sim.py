"""

"""
import random
import simpy
import pandas as pd
import Regimes

RANDOM_SEED = random.randint(1,10000)
num_chairs = 2
num_nurses = 2
num_docs = 1
num_cashiers = 1
num_pharmacists = 1


#p_inter = 2
SIM_TIME = 30*24*60
#SIM_NAME = 'breast_meta_docetaxel'
#SIM_NAME = 'breast_meta_paclitaxel'
#SIM_NAME = 'breast_meta_xeloda'
SIM_NAME = ''
class audit_vars:
    warm_up = 15
    # Lists used to store audit results
    audit_time = []

    audit_patients_in_ATU = []
    audit_patients_uncomplete = []
    audit_patients_waiting = []
    audit_patients_waiting_p1 = []
    audit_patients_waiting_p2 = []
    audit_patients_waiting_p3 = []
    audit_patients_between_treatments = []

    audit_patients_between_treatment_cycles = []
    audit_patients_at_cashier = []
    audit_patients_at_pharmacy = []
    audit_patients_at_consultation = []
    audit_patients_at_treatment = []
    audit_patients_at_admin = []
    audit_total_patients_adr = []
    audit_curr_patients_adr = []

    audit_resources_used = []
    audit_nurses_occupied = []
    audit_docs_occupied = []
    audit_chairs_occupied = []
    audit_pharmacists_occupied = []
    audit_cashiers_occupied = []
    audit_all_patients_treated = []

    audit_interval = 30
    audit_cost_unit_time=[]
    #visualization data stores
    #resource utilization graphs

    # Set up counter for number fo patients entering simulation
    patient_count = 0
    chair_usage = []
    patients_waiting = 0
    patients_between_treatments = {}
    patients_between_treatment_cycles = {}
    patients_at_cashier = 0
    patients_at_pharmacy = 0
    patients_at_consultation = 0
    patients_at_treatment = 0
    patients_at_admin = 0
    patients_adr = 0

    cost_unit_time = 0
    cost_unit_time_denom = 0
    cost_units=[]

    patients_waiting_by_priority = [0, 0, 0]
    patient_queuing_results = pd.DataFrame(columns=['priority', 'waiting_time', 'consult_time','treatment_time','cashier_time','pharmacy_time'])
    global hospital
    all_patients = {}
    all_patients_adr = {}
    all_patients_treated = {}
    all_patients_ever = {}
    #all_patients_being_treated = {}
    patient_db={}
    results = pd.DataFrame()


class patient_vars:
    between_visits_time_mean = 1 * 24 * 60
    between_visits_time_sd = 2 * 24 * 60
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

    breast_capecitabine_time_mean = 10
    breast_capecitabine_time_sd = 7/10*breast_capecitabine_time_mean

    post_chemo_pharmacy_time_mean = 5
    post_chemo_pharmacy_time_sd = 7 / 10 * post_chemo_pharmacy_time_mean

    post_chemo_psa_registration_time_mean = 5
    post_chemo_psa_registration_time_sd = 7 / 10 * post_chemo_psa_registration_time_mean

    # Set up probability based generators
    breast_dox_cyclophos_adr_probability = 0.009
    breast_dox_cyclophos_adr_probability_gen = (1 if random.random() <= 0.009 else 0 for _ in range(1000000))
    breast_adj_blood_test1_probability = 0.7
    breast_adj_blood_test1_probability_gen = (1 if random.random() <= 0.7 else 0 for _ in range(1000000))
    breast_adj_blood_test2_probability = 0.7
    breast_adj_blood_test2_probability_gen = (1 if random.random() <= 0.7 else 0 for _ in range(1000000))
    breast_adj_blood_test_atu_ac_probability = 0.3
    breast_adj_blood_test_atu_ac_probability_gen = (1 if random.random() <= 0.3 else 0 for _ in range(1000000))
    breast_adj_blood_test_atu_ac_review_probability = 0.3
    breast_adj_blood_test_atu_ac_review_probability_gen = (1 if random.random() <= 0.3 else 0 for _ in range(100000))
    breast_adj_blood_test_atu_t_probability = 0.3
    breast_adj_blood_test_atu_t_probability_gen = (1 if random.random() <= 0.3 else 0 for _ in range(1000000))
    breast_adj_blood_test_atu_t_review_probability = 0.3
    breast_adj_blood_test_atu_t_review_probability_gen = (1 if random.random() <= 0.3 else 0 for _ in range(100000))
    #breast_paclitax_adr_probability = 0.027
    #breast_paclitax_adr_probability_gen = (1 if random.random() <= 0.027 else 0 for _ in range(1000000))

    breast_adj_blood_test_atu_probability = 0.3
    breast_adj_blood_test_atu_probability_gen = (1 if random.random() <= 0.3 else 0 for _ in range(1000000))
    breast_docetaxel_adr_probability = 0.04
    breast_docetaxel_adr_probability_gen = (1 if random.random() <= 0.04 else 0 for _ in range(1000000))
    breast_paclitaxel_adr_probability = 0.027
    breast_paclitaxel_adr_probability_gen = (1 if random.random() <= 0.027 else 0 for _ in range(1000000))

    dscheduler = {}

    # conditions:
    #conditions_map = {1: 'Breast_Metastatic', 2: 'Breast_Adjuvant', 3: 'GI_Metastatic', 4: 'GI_Adjuvant',5: 'Lung_Metastatic', 6: 'Lung_Adjuvant'}

    # treatment specific variables (costs)
    #Breast_adj_ACP = {'ac_cycles': 4, 't_cycles': 12, 'clinic_costs_1': 310.03, 'fu_clinics': 8,'fu_clinic_cost': 249.19, 'total_atu_cost': 14771.88, 'manpower': 87.9,
    #                       'time': 4988.4272, 'overall_mortality_post': .35, 'overall_mortality_pre': .4,'overall_survivability_post': .863, 'overall_survivability_pre': .842,'os_time_mths': 6}


class Hospital(object):
    def __init__(self, env, num_docs, num_nurses, num_chairs, num_cashiers, num_pharmacists):
        self.env = env
        #self.docs = simpy.PriorityResource(env, num_docs)
        #self.nurses = simpy.PriorityResource(env, num_nurses)
        #self.chairs = simpy.PriorityResource(env, num_chairs)
        self.docs = simpy.PreemptiveResource(env, num_docs)
        self.nurses = simpy.PreemptiveResource(env, num_nurses)
        self.chairs = simpy.PreemptiveResource(env, num_chairs)

        self.cashiers = simpy.Resource(env, num_cashiers)
        self.pharmacists = simpy.Resource(env, num_pharmacists)
        self.regime_details = \
            {
             '1st psa registration time':(patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin', [0.56]),
             'generic waiting time':(patient_vars.generic_waiting_time_mean, patient_vars.generic_waiting_time_sd, None, 'admin', []),
             'consultation':(patient_vars.physician_consultation_1_time_mean, patient_vars.physician_consultation_1_time_sd,['dmo'], 'admin', [149.8/29]),
             'psa payment':(patient_vars.psa_payment_time_sd, patient_vars.psa_payment_time_sd, ['cashier'], 'admin',[0.56]),
             'psa scheduling':(patient_vars.psa_scheduling_time_mean, patient_vars.psa_scheduling_time_sd,['nurse'],'admin',[0.56]),
             '1st blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_time_sd,['nurse'], 'pretreatment',[208.9/30]),
             'time between visit':(patient_vars.between_visits_time_mean, patient_vars.between_visits_time_sd, None, 'time_between_visits',[]),
             '2nd psa registration':(patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin',[0.56]),
             '2nd blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_time_sd, ['nurse'], 'pretreatment',[181.6/30]),
             'dmo 1st consultation': (patient_vars.physician_consultation_1_time_mean, patient_vars.physician_consultation_1_time_sd, ['dmo'],'admin',[149.8/29]),
             'dmo 2nd consultation':(patient_vars.physician_consultation_2_time_mean, patient_vars.physician_consultation_2_time_sd, ['dmo'], 'admin',[float(108.07/11.5)]),
             '3rd psa registration': (patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin',[0.56]),
             'IV start - ATU (AC)':(patient_vars.IV_start_time_mean, patient_vars.IV_start_time_sd, ['chair', 'nurse'], 'treatment',[22.25]),
             'IV Chemo Infusion - ATU (AC)':(patient_vars.IV_chemo_infusion_time_mean, patient_vars.IV_chemo_infusion_time_sd,['chair', 'nurse'], 'treatment',[30.88]),
             'breast facility':(patient_vars.breast_facility_time_mean, patient_vars.breast_facility_time_sd, None, 'posttreatment',[179.92]),
             'ATU (AC) blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_atu_time_sd, ['nurse'], 'pretreatment',[181.6/15]),
             'ATU (AC) blood test review':(patient_vars.review_test_results_time_mean, patient_vars.review_test_results_time_sd, ['dmo'], 'pretreatment',[]),
             'ATU (AC) blood test screening':(patient_vars.blood_test_screening_time_mean, patient_vars.blood_test_screening_time_sd, ['dmo'], 'pretreatment',[1.18]),
             'ATU (AC) premedication':(patient_vars.breast_atu_premed_time_mean, patient_vars.breast_atu_premed_time_sd,['nurse'], 'pretreatment',[]),
             'ATU (AC) Doxorubicin, Cyclophosphamide':(patient_vars.breast_dox_cyclophos_time_mean, patient_vars.breast_dox_cyclophos_time_sd, ['chair', 'nurse'], 'treatment',[376.93/90]),
             'ATU (AC) Doxorubicin, Cyclophosphamide ADR':(patient_vars.breast_dox_cyclophos_adr_time_mean, patient_vars.breast_dox_cyclophos_adr_time_sd,['adr'], 'treatment', [87.22/60]),
             'ATU (AC) post chemo pharmacy':(patient_vars.post_chemo_pharmacy_time_mean, patient_vars.post_chemo_pharmacy_time_sd,['pharmacist'], 'pharmacy',[]),
             '4th psa registration':(patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin',[0.56]),
             'IV start - ATU (T)':(patient_vars.IV_start_time_mean, patient_vars.IV_start_time_sd, ['chair', 'nurse'], 'treatment',[22.25]),
             'IV Chemo Infusion - ATU (T)':(patient_vars.IV_chemo_infusion_time_mean, patient_vars.IV_chemo_infusion_time_sd,['chair', 'nurse'], 'treatment',[30.88]),
             'ATU (T) blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_atu_time_sd, ['nurse'], 'pretreatment',[181.6/15]),
             'ATU (T) blood test review': (patient_vars.review_test_results_time_mean, patient_vars.review_test_results_time_sd, ['dmo'],'pretreatment',[]),
             'ATU (T) blood test screening': (patient_vars.blood_test_screening_time_mean, patient_vars.blood_test_screening_time_sd, ['dmo'],'pretreatment',[1.18]),
             'ATU (T) premedication':(patient_vars.breast_atu_premed_time_mean, patient_vars.breast_atu_premed_time_sd,['nurse'], 'pretreatment',[]),
             'ATU (T) paclitaxel':(patient_vars.breast_paclitax_time_mean, patient_vars.breast_paclitax_time_sd,['chair', 'nurse'], 'treatment',[654/180]),
             'ATU (T) paclitaxel ADR':(patient_vars.breast_paclitax_adr_time_mean, patient_vars.breast_paclitax_adr_time_sd, ['adr'], 'treatment',[79.59/67.8]),
             'ATU (T) post chemo pharmacy': (patient_vars.post_chemo_pharmacy_time_mean, patient_vars.post_chemo_pharmacy_time_sd, ['pharmacist'],'pharmacy',[]),

             'IV Chemo Infusion - ATU': (patient_vars.IV_chemo_infusion_time_mean, patient_vars.IV_chemo_infusion_time_sd, ['chair', 'nurse'], 'treatment', [30.88]),
             'IV start - ATU': (patient_vars.IV_start_time_mean,patient_vars.IV_start_time_sd, ['chair', 'nurse'], 'treatment', [22.25]),
             'ATU blood test': ( patient_vars.blood_test_time_mean, patient_vars.blood_test_atu_time_sd, ['nurse'], 'pretreatment',[181.6/15]),
             'ATU blood test review': (patient_vars.review_test_results_time_mean, patient_vars.review_test_results_time_sd, ['dmo'],'pretreatment',[]),
             'ATU blood test screening': (patient_vars.blood_test_screening_time_mean, patient_vars.blood_test_screening_time_sd, ['dmo'], 'pretreatment',[1.18]),
             'ATU premedication': (patient_vars.breast_atu_premed_time_mean, patient_vars.breast_atu_premed_time_sd, ['nurse'],'pretreatment',[]),
             'ATU Docetaxel': (patient_vars.breast_dox_cyclophos_time_mean, patient_vars.breast_dox_cyclophos_time_sd,['chair', 'nurse'], 'treatment',[851.68/120]),
             'ATU Docetaxel ADR': (patient_vars.breast_dox_cyclophos_adr_time_mean, patient_vars.breast_dox_cyclophos_adr_time_sd,['chair', 'nurse'], 'treatment',[107.64/70]),
             'ATU post chemo pharmacy': (patient_vars.post_chemo_pharmacy_time_mean, patient_vars.post_chemo_pharmacy_time_sd, ['pharmacist'],'pharmacy',[]),
             'ATU Paclitaxel': (patient_vars.breast_paclitax_time_mean, patient_vars.breast_paclitax_time_sd,['chair', 'nurse'], 'treatment', [654 / 180]),
             'ATU Paclitaxel ADR': (patient_vars.breast_paclitax_adr_time_mean, patient_vars.breast_paclitax_adr_time_sd,['chair', 'nurse'], 'treatment', [79.59 / 67.8]),
             'ATU capecitabine': (patient_vars.breast_capecitabine_time_mean, patient_vars.breast_capecitabine_time_sd,['nurse'], 'treatment', [142.24 / 10]),
            }

    def adr_yield(self, p_id, mins=0):
        yield self.env.timeout(mins)

    def ovr_nite(self, p_id, hours=0):
        yield self.env.timeout(hours * 60)

    def undergo_treatment(self, treatment_desc, p_id):
        print('hospital class: undergoing treatment / process call:'+ str(treatment_desc))
        if ('generic waiting' in treatment_desc):
            #audit_vars.patients_between_treatments += 1
            audit_vars.patients_between_treatments[p_id] = 1
            print('Patient %s is waiting for the next step at %.2f.' % (p_id, env.now))
        if ('time between visit' in treatment_desc):
            audit_vars.patients_between_treatment_cycles[p_id] = 1
            print('Patient %s is waiting for next visit at %.2f.' % (p_id, env.now))
            print()

        yield self.env.timeout(self.regime_details[treatment_desc][0])


        if ('generic waiting' in treatment_desc):
            #audit_vars.patients_between_treatments -= 1
            del audit_vars.patients_between_treatments[p_id]
            print('Patient %s has finished generic wait at %.2f.' % (p_id, env.now))
        if ('time between visit' in treatment_desc):
            del audit_vars.patients_between_treatment_cycles[p_id]
            print('Patient %s has finished wait and will commence next visit at %.2f.' % (p_id, env.now))


#not sure if we can make this a class
def Patient(env, id, hosp, ptype=None):
    print('Patient %s %s arrives at the hospital at %.2f.' % (id, ptype, env.now))
    p_types={1:'Adjuvant',2:'Metastatic: Docetaxel',3:'Metastatic: Paclitaxel',4:'Metastatic: Xeloda'}

    # SIM_NAME = 'breast_meta_docetaxel'
    # SIM_NAME = 'breast_meta_paclitaxel'
    # SIM_NAME = 'breast_meta_xeloda'

    if(SIM_NAME=='breast_meta_docetaxel'):
        p_type=2
    elif(SIM_NAME=='breast_meta_paclitaxel'):
        p_type=3
    elif(SIM_NAME=='breast_meta_xeloda'):
        p_type=4
    else:
        if(ptype is None):
            p_type = random.randint(1, 4)
        else:
            p_type = ptype

    #regimes = ['1st psa registration time','generic waiting','consultation','psa payment','psa scheduling','1st blood test','IV start - ATU (AC)']
    if(p_type==1):
        regimes = Regimes.Breast_Adjuvant_Regimes(
        patient_vars.breast_adj_blood_test1_probability_gen,
        patient_vars.breast_adj_blood_test2_probability_gen,
        patient_vars.breast_adj_blood_test_atu_ac_probability_gen,
        patient_vars.breast_dox_cyclophos_adr_probability_gen,
        patient_vars.breast_adj_blood_test_atu_t_probability_gen,
        patient_vars.breast_paclitaxel_adr_probability_gen
        )
    if(p_type==2):
        regimes=Regimes.Breast_Metastatic_Regimes('docetaxel',
                                          patient_vars.breast_adj_blood_test1_probability_gen,
                                          patient_vars.breast_adj_blood_test2_probability_gen,
                                          patient_vars.breast_adj_blood_test_atu_probability_gen,
                                          patient_vars.breast_docetaxel_adr_probability_gen
                                  )

    if(p_type==3):
        regimes=Regimes.Breast_Metastatic_Regimes('paclitaxel',
                                          patient_vars.breast_adj_blood_test1_probability_gen,
                                          patient_vars.breast_adj_blood_test2_probability_gen,
                                          patient_vars.breast_adj_blood_test_atu_probability_gen,
                                          patient_vars.breast_paclitaxel_adr_probability_gen
                                  )

    if(p_type==4):
        regimes=Regimes.Breast_Metastatic_Regimes('capecitabine',
                                          patient_vars.breast_adj_blood_test1_probability_gen,
                                          patient_vars.breast_adj_blood_test2_probability_gen,
                                          None,
                                          None
                                  )


    p_priority = random.randint(1, 3)
    audit_vars.patient_count += 1
    audit_vars.all_patients[id] = (regimes,p_priority)
    audit_vars.all_patients_ever[id] = (regimes, p_priority)
    #audit_vars.all_patients_being_treated = audit_vars.all_patients_being_treated + 1

    p_time_in = env.now


    p_queuing_time=0; p_time_see_doc=0; p_time_see_nurse=0; p_time_cashier=0; p_time_pharmacist=0
    item_count = 0
    for item in regimes:
        dependency = hosp.regime_details[item][2]
        time_of_day = (env.now % (24*60)) / 60
        print('time of day = '+str(time_of_day) +' env_now='+str(env.now))
        if(time_of_day>=17 and time_of_day<=23 and (dependency is None or 'ADR' not in item and 'adr' not in dependency)):
            yield env.process(hosp.ovr_nite(id, (23-time_of_day+8+random.randint(0,8))))
        if(time_of_day>=0 and time_of_day<=8 and (dependency is None or 'ADR' not in item and 'adr' not in dependency)):
            yield env.process(hosp.ovr_nite(id, (8-time_of_day+random.randint(0,8))))

        cost_min = hosp.regime_details[item][4]
        print('Patient Priority:' + str(p_priority) + ' Treatment Regiment:' + str(p_types[p_type])+' '+str(hosp.regime_details[item][0])+ ' dependency:'+str(dependency)+' ')
        cost_min = cost_min[0] if len(cost_min)>0 else 0
        #audit_vars.cost_unit_time+=cost_min
        #audit_vars.cost_unit_time_denom += 1
        #print(dependency)
        if (dependency is None):
            audit_vars.cost_units.append(cost_min)
            yield env.process(hosp.undergo_treatment(item, id))
            audit_vars.cost_units.remove(cost_min)
        else:
            #if ADR, need to prioritise for 2 ATU nurses, 1 DMO and 1 Pharmacist
            if('ADR' in item or 'adr' in dependency):
                audit_vars.patients_waiting += 1
                audit_vars.patients_waiting_by_priority[1 - 1] += 1
                audit_vars.patients_adr += 1
                audit_vars.all_patients_adr[id] = 1

                n1_adr_req = hosp.nurses.request(preempt=True)
                n2_adr_req = hosp.nurses.request(preempt=True)
                ch_adr_req = hosp.chairs.request(preempt=True)
                adr_dmo_req = hosp.docs.request(preempt=True)
                adr_pharm_req = hosp.pharmacists.request()

                '''
                print('ADR!!!!!')
                with hosp.chairs.request(priority=1) as adr_chr_req:
                    yield adr_chr_req
                    with hosp.docs.request(priority=1) as adr_doc_req:
                        yield adr_doc_req
                        with hosp.nurses.request(priority=1) as adr_nur_req:
                            yield adr_nur_req
                            with hosp.pharmacists.request() as adr_phm_req:
                                yield adr_phm_req
                                adr_treatment = env.now
                                p_queuing_time = env.now - p_time_in
                                print('Patient %s gets attended due to ADR: dmo, 2 nurses, pharmacist at %.2f.: %s.' % (id, env.now, item))
                                audit_vars.patients_at_treatment += 1

                                audit_vars.patients_waiting -= 1
                                audit_vars.patients_waiting_by_priority[1 - 1] -= 1
                                audit_vars.cost_units.append(cost_min)

                                yield env.process(hosp.undergo_treatment(item, id))

                                audit_vars.patients_at_treatment -= 1
                                audit_vars.patients_adr -= 1

                                hosp.chairs.release(adr_chr_req)
                                hosp.nurses.release(adr_nur_req)
                                hosp.docs.release(adr_doc_req)
                                hosp.pharmacists.release(adr_phm_req)
                                print('Patient %s ends ADR treatment: dmo, 2 nurses, pharmacist at %.2f.: %s.' % (id, env.now, item))
                                print('nurses:'+str(audit_vars.hospital.nurses.count))
                                print('chairs:'+str(audit_vars.hospital.chairs.count))
                                print('docs:'+str(audit_vars.hospital.docs.count))
                                exit()
                                audit_vars.cost_units.remove(cost_min)

                '''
                print('ADR!!!!!')
                print('nurses:'+str(audit_vars.hospital.nurses.count))
                print('chairs:'+str(audit_vars.hospital.chairs.count))
                print('docs:'+str(audit_vars.hospital.docs.count))
                yield n1_adr_req & n2_adr_req & adr_dmo_req & adr_pharm_req & ch_adr_req

                adr_treatment = env.now
                p_queuing_time = env.now - p_time_in
                print('Patient %s gets attended due to ADR: dmo, 2 nurses, pharmacist at %.2f.: %s.' % (id, env.now, item))
                audit_vars.patients_at_treatment += 1

                audit_vars.patients_waiting -= 1
                audit_vars.patients_waiting_by_priority[1 - 1] -= 1
                audit_vars.cost_units.append(cost_min)

                yield env.process(hosp.undergo_treatment(item, id))

                audit_vars.patients_at_treatment -= 1
                audit_vars.patients_adr -= 1
                hosp.nurses.release(n1_adr_req)
                hosp.nurses.release(n2_adr_req)
                hosp.docs.release(adr_dmo_req)
                hosp.pharmacists.release(adr_pharm_req)
                hosp.chairs.release(ch_adr_req)
                print('Patient %s ends ADR treatment: dmo, 2 nurses, pharmacist at %.2f.: %s.' % (id, env.now, item))
                print('nurses:'+str(audit_vars.hospital.nurses.count))
                print('chairs:'+str(audit_vars.hospital.chairs.count))
                print('docs:'+str(audit_vars.hospital.docs.count))
                #exit()
                audit_vars.cost_units.remove(cost_min)


            elif ('chair' in dependency):
                print('chair dependency!')
                with hosp.chairs.request(priority=p_priority, preempt=False) as chr_request:
                    audit_vars.patients_waiting += 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] += 1
                    yield chr_request
                    print('Patient %s gets chair at %.2f.: %s. Waiting for nurse for treatment.' % (id, env.now, item))
                    #print(audit_vars.all_patients[id])
                    #exit()
                    if ('nurse' in dependency):
                        with hosp.nurses.request(priority=p_priority, preempt=False) as nurchair_request:
                            yield nurchair_request
                            p_time_chair_treatment = env.now
                            p_queuing_time = env.now - p_time_in
                            audit_vars.patients_waiting -= 1
                            audit_vars.patients_waiting_by_priority[p_priority - 1] -= 1

                            print('Patient %s gets attended by nurse at %.2f.: %s.' % (id, env.now, item))
                            audit_vars.patients_at_treatment += 1
                            audit_vars.cost_units.append(cost_min)
                            try:
                                yield env.process(hosp.undergo_treatment(item, id))
                            except simpy.Interrupt:
                                yield env.process(hosp.adr_yield(id, 20))

                            audit_vars.patients_at_treatment -= 1
                            print('Patient %s stops treatment in chair at %.2f.' % (id, env.now))
                            audit_vars.cost_units.remove(cost_min)
                        hosp.chairs.release(chr_request)
                        hosp.nurses.release(nurchair_request)
                    hosp.chairs.release(chr_request)
                    #else:
                    #    audit_vars.patients_waiting -= 1
                    #    audit_vars.patients_waiting_by_priority[p_priority - 1] -= 1

            elif('dmo' in dependency):
                print('dmo dependency!')
                with hosp.docs.request(priority=p_priority, preempt=False) as doc_request:
                    audit_vars.patients_waiting += 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] += 1
                    yield doc_request
                    if ('nurse' in dependency):
                        with hosp.nurses.request(priority=p_priority, preempt=False) as nurdmo_request:
                            yield nurdmo_request
                            p_time_see_doc = env.now
                            p_queuing_time = env.now - p_time_in
                            audit_vars.patients_waiting -= 1
                            audit_vars.patients_waiting_by_priority[p_priority - 1] -= 1

                            print('Patient %s gets attended by nurse & dmo at %.2f.: %s.' % (id, env.now, item))
                            audit_vars.patients_at_consultation += 1
                            audit_vars.cost_units.append(cost_min)
                            print('before treatment nurse count:'+str(hosp.nurses.count))
                            try:
                                yield env.process(hosp.undergo_treatment(item, id))
                            except simpy.Interrupt:
                                yield env.process(hosp.adr_yield(id, 20))

                            audit_vars.patients_at_consultation -= 1
                            print('Patient %s stops treatment with nurse and dmo %.2f.' % (id, env.now))
                            print('after treatment nurse count:' + str(hosp.nurses.count))
                            audit_vars.cost_units.remove(cost_min)
                            hosp.nurses.release(nurdmo_request)
                    else:
                        p_time_see_doc = env.now
                        p_queuing_time = env.now - p_time_in
                        audit_vars.patients_waiting -= 1
                        audit_vars.patients_waiting_by_priority[p_priority - 1] -= 1
                        print('Patient %s gets attended by dmo at %.2f.: %s. ' % (id, env.now, item))
                        audit_vars.patients_at_consultation += 1
                        audit_vars.cost_units.append(cost_min)
                        try:
                            yield env.process(hosp.undergo_treatment(item, id))
                        except simpy.Interrupt:
                            yield env.process(hosp.adr_yield(id, 20))

                        audit_vars.patients_at_consultation -= 1
                        print('Patient %s stops treatment with dmo %.2f.' % (id, env.now))
                        audit_vars.cost_units.remove(cost_min)
                    hosp.docs.release(doc_request)

            elif('nurse' in dependency):
                print('nurse dependency!')
                with hosp.nurses.request(priority=p_priority, preempt=False) as nur_request:
                    audit_vars.patients_waiting += 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] += 1

                    yield nur_request
                    p_time_see_nurse = env.now
                    p_queuing_time = env.now - p_time_in
                    audit_vars.patients_waiting -= 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] -= 1
                    audit_vars.cost_units.append(cost_min)
                    print('Patient %s gets attended by nurse at %.2f.: %s.' % (id, env.now, item))
                    if (hosp.regime_details[item][3] == 'admin'):
                        audit_vars.patients_at_admin += 1
                    else:
                        audit_vars.patients_at_treatment += 1
                    try:
                        yield env.process(hosp.undergo_treatment(item, id))
                    except simpy.Interrupt:
                        yield env.process(hosp.adr_yield(id, 20))

                    if(hosp.regime_details[item][3] == 'admin'):
                        audit_vars.patients_at_admin -= 1
                    else:
                        audit_vars.patients_at_treatment -= 1
                    print('Patient %s stops %s %.2f.' % (id, 'admin process' if hosp.regime_details[item][3]=='admin' else 'treatment', env.now))
                    audit_vars.cost_units.remove(cost_min)
                    hosp.nurses.release(nur_request)
            elif('cashier' in dependency):
                with hosp.cashiers.request() as cas_request:
                    audit_vars.patients_waiting += 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] += 1

                    yield cas_request
                    p_time_cashier = env.now
                    p_queuing_time = env.now - p_time_in

                    audit_vars.patients_waiting -= 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] -= 1
                    audit_vars.cost_units.append(cost_min)
                    print('Patient %s gets attended by cashier at %.2f.: %s.' % (id, env.now, item))
                    audit_vars.patients_at_cashier += 1
                    yield env.process(hosp.undergo_treatment(item, id))
                    audit_vars.patients_at_cashier -= 1
                    print('Patient %s leaves cashiers station at %.2f.' % (id, env.now))
                    audit_vars.cost_units.remove(cost_min)
                    hosp.cashiers.release(cas_request)
            elif('pharmacist' in dependency):
                with hosp.pharmacists.request() as phm_request:
                    audit_vars.patients_waiting += 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] += 1

                    yield phm_request
                    p_time_pharmacist = env.now
                    p_queuing_time = env.now - p_time_in

                    audit_vars.patients_waiting -= 1
                    audit_vars.patients_waiting_by_priority[p_priority - 1] -= 1
                    audit_vars.cost_units.append(cost_min)
                    print('Patient %s gets attended by pharmacist at %.2f.: %s.' % (id, env.now, item))
                    audit_vars.patients_at_pharmacy += 1
                    yield env.process(hosp.undergo_treatment(item, id))
                    audit_vars.patients_at_pharmacy -= 1
                    print('Patient %s leaves pharmacy at %.2f.' % (id, env.now))
                    audit_vars.cost_units.remove(cost_min)
                    hosp.pharmacists.release(phm_request)
            #['priority', 'waiting_time', 'consult_time', 'treatment_time', 'cashier_time', 'pharmacy_time']
            _results = [p_priority, p_queuing_time,p_time_see_doc,p_time_see_nurse,p_time_cashier,p_time_pharmacist]
            if env.now >= audit_vars.warm_up:
                audit_vars.patient_queuing_results.loc[id] = _results
        item_count+=1
        #audit_vars.cost_unit_time -= cost_min
        #audit_vars.cost_unit_time_denom -= 1
    print('removing patient '+str(id))
    print(audit_vars.all_patients)
    del audit_vars.all_patients[id]
    try:
        del audit_vars.patients_between_treatment_cycles[id]
        del audit_vars.patients_between_treatments[id]
    except:
        pass
    #del audit_vars.patients_waiting


    audit_vars.all_patients_treated[id] = (regimes,p_priority)
    #audit_vars.all_patients_being_treated = audit_vars.all_patients_being_treated - 1
    print('patient ' + str(id) + ' removed')



def setup(env, num_docs, num_nurses, num_chairs, num_cashiers, num_pharmacists, sim_mode):
    # Create the hospital
    audit_vars.hospital = Hospital(env, num_docs, num_nurses, num_chairs, num_cashiers, num_pharmacists)
    t_inter = audit_vars.audit_interval
    i = 0
    # Create initial

    #for i in range(2):
    #    env.process(Patient(env, i, audit_vars.hospital))
    # Create more cars while the simulation is running



    if(sim_mode != 'schedule'):
        while True:
            yield env.timeout(random.randint(t_inter, t_inter + 60*1))
            i += 1
            env.process(Patient(env, i, audit_vars.hospital, None))

    else:
        schedule = [
                    (60 * 26, 1),(60 * 1, 1),(60 * 1, 1),(60 * 1, 1),(60 * .5, 1),(60 * .5, 2),(60 * 1, 2),(60 * 1, 1),(60 * 1, 3),(60 * 1, 4),(60 * 1, 1),
                    (60 * 1, 2),(60 * 1, 1),(60 * 1, 1),(60 * 1, 3),(60 * 1, 1),(60 * 1, 2),(60 * 1, 4),(60 * 1, 1),(60 * 1, 2),(60 * 1, 1),
                    (60 * 15, 4), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 2),(60 * 1, 1), (60 * 1, 4),
                    (60 * 15, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 2), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),(60 * 1, 3), (60 * 1, 1),
                    ]
        '''
            (60 * .5, 1),(60 * .5, 2),(60 * 1, 2),(60 * 1, 1),(60 * 1, 3),(60 * 1, 4),(60 * 1, 1),(60 * 1, 1),(60 * 1, 1),(60 * 1, 1),
                    (60 * 15, 2),(60 * 1, 1),(60 * 1, 1),(60 * 1, 3),(60 * 1, 1),(60 * 1, 2),(60 * 1, 4),(60 * 1, 1),(60 * 1, 2),(60 * 1, 1),
                    (60 * 15, 3), (60 * 1, 1), (60 * 1, 4), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 4),(60 * 1, 1), (60 * 1, 1), (60 * 1, 1),
                    (60 * 15, 4), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1),(60 * 1, 2), (60 * 1, 1), (60 * 1, 4),
                    (60 * 15, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 2), (60 * 1, 1), (60 * 1, 1),(60 * 1, 1), (60 * 1, 3), (60 * 1, 1),

            (60 * 15, 1), (60 * .5, 1), (60 * .5, 2), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),
            (60 * 15, 2), (60 * 1, 1), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 2), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 2), (60 * 1, 1),
            (60 * 15, 3), (60 * 1, 1), (60 * 1, 4), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 1), (60 * 1, 1),
            (60 * 15, 4), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 2),
            (60 * 1, 1), (60 * 1, 4),
            (60 * 15, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 2), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),
            (60 * 1, 3), (60 * 1, 1),
            (60 * 15, 1), (60 * .5, 1), (60 * .5, 2), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),
            (60 * 15, 2), (60 * 1, 1), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 2), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 2), (60 * 1, 1),
            (60 * 15, 3), (60 * 1, 1), (60 * 1, 4), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 1), (60 * 1, 1),
            (60 * 15, 4), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 2),
            (60 * 1, 1), (60 * 1, 4),
            (60 * 15, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 2), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),
            (60 * 1, 3), (60 * 1, 1),
            (60 * 15, 1), (60 * .5, 1), (60 * .5, 2), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),
            (60 * 15, 2), (60 * 1, 1), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 2), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 2), (60 * 1, 1),
            (60 * 15, 3), (60 * 1, 1), (60 * 1, 4), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 4), (60 * 1, 1),
            (60 * 1, 1), (60 * 1, 1),
            (60 * 15, 4), (60 * 1, 2), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 3), (60 * 1, 1), (60 * 1, 2),
            (60 * 1, 1), (60 * 1, 4),
            (60 * 15, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 2), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),
            (60 * 1, 3), (60 * 1, 1),

        ]
        '''
                    #(60 * 1, 1), (60 * 1, 1), (60 * 1, 1), (60 * 1, 1),(60 * 1, 1), (60 * 1, 1),(60 * 1, 1), (60 * 1, 1),(60 * 1, 1),
                    #(60 * 1, 1), (60 * 1, 1),(60 * 3, 1), (60 * 2, 1),(60 * 2, 1),(60 * 3, 1), (60 * 2, 1), (60 * 3, 1), (60 * 1, 1),
                    #(60 * 2, 1), (60 * 3, 1), (60 * 1, 1), (60 * 5, 1)]
        for pi in schedule:
            intv, ttype = pi
            yield env.timeout(intv)
            i += 1
            env.process(Patient(env, i, audit_vars.hospital, ttype))

def perform_audit(env):
    """Called at each audit interval. Records simulation time, total
    patients waiting, patients waiting by priority, and number of docs
    occupied. Will then schedule next audit."""

    # Delay before first audit if length of warm-up
    yield env.timeout(audit_vars.warm_up)
    # The trigger repeated audits
    while True:
        # Record time
        audit_vars.audit_time.append(env.now)
        # Record patients waiting by referencing global variables
        audit_vars.audit_patients_waiting.append(audit_vars.patients_waiting)
        audit_vars.audit_patients_waiting_p1.append(audit_vars.patients_waiting_by_priority[0])
        audit_vars.audit_patients_waiting_p2.append(audit_vars.patients_waiting_by_priority[1])
        audit_vars.audit_patients_waiting_p3.append(audit_vars.patients_waiting_by_priority[2])
        # Record patients waiting by asking length of dictionary of all
        # patients (another way of doing things)
        audit_vars.audit_patients_uncomplete.append(len(audit_vars.all_patients))
        audit_vars.audit_all_patients_treated.append(len(audit_vars.all_patients_treated))
        #audit_vars.audit_patients_treated.append(len(audit_vars.all_patients))
        audit_vars.audit_patients_in_ATU.append(len(audit_vars.all_patients)-len(audit_vars.patients_between_treatment_cycles))
        # Record resources occupied
        audit_vars.audit_resources_used.append(audit_vars.hospital.chairs.count+
                                               audit_vars.hospital.nurses.count+
                                               audit_vars.hospital.docs.count+
                                               audit_vars.hospital.cashiers.count+
                                               audit_vars.hospital.pharmacists.count)

        #patients_in_between_treatments=audit_vars.audit_patients_between_treatments
            #len(audit_vars.all_patients) - audit_vars.patients_at_treatment - audit_vars.patients_at_consultation - \
            #                           audit_vars.patients_at_pharmacy - audit_vars.patients_at_cashier - \
            #                           audit_vars.patients_between_treatments - audit_vars.patients_at_admin - audit_vars.patients_waiting

        audit_vars.audit_nurses_occupied.append(audit_vars.hospital.nurses.count)
        audit_vars.audit_chairs_occupied.append(audit_vars.hospital.chairs.count)
        audit_vars.audit_docs_occupied.append(audit_vars.hospital.docs.count)
        audit_vars.audit_pharmacists_occupied.append(audit_vars.hospital.pharmacists.count)
        audit_vars.audit_cashiers_occupied.append(audit_vars.hospital.cashiers.count)

        audit_vars.audit_patients_at_admin.append(audit_vars.patients_at_admin)
        audit_vars.audit_patients_between_treatment_cycles.append(len(audit_vars.patients_between_treatment_cycles))
        audit_vars.audit_patients_between_treatments.append(len(audit_vars.patients_between_treatments))


        audit_vars.audit_patients_at_cashier.append(audit_vars.patients_at_cashier)
        audit_vars.audit_patients_at_pharmacy.append(audit_vars.patients_at_pharmacy)
        audit_vars.audit_patients_at_consultation.append(audit_vars.patients_at_consultation)
        audit_vars.audit_patients_at_treatment.append(audit_vars.patients_at_treatment)

        audit_vars.audit_total_patients_adr.append(len(audit_vars.all_patients_adr))
        audit_vars.audit_curr_patients_adr.append(audit_vars.patients_adr)
        audit_vars.audit_cost_unit_time.append(sum(audit_vars.cost_units)/len(audit_vars.cost_units) if len(audit_vars.cost_units) !=0 else 0)

        '''
        print()
        print('####################################### AUDIT Begin: #######################################')
        print('PATIENTS WAITING:')
        print(audit_vars.patients_waiting)
        print(audit_vars.audit_patients_waiting)
        print('PATIENTS AT ADMIN:')
        print(audit_vars.patients_at_admin)
        print('PATIENTS BETWEEN TREATMENTS CYCLES:')
        print(len(audit_vars.patients_between_treatment_cycles))
        print('PATIENTS BETWEEN TREATMENTS:')
        print(len(audit_vars.patients_between_treatments))

        print('PATIENTS AT CASHIER:')
        print(audit_vars.patients_at_cashier)
        print('PATIENTS AT PHARMACY:')
        print(audit_vars.patients_at_pharmacy)
        print('PATIENTS AT CONSULTATION:')
        print(audit_vars.patients_at_consultation)
        print('PATIENTS AT TREATMENT:')
        print(audit_vars.patients_at_treatment)
        print('PATIENTS IN BETWEEN TREATMENT:')
        print(audit_vars.audit_patients_between_treatments)


        print('PATIENTS DB:')
        print(len(audit_vars.all_patients))
        print('PATIENTS DB Completed treatment:')
        print(len(audit_vars.all_patients_treated))
        print('PATIENTS DB EVER:')
        print(len(audit_vars.all_patients_ever))
        print('PATIENTS ADR EVER:')
        print(len(audit_vars.all_patients_adr))
        print('Resource Utilization:')
        print(audit_vars.audit_resources_used)
        print('nurse utilization:'+str(num_nurses))
        print(audit_vars.hospital.nurses.count/num_nurses)
        print('######################################## AUDIT End: ########################################')
        print()
        '''
        print('PATIENTS ADR EVER:')
        print(len(audit_vars.all_patients_adr))

        # Trigger next audit after interval
        yield env.timeout(audit_vars.audit_interval)

def build_audit_results():
    """At end of model run, transfers results held in lists into a pandas
    DataFrame."""

    audit_vars.results['time'] = audit_vars.audit_time
    audit_vars.results['uncompleted patients'] = audit_vars.audit_patients_uncomplete
        #[a_i - b_i for a_i, b_i in zip(audit_vars.audit_patients_in_ATU, audit_vars.audit_patients_between_treatment_cycles)]
    #audit_vars.results['all patients treated'] = audit_vars.all_patients_treated
    #audit_vars.results['current # of patients'] = audit_vars.all_patients
    #audit_vars.results['current # of patients'] = audit_vars.all_patients
    audit_vars.results['all patients waiting'] = audit_vars.audit_patients_waiting
    audit_vars.results['all patients treated'] = audit_vars.audit_all_patients_treated
    #audit_vars.results['all patients waiting'] = audit_vars.audit_patients_waiting
    audit_vars.results['patients at admin'] = audit_vars.audit_patients_at_admin
    audit_vars.results['patients between treatment cycles'] = audit_vars.audit_patients_between_treatment_cycles
    audit_vars.results['patients at consultation'] = audit_vars.audit_patients_at_consultation
    audit_vars.results['patients at treatment'] = audit_vars.audit_patients_at_treatment
    audit_vars.results['patients at pharmacy'] = audit_vars.audit_patients_at_pharmacy
    audit_vars.results['patients in between treatments'] = audit_vars.audit_patients_between_treatments
    audit_vars.results['patients at cashier'] = audit_vars.audit_patients_at_cashier
    audit_vars.results['patients total ADR'] = audit_vars.audit_total_patients_adr
    audit_vars.results['patients curr ADR'] = audit_vars.audit_curr_patients_adr

    audit_vars.results['priority 1 patients waiting'] = audit_vars.audit_patients_waiting_p1
    audit_vars.results['priority 2 patients waiting'] = audit_vars.audit_patients_waiting_p2
    audit_vars.results['priority 3 patients waiting'] = audit_vars.audit_patients_waiting_p3
    audit_vars.results['resources occupied'] = audit_vars.audit_resources_used
    audit_vars.results['nurses occupied'] = audit_vars.audit_nurses_occupied
    audit_vars.results['docs occupied'] = audit_vars.audit_docs_occupied
    audit_vars.results['chairs occupied'] = audit_vars.audit_chairs_occupied
    audit_vars.results['pharmacists occupied'] = audit_vars.audit_pharmacists_occupied
    audit_vars.results['cashiers occupied'] = audit_vars.audit_cashiers_occupied

    total_resources = num_chairs+num_nurses+num_docs+num_cashiers+num_pharmacists
    audit_vars.results['nurse utilization'] = (audit_vars.results['nurses occupied'].astype(float)/num_nurses).astype(float)
    audit_vars.results['doc utilization'] = (audit_vars.results['docs occupied'].astype(float) / num_docs).astype(float)
    audit_vars.results['chair utilization'] = (audit_vars.results['chairs occupied'].astype(float) / num_chairs).astype(float)
    audit_vars.results['cashier utilization'] = (audit_vars.results['cashiers occupied'].astype(float) / num_cashiers).astype(float)
    audit_vars.results['pharmacist utilization'] = (audit_vars.results['pharmacists occupied'].astype(float) / num_pharmacists).astype(float)

    audit_vars.results['datetime'] = pd.date_range(start='1/1/2020', periods=len(audit_vars.results), freq=str(audit_vars.audit_interval)+'min')
    audit_vars.results['cost per unit time'] = audit_vars.audit_cost_unit_time
    audit_vars.patient_queuing_results.to_csv('patient results.csv')
    audit_vars.results.to_csv('operational results'+SIM_NAME+'.csv')

# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process

sim_mode = 'schedule'
env = simpy.Environment()
env.process(setup(env, num_docs, num_nurses, num_chairs, num_cashiers, num_pharmacists, sim_mode))
env.process(perform_audit(env))
# Execute!
env.run(until=SIM_TIME)
build_audit_results()