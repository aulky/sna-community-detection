# Social Network Analysis (SNA) — Community Detection
## Individual Assignment 3: Zachary Karate Club Network Analysis

Repositori ini berisi implementasi kode, eksperimen komparatif, visualisasi grafis, dan laporan akademis untuk **Individual Assignment 3** mata kuliah **Social Network Analysis (SNA)** dengan topik **Deteksi Komunitas (*Community Detection*)**.

Studi kasus menggunakan jaringan sosial klasik **Zachary Karate Club** (Wayne W. Zachary, 1977) untuk membandingkan tiga paradigma algoritma utama:
1. **Modularity Optimization:** Louvain Algorithm
2. **Information / Label Propagation:** Asynchronous Label Propagation Algorithm (LPA)
3. **Divisive Hierarchical:** Girvan-Newman Algorithm

---

## 📑 Daftar Isi
- [Struktur Repositori](#-struktur-repositori)
- [Tentang Dataset](#-tentang-dataset)
- [Algoritma yang Diimplementasikan](#-algoritma-yang-diimplementasikan)
- [Hasil Eksperimen & Evaluasi](#-hasil-eksperimen--evaluasi)
- [Interpretasi Hasil & Jawaban Pertanyaan Tugas](#-interpretasi-hasil--jawaban-pertanyaan-tugas)
- [Panduan Instalasi & Cara Menjalankan](#-panduan-instalasi--cara-menjalankan)
- [Daftar Pustaka](#-daftar-pustaka)

---


## 🥋 Tentang Dataset

Dataset **Zachary Karate Club** dikumpulkan oleh antropolog **Wayne W. Zachary (1977)** yang meneliti relasi pertemanan informal 34 anggota klub karate di sebuah universitas di Amerika Serikat. 

- **Jumlah Node ($N$):** 34 anggota klub.
- **Jumlah Edge ($M$):** 78 relasi pertemanan tanpa bobot (*unweighted*) dan tidak berarah (*undirected*).
- **Densitas Jaringan:** 0.1389.
- **Rata-rata Derajat:** 4.59.
- **Rata-rata Clustering Coefficient:** 0.5706.
- **Diameter Graf:** 5.
- **Average Shortest Path Length:** 2.4082.
- **Konteks Sejarah (*Ground Truth*):** Terjadi perselisihan internal antara instruktur karate (**Mr. Hi**, Node 1) dan administrator klub (**Officer John A**, Node 34) terkait kenaikan iuran. Konflik ini menyebabkan klub terpecah (*fission*) menjadi dua kelompok terpisah yang masing-masing beranggotakan 17 orang.

---

## 🔬 Algoritma yang Diimplementasikan

| Algoritma | Paradigma | Prinsip Kerja | Keunggulan |
| :--- | :--- | :--- | :--- |
| **Louvain** | Optimasi Modularitas | Heuristik *greedy* dua tahap yang memaksimalkan nilai fungsi objektif Newman-Girvan Modularity ($Q$). | Menemukan sub-kelompok dengan kepadatan relasi internal maksimal. |
| **Label Propagation (LPA)** | Propagasi Informasi | Setiap node secara iteratif mengadopsi label mayoritas tetangga terdekatnya hingga stabil. | Kompleksitas komputasi linear $\mathcal{O}(M)$, sangat cepat. |
| **Girvan-Newman** | Hierarki Divisif | Menghitung *Edge Betweenness Centrality* dan menghapus edge dengan nilai tertinggi secara berulang. | Mampu merekonstruksi struktur faksi hierarkis dan dendrogram pemotongan. |

---

## 📊 Hasil Eksperimen & Evaluasi

Tabel evaluasi kuantitatif dari seluruh metode terhadap *Ground Truth* faksi riil:

| Algoritma / Metode | Jumlah Komunitas ($k$) | Modularity ($Q$) | Distribusi Ukuran Komunitas | ARI vs Ground Truth | NMI vs Ground Truth | Akurasi Node |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ground Truth (Faksi Empiris)** | **2** | 0.3582 | [17, 17] | 1.0000 | 1.0000 | 100% |
| **Louvain Algorithm** | **4** | **0.4198** | [12, 11, 6, 5] | 0.4646 | 0.5878 | - |
| **Label Propagation (LPA)** | **4** | 0.3784 | [18, 11, 3, 2] | 0.6624 | 0.6527 | - |
| **Girvan-Newman (Optimal $Q$)** | **5** | 0.4013 | [12, 10, 6, 5, 1] | 0.3916 | 0.4851 | - |
| **Girvan-Newman ($k=2$ Cut)** | **2** | 0.3600 | [19, 15] | **0.7717** | **0.7324** | **97.06% (33/34)** |

---

## 💡 Interpretasi Hasil & Jawaban Pertanyaan Tugas

### 1. Berapa banyak komunitas yang berhasil dideteksi oleh masing-masing algoritma?
- **Ground Truth:** 2 faksi seimbang (Mr. Hi $= 17$, Officer $= 17$).
- **Louvain:** 4 komunitas (ukuran: 12, 11, 6, 5) dengan $Q = 0.4198$.
- **LPA:** 4 komunitas (ukuran: 18, 11, 3, 2) dengan $Q = 0.3784$.
- **Girvan-Newman (Optimal Modularity):** 5 komunitas pada titik modularitas puncak $k=5$ ($Q = 0.4013$), di mana Node 10 terisolasi sendirian (*singleton*).
- **Girvan-Newman (Pemotongan Faksi $k=2$):** 2 komunitas (ukuran: 19 dan 15) dengan $Q = 0.3600$.

### 2. Apakah pembagian komunitas yang dihasilkan masuk akal jika dikaitkan dengan konteks atau karakteristik dataset yang digunakan?
**Sangat masuk akal**, baik pada level makro (faksi politik sejarah) maupun mikro (sub-kelompok pertemanan):

1. **Kesesuaian Makro (Faksi Sejarah):**
   - Pemotongan **Girvan-Newman pada $k=2$** sangat masuk akal karena berhasil memprediksi faksi asli dengan akurasi **97.06% (33 dari 34 node benar)**, mencapai $\text{ARI} = 0.7717$ dan $\text{NMI} = 0.7324$.
2. **Anomali Node 9 yang Secara Topologi Sangat Rasional:**
   - Di sejarah, Node 9 bergabung dengan faksi Mr. Hi. Namun seluruh algoritma komputer (Louvain, LPA, Girvan-Newman) mengelompokkannya ke faksi Officer.
   - **Bukti Topologi:** Node 9 memiliki 5 relasi pertemanan. Hanya 2 relasi ke kubu Mr. Hi (Node 1, 3), sedangkan **3 relasi (60%) terhubung langsung ke pimpinan kubu Officer (Node 31, 33, 34)**. Secara aliran graf dan kedekatan struktural, Node 9 memang lebih terikat ke Officer. Perbedaannya di dunia nyata membuktikan adanya faktor laten non-topologis (seperti rasa hormat murid kepada guru karate).
3. **Kesesuaian Mikro (Sub-Cliques):**
   - Pembagian Louvain ($k=4$) dan Girvan-Newman optimal ($k=5$) masuk akal karena membedakan lingkaran pertemanan intim di dalam faksi besar:
     - Di kubu Mr. Hi: lingkar inti dojo vs lingkar luar mandiri yang sangat kompak (Node 5, 6, 7, 11, 17).
     - Di kubu Officer: lingkar kepengurusan vs kelompok sebaya (Node 24, 25, 26, 28, 29, 32).
     - Node 10 terisolasi menjadi *singleton* pada GN $k=5$ karena dua edge penghubungnya (ke Node 3 dan Node 34) adalah jembatan dengan nilai *edge betweenness* tertinggi yang dipotong terlebih dahulu.

---

## 🚀 Panduan Instalasi & Cara Menjalankan

### 1. Prasyarat Sistem
- Python >= 3.12
- Paket manajer `uv` (direkomendasikan) atau `pip` standar

### 2. Menyiapkan Lingkungan Virtual & Dependensi

Menggunakan **uv**:
```bash
# Sinkronisasi dependensi dari uv.lock
uv sync
```

Menggunakan **pip**:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r pyproject.toml
```

### 3. Menjalankan Jupyter Notebook
Tersedia dua file notebook:
- **`Individual_Assignment_3.ipynb`** — Notebook bersih tanpa narasi AI berlebih, khusus untuk dikumpulkan (seluruh sel sudah pre-executed).
- **`community_detection_zachary.ipynb`** — Notebook komprehensif lengkap dengan penjelasan metodologis dan eksplorasi data.

Jalankan notebook via terminal:
```bash
jupyter notebook Individual_Assignment_3.ipynb
```
atau buka langsung menggunakan ekstensi Jupyter di VS Code.

### 4. Menjalankan via Skrip Terminal (CLI Pipeline)
Untuk meregenerasi seluruh tabel hasil di folder `results/` dan grafik di folder `figures/`:
```bash
.venv\Scripts\python.exe main.py
```

### 5. Mengompilasi Ulang Laporan Word (.docx)
Untuk meregenerasi dokumen laporan Microsoft Word lengkap dengan gambar dan tabel:
```bash
.venv\Scripts\python.exe build_docx.py
```
File akan otomatis tersimpan di `Laporan_Tugas_3_SNA.docx`.

---

## 📚 Daftar Pustaka

1. **Zachary, W. W. (1977).** *An Information Flow Model for Conflict and Fission in Small Groups.* Journal of Anthropological Research, 33(4), 452–473.
2. **Girvan, M., & Newman, M. E. (2002).** *Community structure in social and biological networks.* Proceedings of the National Academy of Sciences (PNAS), 99(12), 7821–7826.
3. **Newman, M. E. (2004).** *Fast algorithm for detecting community structure in networks.* Physical Review E, 69(6), 066133.
4. **Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008).** *Fast unfolding of communities in large networks.* Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008.
5. **Raghavan, U. N., Albert, R., & Kumara, S. (2007).** *Near linear time algorithm to detect community structures in large-scale networks.* Physical Review E, 76(3), 036106.
6. **Kunegis, J. (2013).** *KONECT: The Koblenz Network Collection.* In Proceedings of the International Conference on World Wide Web Companion (WWW '13), 1343–1350.

---
**Author:** Zaki | Social Network Analysis 2025/2026
