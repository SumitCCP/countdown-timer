from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io, os

app = Flask(__name__)

@app.route('/countdown')
def countdown():
    end = request.args.get('end')
    try:
        end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    except:
        return "Invalid date format. Use ISO format like 2025-06-01T12:00:00Z", 400

    now = datetime.utcnow()
    remaining = end_dt - now

    if remaining.total_seconds() < 0:
        text = "00:00:00"
    else:
        hours, rem = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(rem, 60)
        text = f"{hours:02}:{minutes:02}:{seconds:02}"

    # Create a white image
    img = Image.new('RGB', (220, 60), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load default font
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)

    # Center the text
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # Serve image
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
