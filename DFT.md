
# Design for Test rules

- All design submissions must follow the Design for Test (DFT) rules. Two optical interfaces are available: surface grating couplers (GC), and facet-attached micro-lenses (FaML)

## Grating Couplers

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

- 127 µm pitch, verically aligned, single column, connected circuits
- up to 3 lenses
- opt_in label format: opt_in_TE_1550_FaML_designerUniqueIndentifier
- opt_in label location: the lens and chip edge (0,0) of the FaML cell at the input
- Fiber Array test consists of: 
  - 1 (top FaML): input, laser
  - 2 (middle FaML): output, to detector
  - 3 (bottom FaML): output, to detector
