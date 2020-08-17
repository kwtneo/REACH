import Config
import Patient
import Resources
import random
import simpy
import pandas as pd
import matplotlib.pyplot as plt

global Global_vars
Global_vars = Config.Global_vars





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
        Global_vars.results['patients in ATU'] = Global_vars.audit_patients_in_ATU
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
            x = Global_vars.patient_queuing_results[Global_vars.patient_queuing_results['priority']==priority].index
            y = Global_vars.patient_queuing_results[Global_vars.patient_queuing_results['priority']==priority]['q_time']

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
        ax2.set_ylabel('patients that require waiting')
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
            Global_vars.audit_patients_in_ATU.append(len(Patient.CancerPatient.all_patients))
            # Record resources occupied
            Global_vars.audit_reources_used.append(self.nurse_resources.count)
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
        self.hospitalResources = Resources.HostpitalATUResources(self.env, Global_vars.number_of_docs,
                                                            Global_vars.number_of_nurses,
                                                            Global_vars.number_of_chairs,
                                                            Global_vars.number_of_pharmacists,
                                                            Global_vars.number_of_cashiers)
        self.doc_resources = self.hospitalResources.docs
        self.nurse_resources = self.hospitalResources.nurses
        self.chair_resources = self.hospitalResources.chairs
        self.pharmacists_resources = self.hospitalResources.pharmacists
        self.cashier_resources = self.hospitalResources.cashiers

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


    def trigger_admissions(self):
        """Generates new patient admissions. Each patient is an instance of the
        Patient obect class. This method allocates each patient an ID, adds the
        patient to the dictionary of patients held by the Patient class (static
        class variable), initiates a simpy process (in this model class) to see
        a doc, and then schedules the next admission"""

        # While loop continues generating new patients throughout model run
        while len(Patient.CancerPatient.all_patients) < Global_vars.max_patients:
            # Initialise new patient (pass environment to be used to record
            # current simulation time)
            #p = Patient.BreastAdjuvant_Patient(self.env,Global_vars.patient_count,None)
            p = Patient.BreastMetatstatic_Patient(self.env, Global_vars.patient_count, self.hospitalResources, None)
            Global_vars.patient_count += 1
            print('current patient count=' + str(Global_vars.patient_count))

            # Add patient to dictionary of patients
            Patient.CancerPatient.all_patients[p.id] = p
            self.env.process(p.undergo_regiment())
            # Pass patient to treatment
            #treatment_regime = p.get_treatment_regime()

            #for treatment_item in treatment_regime:
            #    print(treatment_item)
            #    t_time,t_stdev,t_desc,t_resource_depend,t_type = treatment_item
            #
            #   print('regime_item_type:'+t_type+' regime desc:'+t_desc)
            #    #depend on admin,treatment,wait
            #    if (t_type == 'admin'):
            #        self.env.process(self.process_admin(p, t_time, t_desc, t_resource_depend))
            #    if (t_type == 'treatment'):
            #        self.env.process(self.process_treatment(p, t_time, t_desc, t_resource_depend))
            #    if (t_type == 'time_between_visits'):
            #        self.env.process(self.process_wait(p, t_time, t_desc, t_resource_depend))

                # Sample time for next admission
            next_admission = random.expovariate(1 / Global_vars.inter_arrival_time)
            # Schedule next admission
            yield self.env.timeout(next_admission)