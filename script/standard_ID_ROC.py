#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 06:17:06 2018

@author: gtouquet
"""

from ROOT import TFile
import numpy as np

#QCD_file = TFile('samples_root/QCD_tree.root')
#QCD_tree = QCD_file.Get('tree')

Signal_file = TFile('$TAUIDDNN/samples_root/GGH500.root')
Signal_tree = Signal_file.Get('tree')

trees = [Signal_tree] # add trees here

working_points = ['byTightIsolationMVArun2v1DBoldDMwLT', 
                  'byVTightIsolationMVArun2v1DBoldDMwLT',
                  'byMediumIsolationMVArun2v1DBoldDMwLT',
                  'byLooseIsolationMVArun2v1DBoldDMwLT',
                  'byVLooseIsolationMVArun2v1DBoldDMwLT']

tauID_cond = ' && '.join(['decayModeFinding > 0.5',
                          'againstElectronVLooseMVA6 >0.5',
                          'againstMuonLoose3 > 0.5',
                          'abs(Tau_leadChargedHadrCand_dz) < 0.2'])

results = {'n_goodID_jet':{},
           'n_badID_jet':{},
           'n_goodID_tau':{},
           'n_badID_tau':{}}

for wp in working_points:
    for result in results:
        results[result][wp] = 0

for tree in trees:
    for wp in working_points:
        results['n_goodID_tau'][wp] += tree.GetEntries(tauID_cond+' && {wp} >0.5'.format(wp=wp)+' && isSignal == 1')
        results['n_badID_tau'][wp] += tree.GetEntries('isSignal == 1') - results['n_goodID_tau'][wp]
        results['n_badID_jet'][wp] += tree.GetEntries(tauID_cond+' && {wp} >0.5'.format(wp=wp)+' && isSignal == 0')
        results['n_goodID_jet'][wp] += tree.GetEntries('isSignal == 0') - results['n_badID_jet'][wp]
        
points = []

for wp in working_points:
    tauID_eff = float(results['n_goodID_tau'][wp]) / ( results['n_goodID_tau'][wp] + results['n_badID_tau'][wp] )
    misID_prob = float(results['n_badID_jet'][wp]) / ( results['n_badID_jet'][wp] + results['n_goodID_jet'][wp] )
    points.append([tauID_eff,misID_prob])
    
points = np.array(points)

np.save('$TAUIDDNN/samples_numpy/standardID',points)


#def is_rec_Tau(jet, WP):
#    decayModeFinding = jet.decayModeFinding > 0.5
#    against_electron = jet.againstElectronVLooseMVA6 >0.5
#    against_muon = jet.againstMuonLoose3 > 0.5
#    tau_dz = abs(jet.Tau_leadChargedHadrCand_dz) < 0.2 
#    iso = getattr(jet, WP) > 0.5
#    is_rec_tau = decayModeFinding and against_electron and against_muon and tau_dz and iso
#    return is_rec_tau
#
#njets_tot = 0
#for tree in trees:
#    njets_tot += tree.GetEntries()
#
#ijet = 0
#for tree in trees:
#    for jet in tree:
#        
#        if jet.isSignal:
#            for wp in working_points:
#                if is_rec_Tau(jet,wp):
#                    working_points[wp][2] += 1 # n_goodID_tau
#                else:
#                    working_points[wp][3] += 1 # n_badID_tau
#        else:
#            for wp in working_points:
#                if is_rec_Tau(jet,wp):
#                    working_points[wp][1] += 1 # n_badID_jet
#                else:
#                    working_points[wp][0] += 1 # n_goodID_jet
#
