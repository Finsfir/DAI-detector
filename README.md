## Documentation:

### Tech stack:
    1. I use Open CV for working with images and video
    2. I use Image AI as YOLO v3 framework for object detection
        GitHub: https://github.com/OlafenwaMoses/ImageAI/
    3. I use openpyxl for writing Excel files
    4. I use PyQT as User Interface
    5. Deploy via py2exe
    
### Deployment environment:
As packet manager I use Anaconda. Firstly create an environment:
    <pre><code>
    conda create -n "environment-name" --file requirements.txt
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

## If you need trained YOLO model, you can take ask me
