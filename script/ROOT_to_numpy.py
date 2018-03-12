from ROOT import TFile
import numpy as np
from root_numpy import tree2array

class Image_ptcs(object):
    """Creates and holds a binned map (= numpy array)
    in the (eta,phi) plane of the chosen attribute 
    of given set of particles
    """
    
    def __init__(self, n_pixel_eta, n_pixel_phi,
                 pdgid=0, z='e', ptcs_from=origin):
        self.n_pixel_eta = n_pixel_eta
        self.n_pixel_phi = n_pixel_phi
        self.pdgid = pdgid
        self.z = z
        self.build(origin)
            
    def build(self, origin):
        self.build_from_tree(origin)
            
    def build_from_tree(self, tree):
        list_of_branches_names = ['ptc_{n}_{val}']# use combination for number and var, handle gen?
        self.origin_array = tree2array(tree, branches = list_of_branches_names)
        self.images = []
        for i in len(self.origin_array[0]):#length of njet?
            image = [] # turn that ingto numpy array of size n_pixx npixy
            for ptc in ptcs:
                if ptc.whatev == -99 :
                    continue
                else:
                       image[findbin(ptc.eta),findbin(ptc.phi)] += ptc.(self.z)
            self.images.append(image)
        self.images = np.array(self.images) #to be checked too

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