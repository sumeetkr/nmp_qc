#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    utils.py: Functions to process dataset graphs.

    Usage:

"""

from __future__ import print_function

import networkx as nx
import rdkit

__author__ = "Pau Riba, Anjan Dutta"
__email__ = "priba@cvc.uab.cat, adutta@cvc.uab.cat"


def qm9_nodes(g, hydrogen=False):
    h = {}
    for n, d in g.nodes_iter(data=True):
        h_t = []
        # Atom type (One-hot H, C, N, O F)
        h_t += [int(d['a_type'] == x) for x in ['H', 'C', 'N', 'O', 'F']]
        # Atomic number
        h_t.append(d['a_num'])
        # Partial Charge
        h_t.append(d['pc'])
        # Acceptor
        h_t.append(d['acceptor'])
        # Donor
        h_t.append(d['donor'])
        # Aromatic
        h_t.append(int(d['aromatic']))
        # Hybradization
        h_t += [int(d['hybridization'] == x) for x in [rdkit.Chem.rdchem.HybridizationType.SP, rdkit.Chem.rdchem.HybridizationType.SP2, rdkit.Chem.rdchem.HybridizationType.SP3]]
        # If number hydrogen is used as a
        if hydrogen:
            h_t.append(d['num_h'])
        h[n] = h_t
    return h


def qm9_edges(g, e_representation='chem_graph'):
    e={}
    for n1, n2, d in g.edges_iter(data=True):
        e_t = []
        # Raw distance function
        if e_representation == 'chem_graph':
            if d['b_type'] is None:
                g.remove_edge(n1, n2)
            else:
                e_t += [i+1 for i, x in enumerate([rdkit.Chem.rdchem.BondType.SINGLE, rdkit.Chem.rdchem.BondType.DOUBLE,
                                                rdkit.Chem.rdchem.BondType.TRIPLE, rdkit.Chem.rdchem.BondType.AROMATIC])
                        if x == d['b_type']]
        elif e_representation == 'distance_bin':
            if d['b_type'] is None:

                step = 0.5
                start = 2
                b = 9
                for i in range(0, 9):
                    if d['distance']<(start+i*step):
                        b = i
                        break
                e_t.append(b+5)
            else:
                e_t += [i+1 for i, x in enumerate([rdkit.Chem.rdchem.BondType.SINGLE, rdkit.Chem.rdchem.BondType.DOUBLE,
                                                   rdkit.Chem.rdchem.BondType.TRIPLE, rdkit.Chem.rdchem.BondType.AROMATIC])
                        if x == d['b_type']]
        elif e_representation == 'raw_distance':
            if d['b_type'] is None:
                g.remove_edge(n1, n2)
            else:
                e_t.append(d['distance'])
                e_t += [int(d['b_type'] == x) for x in [rdkit.Chem.rdchem.BondType.SINGLE, rdkit.Chem.rdchem.BondType.DOUBLE,
                                                        rdkit.Chem.rdchem.BondType.TRIPLE, rdkit.Chem.rdchem.BondType.AROMATIC]]
        else:
            print('Incorrect Edge representation transform')
            quit()
        if e_t:
            e[(n1, n2)] = e_t
    return g, e