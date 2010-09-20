#!/usr/bin/python

from numpy import array, flatnonzero, arange, shape, zeros, ones
from struct import unpack, calcsize
import tables
import sys
import os.path
try:
    import psyco
    psyco.full()
except:
    pass

class CNTData():
    """A class for reading Neuroscan .cnt files."""

    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'rb')
        
        self.info = {}
        self.get_setup()
        
        self.file.seek(900)
        self.electrodes = {}
        for e in xrange(self.info["nchannels"]):
            electrode = self.get_electrode()
            self.electrodes[electrode.label] = electrode
        
    def get(self, ctype, size=1):
        """Reads and unpacks binary data into the desired ctype."""
        chunk = self.file.read(calcsize(ctype) * size)
        return unpack(ctype * size, chunk)[0]

    def get_electrode(self):
        label = self.get('10s').strip('\x00')
        
        electrode = Electrode(label)
        electrode.reference      = self.get('?')
        electrode.skip           = self.get('?')
        electrode.reject         = self.get('?')
        electrode.display        = self.get('?')
        electrode.bad            = self.get('?')
        electrode.n              = self.get('H')
        electrode.avg_reference  = self.get('s')
        electrode.clipadd        = self.get('s')
        electrode.x_coord        = self.get('f')
        electrode.y_coord        = self.get('f')
        electrode.veog_wt        = self.get('f')
        electrode.veog_std       = self.get('f')
        electrode.snr            = self.get('f')
        electrode.heog_wt        = self.get('f')
        electrode.heog_std       = self.get('f')
        electrode.baseline       = self.get('h')
        electrode.filtered       = self.get('s')
        electrode.fsp            = self.get('s')
        electrode.aux1_wt        = self.get('f')
        electrode.aux1_std       = self.get('f')
        electrode.senstivity     = self.get('f')
        electrode.gain           = self.get('s')
        electrode.hipass         = self.get('s')
        electrode.lopass         = self.get('s')
        electrode.page           = self.get('B')
        electrode.size           = self.get('B')
        electrode.impedance      = self.get('B')
        electrode.physicalchnl   = self.get('B')
        electrode.rectify        = self.get('s')
        electrode.calib          = self.get('f')
        
        return electrode
    
    def get_setup(self):
        self.file.seek(0)
        self.info["rev"]               = self.get('12s')
        self.info["nextfile"]          = self.get('l')
        self.info["prevfile"]          = self.get('L')
        self.info["type"]              = self.get('b')
        self.info["id"]                = self.get('20s')
        self.info["oper"]              = self.get('20s')
        self.info["doctor"]            = self.get('20s')
        self.info["referral"]          = self.get('20s')
        self.info["hospital"]          = self.get('20s')
        self.info["patient"]           = self.get('20s')
        self.info["age"]               = self.get('h')
        self.info["sex"]               = self.get('s')
        self.info["hand"]              = self.get('s')
        self.info["med"]               = self.get('20s')
        self.info["category"]          = self.get('20s')
        self.info["state"]             = self.get('20s')
        self.info["date"]              = self.get('10s')
        self.info["time"]              = self.get('12s')
        self.info["mean_age"]          = self.get('f')
        self.info["stdev"]             = self.get('f')
        self.info["n"]                 = self.get('h')
        self.info["compfile"]          = self.get('38s')
        self.info["spectwincomp"]      = self.get('f')
        self.info["meanaccuracy"]      = self.get('f')
        self.info["meanlatency"]       = self.get('f')
        self.info["sortfile"]          = self.get('46s')
        self.info["numevents"]         = self.get('i')
        self.info["compoper"]          = self.get('b')
        self.info["avgmode"]           = self.get('b')
        self.info["review"]            = self.get('b')
        self.info["nsweeps"]           = self.get('H')
        self.info["compsweeps"]        = self.get('H')
        self.info["acceptcnt"]         = self.get('H')
        self.info["rejectcnt"]         = self.get('H')
        self.info["pnts"]              = self.get('H')
        self.info["nchannels"]         = self.get('H')
        self.info["avgupdate"]         = self.get('H')
        self.info["domain"]            = self.get('b')
        self.info["variance"]          = self.get('b')
        self.info["rate"]              = self.get('H')
        self.info["scale"]             = self.get('d')
        self.info["veogcorrect"]       = self.get('b')
        self.info["heogcorrect"]       = self.get('b')
        self.info["aux1correct"]       = self.get('b')
        self.info["aux2correct"]       = self.get('b')
        self.info["veogtrig"]          = self.get('f')
        self.info["heogtrig"]          = self.get('f')
        self.info["aux1trig"]          = self.get('f')
        self.info["aux2trig"]          = self.get('f')
        self.info["heogchnl"]          = self.get('h')
        self.info["veogchnl"]          = self.get('h')
        self.info["aux1chnl"]          = self.get('h')
        self.info["aux2chnl"]          = self.get('h')
        self.info["veogdir"]           = self.get('b')
        self.info["heogdir"]           = self.get('b')
        self.info["aux1dir"]           = self.get('b')
        self.info["aux2dir"]           = self.get('b')
        self.info["veog_n"]            = self.get('h')
        self.info["heog_n"]            = self.get('h')
        self.info["aux1_n"]            = self.get('h')
        self.info["aux2_n"]            = self.get('h')
        self.info["veogmaxcnt"]        = self.get('h')
        self.info["heogmaxcnt"]        = self.get('h')
        self.info["aux1maxcnt"]        = self.get('h')
        self.info["aux2maxcnt"]        = self.get('h')
        self.info["veogmethod"]        = self.get('b')
        self.info["heogmethod"]        = self.get('b')
        self.info["aux1method"]        = self.get('b')
        self.info["aux2method"]        = self.get('b')
        self.info["ampsensitivity"]    = self.get('f')
        self.info["lowpass"]           = self.get('b')
        self.info["highpass"]          = self.get('b')
        self.info["notch"]             = self.get('b')
        self.info["autoclipadd"]       = self.get('b')
        self.info["baseline"]          = self.get('b')
        self.info["offstart"]          = self.get('f')
        self.info["offstop"]           = self.get('f')
        self.info["reject"]            = self.get('b')
        self.info["rejstart"]          = self.get('f')
        self.info["rejstop"]           = self.get('f')
        self.info["rejmin"]            = self.get('f')
        self.info["rejmax"]            = self.get('f')
        self.info["trigtype"]          = self.get('b')
        self.info["trigval"]           = self.get('f')
        self.info["trigchnl"]          = self.get('b')
        self.info["trigmask"]          = self.get('h')
        self.info["trigisi"]           = self.get('f')
        self.info["trigmin"]           = self.get('f')
        self.info["trigmax"]           = self.get('f')
        self.info["trigdir"]           = self.get('b')
        self.info["autoscale"]         = self.get('b')
        self.info["n2"]                = self.get('h')
        self.info["dir"]               = self.get('b')
        self.info["dispmin"]           = self.get('f')
        self.info["dispmax"]           = self.get('f')
        self.info["xmin"]              = self.get('f')
        self.info["xmax"]              = self.get('f')
        self.info["automin"]           = self.get('f')
        self.info["automax"]           = self.get('f')
        self.info["zmin"]              = self.get('f')
        self.info["zmax"]              = self.get('f')
        self.info["lowcut"]            = self.get('f')
        self.info["highcut"]           = self.get('f')
        self.info["common"]            = self.get('b')
        self.info["savemode"]          = self.get('b')
        self.info["manmode"]           = self.get('b')
        self.info["ref"]               = self.get('10s')
        self.info["rectify"]           = self.get('b')
        self.info["displayxmin"]       = self.get('f')
        self.info["displayxmax"]       = self.get('f')
        self.info["phase"]             = self.get('b')
        self.info["screen"]            = self.get('16s')
        self.info["calmode"]           = self.get('h')
        self.info["calmethod"]         = self.get('h')
        self.info["calupdate"]         = self.get('h')
        self.info["calbaseline"]       = self.get('h')
        self.info["calsweeps"]         = self.get('h')
        self.info["calattenuator"]     = self.get('f')
        self.info["calpulsevolt"]      = self.get('f')
        self.info["calpulsestart"]     = self.get('f')
        self.info["calpulsestop"]      = self.get('f')
        self.info["calfreq"]           = self.get('f')
        self.info["taskfile"]          = self.get('34s')
        self.info["seqfile"]           = self.get('34s')
        self.info["spectmethod"]       = self.get('b')
        self.info["spectscaling"]      = self.get('b')
        self.info["spectwindow"]       = self.get('b')
        self.info["spectwinlength"]    = self.get('f')
        self.info["spectorder"]        = self.get('b')
        self.info["notchfilter"]       = self.get('b')
        self.info["headgain"]          = self.get('h')
        self.info["additionalfiles"]   = self.get('i')
        self.info["unused"]            = self.get('5s')
        self.info["fspstopmethod"]     = self.get('h')
        self.info["fspstopmode"]       = self.get('h')
        self.info["fspfvalue"]         = self.get('f')
        self.info["fsppoint"]          = self.get('h')
        self.info["fspblocksize"]      = self.get('h')
        self.info["fspp1"]             = self.get('H')
        self.info["fspp2"]             = self.get('H')
        self.info["fspalpha"]          = self.get('f')
        self.info["fspnoise"]          = self.get('f')
        self.info["fspv1"]             = self.get('h')
        self.info["montage"]           = self.get('40s')
        self.info["eventfile"]         = self.get('40s')
        self.info["fratio"]            = self.get('f')
        self.info["minor_rev"]         = self.get('b')
        self.info["eegupdate"]         = self.get('h')
        self.info["compressed"]        = self.get('b')
        self.info["xscale"]            = self.get('f')
        self.info["yscale"]            = self.get('f')
        self.info["xsize"]             = self.get('f')
        self.info["ysize"]             = self.get('f')
        self.info["acmode"]            = self.get('b')
        self.info["commonchnl"]        = self.get('B')
        self.info["xtics"]             = self.get('b')
        self.info["xrange"]            = self.get('b')
        self.info["ytics"]             = self.get('b')
        self.info["yrange"]            = self.get('b')
        self.info["xscalevalue"]       = self.get('f')
        self.info["xscaleinterval"]    = self.get('f')
        self.info["yscalevalue"]       = self.get('f')
        self.info["yscaleinterval"]    = self.get('f')
        self.info["scaletoolx1"]       = self.get('f')
        self.info["scaletooly1"]       = self.get('f')
        self.info["scaletoolx2"]       = self.get('f')
        self.info["scaletooly2"]       = self.get('f')
        self.info["port"]              = self.get('h')
        self.info["numsamples"]        = self.get('L')
        self.info["filterflag"]        = self.get('b')
        self.info["lowcutoff"]         = self.get('f')
        self.info["lowpoles"]          = self.get('h')
        self.info["highcutoff"]        = self.get('f')
        self.info["highpoles"]         = self.get('h')
        self.info["filtertype"]        = self.get('b')
        self.info["filterdomain"]      = self.get('b')
        self.info["snrflag"]           = self.get('b')
        self.info["coherenceflag"]     = self.get('b')
        self.info["continuoustype"]    = self.get('b')
        self.info["eventtablepos"]     = self.get('L')
        self.info["continuousseconds"] = self.get('f')
        self.info["channeloffset"]     = self.get('l')
        self.info["autocorrectflag"]   = self.get('b')
        self.info["dcthreshold"]       = self.get('B')
    
    def get_data(self):
        file.seek(900 + (75 * self.info['nchannels']))
    

        
class Electrode():
    def __init__(self, label):
        self.label = label
    
    def __unicode__(self):
        return self.label
            
            
            
            
   

    
    
    
    

def load(squid, h5f):
    for channel in xrange(squid.channel_count):
        print "Reading channel %d ..." % channel
        h5f.root.raw_data[channel, :] = squid.get_channel(channel)

if __name__ == "__main__":

    for sqd_filename in sys.argv[1:]:
        print sqd_filename

        squid = SquidData(sqd_filename)

        h5_filename = os.path.splitext(sqd_filename)[0] + ".h5"
        array_shape = (squid.channel_count, squid.actual_sample_count)

        h5f = tables.openFile(h5_filename, mode='w', title="MEG data")

        h5f.createCArray(
            where=h5f.root, 
            name='raw_data', 
            atom=tables.Int16Atom(), 
            shape=array_shape, 
            filters=tables.Filters(1))


        h5f.createCArray(
            where=h5f.root, 
            name='convfactor', 
            atom=tables.Float32Atom(), 
            shape=shape(squid.convfactor), 
            filters=tables.Filters(1))
        h5f.root.convfactor[:] = squid.convfactor

        load(squid, h5f)

        print "Output %s" % h5_filename
        h5f.close()
        
