#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 13:29:53 2018

@author: gtouquet
"""
import numpy as np
from ROOT import TFile, TGraph, TCanvas, TLegend, TH1F
from array import array

class ROCcurve(object):
    """Allows to easily draw ROC curves for given data:
        
        nn_output : 1 * n sized array of network predictions
        wanted_output : 1* n sized array of wanted output
    """
    
    def __init__(self, nn_output, wanted_output,
                 signal_value=1., background_value=0.,
                 npoints=100, save=None, verbose=False):
        self.nn_output = nn_output
        self.wanted_output = wanted_output
        self.signal_value = signal_value
        self.background_value = background_value
        self.npoints = npoints
        self.verbose = verbose
        self.WPs = []
        self.make()
        if save:
            self.draw(display=False,standard=True)
            self.save(save)
        
    def make(self):
        if self.verbose:
            j = 0
        for i in np.linspace(self.background_value,
                             self.signal_value,
                             self.npoints):
            if self.verbose:
                j+=1
                print 'event:',j,'/',self.npoints
            self.test_working_point(i)
            
    def test_working_point(self, working_point, addWP=True):
        n_goodID_signal = 0
        n_goodID_background = 0
        n_badID_signal = 0
        n_badID_background = 0
        for i in xrange(len(self.nn_output)):
            if self.nn_output[i]>working_point:
                if self.wanted_output[i]==self.signal_value:
                    n_goodID_signal+=1
                else:
                    n_badID_background+=1
            else:
                if self.wanted_output[i]==self.background_value:
                    n_goodID_background+=1
                else:
                    n_badID_signal+=1
        signalID_rate = float(n_goodID_signal) / (n_goodID_signal + n_badID_signal)
        backgroundID_rate = float(n_goodID_background) / (n_goodID_background + n_badID_background)
        if addWP:
            self.WPs.append([signalID_rate,backgroundID_rate])
        return [signalID_rate,backgroundID_rate]
    
    def draw(self, display=False, same=False, standard=False):
        self.graph = TGraph(self.npoints,
                            array('d',[1.-x[1] for x in self.WPs]),
                            array('d',[x[0] for x in self.WPs]))
        self.graph.SetLineColor(4)
        self.graph.SetMarkerColor(4)
        self.graph.SetMarkerStyle(20)
        self.graph.SetTitle('Tau ID ROC curve')
        self.graph.SetName('graph')
        self.graph.GetYaxis().SetTitle('#tau_h ID efficiency')
        self.graph.GetXaxis().SetTitle('mis-ID probability')
        if standard: # add DNN naming scheme
            self.std_graph = TGraph(5,
                                    array('d',[0.00631245,0.00774533,0.00948803,0.01123073,0.01386415]),
                                    array('d',[0.31189653,0.36518059,0.4134581,0.45964954,0.50363571]))
            self.std_graph.SetName('std_graph')
            self.std_graph.SetLineColor(2)
            self.std_graph.SetMarkerColor(2)
            self.std_graph.SetMarkerStyle(21)
        if display:
            if same:
                self.graph.Draw('same')
            else:
                self.backhist = TH1F('backhist','Tau ID ROC curve',1,0.,0.05)
                self.backhist.GetYaxis().SetTitle('#tau_{h} ID efficiency')
                self.backhist.GetXaxis().SetTitle('mis-ID probability')
                self.backhist.GetYaxis().SetRangeUser(0.,1.1)
                self.backhist.SetStats(0)
                self.legend = TLegend(0.6,0.7,0.9,0.9)
                self.legend.AddEntry(self.graph,'my DNN','p')
                self.canvas = TCanvas()
                self.backhist.Draw()
                self.graph.Draw('same p')
                if standard:
                    self.legend.AddEntry(self.std_graph,'standard ID','p')
                    self.std_graph.Draw('same p')
                self.legend.Draw()
                
                
    def save(self, name):
        self.file = TFile('../outputs/'+name+'.root','recreate')
        self.graph.Write()
        self.std_graph.Write()
        if hasattr(self, 'canvas'):
            self.canvas.SaveAs('../outputs/'+name+'.pdf')