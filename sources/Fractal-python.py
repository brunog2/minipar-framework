import turtle

def draw_sierpinski_carpet(x, y, r, degree):
    """
    Desenha o fractal do tapete de Sierpinski recursivamente.
    x, y: coordenadas do centro do quadrado.
    r: metade do comprimento do lado do quadrado.
    degree: número de iterações.
    """
    if degree <= 0:
        return

    # Desenha o quadrado central que está sendo removido (ou o próprio quadrado)
    turtle.up()
    turtle.goto(x - r, y - r)
    turtle.down()
    # Usa uma cor para o "espaço" vazio, como branco, para simular a remoção
    # Ou uma cor de destaque para o centro preenchido, dependendo da interpretação do algoritmo.
    # O código original parece desenhar o quadrado, então vamos preencher o centro.
    turtle.fillcolor("white")
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(2 * r)
        turtle.left(90)
    turtle.end_fill()
    
    # Previne que o quadrado central seja desenhado nas chamadas recursivas,
    # caso o objetivo seja um tapete vazio no centro.
    # Para o desenho da imagem, o quadrado central é desenhado.

    # Chamadas recursivas para os 8 quadrados menores ao redor do centro
    new_r = r / 3
    new_degree = degree - 1

    # Quadrante superior esquerdo (x-r, y+r) na definição da imagem
    draw_sierpinski_carpet(x - new_r, y + new_r, new_r, new_degree)
    # Quadrante superior direito (x+r, y+r) na definição da imagem
    draw_sierpinski_carpet(x + new_r, y + new_r, new_r, new_degree)
    # Quadrante inferior esquerdo (x-r, y-r) na definição da imagem
    draw_sierpinski_carpet(x - new_r, y - new_r, new_r, new_degree)
    # Quadrante inferior direito (x+r, y-r) na definição da imagem
    draw_sierpinski_carpet(x + new_r, y - new_r, new_r, new_degree)
    
    # Adicionando os outros 4 quadrados laterais/horizontais/verticais
    draw_sierpinski_carpet(x - new_r, y, new_r, new_degree) # Esquerda
    draw_sierpinski_carpet(x + new_r, y, new_r, new_degree) # Direita
    draw_sierpinski_carpet(x, y + new_r, new_r, new_degree) # Cima
    draw_sierpinski_carpet(x, y - new_r, new_r, new_degree) # Baixo
    
    # O centro (x, y) não é chamado recursivamente.

def main():
    turtle.speed(0)  # Velocidade máxima de desenho
    turtle.hideturtle()
    turtle.tracer(100, 0) # Acelera a visualização
    
    # Definir as dimensões iniciais
    initial_x = 0
    initial_y = 0
    initial_r = 150 # Metade do lado
    iterations = 60  # Número de iterações (grau de profundidade)

    # Iniciar o desenho do fractal
    # O primeiro quadrado é o maior, que contém todos os outros
    # Desenha o quadrado inicial grande (opcional, pode ser o fundo)
    # draw_square(initial_x, initial_y, initial_r) 

    # Começa o processo recursivo que preenche os sub-quadrados
    draw_sierpinski_carpet(initial_x, initial_y, initial_r, iterations)

    turtle.update() # Atualiza a tela após desenhar tudo
    turtle.done()

if __name__ == "__main__":
    main()