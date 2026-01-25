import os
import sys
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---

# Project Settings
BASE_PROJECT_DIR = "."
FONT_PATH = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
BACKGROUND_IMAGE_PATH = "./wood_bg.png"

# App Specific Configs
APPS = {
    "pet-medication": {
        "captions": [
            "体重・通院予定・投薬を\nしっかり管理",
            "カレンダーで\n一目瞭然",
            "体重の推移を\nグラフで確認",
            "複数のワンちゃん・ネコちゃんを\n一元管理" 
        ],
        "bg_image": BACKGROUND_IMAGE_PATH, # Default
        "text_color": (0, 0, 0),
        "stroke_color": (255, 255, 255)
    },
    "quote-calendar": {
        "captions": [
            "毎日の名言で\n心に火を灯す",
            "カレンダーで\n名言を振り返り",
            "毎日の気づきを\n記録する"
        ],
        "bg_image": BACKGROUND_IMAGE_PATH,
        "text_color": (0, 0, 0),
        "stroke_color": (255, 255, 255)
    },
    "trivia-calendar": {
        "captions": [
            "毎日の豆知識で\n会話のネタに",
            "カレンダーで\n知識を振り返り",
            "お気に入りで\nいつでも見返せる"
        ],
        "bg_image": BACKGROUND_IMAGE_PATH,
        "text_color": (0, 0, 0),
        "stroke_color": (255, 255, 255)
    },
    "triming-log": {
        "captions": [
            "愛犬のトリミングを\n美しく記録",
            "次回の予約を\n忘れない通知機能",
            "過去のスタイルを\n写真で振り返り"
        ],
        "bg_image": BACKGROUND_IMAGE_PATH,
        "text_color": (0, 0, 0),
        "stroke_color": (255, 255, 255)
    },
    "parking-calculator": {
        "captions": [
            "駐車料金を\nリアルタイム計算",
            "設定金額で\n通知してお知らせ",
            "複数の駐車場を\n比較・管理"
        ],
        "bg_image": BACKGROUND_IMAGE_PATH,
        "text_color": (0, 0, 0),
        "stroke_color": (255, 255, 255)
    },
    "exam-countdown": {
        "captions": [
            "試験日まで\nあと何日？",
            "勉強記録を\n一言添えて記録",
            "ホーム画面で\nいつでも確認",
            "アクティビティを\n確認"
        ],
        "bg_image": BACKGROUND_IMAGE_PATH,
        "text_color": (0, 0, 0),
        "stroke_color": (255, 255, 255)
    }
}

# Device Specifications
DEVICES = {
    "iphone": {
        "size": (1284, 2778), # 6.5 inch / 6.7 inch scaled
        "base_font_size": 110,
        "screenshot_resize_ratio": 0.82,
        "body_radius": 80,
        "padding": 40,
        "bezel_top": 40,
        "bezel_bottom": 40,
        "notch": None, # User reported screenshot already has notch
        "y_text_start": 250,
        "y_phone_offset": 150
    },
    "ipad": {
        "size": (2048, 2732), # iPad Pro 12.9 (approx ratio)
        "base_font_size": 140,
        "screenshot_resize_ratio": 0.85,
        "body_radius": 60,
        "padding": 50,
        "bezel_top": 50, # Uniform bezel for iPad
        "bezel_bottom": 50,
        "notch": None, # No notch usually, or uniform bezel
        "y_text_start": 200,
        "y_phone_offset": 150
    }
}

# --- HELPERS ---

def create_background(width, height, bg_path):
    try:
        bg = Image.open(bg_path)
        # Resize to cover
        scale_w = width / bg.width
        scale_h = height / bg.height
        scale = max(scale_w, scale_h)
        new_w = int(bg.width * scale)
        new_h = int(bg.height * scale)
        bg = bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        bg = bg.crop((left, top, left+width, top+height))
        return bg.convert('RGB')
    except Exception as e:
        print(f"Bg load error: {e}")
        return Image.new('RGB', (width, height), (200, 200, 200))

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
    os.makedirs(out_dir, exist_ok=True)
    
    # Identify files
    all_files = os.listdir(doc_dir)
    iphone_files = sorted([f for f in all_files if "iphone" in f.lower() and f.endswith(".png")])
    ipad_files = sorted([f for f in all_files if "ipad" in f.lower() and f.endswith(".png")])
    
    # Fallback: if no device specific name, treat all screenshot_*.png as iphone
    if not iphone_files and not ipad_files:
        iphone_files = sorted([f for f in all_files if f.startswith("screenshot_") and f.endswith(".png")])

    print(f"Processing {app_name}: found {len(iphone_files)} iPhone, {len(ipad_files)} iPad images.")

    # Process iPhone
    process_device_batch(app_name, "iphone", iphone_files, config, doc_dir, out_dir)
    
    # Process iPad
    process_device_batch(app_name, "ipad", ipad_files, config, doc_dir, out_dir)

def process_device_batch(app_name, device_type, files, config, doc_dir, out_dir):
    if not files: return
    
    dev_spec = DEVICES[device_type]
    captions = config["captions"]
    
    for i, filename in enumerate(files):
        if i >= len(captions): break
        
        caption = captions[i]
        
        # Canvas
        canvas_w, canvas_h = dev_spec["size"]
        img = create_background(canvas_w, canvas_h, config["bg_image"])
        draw = ImageDraw.Draw(img)
        
        # Text
        font_size = dev_spec["base_font_size"]
        max_text_width = canvas_w - 140
        font, applied_size = get_fitted_font(draw, caption, max_text_width, font_size, FONT_PATH)
        
        y_text = dev_spec["y_text_start"]
        lines = caption.split('\n')
        
        text_color = config["text_color"]
        stroke_color = config["stroke_color"]
        stroke_width = max(6, int(applied_size / 15))

        for line in lines:
            if hasattr(draw, 'textlength'):
                w = draw.textlength(line, font=font)
            else:
                w = draw.textsize(line, font=font)[0]
            x_text = (canvas_w - w) / 2
            
            # Stroke
            for dx in range(-stroke_width, stroke_width+1):
                for dy in range(-stroke_width, stroke_width+1):
                     if dx*dx + dy*dy <= stroke_width*stroke_width:
                        draw.text((x_text+dx, y_text+dy), line, font=font, fill=stroke_color)
            # Fill
            draw.text((x_text, y_text), line, font=font, fill=text_color)
            y_text += int(applied_size * 1.5)
            
        # Screenshot
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
        
        # Phone/Tablet Frame Geometry
        padding = dev_spec["padding"]
        bezel_top = dev_spec["bezel_top"]
        bezel_bottom = dev_spec["bezel_bottom"]
        radius = dev_spec["body_radius"]
        
        body_w = target_w + padding * 2
        body_h = target_h + bezel_top + bezel_bottom
        
        x_body = (canvas_w - body_w) // 2
        y_body = y_text + dev_spec["y_phone_offset"]
        if y_body < 700: y_body = 700 # Minimum top margin for phone
        
        # Shadow
        shadow_offset = 50
        draw.rounded_rectangle(
            [x_body + shadow_offset, y_body + shadow_offset, x_body + body_w + shadow_offset, y_body + body_h + shadow_offset],
            radius=radius, fill=(0,0,0,80)
        )
        
        # Body (Black Frame)
        draw.rounded_rectangle(
            [x_body, y_body, x_body + body_w, y_body + body_h],
            radius=radius, fill=(20, 20, 20)
        )
        
        # Screen (Paste)
        # Screen starts at body + padding + bezel_top
        img.paste(ss, (x_body + padding, y_body + bezel_top))
        
        # Notch (if any)
        notch = dev_spec.get("notch")
        if notch:
            nw, nh, nr = notch["w"], notch["h"], notch["radius"]
            nx = x_body + (body_w - nw) // 2
            ny = y_body + bezel_top # notch usually cuts into screen area, but here we place it on top bezel area?
            # Actually iPhone notch cuts into screen. 
            # Simplified: Draw notch on top of screen content
            draw.rounded_rectangle([nx, ny, nx+nw, ny+nh], radius=nr, fill=(0,0,0))
        
        # Output
        # E.g. iphone_1.png, ipad_1.png
        out_name = f"{device_type}_{i+1}.png"
        img.save(os.path.join(out_dir, out_name))
        print(f"Saved {out_name}")

if __name__ == "__main__":
    # Process both apps if files exist
    process_app("pet-medication")
    process_app("quote-calendar")
    process_app("trivia-calendar")
    process_app("triming-log")
    process_app("triming-log")
    process_app("parking-calculator")
    process_app("exam-countdown")
