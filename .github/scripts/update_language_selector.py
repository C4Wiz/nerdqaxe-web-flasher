import re
import os
import json
import urllib.request

# Read config.ts to get the list of supported languages
with open('src/i18n/config.ts', encoding='utf-8') as f:
    config = f.read()

# Extract language codes from import statements
codes = re.findall(r"^import ([a-z]{2}) from './locales/", config, re.MULTILINE)

# Always put 'en' first, then sort the rest
if 'en' in codes:
    codes.remove('en')
codes = ['en'] + sorted(codes)

print(f'Detected language codes: {codes}')

# Ask Claude to return native language names for each code
api_key = os.environ['ANTHROPIC_API_KEY']
prompt = (
    f'Return a JSON object mapping each of these ISO 639-1 language codes to its native language name '
    f'(i.e. the name of the language written in that language itself). '
    f'Codes: {json.dumps(codes)}. '
    f'Example format: {{"en": "English", "de": "Deutsch", "fr": "Français"}}. '
    f'Return only valid JSON, no markdown, no explanation.'
)

payload = json.dumps({
    'model': 'claude-sonnet-4-5',
    'max_tokens': 256,
    'messages': [{'role': 'user', 'content': prompt}]
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.anthropic.com/v1/messages',
    data=payload,
    headers={
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
    }
)

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())

raw = data['content'][0]['text'].strip()
raw = re.sub(r'^```json\s*', '', raw)
raw = re.sub(r'^```\s*', '', raw)
raw = re.sub(r'```\s*$', '', raw)

lang_labels = json.loads(raw)
print(f'Native language names: {lang_labels}')

# Build the languages array
lines = []
for code in codes:
    label = lang_labels.get(code, code)
    lines.append(f"    {{ value: '{code}', label: '{label}' }},")

languages_array = '\n'.join(lines)

# Write the updated LanguageSelector.tsx
content = f"""import {{ useTranslation }} from 'react-i18next';
import {{ Select, SelectContent, SelectItem, SelectTrigger, SelectValue }} from './ui/select';

const LanguageSelector = () => {{
  const {{ i18n, t }} = useTranslation();

  const languages = [
{languages_array}
  ];

  const handleLanguageChange = (value: string) => {{
    i18n.changeLanguage(value);
  }};

  const getCurrentLanguageLabel = () => {{
    return languages.find(lang => lang.value === i18n.language)?.label || i18n.language;
  }};

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm">{{t('common.language')}}:</span>
      <Select value={{i18n.language}} onValueChange={{handleLanguageChange}}>
        <SelectTrigger className="w-28">
          <SelectValue placeholder={{getCurrentLanguageLabel()}}>
            {{getCurrentLanguageLabel()}}
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          {{languages.map((lang) => (
            <SelectItem key={{lang.value}} value={{lang.value}}>
              {{lang.label}}
            </SelectItem>
          ))}}
        </SelectContent>
      </Select>
    </div>
  );
}};

export default LanguageSelector;
"""

with open('src/components/LanguageSelector.tsx', 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Updated LanguageSelector.tsx')
