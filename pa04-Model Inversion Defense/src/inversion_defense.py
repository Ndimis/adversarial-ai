import numpy as np

class PrivacyGuard:
    def __init__(self, epsilon=0.1):
        """
        Epsilon controls the privacy/utility trade-off. 
        Lower epsilon = More Privacy (More Noise).
        """
        self.epsilon = epsilon

    def apply_differential_privacy(self, prediction_vector):
        """
        Adds Laplacian noise to the output probabilities to prevent inversion.
        """
        # Generate noise based on the epsilon value
        noise = np.random.laplace(0, 1/self.epsilon, len(prediction_vector))
        perturbed_output = prediction_vector + noise
        
        # Re-normalize so it still sums to 1 (like a real probability)
        exp_output = np.exp(perturbed_output)
        return exp_output / exp_output.sum()

    def secure_output(self, raw_prediction):
        """
        Standardizes the output to hide exact floating-point values.
        """
        # Step 1: Add Noise
        safe_probs = self.apply_differential_privacy(raw_prediction)
        
        # Step 2: Rounding to reduce precision for attackers
        return np.round(safe_probs, 2).tolist()

if __name__ == "__main__":
    guard = PrivacyGuard(epsilon=0.5)
    
    # Raw output from a hypothetical model [Cat, Dog, Bird]
    raw_output = np.array([0.95, 0.04, 0.01])
    
    secure_output = guard.secure_output(raw_output)
    
    print(f"Raw Model Output:    {raw_output}")
    print(f"Privacy-Safe Output: {secure_output}")