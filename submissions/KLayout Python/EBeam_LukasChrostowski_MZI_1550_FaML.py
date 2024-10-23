'''
--- Simple MZI, tested using Facet-Attached Micro Lenses (FaML) ---
  
by Lukas Chrostowski, 2024
   
Example simple script to
 - choose the fabrication technology provided by Applied Nanotools,  using silicon nitride (SiN) waveguides
 - use the SiEPIC-EBeam-PDK technology
 - using KLayout and SiEPIC-Tools, with function including connect_pins_with_waveguide and connect_cell
 - create a new layout with a top cell, limited a design area of 1000 microns wide by 410 microns high.
 - create two Mach-Zehnder Interferometer (MZI) circuits, and one loopback for calibration
   One Mach-Zehnder has a small path length difference, while the other uses a very long spiral.
 - export to OASIS for submission to fabrication
 - display the layout in KLayout using KLive
 
 Test plan
 - count lenses from the bottom up (bottom is 1, top is 6, in this design)
 - laser input on bottom lens (1), detector on second (2), for alignment
 - MZI1: laser on 3, detector on 4, sweep
 - MZI2: laser on 5, detector on 6, sweep
 

Use instructions:

Run in Python, e.g., VSCode

pip install required packages:
 - klayout, SiEPIC, siepic_ebeam_pdk, numpy

'''

designer_name = 'LukasChrostowski'
top_cell_name = 'EBeam_%s_MZI_FaML' % designer_name
export_type = 'static'  # static: for fabrication, PCell: include PCells in file
#export_type = 'PCell'  # static: for fabrication, PCell: include PCells in file

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
floorplan(cell, 1000e3, 695e3)

dbu = ly.dbu

from SiEPIC.scripts import connect_pins_with_waveguide, connect_cell
waveguide_type1='SiN Strip TE 1550 nm, w=750 nm'
waveguide_type_delay='SiN routing TE 1550 nm (compound waveguide)'

# Load cells from library
cell_ebeam_faml = ly.create_cell('ebeam_dream_FaML_SiN_1550_BB', 'EBeam-Dream', 
                                 {'num_channels':4})
cell_ebeam_y = ly.create_cell('ANT_MMI_1x2_te1550_3dB_BB',  'EBeam-SiN')

#######################
# Circuit #1 – Loopback
#######################
# lens cell includes loopback on the bottom two channels
y_offset = 284e3
x,y = 0, y_offset
t = Trans(Trans.R0,x,y)
inst_faml = cell.insert(CellInstArray(cell_ebeam_faml.cell_index(), t))
# automated test label
x,y = 0, -127e3*2 + y_offset
text = Text ("opt_in_TE_1550_device_%s_loopback_faml" % designer_name, t)
cell.shapes(ly.layer(ly.TECHNOLOGY['Text'])).insert(text).text_size = 5/dbu

#######################
# Circuit #2 – MZI
#######################
# automated test label
x,y = 0, y_offset
text = Text ("opt_in_TE_1550_device_%s_mzi_faml" % designer_name, t)
cell.shapes(ly.layer(ly.TECHNOLOGY['Text'])).insert(text).text_size = 5/dbu
# Y branches:
instY1 = connect_cell(inst_faml, 'opt1', cell_ebeam_y, 'pin1')
instY2 = connect_cell(inst_faml, 'opt2', cell_ebeam_y, 'pin1')
# Waveguides: 
connect_pins_with_waveguide(instY1, 'pin2', instY2, 'pin3', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instY1, 'pin3', instY2, 'pin2', waveguide_type=waveguide_type1, turtle_A=[100,-90])

#######################
# Circuit #3 - MZI, with a very long delay line
#######################
cell_ebeam_delay = ly.create_cell('spiral_paperclip', 'EBeam_Beta',
                                {'waveguide_type':waveguide_type_delay,
                                'length':315,
                                'loops':8,
                                'flatten':True})
# automated test label
x,y = 0, 127e3*2 + y_offset
text = Text ("opt_in_TE_1550_device_%s_mzi2_faml" % designer_name, t)
cell.shapes(ly.layer(ly.TECHNOLOGY['Text'])).insert(text).text_size = 5/dbu
# Y branches:
instY1 = connect_cell(inst_faml, 'opt3', cell_ebeam_y, 'pin1')
instY2 = connect_cell(inst_faml, 'opt4', cell_ebeam_y, 'pin1')
# Spiral:
instSpiral = connect_cell(instY2, 'pin2', cell_ebeam_delay, 'optA')
instSpiral.transform(Trans(110e3,0))
# Waveguides:
connect_pins_with_waveguide(instY1, 'pin2', instY2, 'pin3', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instY2, 'pin2', instSpiral, 'optA', waveguide_type=waveguide_type1)
connect_pins_with_waveguide(instY1, 'pin3', instSpiral, 'optB', waveguide_type=waveguide_type1,turtle_A=[50,90])


# Zoom out
zoom_out(cell)

# Export for fabrication, removing PCells
path = os.path.dirname(os.path.realpath(__file__))
filename, extension = os.path.splitext(os.path.basename(__file__))
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
