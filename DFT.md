
# Design for Test rules

- All design submissions must follow the Design for Test (DFT) rules. Three optical interfaces are available: surface grating couplers (GC), facet-attached micro-lenses (FaML), and facet-attached vertical emitters (FAVE).

## Grating Couplers

- area design maximum: 1000 µm wide, 500 µm high
- grating coupler cells:
  - SiEPIC_EBeam_PDK -> EBeam-SiN -> 
    - GC_SiN_TE_1310_8degOxide_BB
    - GC_SiN_TE_1550_8degOxide_BB
- 127 µm pitch, verically aligned, single column, connected circuits
- up to 4 grating couplers
- opt_in label format: opt_in_TE_1550_device_designerUniqueIndentifier
- opt_in label location: the tip (0,0) of the grating coupler cell at the input
- Fiber Array test consists of: 
  - 1 (top GC): output, to detector
  - 2: input, laser
  - 3: output, to detector
  - 4 (bottom GC): output, to detector
  
## Facet-attached Micro-Lenses (FaML)

- area design maximum: 1000 µm wide, 500 µm high
- FaML coupler cells:
  - SiEPIC_EBeam_PDK -> EBeam-Dream -> 
    - ebeam_dream_FaML_SiN_1550_BB
- 127 µm pitch, verically aligned, single column, connected circuits
- up to 4 lenses
- opt_in label format: opt_in_TE_1550_FaML_designerUniqueIndentifier
- opt_in label location: the lens and chip edge (0,0) of the FaML cell at the input
- Fiber Array test consists of: 
  - 1 (top FaML): input, laser
  - 2 (middle FaML): output, to detector
  - 3 (middle FaML): output, to detector
  - 4 (bottom FaML): output, to detector

## Facet-attached Vertical Emitters (FAVE)

- area design maximum: 1000 µm wide, 500 µm high
- FaML coupler cells:
  - SiEPIC_EBeam_PDK -> EBeam-Dream -> 
    - ebeam_dream_FAVE_SiN_1550_BB
- 127 µm pitch, verically aligned, single column, connected circuits
- up to 4 lenses
- opt_in label format: opt_in_TE_1550_FAVE_designerUniqueIndentifier
- opt_in label location: the edge (0,0) of the FAVE cell at the input
- Fiber Array test consists of: 
  - 1 (top FAVE): input, laser
  - 2 (middle FAVE): output, to detector
  - 3 (middle FAVE): output, to detector
  - 4 (bottom FAVE): output, to detector
