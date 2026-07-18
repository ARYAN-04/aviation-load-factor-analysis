import os
import glob
import pandas as pd

from src.config import COL_INDICES, COL_NAMES, STRICT_START_ROW, RAW_DIR, PROCESSED_DIR


def get_data_slice(df, start_month, num_months, offset=0):
    try:
        start_idx = df[
            df.iloc[:, 0].astype(str).str.strip().str.upper() == start_month
        ].index[offset]
        data = df.iloc[start_idx : start_idx + num_months, COL_INDICES].copy()
        return data
    except Exception:
        return None


def get_fy_months(session_str):
    s_yr, e_yr = session_str.split("-")[0][-2:], session_str.split("-")[1][-2:]
    return [f"{str(m).zfill(2)}/{s_yr}" for m in range(4, 13)] + [
        f"{str(m).zfill(2)}/{e_yr}" for m in range(1, 4)
    ]


def process_regular_fy_file_strict(filepath):
    fname = os.path.basename(filepath)
    try:
        parts = fname.replace(".xlsx", "").split("_")
        session, airline, code = parts[0], parts[1], parts[2]

        df = pd.read_excel(filepath, header=None)
        data_slice = df.iloc[
            STRICT_START_ROW : STRICT_START_ROW + 12, COL_INDICES
        ].copy()

        data_slice.columns = COL_NAMES
        data_slice.insert(0, "Date", get_fy_months(session))
        data_slice["Airline"] = airline
        data_slice["Type"] = code
        data_slice["Session"] = session

        out_path = os.path.join(PROCESSED_DIR, f"{session}_{airline}_{code}_master.csv")
        data_slice.to_csv(out_path, index=False)
        return True
    except Exception as e:
        print(f"Error in {fname}: {e}")
        return False


def stitch_special_fy(airline, code):
    f21 = os.path.join(RAW_DIR, f"{airline}_2021-22.xlsx")
    f22 = os.path.join(RAW_DIR, f"{airline}_2022-23.xlsx")

    if not (os.path.exists(f21) and os.path.exists(f22)):
        return False

    df21_all = pd.read_excel(f21, header=None)
    df22_all = pd.read_excel(f22, header=None)

    offset = 0 if code == "1" else 25

    apr_dec = df21_all.iloc[
        STRICT_START_ROW + 3 + offset : STRICT_START_ROW + 12 + offset, COL_INDICES
    ].copy()
    apr_dec.columns = COL_NAMES
    apr_dec.insert(0, "Date", [f"{str(m).zfill(2)}/21" for m in range(4, 13)])

    jan_mar = df22_all.iloc[
        STRICT_START_ROW + offset : STRICT_START_ROW + 3 + offset, COL_INDICES
    ].copy()
    jan_mar.columns = COL_NAMES
    jan_mar.insert(0, "Date", [f"{str(m).zfill(2)}/22" for m in range(1, 4)])

    combined = pd.concat([apr_dec, jan_mar])
    combined["Airline"] = airline
    combined["Type"] = code
    combined["Session"] = "2021-22"

    out_path = os.path.join(PROCESSED_DIR, f"2021-22_{airline}_{code}_master.csv")
    combined.to_csv(out_path, index=False)
    return True


def run_master_pipeline():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    regular_count = 0
    for f in glob.glob(os.path.join(RAW_DIR, "*.xlsx")):
        if os.path.basename(f)[0].isdigit():
            if process_regular_fy_file_strict(f):
                regular_count += 1

    stitch_count = 0
    special_files = [
        b for b in os.listdir(RAW_DIR) if b.endswith(".xlsx") and not b[0].isdigit()
    ]
    airlines = set(b.split("_")[0] for b in special_files)
    for air in airlines:
        for code in ["1", "2"]:
            if stitch_special_fy(air, code):
                stitch_count += 1

    total = len(os.listdir(PROCESSED_DIR))
    print(
        f"Pipeline Complete. Regular: {regular_count}, Stitched: {stitch_count}, Total: {total}"
    )
