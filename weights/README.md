# Model Weights Directory

This directory should contain the trained model weights for:

1. **Detection Model** (`Model_det_small/`)
   - `inference.json` - Model architecture definition
   - `inference.pdiparams` - Model parameters/weights

2. **Recognition Model** (`Model_rec/`)
   - `inference.json` - Model architecture definition
   - `inference.pdiparams` - Model parameters/weights

## Setup Instructions

### Option 1: Use Setup Script (Recommended)
```bash
cd /Users/macbook/Desktop/Kyanon/ocr_server
./setup_models.sh
```

### Option 2: Manual Copy
```bash
cd /Users/macbook/Desktop/Kyanon

# Copy detection model
cp -r Model_det_small ocr_server/weights/

# Copy recognition model
cp -r Model_rec ocr_server/weights/
```

## Verification

After copying, verify the structure:
```bash
cd weights
ls -la Model_det_small/
ls -la Model_rec/
```

You should see:
```
Model_det_small/
├── inference.json
└── inference.pdiparams

Model_rec/
├── inference.json
└── inference.pdiparams
```

## Notes

- Model files are NOT included in git (see `.gitignore`)
- Model files must be copied before running the server
- Detection model: PaddleOCR DBNet architecture
- Recognition model: CTC-based text recognition
- Both models use PaddlePaddle framework
- Models run on CPU by default
