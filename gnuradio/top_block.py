#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed Sep 18 16:39:58 2019
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.symbol_dur = symbol_dur = 0.000505
        self.samp_rate = samp_rate = 2e6
        self.radio_freq = radio_freq = 303.8e6

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate,
        	v_scale=.2,
        	v_offset=.5,
        	t_scale=0.005,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_NORM,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(radio_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(0, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('/media/psf/Home/Desktop/fpgen.wav', 1, 2000000, 8)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_c([0,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0], True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.1, .11, 0)
        self.blocks_repeat_0_3 = blocks.repeat(gr.sizeof_gr_complex*1, int(samp_rate*symbol_dur))
        self.blocks_patterned_interleaver_0 = blocks.patterned_interleaver(gr.sizeof_gr_complex*1, ([0,1,2]))
        self.blocks_interleave_0 = blocks.interleave(gr.sizeof_gr_complex*1, 96)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.analog_const_source_x_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_patterned_interleaver_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_interleave_0, 1))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_patterned_interleaver_0, 2))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_interleave_0, 0), (self.blocks_repeat_0_3, 0))
        self.connect((self.blocks_patterned_interleaver_0, 0), (self.blocks_interleave_0, 0))
        self.connect((self.blocks_repeat_0_3, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_patterned_interleaver_0, 1))

    def get_symbol_dur(self):
        return self.symbol_dur

    def set_symbol_dur(self, symbol_dur):
        self.symbol_dur = symbol_dur
        self.blocks_repeat_0_3.set_interpolation(int(self.samp_rate*self.symbol_dur))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_repeat_0_3.set_interpolation(int(self.samp_rate*self.symbol_dur))

    def get_radio_freq(self):
        return self.radio_freq

    def set_radio_freq(self, radio_freq):
        self.radio_freq = radio_freq
        self.osmosdr_sink_0.set_center_freq(self.radio_freq, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
