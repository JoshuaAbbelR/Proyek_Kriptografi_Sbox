import streamlit as st
import pandas as pd
from io import BytesIO
import tempfile
from sbox_functions import validate_sbox, nonlinearity, sac, bic_nl, calculate_bic_sac, lap, dap

st.title("S-Box Verification Tool")
st.write("Unggah file S-Box dalam format Excel untuk memulai verifikasi.")

# Upload file
uploaded_file = st.file_uploader("Upload File S-Box (Excel)", type=["xlsx"])

if uploaded_file:
    # Baca file Excel dan konversi ke daftar
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
            "Bit Independence Criterion - NL (BIC-NL)",
            "Bit Independence Criterion - SAC (BIC-SAC)",
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
            if "Bit Independence Criterion - NL (BIC-NL)" in selected_ops:
                results["BIC-NL"] = bic_nl(sbox, n)
            if "Bit Independence Criterion - SAC (BIC-SAC)" in selected_ops:
                results["BIC-SAC"] = calculate_bic_sac(sbox)
            if "Linear Approximation Probability (LAP)" in selected_ops:
                results["LAP"] = lap(sbox, n)
            if "Differential Approximation Probability (DAP)" in selected_ops:
                results["DAP"] = dap(sbox, n)

            st.write("Hasil Operasi:")
            st.json(results)

            # Download hasil menggunakan BytesIO
            result_df = pd.DataFrame(list(results.items()), columns=["Metric", "Value"])
            
            # Gunakan BytesIO untuk membuat file Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                result_df.to_excel(writer, index=False, sheet_name="S-Box Results")
            processed_data = output.getvalue()

            st.download_button(
                label="Download Excel",
                data=processed_data,
                file_name="hasil_sbox.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            # Alternatif: Download menggunakan file sementara
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                with pd.ExcelWriter(tmp_file.name, engine="openpyxl") as writer:
                    result_df.to_excel(writer, index=False, sheet_name="S-Box Results")
                tmp_file.seek(0)  # Pastikan file dibaca dari awal
                st.download_button(
                    label="Download Excel (Alternatif)",
                    data=open(tmp_file.name, "rb").read(),
                    file_name="hasil_sbox_alt.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
