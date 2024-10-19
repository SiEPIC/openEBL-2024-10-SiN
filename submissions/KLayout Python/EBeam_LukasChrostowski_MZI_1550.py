'''
--- Simple MZI ---
  
by Lukas Chrostowski, 2024


   
Example simple script to
 - create a new layout with a top cell
 - create an MZI
 - export to OASIS for submission to fabrication

using SiEPIC-Tools function including connect_pins_with_waveguide and connect_cell

Use instructions:

Run in Python, e.g., VSCode

pip install required packages:
 - klayout, SiEPIC, siepic_ebeam_pdk, numpy

'''

designer_name = 'LukasChrostowski'
top_cell_name = 'EBeam_%s_MZI' % designer_name
#export_type = 'static'  # static: for fabrication, PCell: include PCells in file
export_type = 'PCell'  # static: for fabrication, PCell: include PCells in file

import pya
from pya import *

import SiEPIC
from SiEPIC._globals import Python_Env
from SiEPIC.scripts import connect_cell, connect_pins_with_waveguide, zoom_out, export_layout
from SiEPIC.utils.layout import new_layout, floorplan
from SiEPIC.extend import to_itype
from SiEPIC.verification import layout_check
 
import os

if Python_Env == 'Script':
    # For external Python mode, when installed using pip install siepic_ebeam_pdk
    import siepic_ebeam_pdk

print('EBeam_LukasChrostowski_MZI layout script')
 
tech_name = 'EBeam'

from packaging import version
if version.parse(SiEPIC.__version__) < version.parse("0.5.4"):
    raise Exception("Errors", "This example requires SiEPIC-Tools version 0.5.4 or greater.")

'''
Create a new layout using the EBeam technology,
with a top cell
and Draw the floor plan
'''    
cell, ly = new_layout(tech_name, top_cell_name, GUI=True, overwrite = True)
floorplan(cell, 1000e3, 410e3)

dbu = ly.dbu

from SiEPIC.scripts import connect_pins_with_waveguide, connect_cell
waveguide_type1='SiN Strip TE 1550 nm, w=750 nm'
waveguide_type_delay='SiN routing TE 1550 nm (compound waveguide)'

# Load cells from library
cell_ebeam_gc = ly.create_cell('GC_SiN_TE_1550_8degOxide_BB', 'EBeam-SiN')
cell_ebeam_y = ly.create_cell('ANT_MMI_1x2_te1550_3dB_BB',  'EBeam-SiN')

#######################
# Circuit #1 – Loopback
#######################
# grating couplers, place at absolute positions
x,y = 60000, 14500
t = Trans(Trans.R0,x,y)
instGC1 = cell.insert(CellInstArray(cell_ebeam_gc.cell_index(), t))
t = Trans(Trans.R0,x,y+127000)
instGC2 = cell.insert(CellInstArray(cell_ebeam_gc.cell_index(), t))
# automated test label
text = Text ("opt_in_TE_1550_device_%s_MZI" % designer_name, t)
cell.shapes(ly.layer(ly.TECHNOLOGY['Text'])).insert(text).text_size = 5/dbu
# Waveguide:
connect_pins_with_waveguide(instGC1, 'opt1', instGC2, 'opt1', waveguide_type=waveguide_type1)

#######################
# Circuit #2 – MZI
#######################
x += 110e3
# grating couplers, place at absolute positions
t = Trans(Trans.R0,x,y)
instGC3 = cell.insert(CellInstArray(cell_ebeam_gc.cell_index(), t))
t = Trans(Trans.R0,x,y+127000)
instGC4 = cell.insert(CellInstArray(cell_ebeam_gc.cell_index(), t))
# automated test label
text = Text ("opt_in_TE_1550_device_%s_loopback" % designer_name, t)
cell.shapes(ly.layer(ly.TECHNOLOGY['Text'])).insert(text).text_size = 5/dbu
# Y branches:
instY1 = connect_cell(instGC3, 'opt1', cell_ebeam_y, 'pin1')
instY2 = connect_cell(instGC4, 'opt1', cell_ebeam_y, 'pin1')
# Waveguides: 
connect_pins_with_waveguide(instY1, 'pin2', instY2, 'pin3', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instY1, 'pin3', instY2, 'pin2', waveguide_type=waveguide_type1, turtle_A=[100,-90])

#######################
# Circuit #3 - MZI, with a very long delay line
#######################
cell_ebeam_delay = ly.create_cell('spiral_paperclip', 'EBeam_Beta',
                                {'waveguide_type':waveguide_type_delay,
                                'length':325,
                                'loops':8,
                                'flatten':True})
x,y = 60000, 14500+127e3*2
t = Trans(Trans.R0,x,y)
instGC1 = cell.insert(CellInstArray(cell_ebeam_gc.cell_index(), t))
t = Trans(Trans.R0,x,y+127e3)
instGC2 = cell.insert(CellInstArray(cell_ebeam_gc.cell_index(), t))
# automated test label
text = Text ("opt_in_TE_1550_device_%s_MZI3" % designer_name, t)
cell.shapes(ly.layer(ly.TECHNOLOGY['Text'])).insert(text).text_size = 5/dbu
# Y branches:
instY1 = connect_cell(instGC1, 'opt1', cell_ebeam_y, 'pin1')
instY1.transform(Trans(20000,0))
instY2 = connect_cell(instGC2, 'opt1', cell_ebeam_y, 'pin1')
instY2.transform(Trans(20000,0))
# Spiral:
instSpiral = connect_cell(instY2, 'pin2', cell_ebeam_delay, 'optA')
instSpiral.transform(Trans(110e3,0))
# Waveguides:
connect_pins_with_waveguide(instGC1, 'opt1', instY1, 'pin1', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instGC2, 'opt1', instY2, 'pin1', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instY1, 'pin2', instY2, 'pin3', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instY2, 'pin2', instSpiral, 'optA', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instY1, 'pin3', instSpiral, 'optB', waveguide_type=waveguide_type1,turtle_A=[50,90])


# Zoom out
zoom_out(cell)

# Export for fabrication, removing PCells
path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.splitext(os.path.basename(__file__))[0]
if export_type == 'static':
    file_out = export_layout(cell, path, filename, relative_path = '..', format='oas', screenshot=True)
else:
    file_out = os.path.join(path,'..',filename+'.oas')
    ly.write(file_out)

# Verify
file_lyrdb = os.path.join(path,filename+'.lyrdb')
num_errors = layout_check(cell = cell, verbose=False, GUI=True, file_rdb=file_lyrdb)
print('Number of errors: %s' % num_errors)

# Display the layout in KLayout, using KLayout Package "klive", which needs to be installed in the KLayout Application
if Python_Env == 'Script':
    from SiEPIC.utils import klive
    klive.show(file_out, lyrdb_filename=file_lyrdb, technology=tech_name)
