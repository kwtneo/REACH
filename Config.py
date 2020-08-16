import random
import pandas as pd


class Global_vars:
    # Set up counter for number for patients entering simulation
    patient_count = 0

    # Set up running counts of patients waiting (total and by priority)
    patients_db = {}
    patients_waiting = 0
    patients_waiting_for_nurses = 0
    patients_waiting_for_chairs = 0
    patients_waiting_for_docs = 0
    patients_waiting_for_cashiers = 0
    patients_waiting_for_pharmacists = 0
    patients_waiting_by_priority = [0, 0, 0]

    treatment_time = 0
    admin_time = 0
    inter_treatment_time = 0

    # Simulation run time and warm-up (warm-up is time before audit results are
    # collected)
    sim_duration = 20 * 24 * 60
    warm_up = 5

    # Average time between patients arriving
    inter_arrival_time = .25 * 24 * 60

    # TO BE IMPLEMENTED
    # Number of DMOs/doctors in ATU
    number_of_docs = 1

    # Number of nurses in ATU
    number_of_nurses = 1

    # number of chairs in ATU
    number_of_chairs = 1

    # number of pharmacists
    number_of_pharmacists = 1

    # number of cashiers
    number_of_cashiers = 1

    # Time between audits
    audit_interval = 1

    # Various inputs - ad this point only averages/means, but placeholders for standard deviation
    # Average and standard deviation of time patients spends for various activities
    max_patients = 10


    # appointment_time_mean = 18
    # appointment_time_sd = 7

    # Lists used to store audit results
    audit_time = []
    audit_patients_in_ATU = []
    audit_patients_waiting = []
    audit_patients_waiting_for_nurses = []
    audit_patients_waiting_for_chairs = []
    audit_patients_waiting_for_docs = []
    audit_patients_waiting_for_cashiers = []
    audit_patients_waiting_for_pharmacists = []
    audit_patients_waiting_p1 = []
    audit_patients_waiting_p2 = []
    audit_patients_waiting_p3 = []
    audit_reources_used = []

    # Set up dataframes to store results (will be transferred from lists)
    patient_queuing_results = pd.DataFrame(columns=['priority', 'q_time', 'treatment_time'])
    results = pd.DataFrame()
    patient_treatment_queuing_results = pd.DataFrame(columns=['priority', 'q_time', 'treatment_time'])
    patient_admin_queuing_results = pd.DataFrame(columns=['priority', 'q_time', 'admin_time'])
    # patient_treatment_queuing_results = pd.DataFrame(columns=['priority', 'q_time', 'treatment_time'])



