## Documentation:

### Tech stack:
    1. I use Open CV for working with images and video
    2. I use Image AI as YOLO v3 framework for object detection
        GitHub: https://github.com/OlafenwaMoses/ImageAI/
    3. I use openpyxl for writing Excel files
    4. I use PyQT as User Interface
    5. Deploy via py2exe
    
### Deployment environment:
As packet manager i use Anaconda. Firstly create an environment:
    <pre><code>
    conda create -n ImageAI -c anaconda keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0 jupyter
    </code></pre>
Next import Tensorflow:
    <pre><code>
    pip install tensorflow==2.4.0
    </code></pre>
    <pre><code>
    pip install tensorflow-gpu==2.4.0
    </code></pre>
Check for updates:
    <pre><code>
    pip install imageai --upgrade
    </code></pre>
Now install libraries:
    <pre><code>
    pip install pandas
    </code></pre>
    <pre><code>
    pip install openpyxl
    </code></pre>
    <pre><code>
    pip install pyqt5
    </code></pre>
    <pre><code>
    pip install pyqt5-tools
    </code></pre>
    <pre><code>
    pip install py2exe
    </code></pre>
    
    
## Annotating Data:
I use the labelImg annotation tool:
https://github.com/tzutalin/labelImg#hotkeys

### First cascade detect classes below:
- DAI - the workspace of DAI

### Second cascade detect classes below:

- cMCH - the center of the micron clock hand
- eMCH - the edge of the micron clock hand
- mmWS - mm clock face workzone
- mmCH - mm clock hand
