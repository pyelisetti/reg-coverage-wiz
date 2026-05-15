#!/usr/bin/env python3
"""
Architecture Diagram Generator
Generates PNG and JPEG images for the Coverage Analyzer architecture documentation
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
OUTPUT_DIR = "docs/images"
WIDTH = 1920
HEIGHT = 1080
BACKGROUND_COLOR = "#ffffff"
PRIMARY_COLOR = "#2563eb"  # Blue
SECONDARY_COLOR = "#10b981"  # Green
ACCENT_COLOR = "#f59e0b"  # Orange
TEXT_COLOR = "#1f2937"  # Dark gray
LIGHT_GRAY = "#f3f4f6"
BORDER_COLOR = "#d1d5db"

def create_output_dir():
    """Create output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✓ Output directory created: {OUTPUT_DIR}")

def get_font(size):
    """Get font, fallback to default if custom font not available"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", size)
        except:
            return ImageFont.load_default()

def draw_rounded_rectangle(draw, coords, radius, fill, outline=None, width=2):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = coords
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, x1, y1, x2, y2, color, width=4):
    """Draw an arrow from (x1,y1) to (x2,y2)"""
    # Draw line
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

    # Draw arrowhead
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_length = 15
    arrow_angle = math.pi / 6

    point1_x = x2 - arrow_length * math.cos(angle - arrow_angle)
    point1_y = y2 - arrow_length * math.sin(angle - arrow_angle)
    point2_x = x2 - arrow_length * math.cos(angle + arrow_angle)
    point2_y = y2 - arrow_length * math.sin(angle + arrow_angle)

    draw.polygon([(x2, y2), (point1_x, point1_y), (point2_x, point2_y)], fill=color)

def draw_centered_text(draw, text, x, y, font, color, max_width=None):
    """Draw centered text"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if max_width and text_width > max_width:
        # Word wrap
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        # Draw multiple lines
        line_height = text_height + 5
        total_height = len(lines) * line_height
        start_y = y - total_height // 2

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            draw.text((x - line_width // 2, start_y + i * line_height), line, fill=color, font=font)
    else:
        draw.text((x - text_width // 2, y - text_height // 2), text, fill=color, font=font)

def generate_high_level_architecture():
    """Generate the main high-level architecture diagram"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = get_font(48)
    heading_font = get_font(32)
    subheading_font = get_font(24)
    text_font = get_font(18)
    small_font = get_font(14)

    # Title
    draw_centered_text(draw, "Regulatory Test Coverage Analyzer", WIDTH // 2, 60, title_font, PRIMARY_COLOR)
    draw_centered_text(draw, "High-Level Architecture", WIDTH // 2, 110, heading_font, TEXT_COLOR)

    # User/Browser Layer (Top)
    browser_box = [WIDTH // 2 - 300, 180, WIDTH // 2 + 300, 280]
    draw_rounded_rectangle(draw, browser_box, 15, LIGHT_GRAY, PRIMARY_COLOR, 3)
    draw_centered_text(draw, "User Browser", WIDTH // 2, 210, subheading_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Upload Excel Files", WIDTH // 2, 240, text_font, TEXT_COLOR)

    # Arrow down
    draw_arrow(draw, WIDTH // 2, 280, WIDTH // 2, 340, PRIMARY_COLOR)

    # EC2 Instance Layer
    ec2_box = [150, 340, WIDTH - 150, 720]
    draw_rounded_rectangle(draw, ec2_box, 20, "#e0f2fe", PRIMARY_COLOR, 4)
    draw_centered_text(draw, "AWS EC2 Instance", WIDTH // 2, 370, heading_font, PRIMARY_COLOR)

    # Node.js Application
    node_box = [200, 420, WIDTH // 2 - 50, 580]
    draw_rounded_rectangle(draw, node_box, 15, "#dbeafe", PRIMARY_COLOR, 2)
    draw_centered_text(draw, "Node.js App", (node_box[0] + node_box[2]) // 2, 450, subheading_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Express Server", (node_box[0] + node_box[2]) // 2, 490, text_font, TEXT_COLOR)
    draw_centered_text(draw, "Excel Parser", (node_box[0] + node_box[2]) // 2, 520, text_font, TEXT_COLOR)
    draw_centered_text(draw, "File Upload Handler", (node_box[0] + node_box[2]) // 2, 550, text_font, TEXT_COLOR)

    # AI Integration Layer
    ai_box = [WIDTH // 2 + 50, 420, WIDTH - 200, 580]
    draw_rounded_rectangle(draw, ai_box, 15, "#d1fae5", SECONDARY_COLOR, 2)
    draw_centered_text(draw, "AI Integration", (ai_box[0] + ai_box[2]) // 2, 450, subheading_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Prompt Engineering", (ai_box[0] + ai_box[2]) // 2, 490, text_font, TEXT_COLOR)
    draw_centered_text(draw, "Response Parser", (ai_box[0] + ai_box[2]) // 2, 520, text_font, TEXT_COLOR)
    draw_centered_text(draw, "Error Handling", (ai_box[0] + ai_box[2]) // 2, 550, text_font, TEXT_COLOR)

    # Environment Config
    env_box = [250, 610, WIDTH // 2 - 100, 690]
    draw_rounded_rectangle(draw, env_box, 10, "#fef3c7", ACCENT_COLOR, 2)
    draw_centered_text(draw, ".env Config", (env_box[0] + env_box[2]) // 2, 640, text_font, ACCENT_COLOR)
    draw_centered_text(draw, "API Keys", (env_box[0] + env_box[2]) // 2, 670, small_font, TEXT_COLOR)

    # Security
    security_box = [WIDTH // 2 + 100, 610, WIDTH - 250, 690]
    draw_rounded_rectangle(draw, security_box, 10, "#fef3c7", ACCENT_COLOR, 2)
    draw_centered_text(draw, "Security Layer", (security_box[0] + security_box[2]) // 2, 640, text_font, ACCENT_COLOR)
    draw_centered_text(draw, "HTTPS / TLS", (security_box[0] + security_box[2]) // 2, 670, small_font, TEXT_COLOR)

    # Arrow to Claude
    draw_arrow(draw, WIDTH // 2, 720, WIDTH // 2, 780, SECONDARY_COLOR, 5)
    draw_centered_text(draw, "HTTPS API Call", WIDTH // 2 + 100, 750, text_font, SECONDARY_COLOR)

    # Claude API (External)
    claude_box = [WIDTH // 2 - 350, 780, WIDTH // 2 + 350, 960]
    draw_rounded_rectangle(draw, claude_box, 20, "#f0fdf4", SECONDARY_COLOR, 4)
    draw_centered_text(draw, "Anthropic Claude API", WIDTH // 2, 820, heading_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Claude Sonnet 4.6", WIDTH // 2, 860, subheading_font, TEXT_COLOR)

    # AI Capabilities
    cap_y = 900
    capabilities = ["Semantic Analysis", "Coverage Detection", "Gap Identification", "Summary Generation"]
    cap_x_start = WIDTH // 2 - 350
    cap_width = 700 // len(capabilities)
    for i, cap in enumerate(capabilities):
        x = cap_x_start + (i * 700 // len(capabilities)) + cap_width // 2
        draw_centered_text(draw, cap, x, cap_y, small_font, TEXT_COLOR)

    # Legend
    legend_y = HEIGHT - 80
    draw.ellipse([200, legend_y - 10, 220, legend_y + 10], fill=PRIMARY_COLOR)
    draw.text((230, legend_y - 8), "Application Layer", fill=TEXT_COLOR, font=small_font)

    draw.ellipse([500, legend_y - 10, 520, legend_y + 10], fill=SECONDARY_COLOR)
    draw.text((530, legend_y - 8), "AI Processing", fill=TEXT_COLOR, font=small_font)

    draw.ellipse([750, legend_y - 10, 770, legend_y + 10], fill=ACCENT_COLOR)
    draw.text((780, legend_y - 8), "Configuration & Security", fill=TEXT_COLOR, font=small_font)

    # Save
    png_path = os.path.join(OUTPUT_DIR, "architecture-high-level.png")
    jpg_path = os.path.join(OUTPUT_DIR, "architecture-high-level.jpg")
    img.save(png_path, "PNG")
    img.save(jpg_path, "JPEG", quality=95)
    print(f"✓ Generated: {png_path}")
    print(f"✓ Generated: {jpg_path}")

def generate_data_flow_diagram():
    """Generate the data flow diagram"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = get_font(48)
    heading_font = get_font(28)
    text_font = get_font(18)
    small_font = get_font(14)

    # Title
    draw_centered_text(draw, "Data Flow & Processing Pipeline", WIDTH // 2, 60, title_font, PRIMARY_COLOR)

    # Phase 1: Upload
    phase1_y = 150
    draw_centered_text(draw, "PHASE 1: File Upload & Parsing", WIDTH // 2, phase1_y, heading_font, PRIMARY_COLOR)

    # User uploads
    box1 = [150, phase1_y + 50, 500, phase1_y + 180]
    draw_rounded_rectangle(draw, box1, 15, "#dbeafe", PRIMARY_COLOR, 3)
    draw_centered_text(draw, "User Action", 325, phase1_y + 80, text_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Select Files:", 325, phase1_y + 110, small_font, TEXT_COLOR)
    draw_centered_text(draw, "• Questionnaire.xlsx", 325, phase1_y + 135, small_font, TEXT_COLOR)
    draw_centered_text(draw, "• Inventory.xlsx", 325, phase1_y + 160, small_font, TEXT_COLOR)

    # Arrow
    draw_arrow(draw, 500, phase1_y + 115, 650, phase1_y + 115, PRIMARY_COLOR)

    # Server processing
    box2 = [650, phase1_y + 50, 1000, phase1_y + 180]
    draw_rounded_rectangle(draw, box2, 15, "#dbeafe", PRIMARY_COLOR, 3)
    draw_centered_text(draw, "Server Processing", 825, phase1_y + 80, text_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Multer receives files", 825, phase1_y + 110, small_font, TEXT_COLOR)
    draw_centered_text(draw, "xlsx parser extracts", 825, phase1_y + 135, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Data preview sent", 825, phase1_y + 160, small_font, TEXT_COLOR)

    # Arrow
    draw_arrow(draw, 1000, phase1_y + 115, 1150, phase1_y + 115, PRIMARY_COLOR)

    # Preview
    box3 = [1150, phase1_y + 50, 1500, phase1_y + 180]
    draw_rounded_rectangle(draw, box3, 15, "#dbeafe", PRIMARY_COLOR, 3)
    draw_centered_text(draw, "UI Preview", 1325, phase1_y + 80, text_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Show first 3 items", 1325, phase1_y + 110, small_font, TEXT_COLOR)
    draw_centered_text(draw, "from each dataset", 1325, phase1_y + 135, small_font, TEXT_COLOR)

    # Phase 2: AI Analysis
    phase2_y = 400
    draw_centered_text(draw, "PHASE 2: AI Analysis (The Brain)", WIDTH // 2, phase2_y, heading_font, SECONDARY_COLOR)

    # Build prompt
    box4 = [150, phase2_y + 50, 500, phase2_y + 200]
    draw_rounded_rectangle(draw, box4, 15, "#d1fae5", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Prompt Builder", 325, phase2_y + 80, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "System instructions", 325, phase2_y + 115, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Questionnaire data", 325, phase2_y + 140, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Test inventory data", 325, phase2_y + 165, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Analysis criteria", 325, phase2_y + 190, small_font, TEXT_COLOR)

    # Arrow
    draw_arrow(draw, 500, phase2_y + 125, 650, phase2_y + 125, SECONDARY_COLOR, 5)
    draw_centered_text(draw, "API Request", 575, phase2_y + 100, small_font, SECONDARY_COLOR)

    # Claude AI
    box5 = [650, phase2_y + 50, 1200, phase2_y + 200]
    draw_rounded_rectangle(draw, box5, 15, "#d1fae5", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Claude Sonnet 4.6", 925, phase2_y + 80, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Semantic matching by INTENT", 925, phase2_y + 120, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Calculate coverage percentages", 925, phase2_y + 145, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Identify gaps & generate insights", 925, phase2_y + 170, small_font, TEXT_COLOR)

    # Arrow
    draw_arrow(draw, 1200, phase2_y + 125, 1350, phase2_y + 125, SECONDARY_COLOR, 5)
    draw_centered_text(draw, "JSON Response", 1275, phase2_y + 100, small_font, SECONDARY_COLOR)

    # Results
    box6 = [1350, phase2_y + 50, 1700, phase2_y + 200]
    draw_rounded_rectangle(draw, box6, 15, "#d1fae5", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Analysis Results", 1525, phase2_y + 80, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Coverage %", 1525, phase2_y + 120, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Gap analysis", 1525, phase2_y + 145, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Executive summary", 1525, phase2_y + 170, small_font, TEXT_COLOR)

    # Phase 3: Visualization
    phase3_y = 680
    draw_centered_text(draw, "PHASE 3: Results Visualization", WIDTH // 2, phase3_y, heading_font, ACCENT_COLOR)

    # Format
    box7 = [300, phase3_y + 50, 700, phase3_y + 150]
    draw_rounded_rectangle(draw, box7, 15, "#fef3c7", ACCENT_COLOR, 3)
    draw_centered_text(draw, "Format Results", 500, phase3_y + 80, text_font, ACCENT_COLOR)
    draw_centered_text(draw, "Coverage cards", 500, phase3_y + 110, small_font, TEXT_COLOR)
    draw_centered_text(draw, "Status indicators", 500, phase3_y + 135, small_font, TEXT_COLOR)

    # Arrow
    draw_arrow(draw, 700, phase3_y + 100, 850, phase3_y + 100, ACCENT_COLOR)

    # Display
    box8 = [850, phase3_y + 50, 1250, phase3_y + 150]
    draw_rounded_rectangle(draw, box8, 15, "#fef3c7", ACCENT_COLOR, 3)
    draw_centered_text(draw, "Interactive Dashboard", 1050, phase3_y + 80, text_font, ACCENT_COLOR)
    draw_centered_text(draw, "Prominent % display", 1050, phase3_y + 110, small_font, TEXT_COLOR)
    draw_centered_text(draw, "AI-generated summary", 1050, phase3_y + 135, small_font, TEXT_COLOR)

    # Timing info
    timing_y = HEIGHT - 120
    draw_rounded_rectangle(draw, [200, timing_y, WIDTH - 200, timing_y + 80], 10, LIGHT_GRAY, BORDER_COLOR, 2)
    draw_centered_text(draw, "Total Processing Time: 15-45 seconds", WIDTH // 2, timing_y + 25, text_font, TEXT_COLOR)
    draw_centered_text(draw, "Upload: 1-2s  |  Parsing: 0.5-1s  |  AI Analysis: 10-35s  |  Rendering: 0.5-1s", WIDTH // 2, timing_y + 55, small_font, TEXT_COLOR)

    # Save
    png_path = os.path.join(OUTPUT_DIR, "data-flow-diagram.png")
    jpg_path = os.path.join(OUTPUT_DIR, "data-flow-diagram.jpg")
    img.save(png_path, "PNG")
    img.save(jpg_path, "JPEG", quality=95)
    print(f"✓ Generated: {png_path}")
    print(f"✓ Generated: {jpg_path}")

def generate_aws_deployment_diagram():
    """Generate AWS deployment architecture diagram"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = get_font(48)
    heading_font = get_font(28)
    text_font = get_font(18)
    small_font = get_font(14)

    # Title
    draw_centered_text(draw, "AWS EC2 Deployment Architecture", WIDTH // 2, 60, title_font, PRIMARY_COLOR)

    # AWS Cloud border
    aws_border = [100, 150, WIDTH - 100, HEIGHT - 150]
    draw_rounded_rectangle(draw, aws_border, 25, "#fff7ed", "#ea580c", 4)
    draw.text((120, 165), "AWS Cloud", fill="#ea580c", font=heading_font)

    # Internet Gateway
    igw_box = [WIDTH // 2 - 200, 250, WIDTH // 2 + 200, 330]
    draw_rounded_rectangle(draw, igw_box, 15, "#fef3c7", ACCENT_COLOR, 3)
    draw_centered_text(draw, "Internet Gateway", WIDTH // 2, 270, text_font, ACCENT_COLOR)
    draw_centered_text(draw, "Security Group: Port 3000 + SSH", WIDTH // 2, 305, small_font, TEXT_COLOR)

    # Arrow down
    draw_arrow(draw, WIDTH // 2, 330, WIDTH // 2, 380, PRIMARY_COLOR)

    # EC2 Instance
    ec2_box = [200, 380, WIDTH - 200, 800]
    draw_rounded_rectangle(draw, ec2_box, 20, "#e0f2fe", PRIMARY_COLOR, 4)
    draw_centered_text(draw, "EC2 Instance (t3.medium)", WIDTH // 2, 415, heading_font, PRIMARY_COLOR)
    draw_centered_text(draw, "2 vCPUs  |  4 GB RAM  |  20 GB SSD", WIDTH // 2, 450, small_font, TEXT_COLOR)

    # Layer 1: PM2
    layer1 = [250, 500, WIDTH - 250, 580]
    draw_rounded_rectangle(draw, layer1, 12, "#dbeafe", PRIMARY_COLOR, 2)
    draw_centered_text(draw, "PM2 Process Manager", WIDTH // 2, 520, text_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Auto-restart • Log management • Zero-downtime", WIDTH // 2, 555, small_font, TEXT_COLOR)

    # Layer 2: Application
    layer2 = [250, 600, WIDTH - 250, 680]
    draw_rounded_rectangle(draw, layer2, 12, "#d1fae5", SECONDARY_COLOR, 2)
    draw_centered_text(draw, "Node.js Application (Express)", WIDTH // 2, 620, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Port 3000  •  File processing  •  AI integration", WIDTH // 2, 655, small_font, TEXT_COLOR)

    # Layer 3: Environment
    layer3_left = [250, 700, WIDTH // 2 - 30, 770]
    draw_rounded_rectangle(draw, layer3_left, 12, "#fef3c7", ACCENT_COLOR, 2)
    draw_centered_text(draw, "Environment", (layer3_left[0] + layer3_left[2]) // 2, 720, text_font, ACCENT_COLOR)
    draw_centered_text(draw, ".env file", (layer3_left[0] + layer3_left[2]) // 2, 750, small_font, TEXT_COLOR)

    layer3_right = [WIDTH // 2 + 30, 700, WIDTH - 250, 770]
    draw_rounded_rectangle(draw, layer3_right, 12, "#fef3c7", ACCENT_COLOR, 2)
    draw_centered_text(draw, "Security", (layer3_right[0] + layer3_right[2]) // 2, 720, text_font, ACCENT_COLOR)
    draw_centered_text(draw, "HTTPS/TLS", (layer3_right[0] + layer3_right[2]) // 2, 750, small_font, TEXT_COLOR)

    # Arrow to Claude
    draw_arrow(draw, WIDTH - 200, 590, WIDTH - 100, 590, SECONDARY_COLOR, 4)
    draw.text((WIDTH - 180, 565), "API", fill=SECONDARY_COLOR, font=small_font)
    draw.text((WIDTH - 180, 585), "Call", fill=SECONDARY_COLOR, font=small_font)

    # Claude API (outside AWS border)
    claude_box = [WIDTH - 650, HEIGHT - 120, WIDTH - 100, HEIGHT - 30]
    draw_rounded_rectangle(draw, claude_box, 15, "#f0fdf4", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Anthropic Claude API", (claude_box[0] + claude_box[2]) // 2, HEIGHT - 90, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "External Service", (claude_box[0] + claude_box[2]) // 2, HEIGHT - 60, small_font, TEXT_COLOR)

    # Cost info
    cost_box = [120, HEIGHT - 120, 480, HEIGHT - 30]
    draw_rounded_rectangle(draw, cost_box, 10, "#fef3c7", ACCENT_COLOR, 2)
    draw_centered_text(draw, "Monthly Cost Estimate", 300, HEIGHT - 95, text_font, ACCENT_COLOR)
    draw_centered_text(draw, "EC2: ~$30  •  Transfer: ~$5", 300, HEIGHT - 65, small_font, TEXT_COLOR)

    # Capacity info
    capacity_y = 860
    draw_rounded_rectangle(draw, [250, capacity_y, WIDTH - 250, capacity_y + 60], 10, LIGHT_GRAY, BORDER_COLOR, 2)
    draw_centered_text(draw, "Capacity: 50 concurrent users  |  500 analyses/day  |  Scalable with Auto Scaling Groups", WIDTH // 2, capacity_y + 30, small_font, TEXT_COLOR)

    # Save
    png_path = os.path.join(OUTPUT_DIR, "aws-deployment.png")
    jpg_path = os.path.join(OUTPUT_DIR, "aws-deployment.jpg")
    img.save(png_path, "PNG")
    img.save(jpg_path, "JPEG", quality=95)
    print(f"✓ Generated: {png_path}")
    print(f"✓ Generated: {jpg_path}")

def generate_ai_comparison_diagram():
    """Generate AI semantic matching vs keyword matching comparison"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = get_font(48)
    heading_font = get_font(32)
    text_font = get_font(20)
    small_font = get_font(16)

    # Title
    draw_centered_text(draw, "AI-Powered Semantic Analysis", WIDTH // 2, 80, title_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Why Traditional Keyword Matching Fails", WIDTH // 2, 140, heading_font, TEXT_COLOR)

    # Dividing line
    draw.line([(WIDTH // 2, 200), (WIDTH // 2, HEIGHT - 200)], fill=BORDER_COLOR, width=3)

    # Left side: Traditional approach
    left_x = WIDTH // 4
    draw_centered_text(draw, "Traditional Keyword Matching", left_x, 220, heading_font, "#dc2626")

    # Example 1
    box1 = [50, 300, WIDTH // 2 - 50, 450]
    draw_rounded_rectangle(draw, box1, 15, "#fee2e2", "#dc2626", 3)
    draw_centered_text(draw, "Test:", left_x, 330, text_font, "#dc2626")
    draw_centered_text(draw, "Verify customer KYC documentation", left_x, 365, small_font, TEXT_COLOR, max_width=400)
    draw_centered_text(draw, "Regulation:", left_x, 405, text_font, "#dc2626")
    draw_centered_text(draw, "Know Your Customer requirements", left_x, 435, small_font, TEXT_COLOR, max_width=400)

    # X mark
    draw.ellipse([left_x - 40, 490, left_x + 40, 570], fill="#dc2626")
    draw_centered_text(draw, "✗", left_x, 530, get_font(60), "#ffffff")
    draw_centered_text(draw, "NO MATCH", left_x, 610, text_font, "#dc2626")
    draw_centered_text(draw, "Different words detected", left_x, 640, small_font, TEXT_COLOR)

    # Example 2
    box2 = [50, 700, WIDTH // 2 - 50, 850]
    draw_rounded_rectangle(draw, box2, 15, "#fee2e2", "#dc2626", 3)
    draw_centered_text(draw, "Limitations:", left_x, 730, text_font, "#dc2626")
    draw_centered_text(draw, "• Misses synonyms", left_x, 765, small_font, TEXT_COLOR)
    draw_centered_text(draw, "• Ignores context", left_x, 795, small_font, TEXT_COLOR)
    draw_centered_text(draw, "• Can't understand intent", left_x, 825, small_font, TEXT_COLOR)

    # Right side: AI approach
    right_x = WIDTH * 3 // 4
    draw_centered_text(draw, "AI Semantic Understanding", right_x, 220, heading_font, SECONDARY_COLOR)

    # Example 1
    box3 = [WIDTH // 2 + 50, 300, WIDTH - 50, 450]
    draw_rounded_rectangle(draw, box3, 15, "#d1fae5", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Test:", right_x, 330, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Verify customer KYC documentation", right_x, 365, small_font, TEXT_COLOR, max_width=400)
    draw_centered_text(draw, "Regulation:", right_x, 405, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Know Your Customer requirements", right_x, 435, small_font, TEXT_COLOR, max_width=400)

    # Check mark
    draw.ellipse([right_x - 40, 490, right_x + 40, 570], fill=SECONDARY_COLOR)
    draw_centered_text(draw, "✓", right_x, 530, get_font(60), "#ffffff")
    draw_centered_text(draw, "MATCH", right_x, 610, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Same regulatory intent understood", right_x, 640, small_font, TEXT_COLOR)

    # Example 2
    box4 = [WIDTH // 2 + 50, 700, WIDTH - 50, 850]
    draw_rounded_rectangle(draw, box4, 15, "#d1fae5", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Advantages:", right_x, 730, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "• Understands synonyms", right_x, 765, small_font, TEXT_COLOR)
    draw_centered_text(draw, "• Considers full context", right_x, 795, small_font, TEXT_COLOR)
    draw_centered_text(draw, "• Grasps regulatory intent", right_x, 825, small_font, TEXT_COLOR)

    # Bottom banner
    banner_y = HEIGHT - 150
    draw_rounded_rectangle(draw, [150, banner_y, WIDTH - 150, banner_y + 100], 15, "#f0fdf4", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Claude AI achieves 95%+ accuracy through semantic understanding", WIDTH // 2, banner_y + 30, text_font, SECONDARY_COLOR)
    draw_centered_text(draw, "Powered by Claude Sonnet 4.6 with 200K token context window", WIDTH // 2, banner_y + 65, small_font, TEXT_COLOR)

    # Save
    png_path = os.path.join(OUTPUT_DIR, "ai-comparison.png")
    jpg_path = os.path.join(OUTPUT_DIR, "ai-comparison.jpg")
    img.save(png_path, "PNG")
    img.save(jpg_path, "JPEG", quality=95)
    print(f"✓ Generated: {png_path}")
    print(f"✓ Generated: {jpg_path}")

def generate_security_layers_diagram():
    """Generate security architecture layers diagram"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # Fonts
    title_font = get_font(48)
    heading_font = get_font(28)
    text_font = get_font(18)
    small_font = get_font(14)

    # Title
    draw_centered_text(draw, "Multi-Layer Security Architecture", WIDTH // 2, 80, title_font, PRIMARY_COLOR)

    # Layer 4 (Bottom - Widest)
    layer4 = [150, 200, WIDTH - 150, 340]
    draw_rounded_rectangle(draw, layer4, 15, "#dbeafe", PRIMARY_COLOR, 3)
    draw_centered_text(draw, "Layer 4: Data Security", WIDTH // 2, 230, heading_font, PRIMARY_COLOR)
    draw_centered_text(draw, "• In-memory processing only  • No persistent storage", WIDTH // 2 - 200, 280, text_font, TEXT_COLOR)
    draw_centered_text(draw, "• Temporary file cleanup  • No PII retention", WIDTH // 2 + 200, 280, text_font, TEXT_COLOR)

    # Layer 3
    layer3 = [250, 370, WIDTH - 250, 510]
    draw_rounded_rectangle(draw, layer3, 15, "#d1fae5", SECONDARY_COLOR, 3)
    draw_centered_text(draw, "Layer 3: API Security", WIDTH // 2, 400, heading_font, SECONDARY_COLOR)
    draw_centered_text(draw, "• HTTPS only (TLS 1.2+)  • API key authentication", WIDTH // 2 - 200, 450, text_font, TEXT_COLOR)
    draw_centered_text(draw, "• Request validation  • Rate limiting", WIDTH // 2 + 200, 450, text_font, TEXT_COLOR)

    # Layer 2
    layer2 = [350, 540, WIDTH - 350, 680]
    draw_rounded_rectangle(draw, layer2, 15, "#fef3c7", ACCENT_COLOR, 3)
    draw_centered_text(draw, "Layer 2: Application Security", WIDTH // 2, 570, heading_font, ACCENT_COLOR)
    draw_centered_text(draw, "• Environment variables (.env)  • File size limits", WIDTH // 2 - 180, 620, text_font, TEXT_COLOR)
    draw_centered_text(draw, "• Input sanitization  • CORS config", WIDTH // 2 + 180, 620, text_font, TEXT_COLOR)

    # Layer 1 (Top - Narrowest)
    layer1 = [450, 710, WIDTH - 450, 850]
    draw_rounded_rectangle(draw, layer1, 15, "#fee2e2", "#dc2626", 3)
    draw_centered_text(draw, "Layer 1: Infrastructure Security (AWS)", WIDTH // 2, 740, heading_font, "#dc2626")
    draw_centered_text(draw, "• VPC isolation  • Security groups", WIDTH // 2 - 150, 790, text_font, TEXT_COLOR)
    draw_centered_text(draw, "• IAM roles  • CloudWatch", WIDTH // 2 + 150, 790, text_font, TEXT_COLOR)

    # Key management box
    key_box = [200, HEIGHT - 180, WIDTH - 200, HEIGHT - 60]
    draw_rounded_rectangle(draw, key_box, 15, LIGHT_GRAY, PRIMARY_COLOR, 3)
    draw_centered_text(draw, "API Key Management", WIDTH // 2, HEIGHT - 150, text_font, PRIMARY_COLOR)
    draw_centered_text(draw, "Stored in .env file (never committed to git)  •  Root-only read access  •  Rotatable without code changes", WIDTH // 2, HEIGHT - 115, small_font, TEXT_COLOR)

    # Save
    png_path = os.path.join(OUTPUT_DIR, "security-layers.png")
    jpg_path = os.path.join(OUTPUT_DIR, "security-layers.jpg")
    img.save(png_path, "PNG")
    img.save(jpg_path, "JPEG", quality=95)
    print(f"✓ Generated: {png_path}")
    print(f"✓ Generated: {jpg_path}")

def main():
    """Main function to generate all diagrams"""
    print("🎨 Architecture Diagram Generator")
    print("=" * 50)

    try:
        # Check if PIL is available
        Image.new('RGB', (100, 100), 'white')
        print("✓ PIL/Pillow is available")
    except Exception as e:
        print(f"✗ Error: PIL/Pillow not available: {e}")
        print("\nPlease install Pillow:")
        print("  pip3 install Pillow")
        return 1

    create_output_dir()
    print("\nGenerating diagrams...\n")

    generate_high_level_architecture()
    print()
    generate_data_flow_diagram()
    print()
    generate_aws_deployment_diagram()
    print()
    generate_ai_comparison_diagram()
    print()
    generate_security_layers_diagram()

    print("\n" + "=" * 50)
    print("✅ All diagrams generated successfully!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("\nGenerated files:")
    print("  • architecture-high-level.png / .jpg")
    print("  • data-flow-diagram.png / .jpg")
    print("  • aws-deployment.png / .jpg")
    print("  • ai-comparison.png / .jpg")
    print("  • security-layers.png / .jpg")
    return 0

if __name__ == "__main__":
    exit(main())
