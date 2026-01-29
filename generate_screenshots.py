import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---

# Project Settings
BASE_PROJECT_DIR = "."
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
BACKGROUND_IMAGE_PATH = "./wood_bg.png"
IPHONE_FRAME_PATH = "./iphone17-frame.png"

# App Specific Configs
APPS = {
    "pet-medication": {
        "title": "かんたん服薬通知",
        "captions": [
            "体重・通院予定・投薬を\nしっかり管理",
            "カレンダーで\n一目瞭然",
            "体重の推移を\nグラフで確認",
            "複数のワンちゃん・ネコちゃんを\n一元管理" 
        ],
        "bg_color": (255, 255, 255),  # White background
        "text_color": (0, 0, 0),
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"  # "single" or "double" (overlapping devices)
    },
    "quote-calendar": {
        "title": "名言カレンダー",
        "captions": [
            "毎日の名言で\n心に火を灯す",
            "カレンダーで\n名言を振り返り",
            "毎日の気づきを\n記録する"
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "trivia-calendar": {
        "title": "豆知識カレンダー",
        "captions": [
            {"text": "毎日の豆知識で 会話のネタに", "highlight": ["豆知識"]},
            {"text": "カレンダーで 知識を振り返り", "highlight": ["カレンダー"]},
            {"text": "お気に入りで いつでも見返せる", "highlight": ["お気に入り"]}
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "highlight_color": (0, 122, 255),  # Blue for highlighted text
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "triming-log": {
        "title": "トリミングログ",
        "captions": [
            "愛犬のトリミングを\n美しく記録",
            "次回の予約を\n忘れない通知機能",
            "過去のスタイルを\n写真で振り返り"
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "parking-calculator": {
        "title": "パーキングリアルタイム計算",
        "captions": [
            "駐車料金を\nリアルタイム計算",
            "設定金額で\n通知してお知らせ",
            "複数の駐車場を\n比較・管理"
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "exam-countdown": {
        "title": "試験カウントダウン",
        "captions": [
            "試験日まで\nあと何日？",
            "勉強記録を\n一言添えて記録",
            "ホーム画面で\nいつでも確認",
            "アクティビティを\n確認"
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "overtime-meter": {
        "title": "残業メーター",
        "captions": [
            "残業時間を秒刻みで\nカウント！",
            "グラフで確認も！"
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "double"  # Use overlapping layout for this app
    },
    "drive-log": {
        "title": "ドライブログ",
        "captions": [
            {"text": "ドライブの記録を登録！", "highlight": ["記録", "登録"]},
            {"text": "複数履歴OK！", "highlight": ["複数履歴", "OK"]},
            {"text": "速度・メモの登録も", "highlight": ["速度", "メモ"]},
            {"text": "写真登録も可能！", "highlight": ["写真登録", "可能"]}
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "highlight_color": (0, 122, 255),  # Blue for highlighted text
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "screenshot-poi": {
        "title": "スクショポイ",
        "captions": [
            {"text": "スクショのみを検出！", "highlight": ["スクショのみ"]},
            {"text": "スワイプ整理！", "highlight": ["スワイプ"]},
            {"text": "まとめて削除", "highlight": ["まとめて"]}
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "highlight_color": (0, 122, 255),  # Blue for highlighted text
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "aquarium-note": {
        "title": "アクアリウムノート",
        "captions": [
            {"text": "複数アクアリウムをまとめて管理", "highlight": ["まとめて"]},
            {"text": "水槽別に日記を記録", "highlight": ["水槽別"]}
        ],
        "bg_color": (255, 255, 255),
        "text_color": (0, 0, 0),
        "highlight_color": (30, 136, 229),  # 1E88E5 - App theme primary color
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    },
    "work-quest": {
        "title": "10分作業クエスト",
        "captions": [
            {"text": "作業でキャラクターGET", "highlight": ["キャラクター"]},
            {"text": "履歴も確認", "highlight": ["履歴"]},
            {"text": "図鑑で手に入れたキャラクターをチェック", "highlight": ["図鑑", "チェック"]},
            {"text": "ボス戦も！", "highlight": ["ボス戦"]}
        ],
        "bg_color": (255, 255, 255),  # 白背景
        "text_color": (0, 0, 0),
        "highlight_color": (0, 122, 255),  # 青でハイライト
        "title_color": (0, 0, 0),
        "stroke_color": (255, 255, 255),
        "layout": "single"
    }
}

# Device Specifications
DEVICES = {
    "iphone": {
        "size": (1242, 2688), # App Store screenshot size
        "base_font_size": 110,
        "title_font_size": 140,
        "screenshot_resize_ratio": 0.82,  # Increased from 0.82 to make screenshots larger
        "body_radius": 120,  # More rounded corners
        "padding": 50,
        "bezel_top": 50,
        "bezel_bottom": 50,
        "notch": None,
        "y_title_start": 180,
        "y_text_start": 320,
        "y_phone_offset": 150,
        "rotation_angle": -8  # Slight rotation for overlapping effect
    },
    "ipad": {
        "size": (2048, 2732), # iPad Pro 12.9 (approx ratio)
        "base_font_size": 100,  # Reduced from 140
        "title_font_size": 130,  # Reduced from 180
        "screenshot_resize_ratio": 0.85,
        "body_radius": 100,  # More rounded corners
        "padding": 60,
        "bezel_top": 60,
        "bezel_bottom": 60,
        "notch": None,
        "y_title_start": 150,
        "y_text_start": 280,
        "y_phone_offset": 150,
        "rotation_angle": -6
    }
}

# --- HELPERS ---

def create_background(width, height, bg_color):
    """Create a solid color background"""
    return Image.new('RGB', (width, height), bg_color)

def rotate_image(image, angle):
    """Rotate image by angle degrees"""
    if angle == 0:
        return image
    # For RGBA images, use transparent background
    if image.mode == 'RGBA':
        return image.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
    else:
        return image.rotate(angle, expand=True, fillcolor=(255, 255, 255))

def get_fitted_font(draw, text, max_width, initial_size, font_path):
    size = initial_size
    try:
        font = ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default(), size

    lines = text.split('\n')
    min_size = int(initial_size * 0.5)
    
    while size > min_size:
        max_line_w = 0
        for line in lines:
            if hasattr(draw, 'textlength'):
                w = draw.textlength(line, font=font)
            else:
                w = draw.textsize(line, font=font)[0]
            if w > max_line_w: max_line_w = w
        
        if max_line_w <= max_width:
            print(f"Fitted font size: {size}")
            return font, size
            
        size -= 5
        try:
            font = ImageFont.truetype(font_path, size)
        except:
            break
    return font, size

def process_app(app_name):
    if app_name not in APPS:
        print(f"App {app_name} not configured.")
        return

    config = APPS[app_name]
    doc_dir = os.path.join(BASE_PROJECT_DIR, app_name, "documents")
    out_dir = os.path.join(BASE_PROJECT_DIR, app_name, "documents_processed")
    
    # Check if documents directory exists
    if not os.path.exists(doc_dir):
        print(f"Documents directory not found for {app_name}: {doc_dir}")
        return
    
    os.makedirs(out_dir, exist_ok=True)
    
    # Identify files
    all_files = os.listdir(doc_dir)
    iphone_files = sorted([f for f in all_files if "iphone" in f.lower() and f.endswith(".png")])
    ipad_files = sorted([f for f in all_files if "ipad" in f.lower() and f.endswith(".png")])
    
    # Fallback: if no device specific name, treat numbered files (1.png, 2.png, etc.) as iphone
    # and remaining .png files as iphone too
    if not iphone_files and not ipad_files:
        numbered_files = sorted([f for f in all_files if f.endswith(".png") and f.replace(".png", "").isdigit()])
        if numbered_files:
            iphone_files = numbered_files
        else:
            iphone_files = sorted([f for f in all_files if f.endswith(".png")])
    elif not iphone_files:
        # If we have iPad files but no iPhone files, check for numbered files
        numbered_files = sorted([f for f in all_files if f.endswith(".png") and f.replace(".png", "").isdigit()])
        if numbered_files:
            iphone_files = numbered_files

    print(f"Processing {app_name}: found {len(iphone_files)} iPhone, {len(ipad_files)} iPad images.")

    # Process iPhone
    process_device_batch(app_name, "iphone", iphone_files, config, doc_dir, out_dir)
    
    # Process iPad
    process_device_batch(app_name, "ipad", ipad_files, config, doc_dir, out_dir)

def apply_rounded_corners(image, radius):
    """Apply rounded corners to an image using a mask"""
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Create mask with rounded corners
    mask = Image.new('L', image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, image.width, image.height], radius=radius, fill=255)
    
    # Apply mask
    output = Image.new('RGBA', image.size, (0, 0, 0, 0))
    output.paste(image, (0, 0), mask)
    return output

def paste_rotated_device(img, screenshot, x, y, padding, bezel_top, bezel_bottom, radius, angle, shadow_offset=20, frame_path=None):
    """Paste a device frame with rotation using frame image if available"""
    target_w = screenshot.width
    target_h = screenshot.height
    
    # Try to use frame image if available
    if frame_path and os.path.exists(frame_path):
        try:
            frame_img = Image.open(frame_path)
            if frame_img.mode != 'RGBA':
                frame_img = frame_img.convert('RGBA')
            
            frame_w, frame_h = frame_img.size
            
            # Analyze frame to find screen area
            # Screen area is typically in the center with bezels around
            # For iPhone 17 frame (363x750), estimate screen area
            # Typical iPhone has bezels: ~6-8% on sides, ~4-6% on top/bottom
            # Maximize screen area ratio to eliminate margins completely
            screen_area_ratio_w = 0.92  # Further increased to minimize side margins
            screen_area_ratio_h = 0.96  # Further increased to minimize top/bottom margins
            
            # Calculate screen area dimensions in original frame
            frame_screen_w = frame_w * screen_area_ratio_w
            frame_screen_h = frame_h * screen_area_ratio_h
            screen_offset_x_orig = (frame_w - frame_screen_w) / 2
            # Adjust vertical position: move screenshot up and reduce margins further
            screen_offset_y_orig = (frame_h - frame_screen_h) / 2 - (frame_h * 0.005)
            
            # Calculate scale to fit screenshot into frame's screen area
            # We want screenshot to fill the screen area completely, even slightly overflow
            scale_w = target_w / frame_screen_w
            scale_h = target_h / frame_screen_h
            scale = max(scale_w, scale_h) * 1.02  # Slightly larger scale to ensure no gaps
            
            # Resize frame to match screenshot size
            new_frame_w = int(frame_w * scale)
            new_frame_h = int(frame_h * scale)
            frame_img = frame_img.resize((new_frame_w, new_frame_h), Image.Resampling.LANCZOS)
            
            # Calculate screen position in resized frame
            screen_offset_x = int(screen_offset_x_orig * scale)
            screen_offset_y = int(screen_offset_y_orig * scale)
            screen_w_in_frame = int(frame_screen_w * scale)
            screen_h_in_frame = int(frame_screen_h * scale)
            
            # Resize screenshot to fill screen area completely (may slightly overflow, but will be masked by frame)
            screenshot_resized = screenshot.resize((screen_w_in_frame, screen_h_in_frame), Image.Resampling.LANCZOS)
            
            # Apply rounded corners to screenshot (stronger rounding)
            screen_radius = max(80, int(min(screen_w_in_frame, screen_h_in_frame) * 0.06))  # ~6% of smaller dimension for stronger rounding
            if screenshot_resized.mode != 'RGBA':
                screenshot_resized = screenshot_resized.convert('RGBA')
            screenshot_resized = apply_rounded_corners(screenshot_resized, screen_radius)
            
            # Create a composite image: first paste screenshot, then frame on top
            # Create base image with screenshot
            composite_img = Image.new('RGBA', (new_frame_w, new_frame_h), (0, 0, 0, 0))
            composite_img.paste(screenshot_resized, (screen_offset_x, screen_offset_y), screenshot_resized)
            
            # Paste frame on top (frame will have transparency where screen should be)
            composite_img.paste(frame_img, (0, 0), frame_img)
            
            device_img = composite_img
            body_w = new_frame_w
            body_h = new_frame_h
        except Exception as e:
            print(f"Error loading frame image: {e}, using default frame")
            frame_path = None
    
    # Fallback to default frame drawing
    if not frame_path or not os.path.exists(frame_path):
        body_w = target_w + padding * 2
        body_h = target_h + bezel_top + bezel_bottom
        
        # Create device frame image
        device_img = Image.new('RGBA', (body_w + shadow_offset * 2, body_h + shadow_offset * 2), (0, 0, 0, 0))
        device_draw = ImageDraw.Draw(device_img)
        
        # Shadow
        shadow_rect = [
            shadow_offset,
            shadow_offset,
            body_w + shadow_offset,
            body_h + shadow_offset
        ]
        device_draw.rounded_rectangle(shadow_rect, radius=radius, fill=(0, 0, 0, 60))
        
        # Frame
        frame_rect = [
            shadow_offset,
            shadow_offset,
            body_w + shadow_offset,
            body_h + shadow_offset
        ]
        device_draw.rounded_rectangle(frame_rect, radius=radius, fill=(20, 20, 20, 255))
        
        # Inner border for depth
        inner_rect = [
            shadow_offset + 2,
            shadow_offset + 2,
            body_w + shadow_offset - 2,
            body_h + shadow_offset - 2
        ]
        device_draw.rounded_rectangle(inner_rect, radius=max(radius - 2, 0), outline=(10, 10, 10, 255), width=1)
        
        # Apply rounded corners to screenshot (stronger rounding)
        screen_radius = max(radius - padding // 2, 50)  # Increased minimum radius for stronger rounding
        if screenshot.mode != 'RGBA':
            screenshot = screenshot.convert('RGBA')
        screenshot = apply_rounded_corners(screenshot, screen_radius)
        
        # Paste screenshot
        screen_x = shadow_offset + padding
        screen_y = shadow_offset + bezel_top
        device_img.paste(screenshot, (screen_x, screen_y), screenshot)
    
    # Rotate if needed
    if angle != 0:
        device_img = rotate_image(device_img, angle)
    
    # Calculate paste position (center the rotated image)
    paste_x = x - device_img.width // 2
    paste_y = y - device_img.height // 2
    
    # Paste with alpha
    img.paste(device_img, (paste_x, paste_y), device_img)
    
    return device_img.width, device_img.height

def draw_text_with_stroke(draw, text, x, y, font, text_color, stroke_color, stroke_width):
    """Draw text with stroke outline"""
    # Draw stroke
    for dx in range(-stroke_width, stroke_width+1):
        for dy in range(-stroke_width, stroke_width+1):
            if dx*dx + dy*dy <= stroke_width*stroke_width:
                draw.text((x+dx, y+dy), text, font=font, fill=stroke_color)
    # Draw fill
    draw.text((x, y), text, font=font, fill=text_color)

def draw_text_with_highlights(draw, text, center_x, y, font, text_color, highlight_color, highlight_words, stroke_color, stroke_width):
    """Draw text with highlighted words in different color"""
    # Calculate total width to center
    if hasattr(draw, 'textlength'):
        total_w = draw.textlength(text, font=font)
    else:
        total_w = draw.textsize(text, font=font)[0]
    x_start = center_x - total_w / 2
    
    # Split text into segments (highlighted and normal)
    segments = []
    current_pos = 0
    text_lower = text.lower()
    
    # Find all highlight positions
    highlight_positions = []
    for word in highlight_words:
        word_lower = word.lower()
        pos = 0
        while True:
            idx = text_lower.find(word_lower, pos)
            if idx == -1:
                break
            highlight_positions.append((idx, idx + len(word), word))
            pos = idx + 1
    
    # Sort by position
    highlight_positions.sort(key=lambda x: x[0])
    
    # Build segments
    pos = 0
    for start, end, word in highlight_positions:
        if start > pos:
            # Normal text before highlight
            segments.append((text[pos:start], text_color, False))
        # Highlighted text
        segments.append((text[start:end], highlight_color, True))
        pos = end
    
    # Remaining text
    if pos < len(text):
        segments.append((text[pos:], text_color, False))
    
    # Draw segments
    x_pos = x_start
    for segment_text, color, is_highlight in segments:
        if segment_text:
            if is_highlight:
                # Draw bold text for highlighted words (draw multiple times with slight offsets)
                bold_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                # Draw stroke first
                for dx in range(-stroke_width, stroke_width+1):
                    for dy in range(-stroke_width, stroke_width+1):
                        if dx*dx + dy*dy <= stroke_width*stroke_width:
                            draw.text((x_pos+dx, y+dy), segment_text, font=font, fill=stroke_color)
                # Draw bold effect (multiple passes with slight offsets)
                for offset_x, offset_y in bold_offsets:
                    draw.text((x_pos + offset_x, y + offset_y), segment_text, font=font, fill=color)
                # Draw main text
                draw.text((x_pos, y), segment_text, font=font, fill=color)
            else:
                # Draw normal text
                # Draw stroke
                for dx in range(-stroke_width, stroke_width+1):
                    for dy in range(-stroke_width, stroke_width+1):
                        if dx*dx + dy*dy <= stroke_width*stroke_width:
                            draw.text((x_pos+dx, y+dy), segment_text, font=font, fill=stroke_color)
                # Draw fill
                draw.text((x_pos, y), segment_text, font=font, fill=color)
            
            # Move position
            if hasattr(draw, 'textlength'):
                x_pos += draw.textlength(segment_text, font=font)
            else:
                x_pos += draw.textsize(segment_text, font=font)[0]

def process_device_batch(app_name, device_type, files, config, doc_dir, out_dir):
    if not files: return
    
    dev_spec = DEVICES[device_type]
    captions = config["captions"]
    layout = config.get("layout", "single")
    
    for i, filename in enumerate(files):
        if i >= len(captions): break
        
        caption_data = captions[i]
        # Support both string and dict format for captions
        if isinstance(caption_data, dict):
            caption_text = caption_data.get("text", "")
            highlight_words = caption_data.get("highlight", [])
        else:
            caption_text = caption_data
            highlight_words = []
        
        # Remove line breaks to fit text in one line
        caption_text = caption_text.replace('\n', ' ')
        
        title = config.get("title", "")
        
        # Canvas
        canvas_w, canvas_h = dev_spec["size"]
        bg_color = config.get("bg_color", (255, 255, 255))
        img = create_background(canvas_w, canvas_h, bg_color)
        draw = ImageDraw.Draw(img)
        
        # Title removed - no longer displaying app name
        title_height_used = 0
        
        # Caption text with highlight support
        font_size = dev_spec["base_font_size"]
        max_text_width = canvas_w - 140
        font, applied_size = get_fitted_font(draw, caption_text, max_text_width, font_size, FONT_PATH)
        
        # No title, start from a higher position
        y_text = dev_spec["y_text_start"] - 100  # Move up when no title
        
        text_color = config.get("text_color", (0, 0, 0))
        highlight_color = config.get("highlight_color", (0, 122, 255))  # Default blue
        stroke_color = config["stroke_color"]
        stroke_width = max(6, int(applied_size / 15))

        # Draw text with highlights (single line)
        if highlight_words:
            # Draw text with mixed colors
            x_text = canvas_w / 2
            draw_text_with_highlights(draw, caption_text, x_text, y_text, font, text_color, highlight_color, highlight_words, stroke_color, stroke_width)
        else:
            # Draw normal text
            if hasattr(draw, 'textlength'):
                w = draw.textlength(caption_text, font=font)
            else:
                w = draw.textsize(caption_text, font=font)[0]
            x_text = (canvas_w - w) / 2
            draw_text_with_stroke(draw, caption_text, x_text, y_text, font, text_color, stroke_color, stroke_width)
            
        # Load screenshots
        src_path = os.path.join(doc_dir, filename)
        try:
            ss = Image.open(src_path)
        except:
            print(f"Failed to open {src_path}")
            continue

        # Resize Screenshot
        target_w = int(canvas_w * dev_spec["screenshot_resize_ratio"])
        ratio = target_w / ss.width
        target_h = int(ss.height * ratio)
        ss = ss.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Device frame settings
        padding = dev_spec["padding"]
        bezel_top = dev_spec["bezel_top"]
        bezel_bottom = dev_spec["bezel_bottom"]
        radius = dev_spec["body_radius"]
        rotation = dev_spec.get("rotation_angle", 0)
        
        body_w = target_w + padding * 2
        body_h = target_h + bezel_top + bezel_bottom
        
        # Calculate device position
        # Ensure text and device don't overlap
        # If no title, move device up by the title height that would have been used
        y_phone_offset = dev_spec["y_phone_offset"]
        if not (title and i == 0):
            # Move up by approximately the title height to compensate for missing title
            y_phone_offset = dev_spec["y_phone_offset"] - title_height_used - 50
        
        # Add spacing between text and device to prevent overlap
        text_bottom = y_text + applied_size + 20  # Bottom of text with some padding
        y_body = text_bottom + 40  # Add 40px spacing between text and device
        if y_body < 500: y_body = 500  # Minimum top margin
        
        # Determine frame path based on device type
        frame_path = None
        if device_type == "iphone" and os.path.exists(IPHONE_FRAME_PATH):
            frame_path = IPHONE_FRAME_PATH
        
        # Handle double layout for first two pages
        if layout == "double" and i == 0:
            # Overlapping layout: place two devices on first page
            # First device (left, rotated left)
            x_body1 = canvas_w // 2 - body_w // 2 - 100
            angle1 = -rotation
            
            paste_rotated_device(
                img, ss, x_body1 + body_w // 2, y_body + body_h // 2,
                padding, bezel_top, bezel_bottom, radius, angle1, shadow_offset=20, frame_path=frame_path
            )
            
            # Second device (right, rotated right) - use next screenshot if available
            if i + 1 < len(files) and i + 1 < len(captions):
                next_filename = files[i + 1]
                next_src_path = os.path.join(doc_dir, next_filename)
                try:
                    ss2 = Image.open(next_src_path)
                    ss2 = ss2.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    
                    x_body2 = canvas_w // 2 - body_w // 2 + 100
                    angle2 = rotation
                    
                    paste_rotated_device(
                        img, ss2, x_body2 + body_w // 2, y_body + body_h // 2,
                        padding, bezel_top, bezel_bottom, radius, angle2, shadow_offset=20, frame_path=frame_path
                    )
                except:
                    pass
            
            # Output first page with both devices
            out_name = f"{device_type}_{i+1}.png"
            img.save(os.path.join(out_dir, out_name))
            print(f"Saved {out_name}")
            
            # Skip second page if we used it in the double layout
            if i + 1 < len(files) and i + 1 < len(captions):
                continue
        elif layout == "double" and i == 1:
            # Skip second page if it was already used in first page
            continue
        else:
            # Single device layout
            x_body = (canvas_w - body_w) // 2
            angle = 0
            
            paste_rotated_device(
                img, ss, x_body + body_w // 2, y_body + body_h // 2,
                padding, bezel_top, bezel_bottom, radius, angle, shadow_offset=20, frame_path=frame_path
            )
            
            # Output
            out_name = f"{device_type}_{i+1}.png"
            img.save(os.path.join(out_dir, out_name))
            print(f"Saved {out_name}")

if __name__ == "__main__":
    # Process apps if files exist
    process_app("pet-medication")
    process_app("quote-calendar")
    process_app("trivia-calendar")
    process_app("triming-log")
    process_app("parking-calculator")
    process_app("exam-countdown")
    process_app("overtime-meter")
    process_app("drive-log")
    process_app("screenshot-poi")
    process_app("aquarium-note")
    process_app("work-quest")