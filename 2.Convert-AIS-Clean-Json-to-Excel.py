#
# Script to convert the Indian Income Tax - AIS Json into Excel file!
# AppInSource - Chetan Ganatra - 07-Sept-25
# 
# Only for educational and reference purpose. Use at your own risk!
#

import json
import pandas as pd
import sys
from pathlib import Path


def make_dataframe(data, labels, context="", transpose=False):
    #print(context)
    if not data:
        return pd.DataFrame(columns=labels if not transpose else ["Field", "Value"])

    # Case 1: list of dicts
    if isinstance(data[0], dict):
        #print('case1')
        df = pd.DataFrame(data)
        missing = [lbl for lbl in labels if lbl not in df.columns]
        df = df.reindex(columns=[*labels, *missing])
    # Case 2: flat list
    elif all(isinstance(x, (str, int, float, type(None))) for x in data):
        #print('case2')
        if len(data) != len(labels):
            print(f"⚠️ Warning: {context} has {len(data)} values but {len(labels)} labels. Aligning row to labels.")
        df = pd.DataFrame([data[:len(labels)]], columns=labels)
    # Case 3: list of lists
    elif isinstance(data[0], (list, tuple)):
        #print('case3')
        rows = []
        for i, row in enumerate(data, start=1):
            #print(len(row),len(labels),row)
            if len(row) > len(labels):
                print(f"⚠️ Warning: Row {i} in {context} has {len(row)} values but {len(labels)} labels. Truncating.")
                row = row[:len(labels)]
            elif len(row) < len(labels):
                print(f"⚠️ Warning: Row {i} in {context} has {len(row)} values but {len(labels)} labels. Padding with None.")
                row = list(row) + [None] * (len(labels) - len(row))
            rows.append(row)
        df = pd.DataFrame(rows, columns=labels)
    else:
        #print('case4')
        df = pd.DataFrame(columns=labels)

    # Apply transpose if requested
    if transpose:
        if df.shape[0] == 1:
            # Single row → make vertical
            df = df.T.reset_index()
            df.columns = ["Field", "Value"]
        else:
            # Multi-row → use melt but safe column names
            df = df.reset_index().melt(id_vars=["index"], var_name="Field", value_name="TransposedValue")
            df = df.drop(columns=["index"])

    return df


def json_to_excel(json_path, excel_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sheets = {}

    # Metadata
    if "metadata" in data:
        #sheets["Metadata"] = pd.DataFrame(list(data["metadata"].items()), columns=["Field", "Value"])
        sheets["Metadata"] = make_dataframe(list(data["metadata"].items()), ["Field", "Value"], context="Metadata", transpose=False)
    #print(f'Metadata done')

    # Header
    if "header" in data:
        #labels = data["header"].get("columnLabel", [])
        labels = [c["name"] if isinstance(c, dict) else c for c in data["header"].get("columnLabel", [])]
        rows = data["header"].get("columnData", [])
        sheets["Header"] = make_dataframe(rows, labels, context="Header")
    #print(f'Header done')

    # Part A (General Info)
    if "partA" in data:
        #labels = data["partA"].get("columnLabel", [])
        labels = [c["name"] if isinstance(c, dict) else c for c in data["partA"].get("columnLabel", [])]
        rows = data["partA"].get("columnData", [])
        #sheets["GeneralInfo"] = make_dataframe(rows, labels, context="GeneralInfo")
        sheets["GeneralInfo"] = make_dataframe(rows, labels, context="GeneralInfo", transpose=True)
    #print(f'Part A done')

    # Part B
    counter = 1
    if "partB" in data:
        for section in data["partB"].get("sections", []):
            all_rows = []
            all_rows.append([section.get('title')])
            all_rows.append([])
            for idx, element in enumerate(section.get("elements", []), start=1):
                title = element.get("title", f"Element{idx}")
                # L2 summary
                if "l2" in element:
                    all_rows.append([element.get('title')])
                    labels = element["l2"].get("columnLabel", [])
                    #labels = [c["name"] if isinstance(c, dict) else c for c in element["l2"].get("columnLabel", [])]
                    rows = element["l2"].get("columnData", [])
                    #print('...................................')
                    if labels:
                        #l2_df = make_dataframe(rows, labels, context=f"{title}_L2")
                        all_rows.append(labels)
                        for ro in rows:
                            all_rows.append(ro)
                        all_rows.append([])                        

                # L1 transactions
                if "l1" in element:
                    all_rows.append([element.get('l1Src')])
                    #labels = [col["name"] for col in element["l1"].get("columnLabel", [])]
                    labels = [c["name"] if isinstance(c, dict) else c for c in element["l1"].get("columnLabel", [])]
                    rows = element["l1"].get("columnData", [])
                    if labels:
                        #l1_df = make_dataframe(rows, labels, context=f"{title}_L1")
                        all_rows.append(labels)
                        for ro in rows:
                            all_rows.append(ro)
                        all_rows.append([])

                # Special case when there is no L2 or L1!
                # Part B3-Information relating to payment of taxes
                if "l2" not in element and "l1" not in element:
                    labels = element.get("columnLabel", [])  
                    rows = element.get("columnData", [])                      
                    if labels and rows:
                        all_rows.append(labels)
                        for ro in rows:
                            all_rows.append(ro)
                        all_rows.append([])

            sheets[f"Section_{counter}"] = pd.DataFrame(all_rows)
            counter += 1

    # Save Excel
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False, header=False)

    print(f"Excel file created: {excel_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_json> [output_excel]")
        sys.exit(1)

    input_json = Path(sys.argv[1])
    output_excel = Path(sys.argv[2]) if len(sys.argv) > 2 else input_json.with_suffix(".xlsx")

    json_to_excel(input_json, output_excel)
