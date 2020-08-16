import Config
import random

Global_vars = Config.Global_vars

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

    def __init__(self, env, condition, treatment_regime=None):
        """Constructor for new patient object.
        """

        # Increment global counts of patients
        Global_vars.patient_count += 1
        print('current patient count='+str(Global_vars.patient_count))

        # Set patient id and priority (random between 1 and 3)
        self.id = Global_vars.patient_count
        self.priority = random.randint(1 , 1)
        self.condition = condition
        self.treatment_regime = treatment_regime
        self.treatment_regime_step = None

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

    def get_treatment_regime(self):
        return None

class BreastAdjuvant_Patient(Patient):
    """extends from Patient - this specifies a patient with specific condition and treatment regime (for now).
    Methods are:
    __init__: constructor for new patient
    treatment_regime()
    """

    def __init__(self, env, treatment_regime):
        Patient.__init__(self,env,condition=2,treatment_regime=treatment_regime)
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


    def get_treatment_regime(self):
        regime = [
                    (Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '1st psa registration time',['nurse']),
                    (Global_vars.generic_waiting_time_mean,Global_vars.generic_waiting_time_sd, 'generic waiting',None),
                    (Global_vars.physician_consultation_1_time_mean,Global_vars.physician_consultation_1_time_sd, 'dmo 1st consultation',['dmo']),
                    (Global_vars.psa_payment_time_sd,Global_vars.psa_payment_time_sd, 'psa payment',['cashier']),
                    (Global_vars.psa_scheduling_time_mean, Global_vars.psa_scheduling_time_sd, 'psa scheduling',['nurse']),
                ]
        if (self.breast_adj_blood_test1):
            regime.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_time_sd, '1st blood test',['nurse']))

        wait1=[(Global_vars.between_visits_time_mean, Global_vars.between_visits_time_sd, 'time between visit',None)]

        regime.append((Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '2nd psa registration',['nurse']))
        if (self.breast_adj_blood_test2):
            regime.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_time_sd, '2nd blood test',['nurse']))
        regime.append((Global_vars.generic_waiting_time_mean, Global_vars.generic_waiting_time_sd, 'generic waiting time', None))
        regime.append((Global_vars.physician_consultation_2_time_mean, Global_vars.physician_consultation_2_time_sd,
                        'dmo 2nd consultation',['dmo']))
        regime.append((Global_vars.psa_payment_time_sd, Global_vars.psa_payment_time_sd, 'psa payment',['cashier']))
        regime.append((Global_vars.psa_scheduling_time_mean, Global_vars.psa_scheduling_time_sd, 'psa scheduling',['nurse']))
        wait2=[(Global_vars.between_visits_time_mean, Global_vars.between_visits_time_sd, 'time between visit', None)]

        regime.append((Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '3rd psa registration',['nurse']))
        regime.append((Global_vars.IV_start_time_mean,Global_vars.IV_start_time_sd,'IV start - ATU (AC)',['chair','nurse']))
        regime.append((Global_vars.IV_chemo_infusion_time_mean, Global_vars.IV_chemo_infusion_time_sd, 'IV Chemo Infusion - ATU (AC)',['chair','nurse']))
        regime.append((Global_vars.breast_facility_time_mean, Global_vars.breast_facility_time_sd, '', None))

        if (self.breast_adj_blood_test_atu_ac):
            regime.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_atu_time_sd, 'ATU (AC) blood test',['nurse']))
            regime.append((Global_vars.review_test_results_time_mean, Global_vars.review_test_results_time_sd, 'ATU (AC) blood test review',['dmo']))
        regime.append((Global_vars.blood_test_screening_time_mean, Global_vars.blood_test_screening_time_sd, 'ATU (AC) blood test screening',['dmo']))
        regime.append((Global_vars.breast_atu_premed_time_mean, Global_vars.breast_atu_premed_time_sd, 'ATU (AC) premedication',['nurse']))
        regime.append((Global_vars.breast_dox_cyclophos_time_mean, Global_vars.breast_dox_cyclophos_time_sd, 'ATU (AC) Doxorubicin, Cyclophosphamide',['chair','nurse']))
        if(self.breast_dox_cyclophos_adr):
            regime.append((Global_vars.breast_dox_cyclophos_adr_time_mean, Global_vars.breast_dox_cyclophos_adr_time_sd, 'ATU (AC) Doxorubicin, Cyclophosphamide ADR',['chair','nurse']))
        regime.append((Global_vars.post_chemo_pharmacy_time_mean, Global_vars.post_chemo_pharmacy_time_sd, 'ATU (AC) post chemo pharmacy',['pharmacist']))
        wait3=[(Global_vars.between_visits_time_mean, Global_vars.between_visits_time_sd,'time between visit',None)]

        regime.append((Global_vars.psa_registration_time_mean, Global_vars.psa_registration_time_sd, '4th psa registration',['nurse']))
        regime.append((Global_vars.IV_start_time_mean,Global_vars.IV_start_time_sd,'IV start - ATU (T)',['chair','nurse']))
        regime.append((Global_vars.IV_chemo_infusion_time_mean, Global_vars.IV_chemo_infusion_time_sd, 'IV Chemo Infusion - ATU (T)',['chair','nurse']))
        regime.append((Global_vars.breast_facility_time_mean, Global_vars.breast_facility_time_sd, '', None))

        if (self.breast_adj_blood_test_atu_t):
            regime.append((Global_vars.blood_test_time_mean, Global_vars.blood_test_atu_time_sd, 'ATU (T) blood test',['nurse']))
            regime.append((Global_vars.review_test_results_time_mean, Global_vars.review_test_results_time_sd, 'ATU (T) blood test review',['nurse']))
        regime.append((Global_vars.blood_test_screening_time_mean, Global_vars.blood_test_screening_time_sd, 'ATU (T) blood test screening',['dmo']))
        regime.append((Global_vars.breast_atu_premed_time_mean, Global_vars.breast_atu_premed_time_sd, 'ATU (T) premedication',['nurse']))
        regime.append((Global_vars.breast_paclitax_time_mean, Global_vars.breast_paclitax_time_sd, 'ATU (T) paclitaxel',['chair','nurse']))
        if(self.breast_paclitax_adr):
            regime.append((Global_vars.breast_paclitax_adr_time_mean, Global_vars.breast_paclitax_adr_time_sd, 'ATU (T) paclitaxel ADR',['chair','nurse']))
        regime.append((Global_vars.post_chemo_pharmacy_time_mean, Global_vars.post_chemo_pharmacy_time_sd, 'ATU (T) post chemo pharmacy',['chair','nurse']))
        return regime

class BreastMetatstatic_Patient(Patient):
    """extends from Patient - this specifies a patient with specific condition and treatment regime (for now).
    Methods are:
    __init__: constructor for new patient
    treatment_regime()
    """

    def __init__(self):
        Patient.__init__(self,self.env,condition=1)
        self.metastatic_regiment = random.randint(1, 3)
    def get_treatment_regime(self):
        return
