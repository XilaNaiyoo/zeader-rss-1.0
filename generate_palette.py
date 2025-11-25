import colorsys

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def generate_palette(base_color_hex):
    base_rgb = hex_to_rgb(base_color_hex)
    base_h, base_l, base_s = colorsys.rgb_to_hls(base_rgb[0]/255.0, base_rgb[1]/255.0, base_rgb[2]/255.0)

    # Tailwind-like lightness scale (approximate)
    # 50: 0.95, 100: 0.9, 200: 0.8, 300: 0.7, 400: 0.6, 500: 0.5, 600: 0.4, 700: 0.3, 800: 0.2, 900: 0.1, 950: 0.05
    # Adjusting to match the input color as close to 500 or 600 as possible.
    # The user's color #1d7d8c (29, 125, 140) has lightness ~0.33. This is quite dark.
    # If we map it to 600 or 700, the lighter shades will be generated accordingly.
    
    # Let's map #1d7d8c to 600 (since it's a bit dark) and generate others.
    # Or we can just generate a scale based on lightness.
    
    scales = {
        50: 0.95,
        100: 0.9,
        200: 0.8,
        300: 0.7,
        400: 0.6,
        500: 0.5,
        600: 0.4, # Target is close to this
        700: 0.3,
        800: 0.2,
        900: 0.1,
        950: 0.05
    }
    
    # We want to preserve the hue and saturation mostly, but adjust lightness.
    # However, tailwind colors also shift saturation.
    # For simplicity, let's just adjust lightness.
    
    # If we treat the input as the "primary" brand color, we usually assign it to 500 or 600.
    # Let's assign it to 600 because 29/125/140 is visually quite strong/dark.
    
    palette = {}
    
    # Calculate the "shift" needed if we were to pin it.
    # But simple lightness override is easier.
    
    for key, lightness in scales.items():
        # Adjust lightness based on the base color's lightness?
        # Or just force the lightness.
        
        # Let's try to keep the base color as one of the keys.
        # If we say #1d7d8c is 600.
        
        if key == 600:
             r, g, b = base_rgb
        else:
            # We need to interpolate or extrapolate.
            # A simple way is to blend with white (for <600) and black (for >600).
            if key < 600:
                # Blend with white
                # factor 0 = base, 1 = white
                # 50 is 95% white?
                # Let's use a simple linear interpolation for now.
                factor = (600 - key) / 600.0 * 0.9 # Scale factor
                r = base_rgb[0] + (255 - base_rgb[0]) * factor
                g = base_rgb[1] + (255 - base_rgb[1]) * factor
                b = base_rgb[2] + (255 - base_rgb[2]) * factor
            else:
                # Blend with black
                # factor 0 = base, 1 = black
                factor = (key - 600) / 400.0 * 0.8
                r = base_rgb[0] * (1 - factor)
                g = base_rgb[1] * (1 - factor)
                b = base_rgb[2] * (1 - factor)
                
        palette[key] = f"{int(r)} {int(g)} {int(b)}"
        
    return palette

p = generate_palette('#1d7d8c')
for k, v in p.items():
    print(f"--theme-primary-{k}: {v};")
