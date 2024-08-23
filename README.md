# Greptile Take Home: Variable Refactoring 

## Problem Statement 

## Solution 

## How to run

### **Prerequisites**
1. **Python 3.7 or higher:** Make sure you have Python 3.7+ installed on your system.
2. **Pip:** Ensure `pip` is installed to manage Python packages.
3. **Virtual Environment (Optional but recommended):** Create and activate a virtual environment to keep dependencies isolated.

### **Step 1: Clone the Repository
```bash
  git clone https://github.com/nbudhraj/greptile-replace-bad-vars.git
```

### **Step 2: Install Required Python Packages
```bash
  pip install -r requirements.txt
```

### **Step 3: Set Up Environment Variables
1. Create a `.env` file in the same directory as the script
2. Add the following environment variables to the .env file:

### **Step 3: Set Up Environment Variables**
- Create a `.env` file in the same directory as the script.
- Add the following environment variables to the `.env` file:

  ```plaintext
  GREPTILE_API_KEY=your_greptile_api_key
  GITHUB_TOKEN=your_github_token
  ``` 
- Replace your_greptile_api_key and your_github_token with your actual Greptile API key and GitHub token.

### **Step 4: Run the Script**
- To run the script, use the following command:

```bash
   python3 refactor.py
```

## Demo


## Improvements

## API Feedback
Highlight the difference in response from query and search --> what that response would look like 
Response structure was unexpected

Interesting edge case: changed the repository name, indexing cannot find it!

Initial Idea: Directory Refactoring, cannot do that with the query APIS!

