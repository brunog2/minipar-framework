const KEYWORDS = [
  'class',
  'extends',
  'new',
  'this',
  'super',
  'func',
  'var',
  'if',
  'else',
  'while',
  'do',
  'for',
  'return',
  'break',
  'continue',
  'seq',
  'par',
  'c_channel',
  's_channel',
  'in',
  'print',
  'println',
  'input',
  'send',
  'receive',
];

const TYPES = ['number', 'string', 'bool', 'void', 'list', 'dict'];

const ATOMS = ['true', 'false', 'null'];

export function registerMiniparLanguage(): void {
  const monaco = (window as Window & { monaco?: typeof import('monaco-editor') })
    .monaco;
  if (!monaco) {
    return;
  }

  monaco.languages.register({ id: 'minipar' });

  monaco.languages.setMonarchTokensProvider('minipar', {
    keywords: KEYWORDS,
    typeKeywords: TYPES,
    atoms: ATOMS,

    tokenizer: {
      root: [
        [/#.*$/, 'comment'],
        [/"([^"\\]|\\.)*$/, 'string.invalid'],
        [/"/, 'string', '@string_double'],
        [/'([^'\\]|\\.)*$/, 'string.invalid'],
        [/'/, 'string', '@string_single'],
        [/\d+(\.\d+)?/, 'number'],
        [
          /[a-zA-Z_]\w*/,
          {
            cases: {
              '@keywords': 'keyword',
              '@typeKeywords': 'type',
              '@atoms': 'constant',
              '@default': 'identifier',
            },
          },
        ],
        [/[+\-*/%<>=!&|^~]+/, 'operator'],
        [/[{}()[\];,.:]/, 'delimiter'],
        [/\s+/, 'white'],
      ],
      string_double: [
        [/[^\\"]+/, 'string'],
        [/\\./, 'string.escape'],
        [/"/, 'string', '@pop'],
      ],
      string_single: [
        [/[^\\']+/, 'string'],
        [/\\./, 'string.escape'],
        [/'/, 'string', '@pop'],
      ],
    },
  });
}
