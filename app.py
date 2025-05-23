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
    bbox = draw.textbbox((0, 0), text, font=font) text_width = bbox[2] - bbox[0] text_height = bbox[3] - bbox[1]

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



import traceback  # Add this to the top

@app.route('/countdown')
def countdown():
    try:
        end = request.args.get('end')
        end_dt = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.utcnow()
        remaining = end_dt - now

        if remaining.total_seconds() < 0:
            text = "00:00:00"
        else:
            hours, rem = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(rem, 60)
            text = f"{hours:02}:{minutes:02}:{seconds:02}"

        img = Image.new('RGB', (220, 60), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font) text_width = bbox[2] - bbox[0] text_height = bbox[3] - bbox[1]
        draw.text(((220 - text_width) / 2, (60 - text_height) / 2), text, font=font, fill=(0, 0, 0))

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        print("Error:", e)
        print(traceback.format_exc())  # This shows the full traceback in the Render logs
        return "Something went wrong", 500
