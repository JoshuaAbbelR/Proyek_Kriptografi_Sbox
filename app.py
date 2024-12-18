import streamlit as st
import pandas as pd
from sbox_functions import validate_sbox, nonlinearity, sac, bic_nl, lap, dap

st.title("S-Box Verification Tool")
st.write("Upload file S-Box dalam format Excel untuk memulai verifikasi.")

# Upload file
uploaded_file = st.file_uploader("Upload File S-Box (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=None)
    sbox = df.values.flatten().tolist()

    st.write("Data S-Box yang diunggah:")
    st.dataframe(df)

    # Validasi S-Box
    is_valid, message = validate_sbox(sbox)
    if not is_valid:
        st.error(message)
    else:
        st.success(message)

        # Pilihan operasi
        operations = [
            "Nonlinearity (NL)",
            "Strict Avalanche Criterion (SAC)",
            "Bit Independence Criterion (BIC-NL)",
            "Linear Approximation Probability (LAP)",
            "Differential Approximation Probability (DAP)",
        ]
        selected_ops = st.multiselect("Pilih Operasi", operations)

        # Jalankan operasi
        if st.button("Jalankan Operasi"):
            results = {}
            n = 8
            if "Nonlinearity (NL)" in selected_ops:
                results["Nonlinearity"] = nonlinearity(sbox, n, n)
            if "Strict Avalanche Criterion (SAC)" in selected_ops:
                results["SAC"] = sac(sbox, n)
            if "Bit Independence Criterion (BIC-NL)" in selected_ops:
                results["BIC-NL"] = bic_nl(sbox, n)
            if "Linear Approximation Probability (LAP)" in selected_ops:
                results["LAP"] = lap(sbox, n)
            if "Differential Approximation Probability (DAP)" in selected_ops:
                results["DAP"] = dap(sbox, n)

            st.write("Hasil Operasi:")
            st.json(results)

            # Download hasil
            if st.button("Download Hasil"):
                result_df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])
                st.download_button(
                    "Download Excel",
                    result_df.to_excel(index=False),
                    file_name="sbox_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )