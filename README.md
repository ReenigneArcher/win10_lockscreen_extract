# Win10 Lockscreen Extract

This is a Python 3 script that extracts Windows 10 lock screen images

## Requirement

- Windows 10
- Python 3

## How it works

1. A script looks for files in `~/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets/`
1. A script copies files whose dimensions are either 1920x1080 or 1080x1920
1. It automatically matches landscape and portrait pictures

## Usage

```batch
pip install -r requirements.txt
cd /d <script directory>
python3 extract.py
```

## To Do
- [ ] Add argument to only select portrait or landscape
- [ ] Use default config values if config.ini is not found current working directory
- [ ] Additional code cleanup
