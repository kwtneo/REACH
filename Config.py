import random

class Global_vars:
    """Storage of global variables. No object instance created. All times are
    in minutes"""

    # Simulation run time and warm-up (warm-up is time before audit results are
    # collected)
    sim_duration = 1*24*60
    warm_up = 5

    # Average time between patients arriving
    inter_arrival_time = .25*24*60

    # TO BE IMPLEMENTED
    # Number of DMOs/doctors in ATU
    number_of_docs = 2

    # Number of nurses in ATU
    number_of_nurses = 2

    # number of chairs in ATU
    number_of_chairs = 2


    # Time between audits
    audit_interval = 1

    # Various inputs - ad this point only averages/means, but placeholders for standard deviation
    # Average and standard deviation of time patients spends for various activities
    max_patients = 100
    between_visits_time_mean = 1*24*60
    between_visits_time_sd = 3 * 24 * 60
    psa_registration_time_mean = 10
    psa_registration_time_sd = 7
    generic_waiting_time_mean = 95.7
    generic_waiting_time_sd = 7/10*generic_waiting_time_mean
    physician_consultation_1_time_mean = 29
    physician_consultation_1_time_sd = 7/10*physician_consultation_1_time_mean
    psa_payment_time_mean = 7.5
    psa_payment_time_sd = 7/10*psa_payment_time_mean
    psa_scheduling_time_mean = 7.5
    psa_scheduling_time_sd = 7/10*psa_scheduling_time_mean

    blood_test_time_mean = 30
    blood_test_time_sd = 7/10*blood_test_time_mean
    blood_test_atu_time_mean = 15
    blood_test_atu_time_sd = 7/10*blood_test_atu_time_mean
    blood_test_screening_time_mean = 15
    blood_test_screening_time_sd = 7/10*blood_test_screening_time_mean

    physician_consultation_2_time_mean = 11.5
    physician_consultation_2_time_sd = 7/10*physician_consultation_2_time_mean
    IV_start_time_mean = 1
    IV_start_time_sd = 7/10*IV_start_time_mean
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
    breast_paclitax_time_sd = 7/10*breast_paclitax_time_mean
    breast_paclitax_adr_time_mean = 67.8
    breast_paclitax_adr_time_sd = 7/10*breast_paclitax_adr_time_mean

    post_chemo_pharmacy_time_mean = 5
    post_chemo_pharmacy_time_sd = 7/10 * post_chemo_pharmacy_time_mean

    post_chemo_psa_registration_time_mean = 5
    post_chemo_psa_registration_time_sd = 7/10 * post_chemo_psa_registration_time_mean

    #appointment_time_mean = 18
    #appointment_time_sd = 7

    # Lists used to store audit results
    audit_time = []
    audit_patients_in_ED = []
    audit_patients_waiting = []
    audit_patients_waiting_p1 = []
    audit_patients_waiting_p2 = []
    audit_patients_waiting_p3 = []
    audit_reources_used = []

    # Set up dataframes to store results (will be transferred from lists)
    patient_queuing_results = pd.DataFrame(columns=['priority', 'q_time', 'treatment_time'])
    results = pd.DataFrame()

    # Set up counter for number for patients entering simulation
    patient_count = 0

    # Set up running counts of patients waiting (total and by priority)
    patients_db = {}
    patients_waiting = 0
    patients_waiting_by_priority = [0, 0, 0]

    # Set up probability based generators
    breast_dox_cyclophos_adr_probability = 0.009
    breast_dox_cyclophos_adr_probability_gen = (0 if random.random() < 0.009 else 1 for _ in range(10000))
    breast_adj_blood_test1_probability = 0.7
    breast_adj_blood_test1_probability_gen = (0 if random.random() < 0.7 else 1 for _ in range(10000))
    breast_adj_blood_test2_probability = 0.7
    breast_adj_blood_test2_probability_gen = (0 if random.random() < 0.7 else 1 for _ in range(10000))
    breast_adj_blood_test_atu_ac_probability = 0.3
    breast_adj_blood_test_atu_ac_probability_gen = (0 if random.random() < 0.3 else 1 for _ in range(10000))
    breast_adj_blood_test_atu_ac_review_probability = 0.3
    breast_adj_blood_test_atu_ac_review_probability_gen = (0 if random.random() < 0.3 else 1 for _ in range(10000))
    breast_adj_blood_test_atu_t_probability = 0.3
    breast_adj_blood_test_atu_t_probability_gen = (0 if random.random() < 0.3 else 1 for _ in range(10000))
    breast_adj_blood_test_atu_t_review_probability = 0.3
    breast_adj_blood_test_atu_t_review_probability_gen = (0 if random.random() < 0.3 else 1 for _ in range(10000))
    breast_paclitax_adr_probability = 0.027
    breast_paclitax_adr_probability_gen = (0 if random.random() < 0.027 else 1 for _ in range(10000))

    #conditions:
    conditions_map={1:'Breast_Metastatic',2:'Breast_Adjuvant',3:'GI_Metastatic',4:'GI_Adjuvant',5:'Lung_Metastatic',6:'Lung_Adjuvant'}
    breast_metastatic_map={1:''}

    # treatment specific variables NOT USER
    treatment_time = 0
    regimen_vars={}
    Breast_adj_ACP = {'ac_cycles':4,'t_cycles':12,'clinic_costs_1':310.03,'fu_clinics':8, 'fu_clinic_cost':249.19,'total_atu_cost':14771.88,'manpower':87.9,
                      'time':4988.4272,'overall_mortality_post':.35,'overall_mortality_pre':.4,'overall_survivability_post':.863,'overall_survivability_pre':.842,
                      'os_time_mths':6}
    #Breast_met_Dox
    #Breast_met_Pax
    #Breast_met_Cap
    #Lung_adj_GemCis
    #Lung_met_PCP
    #Lung_met_Pemz
    #Lung_met_Osi
    #GI_adj_Capox
    #GI_met_Cap
    #GI_met_Folfox
    #GI_met_Capox


