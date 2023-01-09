# ROC’n’ROLL

## Project description
Application ROC’n’ROLL is a data visualization tool for better insight into the classifying model results. The tool allows the user to manually add and edit the responses of a classifier or load their own data file with the results and check what the possible changes in the values configuration introduce to the metrics scores. The plot is interactive, allowing to freely change the points position, labels, and their occurrence on the plot.

## External specification

### Launching the application
The user can run the application using the .exe file. After starting the program, the application window should appear:

![Screen1](https://user-images.githubusercontent.com/105949530/211389910-c17566f8-2f0f-4c38-ac36-7221c8562cfa.png)

### Using the application
By using the appropriate buttons, the user can add a point to the axis, invert the classes of all existing points and generate a random set of points. By holding down the left mouse button, the user can change the position of the point on the axis. By clicking on the point with the right mouse button, a window will be displayed that allows to change the settings of this point.

Adding the new point:  

![Screen2](https://user-images.githubusercontent.com/105949530/211389922-d0dbbd69-dc17-46a2-9e58-00559041d984.png)

Changing the existing point:  

![Screen3](https://user-images.githubusercontent.com/105949530/211390149-8df31381-b279-4360-a95f-b09a58d82ce0.png)

Points can be loaded or saved by clicking on one of the buttons located in the upper left corner of the application. The following window should appear:

![Screen4](https://user-images.githubusercontent.com/105949530/211389986-0e21b6d4-3fd5-4157-9c74-e015c4ab151a.png)

### Dependencies
    
    pip install -r requirements.txt

### Deployment
To bundle into a single platform specyfic executable, run:
    
    pyinstaller -F -w run.py
