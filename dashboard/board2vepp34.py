#!/usr/bin/env python3

from cxwidgets.aQt.QtWidgets import QLabel, QApplication
from cxwidgets.aQt.QtCore import Qt
from cxwidgets.aQt import QtGui

from cxwidgets import CXSwitch, CXSpinBox, CXPushButton, CXEventLed, CXTextComboBox, CXLineEdit, CXProgressBar,\
    HLine, BaseGridW, CXIntComboBox, CXIntLabel, CXStateLed

from acc_ctl.mode_defs import mode_colors
import os.path as op

script_path = op.dirname(op.realpath(__file__))

ctrl_srv = 'cxout:0'


class InjExtCtl(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        grid = self.grid
        grid.addWidget(QLabel("Injection complex info"), 0, 0, 1, 4, Qt.AlignHCenter)

        grid.addWidget(QLabel("linac run-mode"), 1, 0, 1, 1, Qt.AlignRight)
        self.linac_mode_cb = CXIntComboBox(cname='canhw:19.syn_ie4.mode', values={0: 'continuous', 1: 'counter'})
        grid.addWidget(self.linac_mode_cb, 1, 1)

        grid.addWidget(QLabel("beam switch"), 2, 0, 1, 1, Qt.AlignRight)

        # turning magnet control
        grid.addWidget(QLabel("beam dump state"), 3, 0, 1, 1, Qt.AlignRight)
        self.linac_dump_state = CXIntLabel(cname=f'{ctrl_srv}.rotmag.cur_direction',
                                           values={2: '->Dump', 1: '->Ring', 3: 'between'},
                                           colors={2: '#FF0000', 1: '#00FF00', 3: '#FFFF00'})
        grid.addWidget(self.linac_dump_state, 3, 1)

        grid.addWidget(QLabel("e-shots"), 4, 0, 1, 1, Qt.AlignRight)
        self.sb_eshots = CXSpinBox(cname=f'{ctrl_srv}.ddm.eshots')
        grid.addWidget(self.sb_eshots, 4, 1)

        grid.addWidget(QLabel("p-shots"), 4, 2, 1, 1, Qt.AlignRight)
        self.sb_eshots = CXSpinBox(cname=f'{ctrl_srv}.ddm.pshots')
        grid.addWidget(self.sb_eshots, 4, 3)

        grid.addWidget(QLabel("weapon"), 5, 0, 1, 1, Qt.AlignRight)
        self.cb_particles = CXTextComboBox(cname=f'{ctrl_srv}.ddm.particles', values=['e', 'p'],
                                           icons=[script_path + '/img/electron.png', script_path + '/img/positron.png'])
        grid.addWidget(self.cb_particles, 5, 1)


class InjExtState(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("shots left"), 1, 0)
        self.sb_nshots = CXSpinBox(cname=f'{ctrl_srv}.ddm.shots_left')
        self.grid.addWidget(self.sb_nshots, 1, 1)

        self.grid.addWidget(QLabel("injected"), 1, 2, Qt.AlignRight)
        self.inj_led = CXEventLed(cname=f'{ctrl_srv}.ddm.injected')
        self.grid.addWidget(self.inj_led, 1, 3, Qt.AlignLeft)

        self.grid.addWidget(QLabel("extracted"), 2, 2, Qt.AlignRight)
        self.ext_led = CXEventLed(cname=f'{ctrl_srv}.ddm.extracted')
        self.grid.addWidget(self.ext_led, 2, 3, Qt.AlignLeft)

        self.grid.addWidget(QLabel("state"), 3, 0)
        self.state_line = CXLineEdit(cname=f'{ctrl_srv}.ddm.state', readonly=True, max_len=100)
        self.grid.addWidget(self.state_line, 3, 1)

        self.grid.addWidget(QLabel("runmode"), 4, 0)
        self.runmode_line = CXLineEdit(cname=f'{ctrl_srv}.ddm.icrunmode', readonly=True, max_len=100)
        self.grid.addWidget(self.runmode_line, 4, 1)


class K500State(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("K500 mode"), 0, 0, 1, 4, Qt.AlignHCenter)

        self.grid.addWidget(QLabel("mode"), 1, 0)
        vals = ['e2v2', 'p2v2', 'e2v4', 'p2v4']
        self.cb_particles = CXTextComboBox(cname=f'{ctrl_srv}.k500.modet', values=vals,
                                           colors=[mode_colors[x] for x in vals])
        self.grid.addWidget(self.cb_particles, 1, 1)


class PUSwitch(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("Particles&users switching"), 0, 0, 1, 2, Qt.AlignHCenter)

        self.sw_progress = CXProgressBar(cname=f'{ctrl_srv}.k500.mode_progress')
        self.grid.addWidget(self.sw_progress, 1, 0, 1, 2)

        self.grid.addWidget(QLabel("allow vepp2k automatics"), 2, 0)
        self.auto_v2k_led = CXStateLed(cname=f'{ctrl_srv}.ddm.v2k_auto')
        self.auto_v2k_led.setDiameter(50)
        self.grid.addWidget(self.auto_v2k_led, 2, 1)

        self.grid.addWidget(QLabel("allow vepp3/4 automatics"), 3, 0)
        self.auto_v4_led = CXStateLed(cname=f'{ctrl_srv}.ddm.vepp4_auto')
        self.auto_v4_led.setDiameter(50)
        self.grid.addWidget(self.auto_v4_led, 3, 1)


class BeamUserRequest(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(QLabel("Beg for mercy\n(no beam)"), 0, 0)
        self.grid.addWidget(CXSwitch(cname=f'{ctrl_srv}.vepp4_bu.ask_no_beam'), 0, 1)


class DDMWidget(BaseGridW):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.grid.addWidget(HLine(), 1, 0)
        self.inj_ext = InjExtCtl()
        self.grid.addWidget(self.inj_ext, 2, 0)

        self.grid.addWidget(HLine(), 3, 0)
        self.inj_ext_st = InjExtState()
        self.grid.addWidget(self.inj_ext_st, 4, 0)

        self.grid.addWidget(HLine(), 5, 0)

        self.k500_st = K500State()
        self.grid.addWidget(self.k500_st, 6, 0)

        self.grid.addWidget(HLine(), 7, 0)

        self.pu_sw = PUSwitch()
        self.grid.addWidget(self.pu_sw, 8, 0)

        self.grid.addWidget(HLine(), 9, 0)

        self.grid.addWidget(BeamUserRequest(), 10, 0)


app = QApplication(['Particle beam attack warning'])

w = DDMWidget()
w.show()

app.exec_()
