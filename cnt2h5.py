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

    def __init__(self, filename, channels=arange(192)):
        self.filename = filename
        self.file = open(self.filename, 'rb')
        
        self.get_electloc()
        self.get_setup()
        
    def get(self, ctype, size=1):
        """Reads and unpacks binary data into the desired ctype."""
        chunk = self.file.read(calcsize(ctype) * size)
        return unpack(ctype * size, chunk)

    def get_electloc(self):
        label        = self.get('10s')[0]
        reserved1    = self.get('5s')[0]
        n            = self.get('h')[0]
        reserved2    = self.get('30s')[0]
        baseline     = self.get('h')[0]
        reserved3    = self.get('10s')[0]
        sensitivity  = self.get('f')[0]
        reserved4    = self.get('8s')[0]
        calib        = self.get('f')[0]
    
    def get_setup(self):
        header_offset = self.get('900x')[]
    
   

    def get_data_info(self):
        if self.acq_type == 1:
            self.file.seek(144)
            self.raw_offset = self.get('l')[0]
            self.data_type = 'h' # 2-byte Integer
        elif acq_type == 2:
            self.file.seek(160)
            self.ave_offset = self.get('l')[0]
            self.data_type = 'd' # 8-byte Real
        elif acq_type == 3:
            f.seek(144)
            raw_offset = self.get('l')[0]
            self.data_type = 'h' # 2-byte Integer
        else:
            print "Error!"

def get_data():
    file.seek(900 + (75 * 32))
    
    
    
    

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
        
