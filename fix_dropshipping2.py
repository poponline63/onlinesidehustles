
with open('dropshipping.html', encoding='utf-8') as f:
    content = f.read()

# Find the first script block to clean (the one with nav scroll at the top)
# Find start of this specific block
script1_marker = '<script>\n// Nav scroll\nconst nav = document.getElementById'
script1_start = content.find('<script>\n// Nav scroll')
if script1_start == -1:
    # Try alternate search
    script1_start = content.find('// Nav scroll\nconst nav')
    if script1_start != -1:
        # Back up to find the opening <script> tag
        script1_start = content.rfind('<script>', 0, script1_start)

if script1_start == -1:
    print("Could not find first script block by nav scroll marker")
    # Show all <script> positions
    pos = 0
    while True:
        p = content.find('<script>', pos)
        if p == -1:
            break
        print(f"  <script> at {p}: {repr(content[p:p+60])}")
        pos = p + 1
else:
    print(f"Found first script block at {script1_start}")
    # Find its end
    script1_end = content.find('</script>', script1_start) + len('</script>')
    print(f"Ends at {script1_end}")
    print(f"Preview: {repr(content[script1_start:script1_start+120])}")

    # Replace with minimal version keeping fade-in and FAQ
    replacement = '''<script>
// Scroll fade-in
const fadeObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); fadeObs.unobserve(entry.target); }
    });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.anim-fade-up').forEach(el => fadeObs.observe(el));

// FAQ accordion
document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
        const item = q.parentElement;
        const wasOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
        if (!wasOpen) item.classList.add('open');
    });
});
</script>'''

    new_content = content[:script1_start] + replacement + content[script1_end:]
    with open('dropshipping.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Done. New file length: {len(new_content)}")
