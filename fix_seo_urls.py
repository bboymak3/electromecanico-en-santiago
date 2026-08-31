#!/usr/bin/env python3
"""
FIX SEO - Convertir TODOS los href relativos a absolutos y eliminar <base href>
Esto soluciona el problema de 894 URLs basura en Google Search Console.

Causa raíz: Los href relativos como href="comunas/santiago.html" se resuelven
incorrectamente cuando Google accede al sitio desde URLs no canónicas, generando
URLs basura como /taxis/comunas/santiago.html en efecto cascada.

Solución: Convertir TODOS los href a rutas absolutas (/comunas/santiago.html)
y eliminar las etiquetas <base href> que ya no son necesarias.
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_html_files():
    """Get all HTML files in the project"""
    patterns = [
        os.path.join(BASE_DIR, '*.html'),
        os.path.join(BASE_DIR, 'comunas', '*.html'),
        os.path.join(BASE_DIR, 'vehiculos', '*.html'),
        os.path.join(BASE_DIR, 'servicios', '*.html'),
        os.path.join(BASE_DIR, 'blog', '*.html'),
        os.path.join(BASE_DIR, 'marcas_automotrices', '*.html'),
    ]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))
    return files

def get_relative_dir(filepath):
    """Get the directory of the file relative to BASE_DIR"""
    return os.path.relpath(os.path.dirname(filepath), BASE_DIR)

def fix_href_in_file(filepath):
    """Convert all relative hrefs to absolute paths in an HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    rel_dir = get_relative_dir(filepath)
    
    # 1. Remove <base href> tags
    content = re.sub(r'<base\s+href="[^"]*"\s*/?>', '', content)
    content = re.sub(r"<base\s+href='[^']*'\s*/?>", '', content)
    
    # 2. Fix ../globalpro.html -> / (broken link in vehiculos and marcas pages)
    content = content.replace('href="../globalpro.html"', 'href="/"')
    content = content.replace("href='../globalpro.html'", "href='/'")
    
    # 3. Convert relative hrefs to absolute based on the file's directory
    # We need to handle different patterns:
    #   - From root: href="comunas/santiago.html" -> href="/comunas/santiago.html"
    #   - From /comunas/: href="../index.html" -> href="/"
    #   - From /comunas/: href="santiago.html" -> href="/comunas/santiago.html"
    #   - From /vehiculos/: href="ford-fiesta.html" -> href="/vehiculos/ford-fiesta.html"
    #   - From /vehiculos/: href="../comunas/santiago.html" -> href="/comunas/santiago.html"
    #   - From /blog/: href="index.html" -> href="/blog/"
    #   - From /servicios/: href="cambio-de-aceite-a-domicilio.html" -> href="/servicios/cambio-de-aceite-a-domicilio.html"
    
    def convert_href(match):
        full_match = match.group(0)
        quote_char = match.group(1)  # " or '
        href_value = match.group(2)
        
        # Skip absolute URLs, anchors, protocols, and mailto/tel/javascript
        if href_value.startswith('/') or href_value.startswith('#') or \
           href_value.startswith('http://') or href_value.startswith('https://') or \
           href_value.startswith('mailto:') or href_value.startswith('tel:') or \
           href_value.startswith('javascript:') or href_value.startswith('data:') or \
           href_value == '' or href_value == '#':
            return full_match
        
        # Calculate absolute path from relative path
        # Resolve .. and . components
        if rel_dir == '.':
            # File is in root directory
            abs_path = '/' + href_value
        else:
            # File is in a subdirectory
            parts = rel_dir.replace('\\', '/').split('/')
            href_parts = href_value.split('/')
            
            for part in href_parts:
                if part == '..':
                    if parts:
                        parts.pop()
                elif part != '.':
                    parts.append(part)
            
            abs_path = '/' + '/'.join(parts)
        
        # Normalize: remove double slashes, trailing dots
        abs_path = abs_path.replace('//', '/')
        
        # Convert .html extensions to clean URLs (without .html) for page links
        # But keep .html for files that exist with .html (like in /blog/)
        # Actually, let's keep the .html for now since Cloudflare handles the redirect
        
        # Special case: index.html -> directory with trailing slash
        if abs_path.endswith('/index.html'):
            abs_path = abs_path[:-10] + '/'
            if not abs_path.endswith('/'):
                abs_path += '/'
        # Special case: ../index.html from root files -> /
        elif abs_path == '/index.html':
            abs_path = '/'
        
        return f'href={quote_char}{abs_path}{quote_char}'
    
    # Match href="value" or href='value'
    content = re.sub(r'href=(["\'])([^"\']+)\1', convert_href, content)
    
    # 4. Also fix src attributes for images that might be relative
    # (only fix src that starts with ../ or relative paths, not http or /)
    def convert_src(match):
        full_match = match.group(0)
        quote_char = match.group(1)
        src_value = match.group(2)
        
        if src_value.startswith('/') or src_value.startswith('#') or \
           src_value.startswith('http://') or src_value.startswith('https://') or \
           src_value.startswith('data:') or src_value.startswith('mailto:') or \
           src_value.startswith('tel:'):
            return full_match
        
        # Calculate absolute path
        if rel_dir == '.':
            abs_path = '/' + src_value
        else:
            parts = rel_dir.replace('\\', '/').split('/')
            src_parts = src_value.split('/')
            
            for part in src_parts:
                if part == '..':
                    if parts:
                        parts.pop()
                elif part != '.':
                    parts.append(part)
            
            abs_path = '/' + '/'.join(parts)
        
        abs_path = abs_path.replace('//', '/')
        return f'src={quote_char}{abs_path}{quote_char}'
    
    content = re.sub(r'src=(["\'])([^"\']+)\1', convert_src, content)
    
    # 5. Fix action attributes in forms
    def convert_action(match):
        full_match = match.group(0)
        quote_char = match.group(1)
        action_value = match.group(2)
        
        if action_value.startswith('/') or action_value.startswith('#') or \
           action_value.startswith('http://') or action_value.startswith('https://'):
            return full_match
        
        if rel_dir == '.':
            abs_path = '/' + action_value
        else:
            parts = rel_dir.replace('\\', '/').split('/')
            action_parts = action_value.split('/')
            
            for part in action_parts:
                if part == '..':
                    if parts:
                        parts.pop()
                elif part != '.':
                    parts.append(part)
            
            abs_path = '/' + '/'.join(parts)
        
        abs_path = abs_path.replace('//', '/')
        return f'action={quote_char}{abs_path}{quote_char}'
    
    content = re.sub(r'action=(["\'])([^"\']+)\1', convert_action, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = get_html_files()
    modified_count = 0
    
    for filepath in sorted(files):
        rel_path = os.path.relpath(filepath, BASE_DIR)
        if fix_href_in_file(filepath):
            modified_count += 1
            print(f'  ✓ Fixed: {rel_path}')
        else:
            print(f'  - No changes: {rel_path}')
    
    print(f'\nTotal: {len(files)} files scanned, {modified_count} files modified')

if __name__ == '__main__':
    main()
