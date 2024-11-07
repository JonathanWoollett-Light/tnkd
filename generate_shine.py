import re

def read_sprite_file(input_path):
    """Read and parse the input sprite definitions file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_sprite_file(output_path, content):
    """Write the modified sprite definitions to a file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

def add_shine_effects(sprite_content):
    """Add shine effects to each spriteType definition."""
    # Pattern to match individual spriteType blocks
    sprite_pattern = re.compile(
        r'spriteType\s*=\s*{[^}]*?name\s*=\s*"([^"]*)"[^}]*?texturefile\s*=\s*"([^"]*)"[^}]*?}',
        re.DOTALL
    )
    
    # Find all sprite definitions
    sprites = list(sprite_pattern.finditer(sprite_content))
    
    # If no sprites found, return original content
    if not sprites:
        return sprite_content
    
    # Build new content
    new_content = "spriteTypes = {\n"
    
    for match in sprites:
        original_sprite = match.group(0)
        name = match.group(1)
        texturefile = match.group(2)
        
        # Add _shine suffix to the name
        shine_name = f"{name}_shine"
        
        # Create new sprite definition with animations
        new_sprite = f'''    spriteType = {{
        name = "{shine_name}"
        texturefile = "{texturefile}"
        effectFile = "gfx/FX/buttonstate.lua"
        animation = {{
            animationmaskfile = "{texturefile}"
            animationtexturefile = "gfx/interface/goals/shine_overlay.dds"
            animationrotation = -90.0        # -90 clockwise 90 counterclockwise(by default)
            animationlooping = no            # yes or no ;)
            animationtime = 0.75             # in seconds
            animationdelay = 0               # in seconds
            animationblendmode = "add"       #add, multiply, overlay
            animationtype = "scrolling"      #scrolling, rotating, pulsing
            animationrotationoffset = {{ x = 0.0 y = 0.0 }}
            animationtexturescale = {{ x = 1.0 y = 1.0 }}
        }}
        animation = {{
            animationmaskfile = "{texturefile}"
            animationtexturefile = "gfx/interface/goals/shine_overlay.dds"
            animationrotation = 90.0         # -90 clockwise 90 counterclockwise(by default)
            animationlooping = no            # yes or no ;)
            animationtime = 0.75             # in seconds
            animationdelay = 0               # in seconds
            animationblendmode = "add"       #add, multiply, overlay
            animationtype = "scrolling"      #scrolling, rotating, pulsing
            animationrotationoffset = {{ x = 0.0 y = 0.0 }}
            animationtexturescale = {{ x = 1.0 y = 1.0 }}
        }}
        legacy_lazy_load = no
    }}'''
        new_content += new_sprite + "\n"
    
    new_content += "}"
    return new_content

def main():
    import sys
    import os
    
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/sprite_definitions.gfx")
        return
    
    input_path = sys.argv[1]
    
    # Create output path by adding _with_shine before the extension
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_with_shine{ext}"
    
    try:
        # Read input file
        content = read_sprite_file(input_path)
        
        # Add shine effects
        modified_content = add_shine_effects(content)
        
        # Write output file
        write_sprite_file(output_path, modified_content)
        
        print(f"Successfully created shine definitions at {output_path}")
    
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()