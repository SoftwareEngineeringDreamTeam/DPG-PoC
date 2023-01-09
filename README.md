# ROC’n’ROLL

## Project description
Application ROC’n’ROLL is a data visualization tool for better insight into the classifying model results. The tool allows the user to manually add and edit the responses of a classifier or load their own data file with the results and check what the possible changes in the values configuration introduce to the metrics scores. The plot is interactive, allowing to freely change the points position, labels, and their occurrence on the plot.

## Dependencies
    
    pip install -r requirements.txt

## Deployment
To bundle into a single platform specyfic executable, run:
    
    pyinstaller -F -w run.py
