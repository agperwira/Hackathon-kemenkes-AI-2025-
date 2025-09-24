import pandas as pd
import joblib
import streamlit as st

import requests
import json

model = joblib.load("isolation_forest_stroke.pkl")
scaler = joblib.load("scaler.pkl")

# Kolom kategorikal sesuai dataset
cat_cols = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]

# Label Encoder yang sama (harus konsisten dengan training)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
def input_data():
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=0, max_value=120, value=45)
    hypertension = st.selectbox("Hypertension", [0, 1])
    heart_disease = st.selectbox("Heart Disease", [0, 1])
    ever_married = st.selectbox("Ever Married", ["Yes", "No"])
    work_type = st.selectbox("Work Type", ["Private", "Self-employed", "Govt_job", "children", "Never_worked"])
    residence_type = st.selectbox("Residence Type", ["Urban", "Rural"])
    avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=100.0)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0)
    bmi = weight / ((height / 100) ** 2)
    smoking_status = st.selectbox("Smoking Status", ["formerly smoked", "never smoked", "smokes", "Unknown"])
    
    new_data = pd.DataFrame([{
        "gender": gender,
        "age": age,
        "hypertension": hypertension,
        "heart_disease": heart_disease,
        "ever_married": ever_married,
        "work_type": work_type,
        "Residence_type": residence_type,
        "avg_glucose_level": avg_glucose_level,
        "bmi": bmi,
        "smoking_status": smoking_status
    }])
    return new_data

def preprocess_input(data):
    # Encode kategori
    for col in cat_cols:
        data[col] = le.fit_transform(data[col].astype(str))

    # Scaling
    scaled_data = scaler.transform(data)

    return scaled_data

# ======================
def prediction(scaled_data):
    pred = model.predict(scaled_data)[0]
    if pred == 1:
        st.success("✅ Hasil Prediksi: Normal (1)")
    else:
        st.error("⚠️ Hasil Prediksi: Anomali (−1)")
# ======================

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
def analyze_risk_with_llm(new_data):
    """
    Mengirim data pasien ke LLM melalui OpenRouter untuk analisis risiko stroke.

    Args:
        new_data (pd.DataFrame): DataFrame yang berisi data pasien.

    Returns:
        dict: Output JSON berisi analisis risiko dan rekomendasi, atau None jika gagal.
    """
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY tidak ditemukan di environment variables.")
        return None

    # Mengambil baris pertama dari DataFrame untuk kemudahan akses
    patient_data = new_data.iloc[0].to_dict()

    # --- Membuat Prompt yang Terstruktur ---
    # Prompt ini menginstruksikan LLM untuk bertindak sebagai asisten medis dan
    # menghasilkan output dalam format JSON yang spesifik.
    system_prompt = """
    Anda adalah seorang asisten medis AI yang dikembangkan oleh Kementerian Kesehatan Republik Indonesia.
    Tugas utama Anda adalah menganalisis data medis dasar untuk mengidentifikasi faktor risiko stroke dan memberikan rekomendasi kesehatan.
    Anda harus selalu memprioritaskan keamanan dan akurasi informasi.
    Penting: Hasil analisis Anda **hanya boleh** dalam format JSON. Anda tidak diizinkan menambahkan teks lain di luar objek JSON.
    Anda harus menggunakan bahasa yang jelas, ringkas, dan mudah dipahami oleh masyarakat umum.
    """
    prompt = f"""
    Anda adalah asisten medis AI yang ahli dalam menganalisis faktor risiko stroke.
    Anda akan diberikan data medis dasar dari seorang pasien.
    Tugas Anda adalah:
    1.  Melakukan analisis risiko awal berdasarkan data yang diberikan.
    2.  Memberikan generalisasi rekomendasi yang berfokus pada perubahan gaya hidup.
    3.  Output harus dalam format JSON.

    Data Pasien:
    - Jenis Kelamin: {patient_data.get('gender', 'tidak diketahui')}
    - Usia: {patient_data.get('age', 'tidak diketahui')} tahun
    - Hipertensi: {'Ya' if patient_data.get('hypertension') else 'Tidak'}
    - Penyakit Jantung: {'Ya' if patient_data.get('heart_disease') else 'Tidak'}
    - Status Pernikahan: {patient_data.get('ever_married', 'tidak diketahui')}
    - Tipe Pekerjaan: {patient_data.get('work_type', 'tidak diketahui')}
    - Tipe Tempat Tinggal: {patient_data.get('Residence_type', 'tidak diketahui')}
    - Rata-rata Kadar Glukosa: {patient_data.get('avg_glucose_level', 'tidak diketahui')}
    - BMI: {patient_data.get('bmi', 'tidak diketahui')}
    - Status Merokok: {patient_data.get('smoking_status', 'tidak diketahui')}

    Silakan berikan analisis Anda dalam format JSON dengan dua kunci utama:
    "analisis_risiko_awal" dan "generalisasi_rekomendasi".
    """

    # --- Konfigurasi Payload untuk OpenRouter API ---
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data_payload = {
        "model": "gpt-oss-20b:free", # Menggunakan contoh model GPT OSS
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "system", "content": system_prompt}
        ],
        "response_format": {"type": "json_schema"}
    }

    try:
        # --- Mengirim Permintaan ke API OpenRouter ---
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data_payload
        )

        # Memastikan respons berhasil
        response.raise_for_status()

        # Mengurai respons JSON
        result = response.json()
        llm_output = result['choices'][0]['message']['content']

        # Mengubah string JSON dari LLM menjadi objek Python
        # Kadang-kadang LLM bisa menambahkan teks di luar JSON,
        # jadi perlu penanganan khusus.
        try:
            json_output = json.loads(llm_output)
            return json_output
        except json.JSONDecodeError:
            print("Peringatan: Output LLM bukan format JSON murni. Mengurai manual.")
            # Di sini bisa ditambahkan logika untuk membersihkan string
            # Misalnya, mencari bagian string yang dimulai dan diakhiri dengan '{' dan '}'
            start_idx = llm_output.find('{')
            end_idx = llm_output.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_string_clean = llm_output[start_idx:end_idx+1]
                try:
                    return json.loads(json_string_clean)
                except json.JSONDecodeError:
                    print("Gagal mengurai string JSON setelah pembersihan.")
                    return None
            return None

    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat menghubungi OpenRouter: {e}")
        return None