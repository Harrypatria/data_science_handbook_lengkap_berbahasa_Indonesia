# Notebooks & Solusi Kode

**Handbook Data Science & AI**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-Educational-0A66C2?style=flat-square)](#)
[![Reproducible](https://img.shields.io/badge/Reproducible-Seed%2042-2EA44F?style=flat-square)](#disiplin)

> Folder terpisah dari handbook (PDF). Berisi latihan syntax dari setiap module dari Handbook Data Science and AI.
> Free handbook on www.convergeni.com

---

## Struktur

| Jenis | Konten | Keterangan |
| :--- | :--- | :--- |
| **Notebooks** | `modul-02` … `modul-15b` | Kode yang dijalankan untuk menghasilkan angka & grafik di handbook |
| **Full-stack** | `modul-17` … `modul-19` | Proyek multi-file (backend, frontend, Docker, CI) |

Modul yang tidak tercantum (0, 1, 2B, 12B, 16, 17B) bersifat konseptual atau sudah tercakup penuh di teks handbook.

---

## Notebook per Modul

| Modul | File | Klien CDC | Fokus |
| :---: | :--- | :--- | :--- |
| **2** | [`modul-02-manipulasi-data-statistik-deskriptif.ipynb`](modul-02-manipulasi-data-statistik-deskriptif.ipynb) | PT Ritel Sentosa | Online Retail (UCI), missing value, mean vs median |
| **3** | [`modul-03-visualisasi-data-matplotlib-seaborn.ipynb`](modul-03-visualisasi-data-matplotlib-seaborn.ipynb) | PT Ritel Sentosa | 180 gerai sintetis, sumbu jujur vs dipotong, Matplotlib vs Seaborn |
| **4** | [`modul-04-statistik-inferensial-correlation-ab-testing.ipynb`](modul-04-statistik-inferensial-correlation-ab-testing.ipynb) | Bank Arta Nusantara | Korelasi, A/B test, Monte Carlo p-value, peeking |
| **5** | [`modul-05-regresi-statistik-statsmodels.ipynb`](modul-05-regresi-statistik-statsmodels.ipynb) | Bank Arta Nusantara | OLS, VIF, inference vs prediction |
| **6** | [`modul-06-ml-supervised-regression-crisp-dm.ipynb`](modul-06-ml-supervised-regression-crisp-dm.ipynb) | PT Komponen Jaya | CRISP-DM regresi, MAE/RMSE/R², data leakage |
| **7** | [`modul-07-ml-supervised-klasifikasi-crisp-dm.ipynb`](modul-07-ml-supervised-klasifikasi-crisp-dm.ipynb) | Bank Arta Nusantara | Klasifikasi `gagal_bayar`, imbalance, ROC/PR-AUC, cost-based threshold |
| **8** | [`modul-08-ml-unsupervised-clustering-crisp-dm.ipynb`](modul-08-ml-unsupervised-clustering-crisp-dm.ipynb) | PT Ritel Sentosa | RFM clustering, elbow, silhouette, segmentasi |
| **9** | [`modul-09-reinforcement-learning-dasar.ipynb`](modul-09-reinforcement-learning-dasar.ipynb) | Konseptual | Q-learning, kurva belajar 500 episode |
| **10** | [`modul-10-optimisasi-riset-operasi.ipynb`](modul-10-optimisasi-riset-operasi.ipynb) | PT Komponen Jaya | Linear programming, daerah layak, kendala aktif |
| **11** | [`modul-11-analisis-jaringan-networkx.ipynb`](modul-11-analisis-jaringan-networkx.ipynb) | PT Komponen Jaya | Graf 43 node, centrality, simulasi kegagalan |
| **12** | [`modul-12-pengenalan-deep-learning-pytorch.ipynb`](modul-12-pengenalan-deep-learning-pytorch.ipynb) | Reproduksi Modul 7 | NN dari nol, training loop, learning rate |
| **13** | [`modul-13-nlp-analisis-teks-bisnis.ipynb`](modul-13-nlp-analisis-teks-bisnis.ipynb) | Talenta Prima | Sastrawi, TF-IDF, sentimen 70 ulasan, keterbatasan negasi |
| **14** | [`modul-14-computer-vision-dasar-opencv.ipynb`](modul-14-computer-vision-dasar-opencv.ipynb) | PT Komponen Jaya | Sobel, Canny, sistem QC komponen |
| **15** | [`modul-15-causal-ai.ipynb`](modul-15-causal-ai.ipynb) | Bank Arta Nusantara | Confounder, selection bias |
| **15B** | [`modul-15b-etika-privasi-bias-ai.ipynb`](modul-15b-etika-privasi-bias-ai.ipynb) | Bank Arta Nusantara | Fairness audit, disparate impact, FNR |

---

## Dependencies

**Base:** `pandas` · `numpy` · `matplotlib`

| Modul | Tambahan |
| :---: | :--- |
| 3 | `seaborn` |
| 4 | `scipy` · `statsmodels` |
| 5 · 6 · 7 · 8 · 12 · 13 · 15B | `scikit-learn` |
| 11 · 15 | `networkx` |
| 12 | `torch` |
| 13 | `Sastrawi` |
| 14 | `opencv-python` |
| 15 | `statsmodels` |

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels scikit-learn networkx torch Sastrawi opencv-python jupyter
```

<div align="center">
Remember: Every expert was once a beginner. Your programming journey is unique, and we're here to support you every step of the way.

## 🌟 Support This Project
**Follow me on GitHub**: [![GitHub Follow](https://img.shields.io/github/followers/Harrypatria?style=social)](https://github.com/Harrypatria?tab=followers)
**Connect on LinkedIn**: [![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/harry-patria/)

Click the buttons above to show your support!

</div>
