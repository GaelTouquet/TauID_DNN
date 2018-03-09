from ROOT import TFile
import numpy as np
from root_numpy import tree2array



def root_to_numpy(root_file_name, numpy_file_name, list_of_branch_names, isSignal=False):
    f = TFile('../samples_root/'+root_file_name+'.root')
    tree = f.Get('tree')
    array = tree2array(tree,
                       branches=list_of_branch_names,
                       condition='isSignal > 0.5' if isSignal else '')
    array = array.view(np.float64).reshape(array.shape + (-1,))
    np.save('../samples_numpy/'+numpy_file_name, array)


list_of_branches_names = []
list_of_branches_names_justjet = []

list_of_branches_names_justjet.extend(['Jet_'+x for x in ['pt','eta','phi','charge','mass','nconstituents']])

list_of_branches_names_justjet.append('isSignal')

#list_of_branches_names.extend(['GenJet_'+x for x in ['pt','eta','phi','charge','mass','nconstituents']])
#list_of_branches_names.extend(['Jet_'+x for x in ['pt','eta','phi','charge','mass','nconstituents']])

for i in xrange(200):
    list_of_branches_names.extend(['ptc_'+str(i)+'_'+x for x in ['pt','eta','phi','charge','mass','pdgid','dxy','dz']])
#    list_of_branches_names.extend(['GenJet_ptc_'+str(i)+'_'+x for x in ['pt','eta','phi','charge','mass','pdgid']]) 
#    
    
list_of_branches_names.append('nPU')
    
# list_of_branches_names.append('run')
# list_of_branches_names.append('lumi')
# list_of_branches_names.append('event')
    
list_of_branches_names.append('isSignal')


background_samples = ['QCD']

signal_samples = ['GGH500']

for name in signal_samples:
    root_to_numpy(name,name,list_of_branches_names,isSignal=True)
    root_to_numpy(name,name+'_justJet',list_of_branches_names_justjet,isSignal=True)
    
for name in background_samples:
    root_to_numpy(name,name,list_of_branches_names,isSignal=False)
    root_to_numpy(name,name+'_justJet',list_of_branches_names_justjet,isSignal=False)