# 🎨 Architecture Diagram Generator

## Overview

This guide explains how to generate professional architecture diagrams as PNG and JPEG images for the Coverage Analyzer documentation.

## Prerequisites

### Install Python Pillow Library

```bash
# Using pip3
pip3 install Pillow

# Or using pip
pip install Pillow

# Verify installation
python3 -c "from PIL import Image; print('Pillow installed successfully!')"
```

## Generate Diagrams

### Step 1: Navigate to Project Directory

```bash
cd /Users/Prashanth/Documents/senslytics/github/mock-data/coverage-analyzer
```

### Step 2: Run the Generator

```bash
python3 generate-diagrams.py
```

### Expected Output

```
🎨 Architecture Diagram Generator
==================================================
✓ PIL/Pillow is available
✓ Output directory created: docs/images

Generating diagrams...

✓ Generated: docs/images/architecture-high-level.png
✓ Generated: docs/images/architecture-high-level.jpg

✓ Generated: docs/images/data-flow-diagram.png
✓ Generated: docs/images/data-flow-diagram.jpg

✓ Generated: docs/images/aws-deployment.png
✓ Generated: docs/images/aws-deployment.jpg

✓ Generated: docs/images/ai-comparison.png
✓ Generated: docs/images/ai-comparison.jpg

✓ Generated: docs/images/security-layers.png
✓ Generated: docs/images/security-layers.jpg

==================================================
✅ All diagrams generated successfully!
📁 Output directory: docs/images
```

## Generated Diagrams

After running the script, you will have the following diagrams:

### 1. **High-Level Architecture** (`architecture-high-level.png/.jpg`)
- Shows complete system architecture
- User browser → EC2 → Claude API flow
- Component breakdown
- Security and configuration layers

### 2. **Data Flow Diagram** (`data-flow-diagram.png/.jpg`)
- Phase 1: File upload & parsing
- Phase 2: AI analysis (the brain)
- Phase 3: Results visualization
- Processing timeline (15-45 seconds)

### 3. **AWS Deployment** (`aws-deployment.png/.jpg`)
- EC2 instance configuration
- Security groups
- Deployment stack (PM2, Node.js, environment)
- Cost and capacity estimates

### 4. **AI Comparison** (`ai-comparison.png/.jpg`)
- Traditional keyword matching vs AI semantic understanding
- Side-by-side examples
- Why AI achieves 95%+ accuracy
- Visual comparison with ✗ and ✓ marks

### 5. **Security Layers** (`security-layers.png/.jpg`)
- Four-layer security architecture
- Infrastructure → Application → API → Data
- API key management
- Security best practices

## Diagram Specifications

- **Resolution**: 1920 x 1080 pixels (Full HD)
- **Format**: PNG (lossless) and JPEG (95% quality)
- **Color Scheme**: 
  - Primary Blue: #2563eb
  - Secondary Green: #10b981
  - Accent Orange: #f59e0b
  - Clean white background
- **Professional Design**: Rounded corners, shadows, clear typography

## Output Directory Structure

```
coverage-analyzer/
├── docs/
│   └── images/
│       ├── architecture-high-level.png
│       ├── architecture-high-level.jpg
│       ├── data-flow-diagram.png
│       ├── data-flow-diagram.jpg
│       ├── aws-deployment.png
│       ├── aws-deployment.jpg
│       ├── ai-comparison.png
│       ├── ai-comparison.jpg
│       ├── security-layers.png
│       └── security-layers.jpg
```

## Using the Diagrams

### In Markdown Documentation

```markdown
![High-Level Architecture](docs/images/architecture-high-level.png)

![Data Flow](docs/images/data-flow-diagram.png)

![AWS Deployment](docs/images/aws-deployment.png)

![AI Comparison](docs/images/ai-comparison.png)

![Security Layers](docs/images/security-layers.png)
```

### In HTML

```html
<img src="docs/images/architecture-high-level.png" alt="High-Level Architecture" width="100%">
```

### In Presentations

- Use PNG for presentations (lossless quality)
- Use JPEG for web/email (smaller file size)

## Troubleshooting

### Issue: "PIL/Pillow not available"

**Solution:**
```bash
pip3 install Pillow
```

### Issue: "Permission denied"

**Solution:**
```bash
chmod +x generate-diagrams.py
python3 generate-diagrams.py
```

### Issue: "No module named 'PIL'"

**Solution:**
```bash
# Uninstall old PIL if exists
pip3 uninstall PIL

# Install Pillow
pip3 install Pillow
```

### Issue: Font rendering issues

The script automatically falls back to system default fonts if custom fonts are not available. The diagrams will still be generated with default fonts.

## Customization

### Change Colors

Edit the color constants at the top of `generate-diagrams.py`:

```python
PRIMARY_COLOR = "#2563eb"  # Blue
SECONDARY_COLOR = "#10b981"  # Green
ACCENT_COLOR = "#f59e0b"  # Orange
```

### Change Resolution

Edit the size constants:

```python
WIDTH = 1920
HEIGHT = 1080
```

For 4K output:
```python
WIDTH = 3840
HEIGHT = 2160
```

### Add New Diagrams

Add a new function in the script:

```python
def generate_my_diagram():
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Your drawing code here
    
    img.save("docs/images/my-diagram.png", "PNG")
    img.save("docs/images/my-diagram.jpg", "JPEG", quality=95)

# Call it in main()
def main():
    # ... existing code ...
    generate_my_diagram()
```

## Image Quality Guidelines

### PNG Files
- Use for: Documentation, GitHub README, presentations
- Pros: Lossless quality, transparent backgrounds (if needed)
- Cons: Larger file size (~500KB - 2MB)

### JPEG Files
- Use for: Emails, web pages, quick sharing
- Pros: Smaller file size (~100KB - 400KB)
- Cons: Slight compression artifacts (minimal at 95% quality)

## Integration with Documentation

The generated diagrams are automatically referenced in:
- `ARCHITECTURE.md` - All diagrams embedded
- `README.md` - Selected diagrams for quick reference
- GitHub repository - Visual documentation

## Next Steps

1. Generate the diagrams: `python3 generate-diagrams.py`
2. Review the output in `docs/images/`
3. Update documentation with image references
4. Commit to git (images are not in .gitignore for documentation purposes)

---

**Note**: The diagrams are designed to be professional and presentation-ready. They can be used in:
- Technical documentation
- Stakeholder presentations
- Architecture review meetings
- Deployment guides
- Training materials
