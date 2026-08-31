#!/usr/bin/env python3
"""
Convert reviews carousel to static grid layout across all HTML files.
Changes:
1. reviews-carousel container -> reviews-grid
2. Remove arrow buttons
3. reviews-track -> reviews-grid inner
4. CSS: flex horizontal scroll -> CSS Grid responsive columns
5. Remove scrollReviews JS function
"""

import re
import glob
import os

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'reviews-carousel' not in content:
        return False
    
    original = content
    
    # 1. Remove the opening carousel container with arrow buttons
    # Old: <div class="reviews-carousel" id="reviewsCarousel">
    #        <button class="reviews-arrow reviews-arrow-left" ...>
    #        <div class="reviews-track" id="reviewsTrack">
    # New: <div class="reviews-grid">
    content = re.sub(
        r'<div class="reviews-carousel"[^>]*>\s*'
        r'<button class="reviews-arrow reviews-arrow-left"[^>]*>.*?</button>\s*'
        r'<div class="reviews-track"[^>]*>',
        '<div class="reviews-grid">',
        content,
        flags=re.DOTALL
    )
    
    # 2. Remove closing track + right arrow + closing carousel
    # Old: </div>
    #        <button class="reviews-arrow reviews-arrow-right" ...>
    #      </div>
    # New: </div>
    content = re.sub(
        r'</div>\s*'
        r'<button class="reviews-arrow reviews-arrow-right"[^>]*>.*?</button>\s*'
        r'</div>',
        '</div>',
        content
    )
    
    # 3. Replace CSS block - carousel styles -> grid styles
    old_css_es = r'''<style>
    \.reviews-carousel \{
      position: relative;
      overflow: hidden;
      margin: 0 -10px;
    \}
    \.reviews-track \{
      display: flex;
      gap: 16px;
      overflow-x: auto;
      scroll-behavior: smooth;
      padding: 10px 45px;
      -ms-overflow-style: none;
      scrollbar-width: none;
    \}
    \.reviews-track::-webkit-scrollbar \{ display: none; \}
    \.google-review-card \{
      min-width: 300px;
      max-width: 340px;
      flex-shrink: 0;
      background: #fff;
      border: 1px solid #e8eaed;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 2px 12px rgba\(0,0,0,0\.06\);
      transition: transform 0\.3s, box-shadow 0\.3s;
    \}
    \.google-review-card:hover \{
      transform: translateY\(-3px\);
      box-shadow: 0 6px 20px rgba\(0,0,0,0\.1\);
    \}
    \.reviews-arrow \{
      position: absolute;
      top: 50%;
      transform: translateY\(-50%\);
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 1px solid #dadce0;
      background: #fff;
      color: #5f6368;
      font-size: 0\.85rem;
      cursor: pointer;
      z-index: 5;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px rgba\(0,0,0,0\.1\);
      transition: all 0\.2s;
    \}
    \.reviews-arrow:hover \{ background:#f1f3f4; border-color:#a80000; color:#a80000; \}
    \.reviews-arrow-left \{ left: 4px; \}
    \.reviews-arrow-right \{ right: 4px; \}
    @media \(max-width: 768px\) \{
      \.google-review-card \{ min-width: 260px; max-width: 280px; padding: 16px; \}
      \.reviews-track \{ padding: 10px 40px; \}
    \}
  </style>'''
    
    new_css_es = '''<style>
    .reviews-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 16px;
      padding: 0;
    }
    .google-review-card {
      background: #fff;
      border: 1px solid #e8eaed;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.06);
      transition: transform 0.3s, box-shadow 0.3s;
    }
    .google-review-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    @media (max-width: 768px) {
      .reviews-grid { grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px; }
      .google-review-card { padding: 16px; }
    }
    @media (max-width: 480px) {
      .reviews-grid { grid-template-columns: 1fr; }
    }
  </style>'''
    
    content = re.sub(old_css_es, new_css_es, content, flags=re.DOTALL)
    
    # Also try to match CSS for EN version (same structure, slightly different indentation possible)
    # Try a more flexible pattern
    if 'reviews-carousel' in content:
        # Flexible pattern for any CSS block containing reviews-carousel
        content = re.sub(
            r'<style>\s*\.reviews-carousel\s*\{[^}]*\}\s*\.reviews-track\s*\{[^}]*\}[^<]*\.reviews-track::-webkit-scrollbar\s*\{[^}]*\}\s*\.google-review-card\s*\{[^}]*\}\s*\.google-review-card:hover\s*\{[^}]*\}\s*\.reviews-arrow\s*\{[^}]*\}\s*\.reviews-arrow:hover\s*\{[^}]*\}\s*\.reviews-arrow-left\s*\{[^}]*\}\s*\.reviews-arrow-right\s*\{[^}]*\}\s*@media\s*\([^)]+\)\s*\{[^}]*\}\s*</style>',
            new_css_es,
            content,
            flags=re.DOTALL
        )
    
    # 4. Remove scrollReviews script
    content = re.sub(
        r'\s*<script>\s*function\s+scrollReviews\s*\([^)]*\)\s*\{[^}]*\}\s*</script>',
        '',
        content
    )
    
    # Also remove any inline scrollReviews if present
    content = re.sub(
        r'\s*<script>\s*function scrollReviews[^<]*</script>',
        '',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False


# Find all HTML files with the carousel
files = []
for pattern in ['**/*.html']:
    files.extend(glob.glob(pattern, recursive=True))

changed = 0
for filepath in sorted(files):
    if process_file(filepath):
        changed += 1
        print(f"  ✓ {filepath}")

print(f"\n✅ Total archivos modificados: {changed}")
