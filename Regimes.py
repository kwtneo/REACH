
def Breast_Adjuvant_Regimes(breast_adj_blood_test1_probability_gen,
                            breast_adj_blood_test2_probability_gen,
                            breast_adj_blood_test_atu_ac_probability_gen,
                            breast_dox_cyclophos_adr_probability_gen,
                            breast_adj_blood_test_atu_t_probability_gen,
                            breast_paclitaxel_adr_probability_gen,
                            ):
    adrs=False
    regimes = []
    time_between = []
    time_between.append('time between visit')
    clinic1=['1st psa registration time','generic waiting time','dmo 1st consultation','psa payment','psa scheduling',]
    clinic1 = ['1st psa registration time', 'dmo 1st consultation', 'psa payment',
               'psa scheduling', ]
    if (next(breast_adj_blood_test1_probability_gen)):
        clinic1.append('1st blood test');

    #regimes.append('time between visit');
    clinic2=[]
    clinic2.append('2nd psa registration')
    #if (next(breast_adj_blood_test2_probability_gen)):
    #    clinic2.append('2nd blood test');clinic2.append('generic waiting time');clinic2.append('dmo 2nd consultation');clinic2.append('psa payment')
    if (next(breast_adj_blood_test2_probability_gen)):
        clinic2.append('2nd blood test');clinic2.append('dmo 2nd consultation');clinic2.append('psa payment')

    clinic2.append('psa scheduling');

    ac_cycle=[]
    ac_cycle.append('3rd psa registration');ac_cycle.append('IV start - ATU (AC)')
    ac_cycle.append('IV Chemo Infusion - ATU (AC)');ac_cycle.append('breast facility')
    if (next(breast_adj_blood_test_atu_ac_probability_gen)):
        ac_cycle.append('ATU (AC) blood test');ac_cycle.append('ATU (AC) blood test review');ac_cycle.append('ATU (AC) blood test screening')
    ac_cycle.append('ATU (AC) premedication');ac_cycle.append('ATU (AC) Doxorubicin, Cyclophosphamide')
    if(next(breast_dox_cyclophos_adr_probability_gen)):
        ac_cycle.append('ATU (AC) Doxorubicin, Cyclophosphamide ADR')
    ac_cycle.append('ATU (AC) post chemo pharmacy');
    #ac_cycle.append('time between visit')


    t_cycle=[]
    t_cycle.append('4th psa registration'),t_cycle.append('IV start - ATU (T)');t_cycle.append('IV Chemo Infusion - ATU (T)');
    t_cycle.append('breast facility')
    if (next(breast_adj_blood_test_atu_t_probability_gen)):
        t_cycle.append('ATU (T) blood test');t_cycle.append('ATU (T) blood test review');t_cycle.append('ATU (T) blood test screening')
    t_cycle.append('ATU (T) premedication');t_cycle.append('ATU (T) paclitaxel')
    #print(breast_paclitax_adr_probability_gen)
    if(next(breast_paclitaxel_adr_probability_gen)):
        t_cycle.append('ATU (T) paclitaxel ADR')
        adrs=True
        print('Patient will have ADR reaction')
    else:
        print('Patient will NOT have ADR reaction')
    t_cycle.append('ATU (T) post chemo pharmacy')

    regimes = clinic1 + time_between + ac_cycle + time_between + clinic2 + time_between + ac_cycle\
              + time_between + clinic2 + time_between + ac_cycle + time_between + clinic2 + time_between\
              + ac_cycle + time_between + clinic2 + time_between + t_cycle + time_between + clinic2 \
              + time_between + t_cycle + time_between + clinic2 + time_between + t_cycle + time_between\
              + clinic2 + time_between + t_cycle + time_between + clinic2

    return regimes


def Breast_Metastatic_Regimes(main_drug='docetaxel',
                              breast_met_blood_test1_probability_gen=None,
                              breast_met_blood_test2_probability_gen=None,
                              breast_met_blood_test_atu_probability_gen=None,
                              breast_met_adr_probability_gen=None
                              ):
    regimes = []
    time_between = []
    time_between.append('time between visit')
    #clinic1=['1st psa registration time','generic waiting time','dmo 1st consultation','psa payment','psa scheduling',]
    clinic1 = ['1st psa registration time', 'dmo 1st consultation', 'psa payment',
               'psa scheduling', ]
    if (next(breast_met_blood_test1_probability_gen)):
        clinic1.append('1st blood test');

    clinic2=[]
    clinic2.append('2nd psa registration')
    #if (next(breast_met_blood_test2_probability_gen)):
    #    clinic2.append('2nd blood test');clinic2.append('generic waiting time');clinic2.append('dmo 2nd consultation');
    #    clinic2.append('psa payment')
    if (next(breast_met_blood_test2_probability_gen)):
        clinic2.append('2nd blood test');clinic2.append('dmo 2nd consultation');
        clinic2.append('psa payment')

    clinic2.append('psa scheduling');


    if(main_drug.lower()=='docetaxel'):
        at_cycle = []
        at_cycle.append('3rd psa registration');
        at_cycle.append('IV start - ATU')
        at_cycle.append('IV Chemo Infusion - ATU');
        at_cycle.append('breast facility')

        if (next(breast_met_blood_test_atu_probability_gen)):
            at_cycle.append('ATU blood test');
            at_cycle.append('ATU blood test review');
            at_cycle.append('ATU blood test screening')
        at_cycle.append('ATU premedication');

        at_cycle.append('ATU Docetaxel')
        if(next(breast_met_adr_probability_gen)):
            at_cycle.append('ATU Docetaxel ADR')
        at_cycle.append('ATU post chemo pharmacy');
        regimes = clinic1 + time_between + at_cycle + time_between\
                  + clinic2  + time_between + at_cycle + time_between + clinic2

    elif(main_drug.lower()=='paclitaxel'):
        at_cycle = []
        at_cycle.append('3rd psa registration');
        at_cycle.append('IV start - ATU')
        at_cycle.append('IV Chemo Infusion - ATU');
        at_cycle.append('breast facility')

        if (next(breast_met_blood_test_atu_probability_gen)):
            at_cycle.append('ATU blood test');
            at_cycle.append('ATU blood test review');
            at_cycle.append('ATU blood test screening')
        at_cycle.append('ATU premedication');

        at_cycle.append('ATU Paclitaxel')
        if(next(breast_met_adr_probability_gen)):
            at_cycle.append('ATU Paclitaxel ADR')
        at_cycle.append('ATU post chemo pharmacy');
        regimes = clinic1 + time_between + at_cycle + time_between\
                  + clinic2  + time_between + at_cycle + time_between + clinic2


    elif(main_drug.lower()=='capecitabine'):
        at_cycle = []
        at_cycle.append('ATU capecitabine')
        #at_cycle.append('ATU post chemo pharmacy');
        regimes = clinic1 + time_between + at_cycle + time_between\
                  + clinic2 + at_cycle + time_between + clinic2


    return regimes

