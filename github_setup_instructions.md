# GitHub Repository Setup Instructions

The Git repository has been successfully set up with the following details:

1. Repository: https://github.com/damolasolanke/Cross_Domain_Predictive_Analytics_Dashboard
2. All team members have dedicated branches:
   - `ade-system-integration` - For Ade's System Integration & Real-Time Analytics work
   - `rujeko-frontend` - For Rujeko's Frontend Development work
   - `emmanuel-visualization` - For Emmanuel's Data Visualization work
   - `julie-api-integration` - For Julie's API Integration & Data Processing work
   - `chao-machine-learning` - For Chao's Machine Learning & Predictive Modeling work

## For Team Members

1. Clone the repository:
   ```
   git clone https://github.com/damolasolanke/Cross_Domain_Predictive_Analytics_Dashboard.git
   ```

2. Check out your assigned branch:
   ```
   git checkout YOUR-BRANCH-NAME
   ```
   
3. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. Make your changes, commit, and push regularly:
   ```
   git add .
   git commit -m "Descriptive commit message"
   git push origin YOUR-BRANCH-NAME
   ```

5. When your feature is complete, create a pull request to merge into the main branch.

## GitHub Authentication

Git has been configured to use a Personal Access Token for authentication, so you won't need to enter credentials each time you push.

Please refer to CONTRIBUTING.md for more information on the development workflow. 