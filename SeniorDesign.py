import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd

TEMPLATE_FILE = "protocol_template.py"
OUTPUT_FILE = "FillBot_Output_File.py"


# ----------------- Functions -----------------

def select_csv():
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if file_path:
        file_label.config(text=os.path.basename(file_path))
        root.selected_file = file_path


def read_csv():
    if not hasattr(root, "selected_file"):
        print("No file selected!")
        return

    try:
        df = pd.read_csv(root.selected_file, header=None)
        
        # Parse columns by position: A=well, B=sample_id, C=location in 384, D=vol of 384, E=location eppendorf, F=vol eppendorf, G=vol aqueous
        wells = []
        sample_ids = []
        location_384 = []
        vol_384 = []
        location_eppendorf = []
        vol_eppendorf = []
        vol_aqueous = []
        combined_data = []
        
        # Skip first row (header)
        for index, row in df.iterrows():
            if index == 0:
                continue
                
            if pd.notna(row.iloc[0]):
                well = str(row.iloc[0]).strip()
                sample_id = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ''
                loc_384 = str(row.iloc[2]).strip() if len(row) > 2 and pd.notna(row.iloc[2]) else ''
                v_384 = str(row.iloc[3]).strip() if len(row) > 3 and pd.notna(row.iloc[3]) else ''
                loc_epp = str(row.iloc[4]).strip() if len(row) > 4 and pd.notna(row.iloc[4]) else ''
                v_epp = str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else ''
                v_aq = str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ''
                
                # Skip rows where only one column has data and all others are empty
                if not sample_id and not loc_384 and not v_384 and not loc_epp and not v_epp and not v_aq:
                    continue
                
                wells.append(well)
                sample_ids.append(sample_id)
                location_384.append(loc_384)
                vol_384.append(v_384)
                location_eppendorf.append(loc_epp)
                vol_eppendorf.append(v_epp)
                vol_aqueous.append(v_aq)
                combined_data.append({
                    'well': well,
                    'sample_id': sample_id,
                    'location_384': loc_384,
                    'vol_384': v_384,
                    'location_eppendorf': loc_epp,
                    'vol_eppendorf': v_epp,
                    'vol_aqueous': v_aq
                })
        
        # Store all variables in root
        root.wells = wells
        root.sample_ids = sample_ids
        root.location_384 = location_384
        root.vol_384 = vol_384
        root.location_eppendorf = location_eppendorf
        root.vol_eppendorf = vol_eppendorf
        root.vol_aqueous = vol_aqueous
        root.combined_data = combined_data
        
        # Display plate visualization based on wells from spreadsheet
        rows = "ABCDEFGH"
        columns = range(1, 13)

        # clear plate display
        for widget in plate_frame.winfo_children():
            widget.destroy()

        # row labels
        for i, r in enumerate(rows):
            tk.Label(
                plate_frame, text=r,
                width=4, height=2, bg="lightgray"
            ).grid(row=i+1, column=0)

        # column labels
        for j, c in enumerate(columns):
            tk.Label(
                plate_frame, text=c,
                width=6, height=2, bg="lightgray"
            ).grid(row=0, column=j+1)

        # plate cells - mark wells from spreadsheet as filled
        for i, r in enumerate(rows):
            for j, c in enumerate(columns):
                well_id = f"{r}{c}"
                
                if well_id in wells:
                    # Find the index of this well
                    idx = wells.index(well_id)
                    text = sample_ids[idx]
                    color = "lightgreen"
                else:
                    text = ""
                    color = "white"

                tk.Label(
                    plate_frame,
                    text=text,
                    bg=color,
                    width=6,
                    height=3,
                    relief="ridge"
                ).grid(row=i+1, column=j+1)

        print("Wells:", wells)
        print("Sample IDs:", sample_ids)
        print("Location 384:", location_384)
        print("Vol 384:", vol_384)
        print("Location Eppendorf:", location_eppendorf)
        print("Vol Eppendorf:", vol_eppendorf)
        print("Vol Aqueous:", vol_aqueous)
        print("Combined Data:", combined_data)

        next_button.pack(pady=10)

    except Exception as e:
        print("CSV error:", e)


def generate_protocol():
    if not hasattr(root, "combined_data"):
        print("No data available!")
        return

    try:
        combined_data = root.combined_data
        wells = root.wells
        sample_ids = root.sample_ids
        location_384 = root.location_384
        vol_384 = root.vol_384
        location_eppendorf = root.location_eppendorf
        vol_eppendorf = root.vol_eppendorf
        vol_aqueous = root.vol_aqueous

        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template = f.read()

        new_protocol = (
        template
        .replace("{{COMBINED_DATA}}", str(combined_data))
        .replace("{{WELLS}}", str(wells))
        .replace("{{SAMPLE_IDS}}", str(sample_ids))
        .replace("{{LOCATION_384}}", str(location_384))
        .replace("{{VOL_384}}", str(vol_384))
        .replace("{{LOCATION_EPPENDORF}}", str(location_eppendorf))
        .replace("{{VOL_EPPENDORF}}", str(vol_eppendorf))
        .replace("{{VOL_AQUEOUS}}", str(vol_aqueous)))

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(new_protocol)

        print("Protocol generated!")
        print("Saved as:", OUTPUT_FILE)

    except Exception as e:
        print("Generation error:", e)



# ----------------- UI -----------------

root = tk.Tk()
root.title("FillBot")
root.geometry("950x600")

file_label = tk.Label(root, text="No file selected")
file_label.pack(pady=5)

tk.Button(root, text="Select CSV", command=select_csv).pack()
tk.Button(root, text="Read CSV", command=read_csv).pack()

plate_frame = tk.Frame(root)
plate_frame.pack(pady=10)

next_button = tk.Button(
    root,
    text="Next → Generate Opentrons Protocol",
    command=generate_protocol
)

root.mainloop()
