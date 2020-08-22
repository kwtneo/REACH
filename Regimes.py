
def Breast_Adjuvant_Regimes(breast_adj_blood_test1_probability_gen,
                            breast_adj_blood_test2_probability_gen,
                            breast_adj_blood_test_atu_ac_probability_gen,
                            breast_dox_cyclophos_adr_probability_gen,
                            breast_adj_blood_test_atu_t_probability_gen,
                            breast_paclitax_adr_probability_gen,
                            ):
    regimes = ['1st psa registration time','generic waiting time','dmo 1st consultation','psa payment','psa scheduling',]
    if (breast_adj_blood_test1_probability_gen):
        regimes.append('1st blood test');
    regimes.append('time between visit');regimes.append('2nd psa registration')
    if (breast_adj_blood_test2_probability_gen):
        regimes.append('2nd blood test');regimes.append('generic waiting time');regimes.append('dmo 2nd consultation');regimes.append('psa payment')
    regimes.append('psa scheduling');regimes.append('3rd psa registration');regimes.append('IV start - ATU (AC)')
    regimes.append('IV Chemo Infusion - ATU (AC)');regimes.append('breast facility')
    if (breast_adj_blood_test_atu_ac_probability_gen):
        regimes.append('ATU (AC) blood test');regimes.append('ATU (AC) blood test review');regimes.append('ATU (AC) blood test screening')
    regimes.append('ATU (AC) premedication');regimes.append('ATU (AC) Doxorubicin, Cyclophosphamide')
    if(breast_dox_cyclophos_adr_probability_gen):
        regimes.append('ATU (AC) Doxorubicin, Cyclophosphamide ADR')
    regimes.append('ATU (AC) post chemo pharmacy');regimes.append('time between visit')
    regimes.append('4th psa registration'),regimes.append('IV start - ATU (T)');regimes.append('IV Chemo Infusion - ATU (T)');regimes.append('breast facility')
    if (breast_adj_blood_test_atu_t_probability_gen):
        regimes.append('ATU (T) blood test');regimes.append('ATU (T) blood test review');regimes.append('ATU (T) blood test screening')
    regimes.append('ATU (T) premedication');regimes.append('ATU (T) paclitaxel')
    if(breast_paclitax_adr_probability_gen):
        regimes.append('ATU (T) paclitaxel ADR')
    regimes.append('ATU (T) post chemo pharmacy')
    return regimes