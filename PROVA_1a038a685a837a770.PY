import math

# Função que retorna um código específico
def my_code():
    return "1a038a685a837a770"

# Função que retorna um nome específico
def my_name():
    return "Gabriely Di Folco Rocha"

# Classe que representa uma força com componentes x e y
class Forca:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'[{self.x:.2f}, {self.y:.2f}]'

# Classe que representa um bloco com posição (p, q) e massa (m)
class Bloco:
    def __init__(self, p, q, m):
        self.p = p
        self.q = q
        self.m = m

    def __str__(self):
        return f'({self.p:.2f}, {self.q:.2f}, {self.m:.2f})'

    # Método para aplicar uma força no bloco
    def aplica_forca(self, forca):
        if isinstance(forca, Forca):
            self.p += forca.x * (1 - math.sin(self.m)) #a bobona confundiu o domínio de sen e colocou (1 - math.sin(math.radians((self.m)))
            self.q += forca.y * (1 - math.sin(self.m))

    # Método para multiplicar um bloco por uma força usando *=
    def __imul__(self, forca):
        if isinstance(forca, Forca):
            self.p += forca.x * (1 - math.sin(self.m)
            self.q += forca.y * (1 - math.sin(self.m)
            return self
        return NotImplemented

    # Método para multiplicar um bloco por uma força usando *
    def __mul__(self, forca):
        if isinstance(forca, Forca):
            new_p = self.p + forca.x * (1 - math.sin(math.radians(self.m)))
            new_q = self.q + forca.y * (1 - math.sin(math.radians(self.m)))
            return Bloco(new_p, new_q, self.m)
        return NotImplemented

    # Método para subtrair um bloco de outro, retornando uma força resultante
    def menos(self, other):
        if isinstance(other, Bloco):
            factor = math.log(1 + math.log(1 + self.m + other.m))
            fr0 = (self.p - other.p) * factor
            fr1 = (self.q - other.q) * factor
            return Forca(fr0, fr1)
        return NotImplemented

    # Método para subtrair um bloco de outro usando -
    def __sub__(self, other):
        return self.menos(other)

# Classe que representa um campo de blocos
class Campo:
    def __init__(self, blocos):
        self.blocos = blocos

    def __str__(self):
        return ', '.join(str(bloco) for bloco in self.blocos)
    
    # Método para mover os blocos aplicando uma lista de forças
    def caminhada(self, lista_forcas):
        novos_blocos = []
        for bloco in self.blocos:
            novo_bloco = bloco
            for forca in lista_forcas:
                novo_bloco = novo_bloco * forca
            novos_blocos.append(novo_bloco)
        self.blocos = novos_blocos
    
    # Método para carregar blocos e forças de um arquivo e aplicar as forças nos blocos
    def carregue(self, filename):
        blocos = []
        forcas = []

        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("Bloco:"):
                    _, p, q, m = line.split()
                    blocos.append(Bloco(float(p), float(q), float(m)))
                elif line.startswith("Força:"):
                    _, x, y = line.split()
                    forcas.append(Forca(float(x), float(y)))
        
        self.blocos = blocos
        self.caminhada(forcas)

# Função que calcula a colisão entre dois pares de força e bloco
def colisao(tupla1, tupla2):
    f1, b1 = tupla1
    f2, b2 = tupla2
    
    # Calculando a força resultante (fr)
    f_diff_x = f1.x - f2.x
    f_diff_y = f1.y - f2.y
    f_sum_x = f1.x + f2.x
    f_sum_y = f1.y + f2.y
    norm_diff = math.sqrt(f_diff_x**2 + f_diff_y**2)
    norm_sum = math.sqrt(f_sum_x**2 + f_sum_y**2)
    
    log_term = math.log(1 + norm_diff + norm_sum)
    fr_x = log_term * f_sum_x
    fr_y = log_term * f_sum_y
    fr = Forca(fr_x, fr_y)
    
    # Calculando o bloco resultante (br)
    b_sum_m = b1.m + b2.m
    log_m = math.log(1 + b_sum_m)
    
    br0 = -0.5 * (b1.p + b2.p) * (1 - math.cos(log_m))
    br1 = -0.5 * (b1.q + b2.q) * (1 - math.cos(log_m))
    br = Bloco(br0, br1, log_m)
    
    return br
