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

# Internal specification

### Textual description
**src/app.py**  
Contains the definitions of the App and MetricsPanel classes. App is the main class of the system, and it contains objects of other classes. The App constructor creates the dpg context, in which functions to create and update plots and metrics are called. MetricsPanel contains functions used to update and display the values of individual metrics.

**src/axis.py**  
Contains the definitions of the Axis, Entity, Point, and Threshold classes. Axis includes functions for drawing the axis, generating random points and handling interactions with all points. Entity is the base class from which Point and Threshold inherit. Point contains functions for drawing, updating, inverting, deleting and changing the position of a given point on the axis. Threshold contains functions for drawing the threshold and changing its position.

**src/data.py**  
Contains the definition of the Data class. This class includes variables that store all necessary data, functions for handling it and updating displayed objects.

**src/metrics.py**  
Contains the definition of the Metrics class. This class includes functions that return the sum of all true positives, true negatives, false positives, and false negatives, as well as functions to calculate all kinds of metrics.

**src/plots.py**  
Contains the definitions of the PlotCurve, PlotMatrix, and Value classes. PlotCurve includes functions for drawing and updating ROC curve, as well as saving it to a PNG file. PlotMatrix class contains functions for drawing and updating the confusion matrix. Value is used to display text as a name-value pair or the value itself.

**src/utils.py**  
Contains the definition of a function to generate random points.

### Dependencies
All required libraries are included in the **requirements.txt** file and can be installed with the command:
    
    pip install -r requirements.txt

### Running the application
To run the application with the command, enter:

    python run.py

### Deployment
To bundle into a single platform specyfic executable, run:
    
    pyinstaller -F -w run.py

### Testing
All unit tests are included in **tests/unit_tests**. To run them use the commands listed below.

    python -m pytest .\tests\unit_tests\data_test.py
    
    python -m pytest .\tests\unit_tests\metrics_test.py
    
    python -m pytest .\tests\unit_tests\utils_test.py
    
## Credits
The team working on the project consisted of the following people:  

*Filip Tomeczek - Team Leader  
Anna Mrukwa - Analyst, Programmer  
Olaf Jaskuła - QA Manager, Tester  
Dominik Zagórnik - Software Architect  
Artur Oleksiński - Lead Developer, Programmer  
Błażej Kołodziej - Technical Writer  
Patryk Piwowarczyk - Administrator  
Piotr Vassev - Programmer, Tester  
Marcel Król - Programmer, Tester*

## License
The project has been created under the MIT License.
    
