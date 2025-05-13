# Generative AI

```
Generative AI is a type of artificial intelligence that can create new content by learning patterns from existing data.

- It generates new content instead of just analyzing or responding to input.

- It's called generative because it generates content.
```

To achieve this, we describe what we want using a prompt — a detailed instruction or input. Generative AI tools respond to these prompts by summarizing complex information, answering questions, or generating creative content like text, stories, code, images, and more.

---

## How Generative AI Works?

At the core of `Generative AI` lie complex alghorithms, often based on neural networks, that learn a given dataset's underlying patterens and structures. This learning process allows the model to capture the data's statistical properties, enabling it to generate new samples that exhibit similar chracteristics.

The process typically involves:

1. **Traning:** The model is trained on large dataset of examples, such as text, images, or music. During traning model learns the statistical relationship between diffrent elements in the data, capturing the pattrens and structures that define the data's chracterstics.

2. **Genration:**  Once trained, the model can generate new content by sampling from the learned distribution. IT based on the learned pattrens until a satisfactory output is produced.

3. **Evaluation:** The generated content is often evaluated based on its quality, originality, and resumblance to human-generated output. This evaluation can be subjective, relying on human judgment, or objective, using metrics that measure specific properties of the generated content.

---

### 🔹 **Types of Generative AI Models**

1. **Generative Adversarial Networks (GANs):**

   * Two competing networks: generator vs. discriminator.
   * Produces highly realistic content.

2. **Variational Autoencoders (VAEs):**

   * Compress data into latent space for controlled generation.
   * Effective in capturing data structure.

3. **Autoregressive Models:**

   * Generate content sequentially (e.g., word by word).
   * Common in text generation.

4. **Diffusion Models:**

   * Add noise and learn to reverse it to generate new data.
   * Used for high-quality image synthesis.

---

### 🔹 **Key Generative AI Concepts**

* **Latent Space:**
  A compressed representation of data used to generate new samples.

* **Sampling:**
  Drawing from learned distributions to produce varied and realistic outputs.

* **Mode Collapse:**
  Generator produces limited variations, reducing output diversity.

* **Overfitting:**
  Model memorizes training data, harming generalization and creativity.

---

### 🔹 **Evaluation Metrics**

* **Inception Score (IS):**
  Measures clarity and diversity of images.

* **Fréchet Inception Distance (FID):**
  Compares generated vs. real image distributions (lower is better).

* **BLEU Score (for text):**
  Assesses similarity between generated and reference text.

---

However, sometimes AI may produce answers that sound correct but are actually incorrect — this is called `"hallucination."`

The quality of the outcome depends on both the data the model was trained on and the prompt given to the AI