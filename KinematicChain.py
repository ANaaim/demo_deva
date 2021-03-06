# -*- coding: utf-8 -*-
import r2mobile
from homogenous2rotation import homogenous2rotation as homogenous2rotation
from Joint import Joint as Joint
import numpy as np
import r2mobile

class KinematicChain:

    def __init__(self, list_segment, phi_ext,
                 name_joint, name_rotation,
                 pos_moment_calculation, frame_moment_calculation,
                 moment_projection='JCS'):
        
        dictionnary_rotation = {'zyx': r2mobile.zyx,
                                'zxy':r2mobile.zxy,
                                'xzy':r2mobile.xzy,
                                'xzy':r2mobile.xzy}
        
        # Initialisation phi_joints, force and moment
        phi_joints = dict()
        force = dict()
        moment = dict()
        name_segment = list()

        for ind_seg, value_segments in enumerate(list_segment):
            name_segment.append(value_segments.segment_name)

        # Calcul mouvement global des list_segment
        euler_glob = dict()

        # Calcul position absolue
        for i in range(len(name_joint)+1):
            euler_glob[name_segment[i]] = np.rad2deg(
                r2mobile.zxy(list_segment[i].Tprox.T_homo))
        # calcul du mouvement relatif
        homo_segment_rel = dict()
        euler_rel = dict()

        for i in range(len(name_joint)):
            homo_segment_rel[name_joint[i]] = homogenous2rotation(
                list_segment[i+1].Tdist, list_segment[i].Tprox)
            euler_rel[name_joint[i]] = np.rad2deg(
                dictionnary_rotation[name_rotation[i]](homo_segment_rel[name_joint[i]].T_homo))

        # Calcul kinetic
        for ind_joint in range(len(name_joint)):
            if ind_joint == 0:
                phi_joints[name_joint[ind_joint]] = Joint(list_segment[ind_joint],
                                                          phi_ext[ind_joint], 200, 6)
            else:
                phi_temp = phi_joints[name_joint[ind_joint-1]].phi_prox_origin + \
                    phi_ext[ind_joint]

                phi_joints[name_joint[ind_joint]] = Joint(
                    list_segment[ind_joint], phi_temp, 200, 6)
        if moment_projection == 'JCS':
            for ind_joint in range(len(name_joint)):
                force[name_joint[ind_joint]], moment[name_joint[ind_joint]] = \
                    phi_joints[name_joint[ind_joint]].projection_JCS(pos_moment_calculation[ind_joint].T_homo[0:3, 3, :],
                                                                     list_segment[ind_joint], list_segment[ind_joint+1], name_rotation[ind_joint])
        else:
            for ind_joint in range(len(name_joint)):
                force[name_joint[ind_joint]], moment[name_joint[ind_joint]] = \
                    phi_joints[name_joint[ind_joint]].get_force_moment(
                    pos_moment_calculation[ind_joint], frame_moment_calculation[ind_joint])

        self.euler_glob = euler_glob
        self.euler_rel = euler_rel
        self.moment = moment
        self.force = force
