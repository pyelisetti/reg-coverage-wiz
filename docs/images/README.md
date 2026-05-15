# Architecture Diagrams

This directory contains professional architecture diagrams for the Regulatory Test Coverage Analyzer.

## 🎨 Generate Diagrams

To create the diagram images:

```bash
# From project root
cd /Users/Prashanth/Documents/senslytics/github/mock-data/coverage-analyzer

# Install Pillow if needed
pip3 install Pillow

# Generate all diagrams
python3 generate-diagrams.py
```

## 📊 Generated Files

After running the generator, this directory will contain:

- `architecture-high-level.png` / `.jpg` - Complete system architecture
- `data-flow-diagram.png` / `.jpg` - Three-phase processing pipeline
- `aws-deployment.png` / `.jpg` - AWS EC2 deployment details
- `ai-comparison.png` / `.jpg` - AI semantic analysis vs keyword matching
- `security-layers.png` / `.jpg` - Multi-layer security architecture

## 📐 Specifications

- **Resolution**: 1920 x 1080 pixels (Full HD)
- **Formats**: PNG (lossless) and JPEG (95% quality)
- **Design**: Professional with clean white background
- **Color Scheme**: Blue, Green, Orange accents

## 📝 Documentation

See parent directory documentation:
- `../GENERATE_DIAGRAMS.md` - Detailed generation guide
- `README-DIAGRAMS.md` - Diagram catalog and usage
- `../ARCHITECTURE.md` - Main architecture documentation
- `../DIAGRAMS_GENERATED.md` - Quick start summary

---

**Note**: Images are generated programmatically and should be regenerated after any architecture changes.
