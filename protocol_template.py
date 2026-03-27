from opentrons import protocol_api, types

metadata = {
    "protocolName": "Auto Generated FillBot Protocol",
    "apiLevel": "2.15"
}


def run(protocol: protocol_api.ProtocolContext):

    DMSO_plate = protocol.load_labware(
        "corning_384_wellplate_112ul_flat", "2"
    )

    aqueous_reservoir = protocol.load_labware(
        "nest_1_reservoir_195ml", "6"
    )

    tiprack_300 = protocol.load_labware(
        "opentrons_96_tiprack_300ul", "4"
    )

    tiprack_1000 = protocol.load_labware(
        "opentrons_96_tiprack_1000ul", "1"
    )

    mix_plate = protocol.load_labware(
        "corning_96_wellplate_360ul_flat", "5"
    )


    NMR_rack = protocol.load_labware(
        "nest_96_wellplate_2ml_deep", "8"
    )

    eppendorf_plate = protocol.load_labware(
        "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap", "9"
    )


    
    pipette_20 = protocol.load_instrument(
        "p20_single_gen2",
        "left",
        tip_racks=[tiprack_300]
    )

    pipette_1000 = protocol.load_instrument(
        "p1000_single_gen2",
        "right",
        tip_racks=[tiprack_1000]
    )
    
    # Set reduced movement speeds
    pipette_20.default_speed = 10
    pipette_1000.default_speed = 150
    # ← injected automatically
    combined_data = {{COMBINED_DATA}}
    wells = {{WELLS}}
    sample_ids = {{SAMPLE_IDS}}
    location_384 = {{LOCATION_384}}
    vol_384 = {{VOL_384}}
    location_eppendorf = {{LOCATION_EPPENDORF}}
    vol_eppendorf = {{VOL_EPPENDORF}}
    vol_aqueous = {{VOL_AQUEOUS}}

    # Offsets for p1000 NMR rack substeps
   
    p1000_nmr_offsets = {
        "mix": {"x": 0, "y": 0, "z": 20},
        "aspirate": {"x": 0, "y": 0, "z": 20},
        "dispense": {"x": 0, "y": 0, "z": 0},
    }

    protocol.comment(f"Wells: {wells}")
    protocol.comment(f"Sample IDs: {sample_ids}")
    protocol.comment(f"Combined data: {combined_data}")

    # Pick up tip once for p1000 and keep it throughout, change to none eventually
    pipette_1000.pick_up_tip()

    del tiprack_1000


    for i, well in enumerate(wells):
       

        
        #Moving to NMR rack
        source_well = mix_plate.wells_by_name()[well]
        dest_well = NMR_rack.wells_by_name()[well]

        mix_loc = source_well.center().move(
            types.Point(
                x=p1000_nmr_offsets["mix"]["x"],
                y=p1000_nmr_offsets["mix"]["y"],
                z=p1000_nmr_offsets["mix"]["z"],
            )
        )

        aspirate_loc = source_well.center().move(
            types.Point(
                x=p1000_nmr_offsets["aspirate"]["x"],
                y=p1000_nmr_offsets["aspirate"]["y"],
                z=p1000_nmr_offsets["aspirate"]["z"],
            )
        )

        dispense_loc = dest_well.center().move(
            types.Point(
                x=p1000_nmr_offsets["dispense"]["x"],
                y=p1000_nmr_offsets["dispense"]["y"],
                z=p1000_nmr_offsets["dispense"]["z"],
            )
        )

        pipette_1000.blow_out(aspirate_loc)
        pipette_1000.mix(3, 100, mix_loc)
        pipette_1000.aspirate(500, aspirate_loc)
        pipette_1000.dispense(500, dispense_loc)
        pipette_1000.blow_out(dispense_loc)

    # Drop p1000 tip after all transfers complete
    pipette_1000.drop_tip()


        #ADD WASH STEP
        
