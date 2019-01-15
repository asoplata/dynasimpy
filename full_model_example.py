#!/bin/env/python

from brian2 import *
# need matplotlib for plotting

import brian2.numpy_ as np
# import numpy as np

# # from https://groups.google.com/forum/#!searchin/briansupport/spike$20detection|sort:relevance/briansupport/NgRAAdPUsik/fv9UcdvGG74J
# class SingleSpikeThreshold(groups.neurongroup.Thresholder):
#     def __init__(self, threshold_value):
#         self.threshold_value = threshold_value
#
#     def __call__(self, P):
#         # This assumes that you are checking
#         # the "v" variable for threshold crossing
#         spikes = (P.v > self.threshold_value).nonzero()[0]
#         # Only keep the first (could also be a
#         # random one, etc) spike if there is more than one
#         spikes = spikes[:1]
#         return spikes

# def le_derp(threshold_value):
#     # This assumes that you are checking
#     # the "v" variable for threshold crossing
#     spikes = (P.v > threshold_value).nonzero()[0]
#     # Only keep the first (could also be a
#     # random one, etc) spike if there is more than one
#     spikes = spikes[:1]



# Compare this to ~/x012-brian2-simulation/testing/first_time/job5.py

# limitations:
#  - any unknown division is assumed be division by seconds?
#  - the "units" of state variables seem to be in time/seconds, because look at the alpha/beta functions being in Hz, EVEN THOUGH the differential equations of said state variables are unitless
#  - can't 'dv/dt +=' inside the equations-string definition, but can to the eqs-string variable outside before it's parsed (obviously)

# TODO:
#  - if big differences, look at units

# AES 20170603
# set_device('cpp_standalone')

# cells = 400
# cells = 75
cells = 15
timelength = 100*ms

Iapp_TC = 0.0*uA # /cm**2
Iapp_RE = 0.0*uA # /cm**2

gAMPA = 0.1*msiemens # /cm**2
gAMPAcort = 0.1*msiemens # /cm**2
gGABAA = 0.06*msiemens # /cm**2
gGABAA_RE = 0.06*msiemens # /cm**2
gGABAB = 0.0*msiemens # /cm**2
gAMPA_cort = 0.1*msiemens
# gAMPA = 0.08*msiemens # /cm**2
# gGABAA = 0.069*msiemens # /cm**2
# gGABAA_RE = 0.069*msiemens # /cm**2
# gGABAB = 0.001*msiemens # /cm**2

defaultclock.dt = 0.01*ms

Cm = 1*uF # /cm**2

gNa = 90*msiemens # /cm**2
ENa = 50*mV
v_shift_Na = 35*mV

gK = 10*msiemens # /cm**2
EK = -100*mV
v_shift_K = 25*mV

gT = 2*msiemens # /cm**2
v_shift_T = 2*mV
phi_hT = 3.73

gH = 0.004*msiemens # /cm**2
EH = -43*mV

gL = 0.01*msiemens # /cm**2
EL = -70*mV

gKL = 0.0172*msiemens # /cm**2
EKL = -100*mV

Na_TC_current = '-gNa*mNa**3*hNa*(v-ENa)'
K_TC_current = '-gK*nK**4*(v-EK)'
Leak_TC_current = '-gL*(v-EL)'
KLeak_TC_current = '-gKL*(v-EKL)'
H_TC_current = '-gH*(o1 + 2*(1 - c1 - o1))*(v-EH)'
T_TC_current = '-gT*ss_mT**2*hT*(v-ET)'
tonic_current_TC = '+Iapp_TC'

EGABAA = -80*mV
# tauGABAA = 5*ms
tauGABAA = 5*ms

EGABAB = -95*mV

RETC_GABAA_current = '-gGABAA/cells*sGABAAtotal*(v-EGABAA)'
# Note "gGABABtotal" is referring to the state variable, NOT the conductance
RETC_GABAB_current = '-gGABAB/cells*gGABABtotal**4/(gGABABtotal**4 + 100)*(v-EGABAB)'

EAMPA = 1*mV

# NOT normalized
CORTTC_AMPA_current = '-gAMPAcort*sAMPAcorttotal*(v-EAMPA)'

tc_eqs = "dv/dt=(" + Na_TC_current + K_TC_current + Leak_TC_current + KLeak_TC_current + H_TC_current + T_TC_current + tonic_current_TC + RETC_GABAA_current + RETC_GABAB_current + CORTTC_AMPA_current + ")/Cm : volt"

# Note "gGABABtotal" is referring to the state variable, NOT the conductance
tc_eqs += '''
sGABAAtotal : 1
gGABABtotal : 1
sAMPAcorttotal : 1
'''

tc_eqs += '''
dmNa/dt = alpha_m_Na*(1-mNa)-beta_m_Na*mNa : 1
alpha_m_Na = .32*(13-(v+v_shift_Na)/mV)/(exp((13-(v+v_shift_Na)/mV)/4.)-1)/ms : Hz
beta_m_Na =  .28*((v+v_shift_Na)/mV-40)/(exp(((v+v_shift_Na)/mV-40)/5.)-1)/ms : Hz
'''

tc_eqs += '''
dhNa/dt = alpha_h_Na*(1-hNa)-beta_h_Na*hNa : 1
alpha_h_Na = 0.128*exp((17-(v+v_shift_Na)/mV)/18.)/ms : Hz
beta_h_Na  = 4./(1+exp((40-(v+v_shift_Na)/mV)/5.))/ms : Hz
'''

tc_eqs += '''
dnK/dt = alpha_n_K*(1-nK)-beta_n_K*nK : 1
alpha_n_K = .032*(15-(v+v_shift_K)/mV)/(exp((15-(v+v_shift_K)/mV)/5)-1)/ms : Hz
beta_n_K = .5*exp((10-(v+v_shift_K)/mV)/40)/ms : Hz
'''

tc_eqs += '''
ET = 1000.*((8.31441*309.15)/(2.*96846))*log(2./Ca)*mV : volt
dhT/dt = (ss_hT - hT)/tau_hT : 1
ss_mT = 1./(1+exp((-((v+v_shift_T)/mV+57))/6.2)) : 1
ss_hT = 1./(1+exp(((v+v_shift_T)/mV+81)/4.)) : 1
tau_hT = (30.8+(211.4+exp(((v+v_shift_T)/mV+113.2)/5.))/(1+exp(((v+v_shift_T)/mV+84)/3.2)))/phi_hT*ms : second
'''

tc_eqs += 'dCa/dt = -10*-'+T_TC_current+'/(Cm*mV)/(2.*96489) + (0.00024/ms - Ca/ms)/5. : 1'

tc_eqs += '''
dc1/dt = beta_c1_H*o1 - alpha_c1_H*c1 : 1
do1/dt = 0.001/ms*(1-c1-o1) - 0.001*(p0/(0.01*ms))*o1 : 1
dp0/dt = 0.0004/ms*(1-p0) - 0.0004/ms*((Ca/(0.002*ms))**4)*p0*ms**4 : 1
alpha_c1_H = ss_hH/tau_sH : Hz
beta_c1_H = (1-ss_hH)/tau_sH : Hz
tau_sH = 20*ms + 1000./(exp((v+71.5*mV)/(14.2*mV))+exp((-(v+89*mV)/mV)/11.6))*ms : second
ss_hH = 1./(1+exp((v+75*mV)/(5.5*mV))) : 1
'''

## RE cells

gNa_RE = 200*msiemens # /cm**2
ENa_RE = 50*mV
v_shift_Na_RE = 55*mV

gK_RE = 20*msiemens # /cm**2
EK_RE = -100*mV
v_shift_K_RE = 55*mV

gT_RE = 3*msiemens # /cm**2
ET_RE = 120*mV # better model is variable based on Ca like above
v_shift_T_RE = 4*mV
phi_mT_RE = 6.81
phi_hT_RE = 3.73

gL_RE = 0.05*msiemens # /cm**2
EL_RE = -90*mV

Na_RE_current = '-gNa_RE*mNa**3*hNa*(v-ENa_RE)'
K_RE_current = '-gK_RE*nK**4*(v-EK_RE)'
Leak_RE_current = '-gL_RE*(v-EL_RE)'
T_RE_current = '-gT_RE*mT**2*hT*(v-ET_RE)'
tonic_current_RE = '+Iapp_RE'

# gAMPA = 0*msiemens # /cm**2
# EAMPA = 1*mV
tauAMPA = 2*ms
# tauAMPA = 2*ms

# TCRE_AMPA_current = '-IAMPA'
TCRE_AMPA_current = '-gAMPA/cells*sAMPAtotal*(v-EAMPA)'
RERE_GABAA_current = '-gGABAA_RE/cells*sGABAAtotal*(v-EGABAA)'

re_eqs = "dv/dt=(" + Na_RE_current + K_RE_current + Leak_RE_current + T_RE_current + tonic_current_RE + TCRE_AMPA_current + RERE_GABAA_current + ")/Cm : volt"

# Interesting, this is sort of how you initialize stuff inside the cells
re_eqs += '''
sAMPAtotal : 1
sGABAAtotal : 1
'''

re_eqs += '''
dmNa/dt = alpha_m_Na*(1-mNa)-beta_m_Na*mNa : 1
alpha_m_Na = .32*(13-(v+v_shift_Na_RE)/mV)/(exp((13-(v+v_shift_Na_RE)/mV)/4.)-1)/ms : Hz
beta_m_Na =  .28*((v+v_shift_Na_RE)/mV-40)/(exp(((v+v_shift_Na_RE)/mV-40)/5.)-1)/ms : Hz
'''

re_eqs += '''
dhNa/dt = alpha_h_Na*(1-hNa)-beta_h_Na*hNa : 1
alpha_h_Na = 0.128*exp((17-(v+v_shift_Na_RE)/mV)/18.)/ms : Hz
beta_h_Na  = 4./(1+exp((40-(v+v_shift_Na_RE)/mV)/5.))/ms : Hz
'''

re_eqs += '''
dnK/dt = alpha_n_K*(1-nK)-beta_n_K*nK : 1
alpha_n_K = .032*(15-(v+v_shift_K_RE)/mV)/(exp((15-(v+v_shift_K_RE)/mV)/5)-1)/ms : Hz
beta_n_K = .5*exp((10-(v+v_shift_K_RE)/mV)/40)/ms : Hz
'''

re_eqs += '''
dmT/dt = (ss_mT - mT)/tau_mT : 1
dhT/dt = (ss_hT - hT)/tau_hT : 1
ss_mT = 1./(1+exp((-((v+v_shift_T_RE)/mV+50))/7.4)) : 1
ss_hT = 1./(1+exp(((v+v_shift_T_RE)/mV+78)/5.)) : 1
tau_mT = (3. + (1.0/(exp(((v+v_shift_T_RE)/mV+25)/10.)+exp(-((v+v_shift_T_RE)/mV+100)/15.))))/phi_mT_RE*ms : second
tau_hT = (85 + (1.0/(exp(((v+v_shift_T_RE)/mV+46)/4. )+exp(-((v+v_shift_T_RE)/mV+405)/50.))))/phi_hT_RE*ms : second
'''

# defaultclock.dt = 0.01*ms

# prefs.codegen.target = 'numpy'
# prefs.codegen.target = 'cython'
# prefs.codegen.target = 'weave'

# prefs.codegen.cpp.compiler = '/usr/bin/gcc'
# prefs.codegen.cpp.extra_compile_args_gcc = ['-w', '-O3', '-ffast-math', '-march=native']
# AES 20170603
# prefs.codegen.cpp.extra_compile_args_gcc = ['-w', '-O3', '-ffast-math', '-march=native','-llapack', '-lblas']

# svs = 1
# svs = (75*(9*15) + 75*75*(5)) / 3



#     spikes = (P.v > threshold_value).nonzero()[0]
# tc = NeuronGroup(cells, model=tc_eqs, method='euler')
tc = NeuronGroup(cells, model=tc_eqs, threshold='v > 0*mV', refractory=1*ms, method='euler')
#tc = NeuronGroup(cells, model=tc_eqs, threshold='v > 0*mV', refractory=3*ms, method='euler')
# tc = NeuronGroup(cells, model=tc_eqs, threshold='v > 0*mV', reset='v = -50*mV', method='euler')
# tc = NeuronGroup(cells, tc_eqs, method='euler', threshold=SingleSpikeThreshold(0*mV))
# tc = NeuronGroup(int(cells), tc_eqs, method='euler', threshold='Ca <= 0', reset='Ca = 0.0000001')

# Initial conditions
tc.v = -65*mV
tc.mNa = 0.95
tc.hNa = 0.04
tc.nK =  0.1
tc.hT =  0.34
tc.Ca =  0.0001
tc.c1 =  0.5
tc.o1 =  0.
tc.p0 =  0.5
tc.sGABAAtotal = 0
tc.gGABABtotal = 0
re = NeuronGroup(cells, model=re_eqs, method='euler')
# re = NeuronGroup(cells, model=re_eqs, threshold='v > 0*mV', reset='v = -50*mV',  method='euler')
re.v = -85*mV
re.mNa = 0.95
re.hNa = 0.54
re.nK =  0.34
re.mT =  0.04
re.hT =  0.34
re.sAMPAtotal = 0.5
# re.tAMPA = 0
re.sGABAAtotal = 0


 
sAMPA=Synapses(tc,re,
               model='''ds/dt=1000.*5.*(1 + tanh(v_pre/(4.*mV)))*(1-s)/ms - (s)/(tauAMPA) : 1 (clock-driven)
                        sAMPAtotal_post = s : 1  (summed)
                     ''')
sAMPA.connect()
#
# sGABAA_RETC=Synapses(re,tc,
#                      model='''ds/dt=1000.*2.*(1 + tanh(v_pre/(4.*mV)))*(1-s)/ms - s/tauGABAA : 1 (clock-driven)
#                               sGABAAtotal_post = s : 1  (summed)
#                            ''')
# sGABAA_RETC.connect()
#
# sGABAA_RERE=Synapses(re,re,
#                      model='''ds/dt=1000.*2.*(1 + tanh(v_pre/(4.*mV)))*(1-s)/ms - s/tauGABAA : 1 (clock-driven)
#                               sGABAAtotal_post = s : 1 (summed)
#                            ''')
# sGABAA_RERE.connect()
#
# gGABAB_RETC=Synapses(re,tc,
#                      model='''dr/dt=1000.*0.5*(2.*(1 + tanh(v_pre/(4.*mV))))*(1-r)/ms - 1000*0.0012*r/ms : 1 (clock-driven)
#                               dg/dt=1000*0.18*r/ms - 1000*0.034*g/ms : 1 (clock-driven)
#                               gGABABtotal_post = g : 1  (summed)
#                            ''')
# gGABAB_RETC.connect()



# corttc = PoissonGroup(cells, np.arange(cells)*Hz)
# sAMPA=Synapses(corttc, tc,
#                model='''ds/dt=1000.*5.*(1 + tanh(v_pre/(4.*mV)))*(1-s) - (s)/(tauAMPA) : 1 (clock-driven)
#                         sAMPAcorttotal_post = s : 1  (summed)
#                      ''')
# sAMPA.connect()



#  neurons = NeuronGroup(1, model="""dv/dt=(gtot-v)/(10*ms) : 1
#                                    gtot : 1""")
#  S=Synapses(input,neurons,
#             model='''dg/dt=-a*g+b*x*(1-g) : 1
#                      gtot_post = g : 1  (summed)
#                      dx/dt=-c*x : 1
#                      w : 1 # synaptic weight
#                   ''',
#             pre='x+=w')


tc_data = StateMonitor(tc, 'v', record=True)
re_data = StateMonitor(re, 'v', record=True)

# syn_data_r0 = StateMonitor(sAMPA, 'r0', record=True)
# syn_data_r1 = StateMonitor(sAMPA, 'r1', record=True)

syn_data2 = StateMonitor(re, 'sAMPAtotal', record=True)

syn_data3= StateMonitor(sAMPA, 'sAMPAtotal', record=True)

# syn_data = StateMonitor(re, 'sGABAAtotal', record=True)
# syn_data = StateMonitor(tc, 'sGABAAtotal', record=True)
# syn_data = StateMonitor(tc, 'gGABABtotal', record=True)

spikes = SpikeMonitor(tc)

# From http://brian2.readthedocs.io/en/2.0.1/user/running.html
# a simple run would not include the monitors
net = Network(collect())  # automatically include G and S
# net.add(tc_data, re_data, syn_data_r0, syn_data_r1, 
#         syn_data2, syn_data3, spikes)  # manually add the monitors

net.add(tc_data, re_data, syn_data2, syn_data3, spikes)  # manually add the monitors

# net.run(10*ms)
# AES 20170603
run(timelength, report='text')
# run(8000*ms, report='text')

# Got an error with v2.0rc1 that, if using "set_device" like above, shouldn't
#   ALSO use "device.build" unless also setting "build_on_run=False"
# device.build(directory='output', compile=True, run=True, debug=False)

# print("Saving TC cell voltages!")
# numpy.savetxt("foo_tc.csv", tc_data.v/mV, delimiter=",")
# print("Done saving TC cell voltages.")
# print("Saving RE cell voltages!")
# numpy.savetxt("foo_re.csv", re_data.v/mV, delimiter=",")
# print("Done saving RE cell voltages.")
# print("Saving synapse activities!")
# numpy.savetxt("foo_syn.csv", syn_data.sAMPAtotal, delimiter=",")
# print("Done saving synapse activities.")

figure()
plot(tc_data.t/ms, tc_data[0].v/mV)
# plot(tc_data.t/ms, tc_data[1].v/mV)
# plot(tc_data.t/ms, tc_data[2].v/mV)
# plot(tc_data.t/ms, tc_data[3].v/mV)
# plot(tc_data.t/ms, tc_data[4].v/mV)
# plot(tc_data.t/ms, tc_data[5].v/mV)
# plot(tc_data.t/ms, tc_data[6].v/mV)
# plot(tc_data.t/ms, tc_data[7].v/mV)
# plot(tc_data.t/ms, tc_data[8].v/mV)
# plot(tc_data.t/ms, tc_data[9].v/mV)

plot(re_data.t/ms, re_data[0].v/mV)
# plot(re_data.t/ms, re_data[1].v/mV)
# plot(re_data.t/ms, re_data[2].v/mV)
# plot(re_data.t/ms, re_data[3].v/mV)
# plot(re_data.t/ms, re_data[4].v/mV)

plot(spikes.t/ms, spikes.i, '.')



plot(syn_data2.t/ms, syn_data2[0].sAMPAtotal)

figure()
# plot(syn_data_r0.t/ms, syn_data_r0[0].r0)
# plot(syn_data_r1.t/ms, syn_data_r1[0].r1)
# # plot(syn_data.t/ms, syn_data[0].sGABAAtotal)
# plot(syn_data.t/ms, syn_data[0].gGABABtotal)


# def visualise_connectivity(S):
#     Ns = len(S.source)
#     Nt = len(S.target)
#     figure(figsize=(10, 4))
#     subplot(121)
#     plot(zeros(Ns), arange(Ns), 'ok', ms=10)
#     plot(ones(Nt), arange(Nt), 'ok', ms=10)
#     for i, j in zip(S.i, S.j):
#         plot([0, 1], [i, j], '-k')
#     xticks([0, 1], ['Source', 'Target'])
#     ylabel('Neuron index')
#     xlim(-0.1, 1.1)
#     ylim(-1, max(Ns, Nt))
#     subplot(122)
#     plot(S.i, S.j, 'ok')
#     xlim(-1, Ns)
#     ylim(-1, Nt)
#     xlabel('Source neuron index')
#     ylabel('Target neuron index')
# 
# visualise_connectivity(sAMPA)



show()

# exit()
