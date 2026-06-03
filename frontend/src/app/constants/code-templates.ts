export type CodeTemplateCategory = 'valid' | 'syntax' | 'semantic';

export interface CodeTemplate {
  id: string;
  label: string;
  category: CodeTemplateCategory;
  description: string;
  expectedResult: string;
  code: string;
}

export interface CodeTemplateGroup {
  category: CodeTemplateCategory;
  label: string;
  templates: CodeTemplate[];
}

export const CODE_TEMPLATE_GROUPS: CodeTemplateGroup[] = [
  {
    category: 'valid',
    label: 'Compilação bem-sucedida',
    templates: [
      {
        id: 'empty-class',
        label: '01 — Classe com método run',
        category: 'valid',
        description:
          'Programa mínimo com uma classe Main e um método run que imprime uma mensagem.',
        expectedResult: 'Compilação OK. Saída esperada na Fase 2: ok.',
        code: `class Main {
  void run() {
    println("ok");
  }
}
`,
      },
      {
        id: 'class-extends',
        label: '02 — Herança com extends',
        category: 'valid',
        description:
          'Duas classes: Animal com atributo name e Dog que estende Animal e define bark().',
        expectedResult:
          'Compilação OK. Valida herança, campos e métodos em hierarquia.',
        code: `class Animal {
  string name;
}

class Dog extends Animal {
  void bark() {
    println("woof");
  }
}
`,
      },
      {
        id: 'print-global',
        label: '03 — println fora de classe',
        category: 'valid',
        description:
          'Chamada println no nível global do programa, sem envolver classe.',
        expectedResult:
          'Compilação OK (se permitido pela gramática). Saída esperada: hello MiniPar.',
        code: `println("hello MiniPar");
`,
      },
      {
        id: 'sierpinski',
        label: '13 — Tapete de Sierpinski (OO)',
        category: 'valid',
        description:
          'Fractal recursivo orientado a objetos: matriz de caracteres * e . exibida no console.',
        expectedResult:
          'Compilação OK. Saída: matriz 27x27 do tapete de Sierpinski via Interpretador.',
        code: `class Sierpinski {
  number isBlack(number x, number y, number n) {
    if (n == 1) {
      return 1;
    }
    number m = n / 3;
    if (x >= m && x < 2 * m && y >= m && y < 2 * m) {
      return 0;
    }
    return this.isBlack(x % m, y % m, m);
  }

  void draw(number order) {
    number n = 1;
    number i = 0;
    while (i < order) {
      n = n * 3;
      i = i + 1;
    }
    number row = 0;
    while (row < n) {
      number col = 0;
      string line = "";
      while (col < n) {
        if (this.isBlack(col, row, n) == 1) {
          line = line + "*";
        } else {
          line = line + ".";
        }
        col = col + 1;
      }
      println(line);
      row = row + 1;
    }
  }
}

class Main {
  void run() {
    Sierpinski carpet = new Sierpinski();
    println("Tapete de Sierpinski (ordem 3):");
    carpet.draw(3);
  }
}
`,
      },
    ],
  },
  {
    category: 'valid',
    label: 'Fase 3 — Demonstrações',
    templates: [
      {
        id: 'channels-par',
        label: '15 — Canais Send/Receive (PAR)',
        category: 'valid',
        description:
          'Declara um canal s_channel, dispara dois branches em paralelo: um envia 42, o outro recebe e armazena em result.',
        expectedResult:
          'Saída esperada: 42. Valida PAR com processos isolados e comunicação via canal.',
        code: `class Main {
  void run() {
    s_channel ch();
    par {
      send(ch, 42);
      receive(ch, result);
    }
    println(result);
  }
}
`,
      },
      {
        id: 'distributed-menu',
        label: '14 — Menu coordenador (3 máquinas)',
        category: 'valid',
        description:
          'Use modo DISTRIBUTED_SOCKETS na UI. O coordenador dispara QuickSort, matriz e fatorial via sockets.',
        expectedResult:
          'Saída agregada: QuickSort (PC1), Matriz (PC2), Fatorial (PC3).',
        code: `class Main {
  void run() {
    println("Menu coordenador: selecione DISTRIBUTED_SOCKETS e Executar.");
  }
}
`,
      },
    ],
  },
  {
    category: 'syntax',
    label: 'Erros de sintaxe (parse)',
    templates: [
      {
        id: 'extends-missing',
        label: '05 — extends sem nome da superclasse',
        category: 'syntax',
        description:
          'A cláusula extends está incompleta: falta o identificador da classe pai.',
        expectedResult:
          'Erro de parse. O analisador deve reportar token inesperado após extends.',
        code: `class Animal {
  string name;
}

class Dog extends  {
  void bark() {
    println("woof");
  }
}
`,
      },
      {
        id: 'invalid-keyword',
        label: '06 — Palavra-chave inválida (exts)',
        category: 'syntax',
        description:
          'Usa "exts" em vez de "extends". Testa reconhecimento de palavras reservadas.',
        expectedResult:
          'Erro de parse. O lexer/parser deve rejeitar a palavra-chave incorreta.',
        code: `class Animal {
  string name;
}

class Dog exts  {
  void bark() {
    println("woof");
  }
}
`,
      },
      {
        id: 'expr-only',
        label: '07 — Expressão solta no programa',
        category: 'syntax',
        description:
          'Um identificador isolado no topo do arquivo, fora de qualquer declaração válida.',
        expectedResult:
          'Parse e semântica OK (ExprStmt). Com Interpretador: erro de runtime — variável a indefinida.',
        code: `a
`,
      },
    ],
  },
  {
    category: 'semantic',
    label: 'Erros semânticos',
    templates: [
      {
        id: 'extends-unknown',
        label: '04 — Superclasse inexistente',
        category: 'semantic',
        description:
          'Dog estende "Arvore", mas essa classe não foi declarada no programa.',
        expectedResult:
          'Parse OK, mas análise semântica deve falhar: superclasse Arvore não encontrada.',
        code: `class Animal {
  string name;
}

class Dog extends Arvore {
  void bark() {
    println("woof");
  }
}
`,
      },
    ],
  },
];

export const ALL_CODE_TEMPLATES: CodeTemplate[] = CODE_TEMPLATE_GROUPS.flatMap(
  (g) => g.templates,
);

export function findCodeTemplate(id: string): CodeTemplate | undefined {
  return ALL_CODE_TEMPLATES.find((t) => t.id === id);
}
