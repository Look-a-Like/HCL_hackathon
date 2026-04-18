# Interview Preparation — HCL Hackathon (Senior Software Engineer 1, AI/ML)

Questions will be spontaneous and based on your work. Be ready to defend every choice you make in code, architecture, and design.

---

## 1. Your Project — "Defend What You Built"

These will be the most common and most important questions.

- Walk me through what you built and what business problem it solves.
- Why did you choose this specific problem to solve?
- What dataset did you use, and why is it representative of the business problem?
- What was the first thing you threw away after trying it?
- If you had 2 more days, what would you change?
- What assumptions did you make that you couldn't validate?
- How does this scale beyond the hackathon demo?

---

## 2. Machine Learning — Concepts & Decisions

### Model Selection
- Why did you choose this model over alternatives? (e.g., XGBoost vs neural net, logistic regression vs SVM)
- What are the bias-variance tradeoffs in your model?
- How did you handle overfitting? Underfitting?
- What cross-validation strategy did you use and why?
- How did you decide on hyperparameters — grid search, random search, Bayesian optimization?

### Feature Engineering
- What features did you engineer and why?
- How did you handle missing values? Why that method specifically?
- How did you handle categorical variables?
- Did you normalize/standardize? Why or why not?
- How did you detect and handle outliers?

### Model Evaluation
- What metric did you optimize for? Why that metric and not another? (accuracy vs F1 vs AUC-ROC vs RMSE)
- How do you know your model isn't just memorizing the training data?
- What's your train/val/test split strategy?
- How would you explain your model's performance to a non-technical stakeholder?

### Model Optimization
- How did you reduce inference latency?
- What techniques did you use for feature selection?
- Did you try ensemble methods? What was the result?
- How would you monitor model drift in production?

---

## 3. Data Pipelines

- Describe your data pipeline from raw input to model output.
- How do you handle dirty/corrupted data in the pipeline?
- What happens when a new batch of data has a different schema than expected?
- How would you make this pipeline production-grade? (idempotency, retries, monitoring)
- What tools/frameworks would you use for orchestration at scale? (Airflow, Prefect, dbt)
- How do you version your datasets? Why does that matter?
- What's the difference between batch processing and streaming? Which did you use and why?

---

## 4. AI Solution Design (Stakeholder Framing)

- How did you translate the business problem into an ML problem?
- What did you ask stakeholders before writing a single line of code?
- How do you decide when a rule-based system is better than ML?
- A stakeholder says "just build a model that predicts X." What's your first response?
- How do you communicate model uncertainty to a non-technical audience?
- Your model is 87% accurate. Is that good enough? How do you answer that?

---

## 5. Dashboards & Reporting

- What visualization library/tool did you use and why?
- What's the most important metric on your dashboard, and why is it front and center?
- How do you decide what to show vs. what to hide from a business user?
- How would you make this dashboard refresh with new data automatically?
- What's the difference between a good dashboard and a cluttered one?

---

## 6. System Design — AI at Scale

These test whether you can think beyond the hackathon.

- How would you serve this model to 10,000 concurrent users?
- Where does your model live — embedded in the app, REST API, batch job? Why?
- How would you A/B test two versions of your model in production?
- What does a CI/CD pipeline for ML look like? (CI for model training, CD for deployment)
- How do you handle model versioning and rollback?
- Explain the difference between online learning and batch retraining. When do you use each?
- What's feature drift vs. concept drift? How do you detect it?

---

## 7. Python & Engineering Craft

- How do you structure a Python ML project for maintainability? (src layout, notebooks vs scripts)
- What's the difference between `fit`, `transform`, and `fit_transform` in sklearn?
- How do you handle memory when processing a dataset that doesn't fit in RAM?
- What's vectorization and why does it matter for ML code performance?
- When do you use a generator vs. loading everything into memory?
- How do you write a unit test for a machine learning function?
- What is `pickle` and when should you NOT use it for model serialization?

---

## 8. Latest AI Trends (HCL Expects You to Know These)

Be ready to have an opinion, not just recite facts.

- **LLMs in enterprise** — How would you integrate an LLM into a business analytics pipeline? What are the risks?
- **RAG (Retrieval-Augmented Generation)** — What is it? When would you use it over fine-tuning?
- **Vector databases** — What problem do they solve? (Pinecone, Chroma, FAISS)
- **MLOps maturity** — What does a mature MLOps setup look like vs. a scrappy one?
- **Responsible AI** — How do you detect and mitigate bias in your model?
- **AutoML** — When is it useful? When is it a crutch?
- **Multimodal models** — What's the current state and where is it headed?
- **Edge AI** — What does deploying ML on edge devices require?

---

## 9. HCL-Specific Context

- HCLTech serves Financial Services, Manufacturing, Life Sciences, Healthcare, Telecom — which of these does your solution apply to, and how would you adapt it for another vertical?
- HCL emphasizes "co-innovation with clients" — how did your hackathon approach demonstrate that mindset?
- HCL's ESG goal: net-zero by 2040. How could AI/ML contribute to that? Can your project tie into it?
- HCL is a global company. How would you adapt your solution for different regulatory environments (GDPR, HIPAA)?

---

## 10. Behavioral Questions (STAR format: Situation, Task, Action, Result)

- Tell me about a time you had to explain a technical concept to a non-technical stakeholder.
- Describe a time a model you built didn't work. What did you do?
- Tell me about a time you disagreed with a technical decision on your team. How did you handle it?
- Give an example of when you had to prioritize speed over quality. Was it the right call?
- How do you stay current with AI/ML research? Give a recent example you applied.

---

## 11. Quick-Fire Concepts — Know These Cold

| Concept | Be Ready To Explain |
|---------|---------------------|
| Precision vs Recall | Trade-off, when to prioritize which |
| L1 vs L2 regularization | Effect on coefficients, when to use each |
| Gradient descent variants | SGD, mini-batch, Adam — differences |
| Attention mechanism | Intuition behind transformers |
| ROC-AUC | What it measures, what 0.5 and 1.0 mean |
| Confusion matrix | All 4 quadrants and what they cost |
| Curse of dimensionality | Why it matters for ML |
| Transfer learning | When and why to use pretrained models |
| SHAP / LIME | Explainability — why it matters in enterprise |
| Data leakage | How it happens, how to prevent it |

---

## 12. The One Question You Must Nail

**"Why should we hire you over someone with more years of experience?"**

Your answer: point to what you built in this hackathon — working code, a live demo, a real decision defended with data. That beats a CV.

---

*Update this file as you build — add questions you got asked, answers that worked, concepts you had to look up.*
