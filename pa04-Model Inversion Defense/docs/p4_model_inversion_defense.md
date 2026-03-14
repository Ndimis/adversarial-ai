# Concept Explainer: Model Inversion Defense

### 🧠 The Core Concept
**Model Inversion** is a sophisticated adversarial attack where an attacker repeatedly queries an AI model to reconstruct the features of the sensitive data used during training. For example, by analyzing the confidence scores of a facial recognition AI, an attacker might be able to recreate a blurry but recognizable image of a person in the training set.

To defend against this, we implement **Output Perturbation** and **Differential Privacy (DP)** concepts:
1.  **Confidence Masking:** Hiding the raw, high-precision probability scores that attackers use to map the model's internal logic.
2.  **Noise Injection:** Adding "Laplacian Noise" to the output. This ensures that the results are statistically accurate but mathematically "noisy" enough to prevent reverse-engineering.
3.  **Precision Reduction:** Rounding decimal places to remove the granular data points that inversion algorithms rely on.



### 🛠️ Lessons Learned
1.  **The Privacy-Utility Trade-off:** There is no free lunch. Adding more noise (lower Epsilon) makes the model more secure but slightly less accurate. Finding the "sweet spot" is the key responsibility of an AI Security Engineer.
2.  **Membership Inference Mitigation:** Even if an attacker can't reconstruct a full record, they often try to guess if a specific individual was part of the training set. These defenses significantly raise the "cost" of such an attack.
3.  **Floating Point Vulnerabilities:** High-precision floating-point numbers are a goldmine for attackers. Simple rounding is often the most cost-effective first line of defense.

### 📝 Key Takeaway
> **A model is only as secure as its outputs.** In a production environment, raw model scores should never be exposed to untrusted users. By applying differential privacy, we ensure that the AI provides value without compromising the privacy of the individuals whose data built it.

### 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt