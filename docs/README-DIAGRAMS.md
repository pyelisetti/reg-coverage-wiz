# 📊 Architecture Diagrams

## Overview

Professional, presentation-ready diagrams for the Regulatory Test Coverage Analyzer architecture documentation.

---

## 🎨 Available Diagrams

### 1. High-Level Architecture
![High-Level Architecture](images/architecture-high-level.png)

**File**: `images/architecture-high-level.png` / `.jpg`

**Description**: Complete system overview showing:
- User browser interface
- AWS EC2 instance with Node.js application
- AI integration layer
- Claude API connection
- Security and configuration components

**Use for**: Executive presentations, technical overview, onboarding documentation

---

### 2. Data Flow & Processing Pipeline
![Data Flow Diagram](images/data-flow-diagram.png)

**File**: `images/data-flow-diagram.png` / `.jpg`

**Description**: Three-phase processing pipeline:
- **Phase 1**: File upload & parsing
- **Phase 2**: AI analysis (the brain)
- **Phase 3**: Results visualization
- Processing timeline: 15-45 seconds

**Use for**: Technical documentation, process walkthroughs, troubleshooting guides

---

### 3. AWS Deployment Architecture
![AWS Deployment](images/aws-deployment.png)

**File**: `images/aws-deployment.png` / `.jpg`

**Description**: AWS infrastructure details:
- EC2 instance configuration (t3.medium)
- Security group setup
- Deployment stack (PM2, Node.js, environment)
- Cost estimates (~$35/month)
- Capacity metrics (50 concurrent users)

**Use for**: DevOps documentation, deployment planning, infrastructure reviews

---

### 4. AI Semantic Analysis Comparison
![AI Comparison](images/ai-comparison.png)

**File**: `images/ai-comparison.png` / `.jpg`

**Description**: Visual comparison:
- Traditional keyword matching (fails)
- AI semantic understanding (succeeds)
- Side-by-side examples with ✗ and ✓
- Why AI achieves 95%+ accuracy
- Advantages of Claude AI

**Use for**: Stakeholder presentations, sales materials, explaining the value proposition

---

### 5. Multi-Layer Security Architecture
![Security Layers](images/security-layers.png)

**File**: `images/security-layers.png` / `.jpg`

**Description**: Four-layer security model:
- **Layer 1**: Infrastructure (AWS VPC, security groups, IAM)
- **Layer 2**: Application (.env, file validation, CORS)
- **Layer 3**: API (HTTPS, authentication, rate limiting)
- **Layer 4**: Data (in-memory processing, no persistence)
- API key management best practices

**Use for**: Security reviews, compliance documentation, audit preparation

---

## 📐 Specifications

### Image Details
- **Resolution**: 1920 x 1080 pixels (Full HD)
- **Formats**: PNG (lossless) and JPEG (95% quality)
- **Color Scheme**:
  - Primary Blue: #2563eb
  - Secondary Green: #10b981
  - Accent Orange: #f59e0b
  - Clean white background
- **Design**: Professional with rounded corners, clear typography, visual hierarchy

### File Sizes
- **PNG files**: ~500KB - 2MB (lossless, for presentations)
- **JPEG files**: ~100KB - 400KB (optimized, for web/email)

---

## 🔧 Generating Diagrams

### Prerequisites

Install Python Pillow library:

```bash
# Using pip3
pip3 install Pillow

# Verify installation
python3 -c "from PIL import Image; print('Pillow installed!')"
```

### Generate All Diagrams

```bash
# Navigate to project directory
cd /Users/Prashanth/Documents/senslytics/github/mock-data/coverage-analyzer

# Run generator
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
```

### Troubleshooting

See [GENERATE_DIAGRAMS.md](../GENERATE_DIAGRAMS.md) for detailed instructions and troubleshooting.

---

## 📝 Usage in Documentation

### Markdown

```markdown
![High-Level Architecture](docs/images/architecture-high-level.png)

![Data Flow](docs/images/data-flow-diagram.png)

![AWS Deployment](docs/images/aws-deployment.png)

![AI Comparison](docs/images/ai-comparison.png)

![Security Layers](docs/images/security-layers.png)
```

### HTML

```html
<img src="docs/images/architecture-high-level.png" alt="Architecture" width="100%">
```

### GitHub README

Images are automatically displayed when referenced in README.md or other markdown files in the repository.

---

## 🎯 When to Use Each Diagram

| Audience | Recommended Diagrams |
|----------|---------------------|
| **Executives** | AI Comparison, High-Level Architecture |
| **Engineers** | Data Flow, AWS Deployment |
| **Security Team** | Security Layers, AWS Deployment |
| **Product Team** | High-Level Architecture, AI Comparison |
| **DevOps** | AWS Deployment, Data Flow |
| **New Team Members** | High-Level Architecture, Data Flow |

---

## 🔄 Updating Diagrams

### When to Update
- Architecture changes
- New AWS services added
- Security model changes
- UI/UX updates
- Process flow modifications

### How to Update
1. Edit `generate-diagrams.py` functions
2. Adjust colors, text, or layout as needed
3. Re-run: `python3 generate-diagrams.py`
4. Review output in `docs/images/`
5. Commit updated images to git

### Customization Options

**Change Colors:**
```python
PRIMARY_COLOR = "#2563eb"  # Blue
SECONDARY_COLOR = "#10b981"  # Green
ACCENT_COLOR = "#f59e0b"  # Orange
```

**Change Resolution:**
```python
WIDTH = 1920
HEIGHT = 1080

# For 4K:
WIDTH = 3840
HEIGHT = 2160
```

**Add New Diagrams:**
```python
def generate_my_custom_diagram():
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    # Your drawing code
    img.save("docs/images/my-diagram.png", "PNG")
```

---

## 📦 Version Control

### What to Commit
✅ **DO commit**:
- Generated PNG/JPEG files (documentation assets)
- `generate-diagrams.py` script
- This documentation

❌ **DON'T commit**:
- Temporary files
- Test outputs
- Draft versions

### Git LFS (Optional)

For large files, consider Git Large File Storage:

```bash
# Install Git LFS
git lfs install

# Track image files
git lfs track "docs/images/*.png"
git lfs track "docs/images/*.jpg"

# Add .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

---

## 🚀 Best Practices

1. **Always regenerate after architecture changes**
2. **Use PNG for presentations** (lossless quality)
3. **Use JPEG for web/email** (smaller size)
4. **Keep source script under version control**
5. **Document any customizations**
6. **Test rendering in target platforms**
7. **Maintain aspect ratios when resizing**

---

## 📚 Additional Resources

- **Main Architecture Doc**: `../ARCHITECTURE.md`
- **Generation Guide**: `../GENERATE_DIAGRAMS.md`
- **Project Overview**: `../PROJECT_OVERVIEW.md`
- **Deployment Guide**: `../QUICKSTART.md`

---

**Generated diagrams are presentation-ready and optimized for:**
- Technical documentation
- Stakeholder presentations
- Architecture review meetings
- Deployment guides
- Training materials
- GitHub README
- Confluence/Wiki pages

*Last Updated: 2026-05-15*
