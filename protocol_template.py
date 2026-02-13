from opentrons import protocol_api

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

    tiprack_20 = protocol.load_labware(
        "opentrons_96_tiprack_20ul", "4"
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
        tip_racks=[tiprack_20]
    )
    pipette_1000 = protocol.load_instrument(
        "p1000_single_gen2",
        "right",
        tip_racks=[tiprack_1000]
    )
    # ← injected automatically
    combined_data = {{COMBINED_DATA}}
    wells = {{WELLS}}
    sample_ids = {{SAMPLE_IDS}}
    location_384 = {{LOCATION_384}}
    vol_384 = {{VOL_384}}
    location_eppendorf = {{LOCATION_EPPENDORF}}
    vol_eppendorf = {{VOL_EPPENDORF}}
    vol_aqueous = {{VOL_AQUEOUS}}

    protocol.comment(f"Wells: {wells}")
    protocol.comment(f"Sample IDs: {sample_ids}")
    protocol.comment(f"Combined data: {combined_data}")

    # Pick up tip once for p1000 and keep it throughout, change to none eventually
    pipette_1000.pick_up_tip()

    for i, well in enumerate(wells):
        
        #DMSO Transfer
        pipette_20.pick_up_tip()
        pipette_20.aspirate(float(vol_384[i]), DMSO_plate.wells_by_name()[location_384[i]])
        pipette_20.dispense(float(vol_384[i]), mix_plate.wells_by_name()[well])
        pipette_20.drop_tip()

        #Buffer Transfer
        pipette_1000.aspirate(float(vol_aqueous[i]), aqueous_reservoir.wells()[0])
        pipette_1000.dispense(float(vol_aqueous[i]), mix_plate.wells_by_name()[well])
        pipette_1000.mix(3, 100, mix_plate.wells_by_name()[well])
        
        
        #Eppendorf Transfer
        pipette_20.pick_up_tip()
        vol_epp = float(vol_eppendorf[i])
        while vol_epp > 0:
            transfer_vol = min(vol_epp, 20)
            pipette_20.aspirate(transfer_vol, eppendorf_plate[location_eppendorf[i]])
            pipette_20.dispense(transfer_vol, mix_plate.wells_by_name()[well])
            vol_epp -= transfer_vol
        pipette_20.drop_tip()

        #Moving to NMR rack
        pipette_1000.mix(3, 100, mix_plate.wells_by_name()[well])
        pipette_1000.aspirate(100, mix_plate.wells_by_name()[well])
        pipette_1000.dispense(100, NMR_rack.wells_by_name()[well])

    # Drop p1000 tip after all transfers complete
    pipette_1000.drop_tip()


        #ADD WASH STEP
        