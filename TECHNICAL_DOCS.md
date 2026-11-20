# PulseFederate: Technical Documentation

## 1. System Architecture
PulseFederate uses a hub-and-spoke Federated Learning architecture:
- **Hospital Nodes (Clients):** Run local training on their private data. Raw data never leaves the node.
- **Central Aggregator (Server):** Orchestrated by Flower. Receives only model weights, performs Weighted FedAvg, and sends the global model back.
- **Backend API:** FastAPI service that manages the simulation, serves the dashboard, and exposes REST endpoints.
- **Frontend Dashboard:** Next.js application for public health officials to monitor training and risk heatmaps.

## 2. Dataset Assumptions & Privacy
- **Synthetic Data:** For this prototype, we generate synthetic tabular data representing EHRs (Age, BMI, Blood Pressure, Glucose, Smoking). 
- **Abu Dhabi Context:** The synthetic data generator is explicitly modeled on the UAE's epidemiological profile. It simulates a population with high obesity rates (mean BMI ~29-31) and a realistic chronic disease baseline (approx. 13% high-risk). 
- **Data Heterogeneity (non-IID):** We simulate 3 sites. Site A and B are urban (2000 patients each). Site C is a smaller rural clinic (1000 patients) with slightly higher BMI baselines to test model fairness.
- **Data Minimization:** The system is architected so that no raw patient records are ever transmitted.
- **Differential Privacy:** We implement DP-SGD (Gradient Clipping + Gaussian Noise) to prevent reverse-engineering of patient data from model weights.

## 3. Clinical Boundaries
- **Decision Support Only:** The system outputs community-level risk probabilities and fairness scores. It is not a diagnostic tool and does not make automated clinical decisions.
- **Fairness Monitoring:** We track per-site accuracy disparity. If a specific hospital node (e.g., the rural clinic) is underperforming, the system flags it, ensuring the global model does not silently fail minority populations.

## 4. Limitations & Phase 2 Roadmap
- **Byzantine Robustness:** The current implementation uses standard Weighted FedAvg. A malicious node could attempt model poisoning. Phase 2 will implement Krum or Trimmed-Mean aggregation.
- **Strict Privacy Accounting:** The current `privacy.py` uses a simplified RDP approximation. Phase 2 will integrate Opacus for strict (ε, δ)-DP accounting.
- **Real-World Integration:** The current prototype runs on synthetic CSVs. Phase 2 will integrate HL7 FHIR APIs to connect to real hospital EHR systems (like Abu Dhabi's Malaffi).