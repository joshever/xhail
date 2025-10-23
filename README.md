# XHAIL: Python Implementation of eXtended Hybrid Abductive-Inductive Learning.

**XHAIL** is a Python-based framework that implements a hybrid approach to logic programming, combining abductive, deductive, and inductive reasoning. It is designed to infer logical rules from background knowledge and examples, facilitating tasks such as knowledge discovery and machine learning.

## 🔍 Overview

The XHail framework processes three main components:

* **Background Knowledge (B)**: A set of logical facts and rules that provide context.
* **Examples (E)**: Observations or data points that the system aims to explain.
* **Hypotheses (H)**: Logical rules or explanations inferred from the background knowledge and examples.

The system employs a compression heuristic that prefers hypotheses with fewer literals, promoting simplicity and interpretability.

## ⚙️ Components

The repository is structured into several directories:

* `xhail/`: Contains the core implementation of the XHail framework.
* `tests/`: Includes some personal tests to validate the functionality of the system.
* `play/`: Provides example logic programs and test cases.

## 🧪 Example Usage

To utilize the XHail framework, you can create a logic program in a `.lp` file and process it using the `xhail.py` script. Here's an example:

1. Create a file named `example.lp` with the following content:

   ```prolog
   %% example.lp
   %%%%%%%%%%%%%%
   
   bird(X) :- penguin(X).
   bird(a).
   bird(b).
   bird(c).
   penguin(d).
   
   #modeh flies(+bird).
   #modeb penguin(+bird).
   #modeb not penguin(+bird).
   
   #example flies(a).
   #example flies(b).
   #example flies(c).
   #example not flies(d).
   ```

2. Run the `xhail.py` script to process the logic program:

   ```bash
   python xhail.py example.lp
   ```

This will output the inferred hypotheses based on the background knowledge and examples provided.

## 🛠️ Installation

To install and use XHail:

1. Clone the repository:

   ```bash
   git clone https://github.com/joshever/xhail.git
   cd xhail
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push to your fork.
5. Submit a pull request detailing your changes.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
