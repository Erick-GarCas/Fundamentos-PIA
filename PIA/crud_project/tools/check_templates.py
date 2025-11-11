import os
from pathlib import Path
p = Path('app/templates')
errors = []
for f in p.rglob('*.html'):
    text = f.read_text(encoding='utf-8')
    # check extends first tag
    stripped = text.lstrip()
    if stripped.startswith('{% load'):
        # ok load before extends allowed? Actually extends must be first tag, but load can be before extends? Django allows load before extends? No, extends must be first tag except for whitespace and comments.
        pass
    if '{% extends' in text:
        idx = text.find('{% extends')
        pre = text[:idx]
        if pre.strip():
            errors.append((str(f), 'extends not first tag'))
    # check any template tags after final endblock
    last_endblock = text.rfind('{% endblock')
    if last_endblock != -1:
        after = text[last_endblock+1:]
        if '{%' in after or '{{' in after:
            errors.append((str(f), 'template tags after last endblock'))
    # naive count of if/endif
    if_count = text.count('{% if')
    endif_count = text.count('{% endif')
    for_count = text.count('{% for')
    endfor_count = text.count('{% endfor')
    if if_count != endif_count:
        errors.append((str(f), f'if/endif count mismatch: {if_count}/{endif_count}'))
    if for_count != endfor_count:
        errors.append((str(f), f'for/endfor count mismatch: {for_count}/{endfor_count}'))

for e in errors:
    print(e)
print('Done. Scanned', sum(1 for _ in p.rglob('*.html')),'templates')
