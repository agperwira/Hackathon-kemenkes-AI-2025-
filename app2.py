import streamlit as st
import time
from utils import input_data, preprocess_input, prediction, analyze_risk_with_llm
import datetime as dt


# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="StrokeScan - Skrining Stroke Berbasis AI",
    page_icon="🧠",
    layout="wide",
)

# --- Judul dan Deskripsi Aplikasi ---
st.title("🧠 StrokeScan: Solusi AI untuk Skrining Stroke Dini")
st.markdown("Sebuah inisiatif dari Kemenkes untuk membantu masyarakat Indonesia mendeteksi risiko stroke secara mandiri menggunakan teknologi AI canggih.")

# --- Tab Navigasi ---
tab1, tab2, tab3, tab4 = st.tabs(["Beranda", "Mulai Skrining", "Tentang Kami", "Deteksi Anomali"])

with tab1:
    st.header("Selamat Datang di StrokeScan")
    st.write("Stroke adalah penyebab kematian utama di Indonesia. Deteksi dini adalah kunci untuk mengurangi dampaknya. StrokeScan hadir untuk membantu Anda dan orang terdekat mengenali gejala awal dengan cepat.")
    
    st.image("https://images.unsplash.com/photo-1549488344-933e146a48d8?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", caption="Deteksi dini stroke dapat menyelamatkan nyawa.")
    
    st.subheader("Bagaimana Cara Kerjanya?")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Ganti dengan video demo proyek
    st.markdown("1. **Isi Kuesioner Risiko:** Jawab pertanyaan tentang riwayat kesehatan Anda.")
    st.markdown("2. **Analisis Wajah & Suara:** Lakukan tes singkat melalui kamera untuk mendeteksi gejala visual dan ucapan.")
    st.markdown("3. **Dapatkan Hasil:** Sistem kami akan memberikan estimasi risiko dan rekomendasi langkah selanjutnya.")

with tab2:
    st.header("Mulai Skrining Mandiri")
    st.warning("Peringatan: Alat ini bukan pengganti diagnosis medis profesional. Jika Anda atau orang terdekat mengalami gejala stroke, segera hubungi layanan darurat.")

    # --- Bagian Kuesioner (Sesuai dengan kriteria 'Predictive Risk Model') ---
    st.subheader("1. Kuesioner Risiko")
    riwayat_penyakit = st.multiselect(
        "Apakah Anda memiliki riwayat berikut?",
        ["Hipertensi", "Diabetes", "Obesitas", "Merokok"]
    )
    usia = st.slider("Berapa usia Anda?", 18, 100)
    
    # --- Tombol untuk memulai tes AI ---
    st.subheader("2. Tes Analisis AI")
    if st.button("Mulai Tes Visual & Suara"):
        with st.spinner('Mempersiapkan kamera dan mikrofon...'):
            time.sleep(3) # Simulasi loading
        
        st.success("Kamera dan mikrofon siap!")
        
        # --- Placeholder untuk modul AI (Analisis Wajah & Suara) ---
        st.markdown("### Tes Analisis Wajah")
        st.write("Silakan arahkan wajah ke kamera dan ikuti instruksi. Tersenyumlah selebar mungkin.")
        # Di sini, Anda akan menempatkan kode untuk integrasi model Computer Vision
        st.info("Fitur ini akan menganalisis simetri wajah Anda.")

        st.markdown("### Tes Analisis Suara")
        st.write("Ucapkan kalimat berikut dengan jelas: 'Langit biru dan awan putih.'")
        # Di sini, Anda akan menempatkan kode untuk integrasi model Speech Recognition
        st.info("Fitur ini akan menganalisis pola bicara Anda.")

        # --- Bagian Hasil (Sesuai kriteria 'Interoperability with MoH's data standard') ---
        with st.spinner('Menganalisis hasil...'):
            time.sleep(5) # Simulasi analisis
            
        st.balloons()
        st.subheader("Hasil Skrining Anda:")
        st.metric(label="Skor Risiko Stroke", value="Rendah", delta_color="inverse")
        st.success("Berdasarkan analisis, risiko stroke Anda saat ini tergolong rendah. Tetap jaga pola hidup sehat!")
        
        # Contoh jika risiko tinggi
        # st.metric(label="Skor Risiko Stroke", value="Tinggi")
        # st.error("Risiko stroke Anda tergolong tinggi. Kami sangat menyarankan Anda untuk segera berkonsultasi dengan dokter.")
        
        st.markdown("---")
        st.markdown("### Rekomendasi Selanjutnya")
        st.write("Silakan kunjungi fasilitas kesehatan terdekat untuk pemeriksaan lebih lanjut atau hubungi **call center Kemenkes**.")
        st.success("Tersambung dengan sistem SatuSehat Kemenkes.")

with tab3:
    st.header("Tentang Kami")
    st.markdown("Tim kami terdiri dari profesional di bidang kesehatan dan engineer AI yang berdedikasi untuk menciptakan solusi teknologi guna meningkatkan kualitas kesehatan masyarakat Indonesia.")
    st.image("https://images.unsplash.com/photo-1549488344-933e146a48d8?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D") # Ganti dengan foto tim Anda

    st.subheader("Visi Kami")
    st.write("Mewujudkan Indonesia yang lebih sehat dan produktif melalui inovasi teknologi yang inklusif dan mudah diakses oleh semua lapisan masyarakat.")

    st.subheader("Tim Pengembang")
    st.markdown("- **[Nama Anggota 1]** - Peran (Contoh: Data Scientist)")
    st.markdown("- **[Nama Anggota 2]** - Peran (Contoh: Dokter Umum)")
    st.markdown("- **[Nama Anggota 3]** - Peran (Contoh: Backend Engineer)")
    st.markdown("- **[Nama Anggota 4]** - Peran (Contoh: UI/UX Designer)")
    st.markdown("- **[Nama Anggota 5]** - Peran (Contoh: Project Manager)")

with tab4:
    st.header("Anomaly Detection untuk Skrining Stroke")
    st.warning("Peringatan: Alat ini bukan pengganti diagnosis medis profesional. Jika Anda atau orang terdekat mengalami gejala stroke, segera hubungi layanan darurat.")

    st.write("Gunakan model Isolation Forest untuk mendeteksi anomali pada data pasien yang mungkin mengindikasikan risiko stroke.")
    st.markdown("Silakan masukkan data pasien di bawah ini dan klik 'Prediksi' untuk melihat hasilnya.")

    st.subheader("Input Data Pasien")
    # Input data
    user_data = input_data()

    if st.button("Prediksi", key="predict_button"):
        # Preprocess
        scaled_data = preprocess_input(user_data)

        # Prediction
        prediction(scaled_data)
    st.markdown("---")
    st.subheader("Analisis Risiko dengan gambar dan suara")
    if st.button("Mulai Tes Visual & Suara", key="ai_test_button"):
        with st.spinner('Mempersiapkan kamera dan mikrofon...'):
            time.sleep(3) # Simulasi loading
        st.warning('fitur ini belum dibuat sepenuhnya, dan ini bukan pengganti diagnosis medis profesional. Jika Anda atau orang terdekat mengalami gejala stroke, segera hubungi layanan darurat.')
        
        st.success("Kamera dan mikrofon siap!")
        
        # --- Placeholder untuk modul AI (Analisis Wajah & Suara) ---
        st.markdown("### Tes Analisis Wajah")
        st.write("Silakan arahkan wajah ke kamera dan ikuti instruksi. Tersenyumlah selebar mungkin.")
        # Di sini, Anda akan menempatkan kode untuk integrasi model Computer Vision
        st.info("Fitur ini akan menganalisis simetri wajah Anda.")

        st.markdown("### Tes Analisis Suara")
        st.write("Ucapkan kalimat berikut dengan jelas: 'Langit biru dan awan putih.'")
        # Di sini, Anda akan menempatkan kode untuk integrasi model Speech Recognition
        st.info("Fitur ini akan menganalisis pola bicara Anda.")

        # --- Bagian Hasil (Sesuai kriteria 'Interoperability with MoH's data standard') ---
        with st.spinner('Menganalisis hasil...'):
            time.sleep(5) # Simulasi analisis
            
        st.balloons()
        st.subheader("Hasil Skrining Anda:")
        st.metric(label="Skor Risiko Stroke", value="Rendah", delta_color="inverse")
        st.success("Berdasarkan analisis, risiko stroke Anda saat ini tergolong rendah. Tetap jaga pola hidup sehat!")
        
        # Contoh jika risiko tinggi
        # st.metric(label="Skor Risiko Stroke", value="Tinggi")
        # st.error("Risiko stroke Anda tergolong tinggi. Kami sangat menyarankan Anda untuk segera berkonsultasi dengan dokter.")
        
        st.markdown("---")
        st.markdown("### Rekomendasi Selanjutnya")
        st.write("Silakan kunjungi fasilitas kesehatan terdekat untuk pemeriksaan lebih lanjut atau hubungi **call center Kemenkes**.")
        st.success("Tersambung dengan sistem SatuSehat Kemenkes.")

    st.subheader("Analisis Risiko dengan LLM")
    
    if st.button("Analisis Risiko dengan LLM", key="llm_analysis_button"):
        with st.spinner('Mengirim data ke LLM untuk analisis risiko...'):
            time.sleep(3) # Simulasi loading

        llm_result = analyze_risk_with_llm(user_data)
        if llm_result:
            st.subheader("Hasil Analisis Risiko dari LLM:")
            st.warning("Hasil ini bersifat informatif dan tidak menggantikan diagnosis medis profesional.")
            st.json(llm_result)
        else:
            st.error("Gagal mendapatkan respons dari LLM. Silakan coba lagi nanti.")
    st.sidebar.info("⚠️ Ini skrining awal, bukan diagnosis. Darurat? Hubungi 119.")