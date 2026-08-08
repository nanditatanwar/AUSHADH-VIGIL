AI-Enabled Herb-Drug Interaction Analyzer
Predict and explain interactions between Ayurvedic medicines and modern drugs using open-source AI.

<img width="648" height="364" alt="image" src="https://github.com/user-attachments/assets/60616bca-7b12-491a-aa46-b5cf48719e41" />
<img width="691" height="358" alt="image" src="https://github.com/user-attachments/assets/18065fe1-d647-40a7-b769-42e11b14a70d" />
<img width="696" height="392" alt="image" src="https://github.com/user-attachments/assets/4dada547-6f4e-4eeb-a58a-e97257bf0072" />
<img width="750" height="391" alt="image" src="https://github.com/user-attachments/assets/64232154-3985-4ba7-b134-fed7878b9ec4" />
<img width="645" height="363" alt="image" src="https://github.com/user-attachments/assets/3521611e-0998-4a7d-aaf3-ad3132be4de9" />
<img width="645" height="363" alt="image" src="https://github.com/user-attachments/assets/0747964d-5219-4d58-b44c-7950c4313ba3" />



📖 Overview

Patients commonly take Ayurvedic medicines alongside modern pharmaceuticals, but herb-drug interactions (HDIs) can alter absorption, metabolism, efficacy, or safety. Traditional methods to identify HDIs are slow and expensive.

AUSHADH-VIGIL is a lightweight, 100% open-source AI platform that:

📚 Stores Ayurvedic herbs/formulations and modern drugs
🔮 Predicts herb-drug interaction probability and risk class
🧠 Explains the likely biological mechanism
🔍 Cross-checks predictions against published literature (PubMed/PMC)


✨ Features

1	Herb / Formulation Database	100+ Ayurvedic herbs and formulations with key constituents
2	Modern Drug Database	200+ generic drugs with targets, enzymes, transporters
3	Interaction Prediction Model	XGBoost / Random Forest classifier predicts interaction probability
4	Risk Classification	Low / Moderate / High risk badge based on predicted probability
5	Mechanism Explanation	SHAP-based explanation + known mechanism text
6	Literature Validation	Searches PubMed/PMC for published reports on the herb-drug pair
7	Interaction Checker UI	Web form: select herb + drug → result card with risk + explanation
8	Dashboard	Top interactions, risk distribution, search history
9	PDF Report Export	Simple PDF report of a checked pair



🧪 Example Use Case
Herb:   Ashwagandha (Withania somnifera)
Drug:   Warfarin

→ Risk Level        : HIGH
→ Probability       : 0.82
→ Mechanism         : Potential CYP3A4 / CYP2C9 interaction; may alter
                       anticoagulant effect
→ Key Features      : Shared CYP enzymes, structural similarity
→ Literature Status : 3 published case reports / studies found
→ Recommendation    : Monitor INR closely if co-administered
🏗️ Architecture
Ayurvedic Pharmacopoeia | PubChem | ChEMBL / DrugBank | PubMed/PMC | Manual curation
                                    │
                                    ▼
                       Cleaned datasets (herbs, drugs,
                       constituents, interactions)
                                    │
                                    ▼
                Feature Engineering (RDKit fingerprints,
                CYP enzyme overlap, transporter overlap,
                shared targets, Tanimoto similarity)
                                    │
                                    ▼
                    ML Model (XGBoost / Random Forest)
                        + SHAP explainability
                                    │
                                    ▼
                 FastAPI backend  ⇄  React + Vite frontend
🛠️ Tech Stack
Layer	Tools
Backend	FastAPI, Uvicorn, Pydantic, SQLAlchemy
Database	SQLite (default) or local PostgreSQL 16
ML / AI	scikit-learn, XGBoost, RDKit, SHAP, pandas
Data Sources	PubChem PUG-REST, ChEMBL API, DrugBank (open subset), Ayurvedic Pharmacopoeia, PubMed/PMC
Molecular Descriptors	RDKit (Morgan fingerprints, descriptors)
Frontend	React, Vite, Tailwind CSS, Recharts
Version Control	Git + GitHub
Environment	Python 3.11 venv, Node 20
📊 Machine Learning Approach
Target: interaction_exists (0 = no known interaction, 1 = potential/known interaction)
Features: Morgan molecular fingerprints, drug descriptors, shared CYP450 enzymes (CYP3A4/2D6/2C9), shared transporters (P-gp/OATP), shared biological targets, Tanimoto similarity, known literature flags
Model: XGBoost (primary), Random Forest (fallback for small datasets)
Evaluation: AUROC, precision, recall, F1, SHAP values

Risk categories:

Probability Range	Risk Level
0.00 – 0.30	🟢 Low
0.30 – 0.70	🟡 Moderate
0.70 – 1.00	🔴 High

🗄️ Database Schema
Table	Key Fields
herbs	id, name, sanskrit_name, constituents, category, source
constituents	id, herb_id, name, smiles, pubchem_cid, mol_features
drugs	id, name, generic_name, targets, enzymes, transporters
interactions	id, herb_id, drug_id, probability, risk_level, mechanism, evidence_count, literature_refs, created_at
literature_refs	id, herb_id, drug_id, title, source, url, year

🚀 Getting Started
Prerequisites
Python 3.11+
Node.js 20+
Git
Backend Setup
bash
git clone https://github.com/<your-org>/aushadh-vigil.git
cd aushadh-vigil/backend

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
Frontend Setup
bash
cd ../frontend
npm install
npm run dev
Database

SQLite is used by default (zero config). To use PostgreSQL instead, set DATABASE_URL in your .env file.



Future Scope
Molecular docking against CYP3A4, CYP2D6, CYP2C9
Personalized prediction based on patient genetics

⚠️ Disclaimer

AUSHADH-VIGIL is a research and educational prototype. It is not a substitute for professional medical advice, diagnosis, or treatment. Predictions should be validated by qualified healthcare professionals before any clinical use.

📄 License

This project is licensed under the MIT License. Data from PubChem, ChEMBL, and PubMed is public domain or permissively licensed. DrugBank data requires license review — use only the open subset, or ChEMBL as an alternative.

📚 References
Surana et al., 2021 — Current perspectives in herbal and conventional drug interactions based on clinical manifestations. Springer
Cytochrome P450 enzyme mediated herbal drug interactions (Part 2). PMC
Pharmacokinetic Interactions between Drugs and Botanical Dietary Supplements. PMC
Pandita et al., 2017 — Evaluation of herb-drug interaction of a polyherbal Ayurvedic formulation through high throughput CYP450 assay. ScienceDirect
Adverse drug reaction and concepts of drug safety in Ayurveda. PMC
ADR reporting in Ayurveda: National Pharmacovigilance Framework. Zenodo
CCRAS — Pharmacological Research
Frontiers — In vitro effect of Withania somnifera, AYUSH-64, and remdesivir on CYP-450 enzymes. Frontiers in Pharmacology

🔗Useful Links
PubChem PUG-REST
ChEMBL API
RDKit Docs
XGBoost Docs
SHAP Docs
FastAPI Docs
React + Vite
