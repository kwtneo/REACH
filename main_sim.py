"""

"""
import random
import simpy


RANDOM_SEED = 42
num_chairs = 1
num_nurses = 1
num_docs = 1
num_cashiers = 1
num_pharmacists = 1


#p_inter = 2
SIM_TIME = 1200

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



class Hospital(object):
    def __init__(self, env, num_docs, num_nurses, num_chairs):
        self.env = env
        self.docs = simpy.PriorityResource(env, num_docs)
        self.nurses = simpy.PriorityResource(env, num_nurses)
        self.chairs = simpy.PriorityResource(env, num_chairs)
        self.cashiers = simpy.Resource(env, num_cashiers)
        self.pharmacists = simpy.Resource(env, num_pharmacists)
        self.regime_details = \
            {
             '1st psa registration time':(patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin'),
             'generic waiting time':(patient_vars.generic_waiting_time_mean, patient_vars.generic_waiting_time_sd, None, 'admin'),
             'consultation':(patient_vars.physician_consultation_1_time_mean, patient_vars.physician_consultation_1_time_sd,['dmo'], 'admin'),
             'psa payment':(patient_vars.psa_payment_time_sd, patient_vars.psa_payment_time_sd, 'psa payment', ['cashier'], 'admin'),
             'psa scheduling':(patient_vars.psa_scheduling_time_mean, patient_vars.psa_scheduling_time_sd,['nurse'],'admin'),
             '1st blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_time_sd,['nurse'], 'admin'),
             'time between visit':(patient_vars.between_visits_time_mean, patient_vars.between_visits_time_sd, None, 'time_between_visits'),
             '2nd psa registration':(patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin'),
             '2nd blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_time_sd, ['nurse'], 'admin'),
             'dmo 1st consultation': (patient_vars.physician_consultation_1_time_mean, patient_vars.physician_consultation_1_time_sd, ['dmo'],'admin'),
             'dmo 2nd consultation':(patient_vars.physician_consultation_2_time_mean,patient_vars.physician_consultation_2_time_sd, ['dmo'], 'admin'),
             '3rd psa registration': (patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin'),
             'IV start - ATU (AC)':(patient_vars.IV_start_time_mean, patient_vars.IV_start_time_sd, ['chair', 'nurse'], 'treatment'),
             'IV Chemo Infusion - ATU (AC)':(patient_vars.IV_chemo_infusion_time_mean, patient_vars.IV_chemo_infusion_time_sd,['chair', 'nurse'], 'treatment'),
             'breast facility':(patient_vars.breast_facility_time_mean, patient_vars.breast_facility_time_sd, None, 'treatment'),
             'ATU (AC) blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_atu_time_sd, ['nurse'], 'treatment'),
             'ATU (AC) blood test review':(patient_vars.review_test_results_time_mean, patient_vars.review_test_results_time_sd, ['dmo'], 'treatment'),
             'ATU (AC) blood test screening':(patient_vars.blood_test_screening_time_mean, patient_vars.blood_test_screening_time_sd, ['dmo'], 'treatment'),
             'ATU (AC) premedication':(patient_vars.breast_atu_premed_time_mean, patient_vars.breast_atu_premed_time_sd,['nurse'], 'treatment'),
             'ATU (AC) Doxorubicin, Cyclophosphamide':(patient_vars.breast_dox_cyclophos_time_mean, patient_vars.breast_dox_cyclophos_time_sd, ['chair', 'nurse'], 'treatment'),
             'ATU (AC) Doxorubicin, Cyclophosphamide ADR':(patient_vars.breast_dox_cyclophos_adr_time_mean,patient_vars.breast_dox_cyclophos_adr_time_sd,['chair', 'nurse'], 'treatment'),
             'ATU (AC) post chemo pharmacy':(patient_vars.post_chemo_pharmacy_time_mean, patient_vars.post_chemo_pharmacy_time_sd,['pharmacist'], 'admin'),
             '4th psa registration':(patient_vars.psa_registration_time_mean, patient_vars.psa_registration_time_sd, ['nurse'], 'admin'),
             'IV start - ATU (T)':(patient_vars.IV_start_time_mean, patient_vars.IV_start_time_sd, ['chair', 'nurse'], 'treatment'),
             'IV Chemo Infusion - ATU (T)':(patient_vars.IV_chemo_infusion_time_mean, patient_vars.IV_chemo_infusion_time_sd,['chair', 'nurse'], 'treatment'),
             'ATU (T) blood test':(patient_vars.blood_test_time_mean, patient_vars.blood_test_atu_time_sd, ['nurse'], 'treatment'),
             'ATU (T) blood test review': (patient_vars.review_test_results_time_mean, patient_vars.review_test_results_time_sd, ['dmo'],'treatment'),
             'ATU (T) blood test screening': (patient_vars.blood_test_screening_time_mean, patient_vars.blood_test_screening_time_sd, ['dmo'],'treatment'),
             'ATU (T) premedication':(patient_vars.breast_atu_premed_time_mean, patient_vars.breast_atu_premed_time_sd,['nurse'], 'treatment'),
             'ATU (T) paclitaxel':(patient_vars.breast_paclitax_time_mean, patient_vars.breast_paclitax_time_sd,['chair', 'nurse'], 'treatment'),
             'ATU (T) paclitaxel ADR':(patient_vars.breast_paclitax_adr_time_mean, patient_vars.breast_paclitax_adr_time_sd, ['chair', 'nurse'], 'treatment'),
             'ATU (T) post chemo pharmacy': (patient_vars.post_chemo_pharmacy_time_mean, patient_vars.post_chemo_pharmacy_time_sd, ['pharmacist'],'admin'),
            }

    def undergo_treatment(self, treatment_desc):
        yield self.env.timeout(self.regime_details[treatment_desc][0])


def Patient(env, id, hosp):
    p_priority = random.randint(1, 1)
    print('Patient %s arrives at the hospital at %.2f.' % (id, env.now))
    #regimes = ['1st psa registration time','generic waiting','consultation','psa payment','psa scheduling','1st blood test','IV start - ATU (AC)']
    regimes = ['1st psa registration time','generic waiting time','dmo 1st consultation','psa payment','psa scheduling',]
    if (patient_vars.breast_adj_blood_test2_probability_gen):
        regimes.append('1st blood test');
    regimes.append('time between visit');regimes.append('2nd psa registration')
    if (patient_vars.breast_adj_blood_test2_probability_gen):
        regimes.append('2nd blood test');regimes.append('generic waiting time');regimes.append('dmo 2nd consultation');regimes.append('psa payment')
    regimes.append('psa scheduling');regimes.append('3rd psa registration');regimes.append('IV start - ATU (AC)')
    regimes.append('IV Chemo Infusion - ATU (AC)');regimes.append('breast facility')
    if (patient_vars.breast_adj_blood_test_atu_ac_probability_gen):
        regimes.append('ATU (AC) blood test');regimes.append('ATU (AC) blood test review');regimes.append('ATU (AC) blood test screening')
    regimes.append('ATU (AC) premedication');regimes.append('ATU (AC) Doxorubicin, Cyclophosphamide')
    if(patient_vars.breast_dox_cyclophos_adr_probability_gen):
        regimes.append('ATU (AC) Doxorubicin, Cyclophosphamide ADR')
    regimes.append('ATU (AC) post chemo pharmacy');regimes.append('time between visit')
    regimes.append('4th psa registration'),regimes.append('IV start - ATU (T)');regimes.append('IV Chemo Infusion - ATU (T)');regimes.append('breast facility')
    if (patient_vars.breast_adj_blood_test_atu_t_probability_gen):
        regimes.append('ATU (T) blood test');regimes.append('ATU (T) blood test review');regimes.append('ATU (T) blood test screening')
    regimes.append('ATU (T) premedication');regimes.append('ATU (T) paclitaxel')
    if(patient_vars.breast_paclitax_adr_probability_gen):
        regimes.append('ATU (T) paclitaxel ADR')
    regimes.append('ATU (T) post chemo pharmacy')

    for item in regimes:

        dependency = hosp.regime_details[item][2]
        #print(dependency)
        if (dependency is None):
            yield env.process(hosp.undergo_treatment(item))
        else:
            if('dmo' in dependency):
                with hosp.docs.request(priority=p_priority) as doc_request:
                    yield doc_request
                    if ('nurse' in dependency):
                        with hosp.nurses.request(priority=p_priority) as nur_request:
                            yield nur_request
                            print('Patient %s gets attended by nurse at %.2f.: %s.' % (id, env.now, item))
                            yield env.process(hosp.undergo_treatment(item))
                            print('Patient %s stops treatment %.2f.' % (id, env.now))
                    else:
                        print('Patient %s gets attended by dmo at %.2f.: %s. ' % (id, env.now, item))
                        yield env.process(hosp.undergo_treatment(item))
                        print('Patient %s stops treatment with dmo %.2f.' % (id, env.now))

            if('chair' in dependency):
                with hosp.chairs.request(priority=p_priority) as chr_request:
                    yield chr_request
                    print('Patient %s gets chair at %.2f.: %s.' % (id, env.now, item))
                    if('nurse' in dependency):
                        with hosp.nurses.request(priority=p_priority) as nur_request:
                            yield nur_request
                            print('Patient %s gets attended by nurse at %.2f.: %s.' % (id, env.now,item))
                            yield env.process(hosp.undergo_treatment(item))
                            print('Patient %s stops treatment in chair at %.2f.' % (id, env.now))

            if('nurse' in dependency):
                with hosp.nurses.request(priority=p_priority) as nur_request:
                    yield nur_request
                    print('Patient %s gets attended by nurse at %.2f.: %s.' % (id, env.now, item))
                    yield env.process(hosp.undergo_treatment(item))
                    print('Patient %s stops treatment %.2f.' % (id, env.now))

            if('cashier' in dependency):
                with hosp.cashiers.request() as cas_request:
                    yield cas_request
                    print('Patient %s gets attended by cashier at %.2f.: %s.' % (id, env.now, item))
                    yield env.process(hosp.undergo_treatment(item))
                    print('Patient %s leaves cashiers station at %.2f.' % (id, env.now))

            if('pharmacist' in dependency):
                with hosp.pharmacists.request() as phm_request:
                    yield phm_request
                    print('Patient %s gets attended by pharmacist at %.2f.: %s.' % (id, env.now, item))
                    yield env.process(hosp.undergo_treatment(item))
                    print('Patient %s leaves pharmacy at %.2f.' % (id, env.now))


def setup(env, num_docs, num_nurses, num_chairs):
    # Create the hospital
    hospital = Hospital(env, num_docs, num_nurses, num_chairs)
    t_inter = 180
    # Create initial
    for i in range(2):
        env.process(Patient(env, i, hospital))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
        i += 1
        env.process(Patient(env, i, hospital))


# Setup and start the simulation
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, num_docs, num_nurses, num_chairs))

# Execute!
env.run(until=SIM_TIME)