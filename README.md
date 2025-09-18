# INFO 5940 
Welcome to the INFO 5940 repository. You will complete your work using [**GitHub Codespaces**](#about-github-codespaces) and save your progress in your own GitHub repository. This guide will walk you through setting up the development environment and running the test notebook.  

## Getting Started 

### Step 1: Fork this repository 
1. Click the **Fork** button (top right of this page).
2. This will create a copy of the repo under **your own GitHub account**.

Forking creates a personal copy of the repo under **your** GitHub account.  
- You can commit, push, and experiment freely.  
- Your work stays separate from the official class materials.

### Step 2: Open your forked repo Codespace
1. Go to **your forked repo**.
2. Click the green **Code** button and switch to the **Codespaces** tab.  
3. Select **Create Codespace**.
4. Wait a few minutes for the environment to finish setting up.

### Step 3: Verify your environment 
Once the Codespace is ready: 
1. Open `test.ipynb` in your codespace.
2. Install the Python 3.11.13 Kernel.  In the top-right corner, click **Select Kernel**.
    1. If **Install/Enable suggested extensions Python + Jupyter** appears, select it, and wait for the install to finish before moving on to the next step.
    2. Select **Python Environments** choose **Python 3.11.13 (first option)**.
3. Run the first code block to check your setup. You should see `openai` import successfully.

## About GitHub Codespaces

[Codespaces](https://docs.github.com/en/codespaces) is a complete software development and execution environment, running in the cloud, with its primary interface being a VSCode instance running in your browser.

Codespaces is not free, but their per-month [free quota](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces#free-quota) is generous.  Codespaces is free under the [GitHub Student Developer Pack](https://education.github.com/pack#github-codespaces).

### Codespaces Tips

* Codespaces keep running even when you close your browser (but will time out and stop after a while)
* Unless you're on a free plan, or within your free quota, costs acrue while the codespace is running, whether or not you have it open in your browser or are working on it
* You can control when it's running, and the space it takes up.  Check out [GitHub's codespaces lifecycle documentation](https://docs.github.com/en/codespaces/about-codespaces/understanding-the-codespace-lifecycle)

## Sync Updates 
To make sure your personal forked repository stays up to date with the original class repository, please follow these steps:
1. Open your forked repo.
2. At the top of the page, you should see a banner or menu option that shows whether your fork is behind the original repo.
3. Click the **Sync fork** button.
4. In the dropdown, choose **Update branch** to pull the latest changes from the original repo into your fork.

## Troubleshooting
- The Jupyter extension should install automatically. If you still cannot select a Python kernel on Jupyter Notebook: Go to the left sidebar >> **Extensions** >> search for **Jupyter** >> reload window (or reinstall it).   
