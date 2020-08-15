
import simpy
import random
import pandas as pd
import matplotlib.pyplot as plt

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
    # number_of_docs = 2

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


class Patient:
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

    def __init__(self, env, condition, treatment_regiment=None, treatment_regiment_step=None):
        """Constructor for new patient object.
        """

        # Increment global counts of patients
        Global_vars.patient_count += 1
        print('current patient count='+str(Global_vars.patient_count))

        # Set patient id and priority (random between 1 and 3)
        self.id = Global_vars.patient_count
        self.priority = random.randint(1 , 1)
        self.condition = condition
        self.treatment_regiment = treatment_regiment
        self.treatment_regiment_step=treatment_regiment_step

        # Set consultation time (time spent with doc) by random normal
        # distribution. If value <0 then set to 0
        #self.consulation_time = random.normalvariate(Global_vars.appointment_time_mean, Global_vars.appointment_time_sd)
        #self.consulation_time = 0 if self.consulation_time < 0 else self.consulation_time

        self.treatment_time_start = 0
        # Set initial queuing time as zero (this will be adjusted in model if
        # patient has to waiti for doc)
        self.queuing_time = 0

        # record simulation time patient enters simulation
        self.time_in = env.now

        # Set up variables to record simulation time that patients see doc and
        # exit simulation
        #self.time_see_doc = 0
        self.waiting_time = 0
        self.entire_treatment_regime_time = 0
        self.time_out = 0

    def treatment_regime(self):
        return None

class BreastAdjuvant_Patient(Patient):
    """extends from Patient - this specifies a patient with specific condition and treatment regime (for now).
    Methods are:
    __init__: constructor for new patient
    treatment_regime()
    """

    def __init__(self, env, treatment_regiment, treatment_regiment_step):
        Patient.__init__(self,env,condition=2,treatment_regiment=treatment_regiment,treatment_regiment_step=treatment_regiment_step)
        #
        #probability of ADR
        self.breast_dox_cyclophos_adr = next(Global_vars.breast_dox_cyclophos_adr_probability_gen)
        self.breast_adj_blood_test1 = next(Global_vars.breast_adj_blood_test1_probability_gen)
        self.breast_adj_blood_test2 = next(Global_vars.breast_adj_blood_test2_probability_gen)
        self.breast_adj_blood_test_atu_ac = next(Global_vars.breast_adj_blood_test_atu_ac_probability_gen)
        self.breast_adj_blood_test_atu_ac_review = self.breast_adj_blood_test_atu_ac
        self.breast_adj_blood_test_atu_t = next(Global_vars.breast_adj_blood_test_atu_t_probability_gen)
        self.breast_adj_blood_test_atu_t_review = self.breast_adj_blood_test_atu_t
        self.breast_paclitax_adr = next(Global_vars.breast_paclitax_adr_probability_gen)
        #self.metastatic_regiment = random.randint(1, 3)


    def treatment_regime(self):
        if(self.treatment_regiment_step is None):
            self.treatment_regiment_step=random.randint(1, 4)
        regime1 = [
                    (Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '1st psa registration time'),
                    (Global_vars.generic_waiting_time_mean,Global_vars.generic_waiting_time_sd, 'generic waiting'),
                    (Global_vars.physician_consultation_1_time_mean,Global_vars.physician_consultation_1_time_sd, 'dmo 1st consultation'),
                    (Global_vars.psa_payment_time_sd,Global_vars.psa_payment_time_sd, 'psa payment'),
                    (Global_vars.psa_scheduling_time_mean, Global_vars.psa_scheduling_time_sd, 'psa scheduling'),
            ]
        if (self.breast_adj_blood_test1):
            regime1.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_time_sd, '1st blood test'))

        wait1=[(Global_vars.between_visits_time_mean, Global_vars.between_visits_time_sd, 'time between visit')]

        regime2 = [(Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '2nd psa registration'),]
        if (self.breast_adj_blood_test2):
            regime2.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_time_sd, '2nd blood test'))
        regime2.append((Global_vars.generic_waiting_time_mean, Global_vars.generic_waiting_time_sd, 'generic waiting time'))
        regime2.append((Global_vars.physician_consultation_2_time_mean, Global_vars.physician_consultation_2_time_sd, 'dmo 2nd consultation'))
        regime2.append((Global_vars.psa_payment_time_sd, Global_vars.psa_payment_time_sd, 'psa payment'))
        regime2.append((Global_vars.psa_scheduling_time_mean, Global_vars.psa_scheduling_time_sd, 'psa scheduling'))
        wait2=[(Global_vars.between_visits_time_mean, Global_vars.between_visits_time_sd, 'time between visit')]

        regime3=[
            (Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '3rd psa registration'),
            (Global_vars.IV_start_time_mean,Global_vars.IV_start_time_sd,'IV start - ATU (AC)'),
            (Global_vars.IV_chemo_infusion_time_mean, Global_vars.IV_chemo_infusion_time_sd, 'IV Chemo Infusion - ATU (AC)'),
            (Global_vars.breast_facility_time_mean, Global_vars.breast_facility_time_sd, ''),
        ]
        if (self.breast_adj_blood_test_atu_ac):
            regime3.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_atu_time_sd, 'ATU (AC) blood test'))
            regime3.append((Global_vars.review_test_results_time_mean, Global_vars.review_test_results_time_sd, 'ATU (AC) blood test review'))
        regime3.append((Global_vars.blood_test_screening_time_mean, Global_vars.blood_test_screening_time_sd, 'ATU (AC) blood test screening'))
        regime3.append((Global_vars.breast_atu_premed_time_mean, Global_vars.breast_atu_premed_time_sd, 'ATU (AC) premedication'))
        regime3.append((Global_vars.breast_dox_cyclophos_time_mean, Global_vars.breast_dox_cyclophos_time_sd, 'ATU (AC) Doxorubicin, Cyclophosphamide'))
        if(self.breast_dox_cyclophos_adr):
            regime3.append((Global_vars.breast_dox_cyclophos_adr_time_mean, Global_vars.breast_dox_cyclophos_adr_time_sd, 'ATU (AC) Doxorubicin, Cyclophosphamide ADR'))
        regime3.append((Global_vars.post_chemo_pharmacy_time_mean, Global_vars.post_chemo_pharmacy_time_sd, 'ATU (AC) post chemo pharmacy'))
        wait3=[(Global_vars.between_visits_time_mean, Global_vars.between_visits_time_sd,'time between visit')]
        regime4=[
            (Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '4th psa registration'),
            (Global_vars.IV_start_time_mean,Global_vars.IV_start_time_sd,'IV start - ATU (T)'),
            (Global_vars.IV_chemo_infusion_time_mean, Global_vars.IV_chemo_infusion_time_sd, 'IV Chemo Infusion - ATU (T)'),
            (Global_vars.breast_facility_time_mean, Global_vars.breast_facility_time_sd, ''),
        ]
        if (self.breast_adj_blood_test_atu_t):
            regime4.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_atu_time_sd, 'ATU (T) blood test'))
            regime4.append((Global_vars.review_test_results_time_mean, Global_vars.review_test_results_time_sd, 'ATU (T) blood test review'))
        regime4.append((Global_vars.blood_test_screening_time_mean, Global_vars.blood_test_screening_time_sd, 'ATU (T) blood test screening'))
        regime4.append((Global_vars.breast_atu_premed_time_mean, Global_vars.breast_atu_premed_time_sd, 'ATU (T) premedication'))
        regime4.append((Global_vars.breast_paclitax_time_mean, Global_vars.breast_paclitax_time_sd, 'ATU (T) paclitaxel'))
        if(self.breast_paclitax_adr):
            regime4.append((Global_vars.breast_paclitax_adr_time_mean, Global_vars.breast_paclitax_adr_time_sd, 'ATU (T) paclitaxel ADR'))
        regime4.append((Global_vars.post_chemo_pharmacy_time_mean, Global_vars.post_chemo_pharmacy_time_sd, 'ATU (T) post chemo pharmacy'))

        if(self.treatment_regiment_step==1):
            return regime1
        if(self.treatment_regiment_step==2):
            return regime2
        if(self.treatment_regiment_step==3):
            return regime3
        if(self.treatment_regiment_step==4):
            return regime4
        return

class BreastMetatstatic_Patient(Patient):
    """extends from Patient - this specifies a patient with specific condition and treatment regime (for now).
    Methods are:
    __init__: constructor for new patient
    treatment_regime()
    """

    def __init__(self):
        Patient.__init__(self,self.env,condition=1)
        self.metastatic_regiment = random.randint(1, 3)
    def treatment_regime(self):
        return




class Model:
    """
    Model class contains the following methods:

    __init__:  constructor for initiating simpy simulation environment.

    build_audit_results: At end of model run, transfers results held in lists
        into a pandas DataFrame.

    chart: At end of model run, plots model results using MatPlotLib.

    perform_audit: Called at each audit interval. Records simulation time, total
        patients waiting, patients waiting by priority, and number of nurses
        occupied. Will then schedule next audit.

    run: Called immediately after initialising simulation object. This method:
        1) Calls method to set up nurse resources.
        2) Initialises the two starting processes: patient admissions and audit.
        3) Starts model envrionment.
        4) Save individual patient level results to csv
        5) Calls the build_audit_results metha and saves to csv
        6) Calls the chart method to plot results

    get_treatment: After a patient arrives (generated in the trigger_admissions
        method of this class), this get_treatment process method is called (with
        patient object, treatment time, treatment description passed to process
        method). This process requires a free nurse resource (resource objects
        held in this model class). The request is prioritised by patient priority
        (lower priority numbers grab resources first). The number of patients
        waiting is incremented, and nurse resources are requested. Once a nurse
        resource becomes available queuing times are recorded (these are saved
        to global results if warm up period has been completed). The patient
        is held for the required time with nurse and then time with nurse recorded.
        The patient is then removed from the Patient class dictionary
        (which triggers Python to remove the patient object).

    trigger_admissions: Generates new patient admissions. Each patient is an
        instance of the Patient obect class. This method allocates each
        patient an ID, adds the patient to the dictionary of patients held by
        the Patient class (static class variable), initiates a simpy process
        (in this model class) to see a nurse, and schedules the next admission.

    """

    def __init__(self):
        """constructor for initiating simpy simulation environment"""
        self.env = simpy.Environment()

    def build_audit_results(self):
        """At end of model run, transfers results held in lists into a pandas
        DataFrame."""

        Global_vars.results['time'] = Global_vars.audit_time
        Global_vars.results['patients in ED'] = Global_vars.audit_patients_in_ED
        Global_vars.results['all patients waiting'] = Global_vars.audit_patients_waiting
        Global_vars.results['priority 1 patients treatment waiting'] = Global_vars.audit_patients_waiting_p1
        Global_vars.results['priority 2 patients treatment waiting'] = Global_vars.audit_patients_waiting_p2
        Global_vars.results['priority 3 patients treatment waiting'] = Global_vars.audit_patients_waiting_p3
        Global_vars.results['resources occupied'] = Global_vars.audit_reources_used

    def chart(self):
        """At end of model run, plots model results using MatPlotLib."""

        # Define figure size and defintion
        fig = plt.figure(figsize=(12, 4.5), dpi=75)
        # Create two charts side by side

        # Figure 1: patient perspective results
        ax1 = fig.add_subplot(131)  # 1 row, 3 cols, chart position 1
        x = Global_vars.patient_queuing_results.index
        # Chart loops through 3 priorites
        markers = ['o', 'x', '^']
        for priority in range(1, 4):
            x = (Global_vars.patient_queuing_results[Global_vars.patient_queuing_results['priority']==priority].index)
            y = (Global_vars.patient_queuing_results[Global_vars.patient_queuing_results['priority']==priority]['q_time'])

            ax1.scatter(x, y,marker=markers[priority - 1],label='Priority ' + str(priority))

        ax1.set_xlabel('Patient')
        ax1.set_ylabel('Queuing time')
        ax1.legend()
        ax1.grid(True, which='both', lw=1, ls='--', c='.75')

        # Figure 2: ED level queuing results
        ax2 = fig.add_subplot(132)  # 1 row, 3 cols, chart position 2
        x = Global_vars.results['time']
        y1 = Global_vars.results['priority 1 patients treatment waiting']
        y2 = Global_vars.results['priority 2 patients treatment waiting']
        y3 = Global_vars.results['priority 3 patients treatment waiting']
        #y4 = Global_vars.results['all patients waiting']
        ax2.plot(x, y1, marker='o', label='Priority 1')
        ax2.plot(x, y2, marker='x', label='Priority 2')
        ax2.plot(x, y3, marker='^', label='Priority 3')
        #ax2.plot(x, y4, marker='s', label='All')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('discrete treatments that require waiting')
        ax2.legend()
        ax2.grid(True, which='both', lw=1, ls='--', c='.75')

        # Figure 3: ED staff usage
        ax3 = fig.add_subplot(133)  # 1 row, 3 cols, chart position 3
        x = Global_vars.results['time']
        y = Global_vars.results['resources occupied']
        ax3.plot(x, y, label='resources occupied')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('resources occupied')
        ax3.legend()
        ax3.grid(True, which='both', lw=1, ls='--', c='.75')

        # Create plot
        plt.tight_layout(pad=3)
        plt.show()

    def perform_audit(self):
        """Called at each audit interval. Records simulation time, total
        patients waiting, patients waiting by priority, and number of nurses
        occupied. Will then schedule next audit."""

        # Delay before first aurdit if length of warm-up
        yield self.env.timeout(Global_vars.warm_up)
        # The trigger repeated audits
        while True:
            # Record time
            Global_vars.audit_time.append(self.env.now)
            # Record patients waiting by referencing global variables
            Global_vars.audit_patients_waiting.append(Global_vars.patients_waiting)
            Global_vars.audit_patients_waiting_p1.append(Global_vars.patients_waiting_by_priority[0])
            Global_vars.audit_patients_waiting_p2.append(Global_vars.patients_waiting_by_priority[1])
            Global_vars.audit_patients_waiting_p3.append(Global_vars.patients_waiting_by_priority[2])
            # Record patients waiting by asking length of dictionary of all
            # patients (another way of doing things)
            Global_vars.audit_patients_in_ED.append(len(Patient.all_patients))
            # Record resources occupied
            Global_vars.audit_reources_used.append(self.nurse_resources.nurses.count)
            # Trigger next audit after interval
            yield self.env.timeout(Global_vars.audit_interval)

    def run(self):
        """Called immediately after initialising simulation object. This method:
        1) Calls method to set up nurse resources.
        2) Initialises the two starting processes: patient admissions and audit.
        3) Starts model envrionment.
        4) Save individual patient level results to csv
        5) Calls the build_audit_results metha and saves to csv
        6) Calls the chart method to plot results
        """

        # Set up resources using Resouces class
        #self.doc_resources = Resources(self.env, Global_vars.number_of_docs)
        self.nurse_resources = Resources(self.env, Global_vars.number_of_nurses)

        # Initialise processes that will run on model run
        self.env.process(self.trigger_admissions())
        self.env.process(self.perform_audit())

        # Run
        self.env.run(until=Global_vars.sim_duration)

        # End of simulation run. Build and save results
        Global_vars.patient_queuing_results.to_csv('patient results.csv')
        self.build_audit_results()

        Global_vars.results.to_csv('operational results.csv')
        # plot results
        self.chart()

    def get_treatment(self, p:Patient, t_time:float, t_desc:str):
        with self.nurse_resources.nurses.request(priority=p.priority) as req:
            # Increment count of number of patients waiting. 1 is subtracted
            # from priority to align priority (1-3) with zero indexed list.
            #if(p.id not in Global_vars.patients_db.keys()):
            Global_vars.treatment_time += t_time

            Global_vars.patients_waiting += 1
            Global_vars.patients_waiting_by_priority[p.priority - 1] += 1
            print('inputs: desc='+t_desc+' time_Input:'+str(t_time)+' counter:'+str(Global_vars.patients_waiting)+' total treatment time:'+str(Global_vars.treatment_time))

            # Wait for resources to become available
            yield req

            # Resources now available. Record time patient starts to see doc
            p.treatment_time_start = self.env.now
            # Record patient queuing time in patient object
            p.queuing_time = self.env.now - p.time_in

            # Reduce count of number of patients (waiting)
            #if(p.id not in Global_vars.patients_db.keys()):
            Global_vars.patients_waiting_by_priority[p.priority - 1] -= 1
            Global_vars.patients_waiting -= 1


            # Create a temporary results list with patient priority and queuing
            # time
            _results = [p.priority, p.queuing_time]

            # Hold patient (with nurse) for treatment time required
            #
            #
            #
            #for treatment_item in treatment_regime:
            #    t_time = treatment_item[0]
                #t_time = random.normalvariate(treatment_item[0], treatment_item[1])
                #t_time = 0 if t_time < 0 else t_time
            yield self.env.timeout(t_time)

            # At end of treatment add time spent to temp results
            _results.append(self.env.now - p.treatment_time_start)

            # Record results in global results data if warm-up complete
            if self.env.now >= Global_vars.warm_up:
                Global_vars.patient_queuing_results.loc[p.id] = _results

            # Delete patient (removal from patient dictionary removes only
            # reference to patient and Python then automatically cleans up)
            #del Patient.all_patients[p.id]


    def trigger_admissions(self):
        """Generates new patient admissions. Each patient is an instance of the
        Patient obect class. This method allocates each patient an ID, adds the
        patient to the dictionary of patients held by the Patient class (static
        class variable), initiates a simpy process (in this model class) to see
        a doc, and then schedules the next admission"""

        # While loop continues generating new patients throughout model run
        while len(Patient.all_patients) < Global_vars.max_patients:
            # Initialise new patient (pass environment to be used to record
            # current simulation time)
            p = BreastAdjuvant_Patient(self.env,None,None)
            # Add patient to dictionary of patients
            Patient.all_patients[p.id] = p
            # Pass patient to treatment
            for treatment_item in p.treatment_regime():
                t_time = treatment_item[0]
                t_desc = treatment_item[2]
                self.env.process(self.get_treatment(p, t_time, t_desc))
                # Sample time for next admission
            next_admission = random.expovariate(1 / Global_vars.inter_arrival_time)
            # Schedule next admission
            yield self.env.timeout(next_admission)


class Resources:
    """Resources class for simpy. resources are nurses and chairs"""
    def __init__(self, env, number_of_nurses, number_of_chairs):
        #self.docs = simpy.PriorityResource(env, capacity=number_of_docs)
        self.chairs = simpy.PriorityResource(env, capacity=number_of_chairs)
        self.nurses = simpy.PriorityResource(env, capacity=number_of_nurses)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Run model
    # if __name__ == '__main__':
    # Initialise model environment
    model = Model()
    # Run model
    model.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

