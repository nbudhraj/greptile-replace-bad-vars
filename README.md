# Greptile Take Home: Variable Refactoring 

## Background 
In software development, code readability and maintainability are critical for efficient collaboration and long-term project health. Poorly named variables can hinder these aspects, making it difficult to understand and maintain the codebase. Often times as a developer, myself, I have no idea how to name my variables. I had a college professor once tell me the hardest part about programming is coming up with good variable names. As a result, I wanted to address this issue by leveraging the Greptile API for code analysis and generating a script to apply suggested improvements.

## Solution 

The solution involves developing a Python script that interacts with the Greptile API to automate the process of improving code quality. It first indexes a specified repository and branch to prepare it for analysis. Once indexing is complete, the script queries the API to identify poorly named variables and suggests better names. It then generates a Python script that you would run at the root of your repo that replaces these variables in the codebase with the suggested names.

Input: remote, repo name, branch
Output: python script

So, essentially a python script that generates another python script :smile:

## How to run

### **Prerequisites**
1. **Python 3.7 or higher:** Make sure you have Python 3.7+ installed on your system.
2. **Pip:** Ensure `pip` is installed to manage Python packages.
3. **Virtual Environment (Optional but recommended):** Create and activate a virtual environment to keep dependencies isolated.

### Step 1: Clone the Repository
```bash
  git clone https://github.com/nbudhraj/greptile-replace-bad-vars.git
```

### Step 2: Install Required Python Packages
```bash
  pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables**
- Create a `.env` file in the same directory as the script.
- Add the following environment variables to the `.env` file:

  ```plaintext
  GREPTILE_API_KEY=your_greptile_api_key
  GITHUB_TOKEN=your_github_token
  ``` 
- Replace your_greptile_api_key and your_github_token with your actual Greptile API key and GitHub token.

### Step 4: Run the Script
- To run the script, use the following command:

```bash
   python3 refactor.py
```

Note: You may need to modify the prompt to ensure that no additional text is returned when querying. We expect to get back a string we can convert to an array.

### Step 5: Run the Replacement Script
- A generated replacement python script will be generated as output 
- Place this script in the root of your local copy of the remote repository and run it

## Demo
(FYI does not run this fast, I edited for brevity LOL)
[![Replace Bad Vars](https://img.youtube.com/vi/M7Dj3GfaT6A/0.jpg)](https://youtu.be/M7Dj3GfaT6A "Replace Bad Vars")



## Improvements
So many things to improve about this tool as it is far from perfect...where to even begin

1. Testing/Validation: Need to come up with comprehensive unit tests to properly validate that this tool will actually work. Testing has been limited to my own repositories, which may not reflect the complexity of production-scale projects.
2. Scalibility: This code will not perform well with larger repos, it will be quite slow and the manual generation of the replacement script may not scale well.
3. Prompt: I wished I could spend more time enhancing the prompt I used for my query. I experimented quite a bit but again need to validate that this is the best possible prompt that I could use.
4. Code Maintainability: The code is definitely monolithic and could benefit from being broken into smaller, modular functions or classes

## API Feedback
1. In the API documentation, it might be nice to have a section explaining the core difference between /query and /search. When I was reading the documentation of both, in my head, I was thinking, "couldn't I manipulate /query to give me back the same response I would get in /search." I'm sure it would be very difficult to do that, but highlighting the power of using one over the other would be helpful.
2. Real-time Github Updates: I ran into an interested edge-case where I updated the name of one of the repos in Github and when I tried hitting /repositories with the new repo name, I got a 404 because it could not find the repo. I used the old repo name instead and it worked. About 10-15 minutes later, the new repo name was picked up. I'm assuming this may be an issue with Github's APIs as opposed to Greptile, but an interesting edge-case to point out.  
3. Overall I thought using Greptile was very straightforward and barely ran into any issues with the APIs!

## Other Ideas
### Repo Structure Refactoring 
Initially, I wanted to develop a tool that would suggest an optimized repository structure (filesystem)and automatically handle the migration from the old setup to the new one. (I struggle with how to structure my code, so I thought it would be cool to build a tool for this!) However, from experimenting with the query API, it appears that a similarity search is being performed using vector embeddings. When hitting the query API, I'm assuming we're receiving a set number of similar vector embeddings. As a result, using Greptile to generate the entire directory structure of a codebase may not be practical in this context.

### Code Heatmap
I wanted to develop a tool to track which parts of a codebase have been modified the most over time. This would help identify sections that may need revisiting or updating, and offer insights into which parts of the codebase are most critical or frequently interacted with. With my personal repositories, I don't think that would've been very easy to build because I unfortunately do not have large codebases in my repos.

## Tools Used
- GPT-4
- Claude-3.5 


