
# Design for Test rules

- All design submissions must follow the Design for Test (DFT) rules. Three optical interfaces are available: surface grating couplers (GC), facet-attached micro-lenses (FaML), and facet-attached vertical emitters (FAVE).
 - Wavelength for testing can be 1310 or 1550 nm, swept over a range of +/- 30 nm

## Grating Couplers

- area design maximum: 1000 µm wide, 500 µm high
- grating coupler cells:
  - SiEPIC_EBeam_PDK -> EBeam-SiN -> 
    - GC_SiN_TE_1310_8degOxide_BB
    - GC_SiN_TE_1550_8degOxide_BB
    - should be facing right
- 127 µm pitch, verically aligned, single column, connected circuits
- up to 4 grating couplers
- The grating coupler that is second from the top should be labeled with an opt_in_TE_1550_device_designerUniqueIndentifier label on the Text layer; it will be connected to the swept tunable laser
- opt_in label format: opt_in_TE_1550_device_designerUniqueIndentifier
- opt_in label location: the tip (0,0) of the grating coupler cell at the input
- Fiber Array test consists of: 
  - 1 (top GC): output, to detector
  - 2: input, laser
  - 3: output, to detector
  - 4 (bottom GC): output, to detector
- See example: EBeam_LukasChrostowski_MZI_1550.oas
  
## Facet-attached Micro-Lenses (FaML)

- area design maximum: 1100 µm wide, 500 µm high
- FaML coupler cells:
  - SiEPIC_EBeam_PDK -> EBeam-Dream -> 
    - ebeam_dream_FaML_SiN_1550_BB
    - should be facing right
    - left edge of the chip (the cell includes 100 µm of deep trench)
- 127 µm pitch, verically aligned, single column, connected circuits
- up to 4 lenses
- opt_in label format: opt_in_TE_1550_***FaML***_designerUniqueIndentifier
- opt_in label location: at the chip edge (0,0) of the FaML cell, at the laser input
- Fiber Array test consists of: 
  - 1 (top FaML): output, to detector
  - 2 (middle FaML): input, laser
  - 3 (middle FaML): output, to detector
  - 4 (bottom FaML): output, to detector
- Filename: must contain ***FaML***, so that it recognized and placed on the edge
- See example: EBeam_LukasChrostowski_MZI1_1550_***FaML***.oas

## Facet-attached Vertical Emitters (FAVE)

- area design maximum: 1000 µm wide, 500 µm high
- FaML coupler cells:
  - SiEPIC_EBeam_PDK -> EBeam-Dream -> 
    - ebeam_dream_FAVE_SiN_1550_BB
    - should be facing right
- The FaML cell contains the Thermal Isolation Trench layer, which needs to be 30 µm away from SiN -- both within the design, as well as neighbour designs.
  - Left & Right side: 22 µm away from the FloorPlan (additional space between designs will be added during merging)
  - Top & Bottom: 9 µm away from the FloorPlan (additional space between designs will be added during merging)
- 127 µm pitch, verically aligned, single column, connected circuits
- up to 4 emitters
- opt_in label format: opt_in_TE_1550_***FAVE***_designerUniqueIndentifier
- opt_in label location: the waveguide opt1 port (0,0) of the FAVE cell, at the laser input
- Fiber Array test consists of: 
  - 1 (top FAVE): output, to detector
  - 2 (middle FAVE): input, laser
  - 3 (middle FAVE): output, to detector
  - 4 (bottom FAVE): output, to detector
- See example: EBeam_LukasChrostowski_MZI_1550_FAVE.oas
